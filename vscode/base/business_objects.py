from datetime import datetime as DT, date
from dateutil.relativedelta import relativedelta
from django.db import connection
from  django.db.models import Q
from django.shortcuts import get_object_or_404
import mysql.connector
import re
from pathlib import Path
from abc import abstractmethod, ABC

from vscode.utils.utils import *
from vscode.att.attribute import *
from vscode.comparator.comp import *
from vscode.loader.loaders import LoginStatusLoader
from vscode.msgr.msgr import *
from vscode.utils.exceptions import *
from vscode.val.vals import *
from vs.models import *
from zope.security.proxy import isinstance



class BusinessObject(BusinessObjectBase):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            # Create the instance if it doesnt exist yet
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        self.message = None
        self.invalidAllowed = True
        self.nullAllowed = True
        
    def isSameBaseState(self, obj):
        result = self.message == obj.message
        if result:
            result = self.invalidAllowed == obj.invalidAllowed
        return result
      
    def isNotBlank(self, att):
        # print(type(att))
        result = True
        s = None
        if not att:
            result = False
        elif not isinstance(att, Attribute):
            result = False
        elif not att.getValue():
            result = False
        if result:
            if isinstance(att.getValue(), bytes):
                s = att.getValue().decode()
            else:
                s = att.getValue()    
            if not isinstance(s, str):
                s = str(att.getValue())
            if result and len(s.strip()) == 0:
                result = False
        return result
      
    def debug(self, msg=None, err=None):
        if err:
            s = None            
            if msg:
                s = 'Error: ' + str(msg) 
            if err:
                s += ' '
                s += str(err)
            logger.debug(s)
   
    @abstractmethod
    def toDb(self):
        pass
    
    @abstractmethod
    def fromDb(self):
        pass
    
    @abstractmethod
    def getAttributeList(self):
        pass
    
    @abstractmethod    
    def validate(self):
        atts = self.getAttributeList()
        BusinessObject.validateAttributes(atts)
        
    @abstractmethod
    def save(self):
        pass
    
    @abstractmethod
    def delete(self):
        pass
    
    @abstractmethod
    def remove(self):
        pass
    
    @staticmethod
    def validateAttributes(attList): 
        super().ValidateAttributes()

    def setInvalidAllowed(self, newInvalidAllowed):
        self.invalidAllowed = newInvalidAllowed
        for att in self.getAttributeList(True):
            att.allowInvalID = newInvalidAllowed
        
    def isInvalidAllowed(self):
        return self.invalidAllowed

    def isNullAllowed(self):
        return self.nullAllowed
    
    def setNullAllowed(self, val):
        self.nullAllowed = val
    @staticmethod    
    def handleException(msg='', ex=None):
        if ex:
            logger.opt(exception=True).debug(msg)

    def getAndPurgeMessage(self):
        msg = self.message
        self.message = None
        return msg
    
    def addMessage(self, m):
        if m is None:
            raise InvalidArgumentException(AttributeMessageFactory.None_ERROR)
        self.message += ('\n' + m)
        


class ResourceAvailability():

    def __init__(self, resource,count=0):  
        self.resource = resource
        self.key = resource.getResourceID()
        self.count = count

    def getResource(self):
        return self.resource
    
    def getCount(self):
        return self.count
    
    def getKey(self):
        return self.key
    
    def setCount(self, count):
        self.count = count
    
    def __str__(self):
        return self.resource.getName() + " " + str(self.count)
    

class Activity(BusinessObject): 
    ACTIVITY_DESCRIPTION_LENGTH = 65000
    ACTIVITY_NAME_LENGTH = 40
    
    def  __init__(self, myDb=None):
        self.myDb = myDb
        self.activityID = IntegerAttribute("activityID")
        self.activityTeamID = IntegerAttribute("activityTeamID")
        self.activityVolunteerID = IntegerAttribute("activityVolunteerID")
        self.activityTaskID = IntegerAttribute("activityTaskID")
        self.name = StringAttribute("name")
        self.description = StringAttribute("description")
        self.date = DateAttribute("date")
        self.hoursWorked = NumericAttribute("hoursWorked")
        self.activityCreateUser = IntegerAttribute("activityCreateUser")
        self.activityUpdateUser = IntegerAttribute("activityUpdateUser")
        self.activityCreateDate = DateAttribute("activityCreateDate")
        self.activityUpdateDate = DateAttribute("activityUpdateDate")
        super().__init__()
        super().setIdProperties(self.activityID)
        super().setTrackingAttributes(self.activityCreateUser,
                self.activityUpdateUser,
                self.activityCreateDate,
                self.activityUpdateDate)

        self.name.allowInvalID = False
        self.name.setNullAllowed(False)
        self.name.setNullStringAllowed(False)
        self.name.setAllSpacesAllowed(False)
        self.name.setMixedCase(True)
        self.name.setHasMaximumLength(True)

        self.description.allowInvalID = False
        self.description.setNullAllowed(False)
        self.description.setNullStringAllowed(True)
        self.description.setAllSpacesAllowed(True)
        self.description.setMixedCase(True)
        self.description.setHasMaximumLength(True)
        self.name.setMaximumLength(Activity.ACTIVITY_NAME_LENGTH)
        self.description.setMaximumLength(Activity.ACTIVITY_DESCRIPTION_LENGTH)
        self.hoursWorked.maximumDigits = 5
        self.hoursWorked.minimumDigits = 0
        self.hoursWorked.minimumDecimalDigits=0
        self.hoursWorked.maximumDecimalDigits=2
        self.hoursWorked.setValue(0)

        self.activityTaskID.allowInvalID = False
        self.activityTaskID.setNullAllowed(False)
        self.activityTaskID.setHasMinimum(True)
        self.activityTaskID.setMinimum(1)
        
        self.date.allowInvalID = False 
        self.date.setNullAllowed(False) 
        self.date.setValue(DT.now())  
        if myDb:
            self.fromDb()
            
        self.hoursWorked.maximumDecimalPoints=2
            
    def getDate(self):
        return self.date.getValue()
    
    def setDate(self, d):
        self.date.setValue(d)
    
    def getCost(self):
        result = 0
        of = ObjectFactory()
        hrs = self.hoursWorked.getValue()
        avID = self.activityVolunteerID.getValue()
        if hrs > 0:
            if avID and avID > 0:
                vol = of.getVolunteer(avid)
                if vol:
                    result = vol.getCost() * hrs
            else:
                atID = self.activityTeamID.getValue()
                if atID and atID > 0:
                    tm = of.getTeam(atid)
                    if tm:
                        result = tm.getHourlyCost() * hrs
        return result 
    
    def getHoursWorked(self):
        return self.hoursWorked.getValue()
    
    def setHoursWorked(self, hoursWorked):
        self.hoursWorked.setValue(hoursWorked)
    
    def setActivityTeamID(self, i):
        self.activityTeamID.setValue(i)
    
    def getActivityVolunteerID(self):
        return self.activityVolunteerID.getValue()
    
    def setActivityVolunteerID(self, i):
        self.activityVolunteerID.setValue(i)
    
    def getActivityID(self):
        return self.activityID.getValue()
    
    def setActivityID(self, i):
        self.activityID.setValue(i)
    
    def getActivityTaskID(self):
        return self.activityTaskID.getValue()
    
    def setActivityTaskID(self, aid):
        self.activityTaskID.setValue(aid)
    
    def getName(self):
        return self.name.getValue()
    
    def setName(self, activity):
        self.name.setValue(activity)
    
    def getDescription(self):
        return self.description.getValue()
    
    def setDescription(self, activity):
        self.description.setValue(activity)
    
    def getActivityCreateUser(self):
        return self.activityCreateUser.getValue()

    def setActivityCreateUser(self, activityCreateUser):
        self.activityCreateUser.setValue(activityCreateUser)
    
    def getActivityUpdateUser(self):
        return self.activityUpdateUser.getValue()
    
    def setActivityUpdateUser(self, activityUpdateUser):
        self.activityUpdateUser.setValue(activityUpdateUser)

    def getActivityCreateDate(self):
        return self.activityCreateDate.getValue()
    
    def setActivityCreateDate(self, activityCreateDate):
        self.activityCreateDate.setValue(activityCreateDate)
    
    def getActivityUpdateDate(self):
        return self.activityUpdateDate.getValue()
    
    def setActivityUpdateDate(self, activityUpdateDate):
        self.activityUpdateDate.setValue(activityUpdateDate)
    
    def setUpdateDate(self, dat):
        self.setActivityUpdateDate(dat)
    
    def setCreateDate(self, dat):
        self.setActivityCreateDate(dat)
    
    def setDatabaseID(self, aid):
        self.setActivityID(aid)
    
    def setUpdateUser(self, aid):
        self.setActivityUpdateUser(aid)
    
    def setCreateUser(self, aid):
        self.setActivityCreateUser(aid)
    
    def getCreateUser(self):
        return self.getActivityCreateUser()
    
    def setID(self, aid):
        self.setActivityID(aid)
        
    def getID(self):
        return self.getActivityID()
        
    def equals(self, obj):
        result = True
        if not obj or not isinstance(obj, Activity):
            result = False
        if result:
            result = super().isSameBaseState(obj)
        if result and self.activityID.value != obj.activityID.value:
            result = False        
        elif self.activityTeamID.value != obj.activityTeamID.value:
            result = False
        elif self.activityVolunteerID.value != obj.activityVolunteerID.value:
            result = False
        elif self.activityTaskID.value != obj.activityTaskID.value:
            result = False
        elif self.description.value != obj.description.value:
            result = False
        elif self.name.value != obj.name.value:
            result = False
        return result
    
    def isSameState(self, vsp):
        return self.equals(vsp)
    
    def compareTo(self, o):
        result = -1
        if not o:
            result = 1
        elif isinstance(o, Activity):
            oKey = o.getDescription()
            key = self.getDescription()
            result = Utils.compareIgnoreCase(key, oKey)
        else:
            raise ClassCastException("Object " + o + "is not an instance of " + str(self.__class__.__name__))
        return result
    
    def getDisplayString(self):
        return self.toString()
    
    def toString(self):
        return str(self.getTaskSequence()) + "|" + str(self.getTaskName())
    
    def __str__(self):
        return self.getDisplayString()
    
    def toDb(self):
        for name, att in self.__dict__.items():
            a = att
            if isinstance(att, Attribute):
                a = att.value
            self.myDb.__dict__[name] = a
    
    def fromDb(self):
        for name, att in self.myDb.__dict__.items():
            if isinstance(att, bytes):
                att = att.decode()
            myAtt = self.__dict__.get(name)
            if not myAtt: 
                self.__dict__[name] = att
            else:
                if isinstance(myAtt, Attribute):
                    myAtt.value = att
                else:
                    myAtt = att
                self.__dict__[name] = myAtt

    def validate(self):
        atts = self.getAttributeList()
        BusinessObject.validateAttributes(atts)
        
    def save(self):
        self.toDb()
        self.myDb.save()       
        self.fromDb()
  
    def remove(self):
        self.myDb.delete()
              
    def delete(self):
        self.myDb.deleteFlag = True
        self.myDb.save()
    
    def getAttributeList(self): 
        return [
            self.activityID,
            self.activityTeamID,
            self.activityVolunteerID,
            self.activityTaskID,
            self.name,
            self.description,
            self.date,
            self.hoursWorked,
            self.activityCreateUser,
            self.activityUpdateUser,
            self.activityCreateDate,
            self.activityUpdateDate
        ]

             
class ConfigurableProperty(BusinessObject):
    
    NAME_SIZE = 40
    VALUE_SIZE = 255
    DESCRIPTION_SIZE = 255
    STRING = 1
    NUMERIC = 2
    BOOLEAN = 3
    
    def __init__(self, myDb=None):
        super().__init__()
        if isinstance(myDb, ConfigurableProperty):
            self.clone()
            self.myDb = DbConfigurableProperty()
            self.toDb()
        else:
            self.myDb = myDb
        self.propertyName = StringAttribute("propertyName")
        self.propertyValue = StringAttribute("propertyValue")
        self.propertyDescription = StringAttribute("propertyDescription")
        self.propertyID = IntegerAttribute("propertyID")
        self.propertyConfigurationSetID = IntegerAttribute("propertyConfigurationSetID")
        self.propertyType = IntegerAttribute("propertyType")
        self.propertyCreateUser = IntegerAttribute("propertyCreateUser")
        self.propertyUpdateUser = IntegerAttribute("propertyUpdateUser")
        self.propertyCreateDate = DateAttribute("propertyCreateDate")
        self.propertyUpdateDate = DateAttribute("propertyUpdateDate")
        super().setIdProperties(self.propertyID)
        super().setTrackingAttributes(
            self.propertyCreateUser,
            self.propertyUpdateUser,
            self.propertyCreateDate,
            self.propertyUpdateDate)

        self.propertyName.allowInvalID = False
        self.propertyName.setHasMaximumLength(True)
        self.propertyName.setAllSpacesAllowed(False)
        self.propertyName.setNullStringAllowed(False)
        self.propertyName.setNullAllowed(False)

        self.propertyValue.allowInvalID = False
        self.propertyValue.setHasMaximumLength(True)
        self.propertyValue.setAllSpacesAllowed(True)
        self.propertyValue.setNullStringAllowed(True)
        self.propertyValue.setNullAllowed(True)

        self.propertyDescription.allowInvalID = False
        self.propertyDescription.setHasMaximumLength(True)
        self.propertyDescription.setAllSpacesAllowed(True)
        self.propertyDescription.setNullStringAllowed(True)
        self.propertyDescription.setNullAllowed(True)

        self.propertyType.allowInvalID = False
        self.propertyType.setHasMaximum(True)
        self.propertyType.setHasMinimum(True)
        self.propertyValue.setNullAllowed(False)

        self.propertyConfigurationSetID.allowInvalID = False
        self.propertyConfigurationSetID.setHasMaximum(False)
        self.propertyConfigurationSetID.setHasMinimum(True)
        self.propertyConfigurationSetID.setMinimum(1)
        self.propertyConfigurationSetID.setNullAllowed(False)

        try:
            self.propertyName.setMaximumLength(ConfigurableProperty.NAME_SIZE)
            self.propertyValue.setMaximumLength(ConfigurableProperty.VALUE_SIZE)
            self.propertyDescription.setMaximumLength(ConfigurableProperty.DESCRIPTION_SIZE)
            self.propertyType.setMinimum(ConfigurableProperty.STRING)
            self.propertyType.setMaximum(ConfigurableProperty.BOOLEAN)
        except InvalidAttributeValueException as iave:
            super().handleException(iave)
        if myDb:
            self.fromDb()
            
    def clone(self, cp):
        try:
            self.propertyName.setValue(cp.propertyName.getValue())
            self.propertyValue.setValue(cp.getPropertyValue())
            self.propertyDescription.setValue(cp.getPropertyDescription())
            self.propertyType.setValue(cp.getPropertyType())
            self.propertyCreateUser.setValue(cp.getPropertyCreateUser())
            self.propertyUpdateUser.setValue(cp.getPropertyUpdateUser())
            self.setCreateDate(DT.now())
            self.setUpdateDate(DT.now())
        except InvalidAttributeValueException as unlikely:
            super().handleException(unlikely)
        super().setDirty(False)
        
    def isSameState(self, vsp):
        result = True
        if not vsp or not isinstance(vsp, ConfigurableProperty):
            result = False
        else:
            result = super().isSameBaseState(vsp)
        
        if result:
            s1 = self.getPropertyName()
            s2 = vsp.getPropertyName()
            result = Utils.areStringsEqual(s1, s2)
        
        if result:
            s1 = self.getPropertyValue()
            s2 = vsp.getPropertyValue()
            result = Utils.areStringsEqual(s1, s2)
        
        if result:
            s1 = self.getPropertyDescription()
            s2 = vsp.getPropertyDescription()
            result = Utils.areStringsEqual(s1, s2)
        
        if result:
            i1 = self.getPropertyID()
            i2 = vsp.getPropertyID()
            result = Utils.areNumbersEqual(i1, i2)
        
        if result:
            i1 = self.getPropertyType()
            i2 = vsp.getPropertyType()
            result = Utils.areNumbersEqual(i1, i2)
        
        if result:
            result = self.getPropertyCreateDate() == vsp.getPropertyCreateDate()
        
        if result:
            result = self.getPropertyUpdateDate() == vsp.getPropertyUpdateDate()
        
        if result:
            s1 = self.getPropertyCreateUser()
            s2 = vsp.getPropertyCreateUser()
            result = Utils.areNumbersEqual(s1, s2)
        
        if result:
            s1 = self.getPropertyUpdateUser()
            s2 = vsp.getPropertyUpdateUser()
            result = Utils.areNumbersEqual(s1, s2)
        
        return result

    def getPropertyName(self):
        return self.propertyName.getValue()
    
    def setPropertyName(self, newName):
                
        self.propertyName.setValue(newName)
    
    def getPropertyValue(self):
        return self.propertyValue.getValue()
   
    def setPropertyValue(self, val):
             
        self.propertyValue.setValue(val)
    
    def getPropertyDescription(self):
        return self.propertyDescription.getValue()
    
    def setPropertyDescription(self, val):
        
        self.propertyDescription.setValue(val)

    def getPropertyType(self):
        return self.propertyType.getValue()
    
    def setPropertyType(self, t):
        
        self.propertyType.setValue(t)
        
    def getPropertyID(self):
        return self.propertyID.getValue()
    
    def setPropertyID(self, val):
        self.propertyID.setValue(val)
        
    def getPropertyCreateUser(self):
        return self.propertyCreateUser.getValue()
        
    def setPropertyCreateUser(self, val):
        self.propertyCreateUser.setValue(val)
        
    def setPropertyUpdateUser(self, val):
        self.propertyUpdateUser.setValue(val)
        
    def setPropertyCreateDate(self, val):
        self.propertyUpdateUser.setValue(val)
        
    def setPropertyUpdateDate(self, val):
        self.propertyUpdateDate.setValue(val)
        
    def getPropertyUpdateUser(self):
        return self.propertyUpdateUser.getValue()
        
    def getPropertyCreateDate(self):
        return self.propertyCreateDate.getValue()
        
    def getPropertyUpdateDate(self):
        return self.propertyUpdateDate.getValue()
        
    def getDisplayString(self):
        result = self.getPropertyName() + "=" + self.getPropertyValue() 
        if self.getPropertyConfigurationSetID():
            result += " set=" 
            result += str(self.getPropertyConfigurationSetID())
        return result
    
    def __str__(self):
        return self.getDisplayString()

    def validate(self):
        super().validate()
        atts = self.getAttributeList()
        BusinessObjectBase.validateAttributes(atts)
        pv = self.getPropertyValue() 
        if self.getPropertyType() == ConfigurableProperty.NUMERIC:
            if not pv or pv.strip() == '':
                msg = self.getPropertyName() + " must not be blank or all spaces"
                raise InvalidAttributeValueException(msg)
            
            if not Utils.isNumeric(pv):
                msg = self.getPropertyName() + " is not numeric"
                raise InvalidAttributeValueException(msg)
            
        elif self.getPropertyType() == ConfigurableProperty.BOOLEAN:
            if not Utils.isBoolean(pv):
                msg = self.getPropertyName() + " is not a valID boolean"
                raise InvalidAttributeValueException(msg) 

    def getPropertyConfigurationSetID(self):
        return self.propertyConfigurationSetID.getValue()
    
    def setPropertyConfigurationSetID(self, uid):
        self.propertyConfigurationSetID.setValue(uid)
    
    def setUpdateUser(self, d):
        self.setPropertyUpdateUser(d)
    
    def getUpdateDate(self):
        return self.getPropertyUpdateDate()
    
    def setCreateUser(self, d):
        self.setPropertyCreateUser(d)
    
    def setCreateDate(self, d):
        self.setPropertyCreateDate(d)
    
    def setUpdateDate(self, d):
        self.setPropertyUpdateDate(d)
    
    def getLastUpdateUser(self):
        return self.getPropertyUpdateUser()
    
    def getCreateUser(self):
        return self.getPropertyCreateUser()
    
    def toDb(self):
        for name, att in self.__dict__.items():
            a = att
            if isinstance(att, Attribute):
                a = att.value
            self.myDb.__dict__[name] = a
            # print(\n + str(name) +  =  ) print(type(a))
    
    def fromDb(self):
        for name, att in self.myDb.__dict__.items():
            myAtt = self.__dict__.get(name)
            if not myAtt: 
                self.__dict__[name] = att
            else:
                a = att
                if isinstance(att, bytes):
                    a = att.decode()
                if isinstance(myAtt, Attribute):
                    myAtt.value = a
                else:
                    myAtt = a
                self.__dict__[name] = myAtt
                # print(name)print(a)   
        # print(self.__dict__)
        
    def save(self):
        self.toDb()
        self.myDb.save()
        self.fromDb()
  
    def remove(self):
            self.myDb.delete()
              
    def delete(self):
        self.myDb.deleteFlag = True
        self.myDb.save()
    
    def getAttributeList(self): 
        return [
            self.propertyName,
            self.propertyValue,
            self.propertyDescription,
            self.propertyID,
            self.propertyConfigurationSetID,
            self.propertyType,
            self.propertyCreateUser,
            self.propertyUpdateUser,
            self.propertyCreateDate,
            self.propertyUpdateDate]

 
class ConfigurablePropertiesManager(VSBase):

    @staticmethod
    def getConfigurableProps():
        if not VSPersistableSystemOption.configurableProps:
            props = ConfigurablePropertiesManager.getConfigurableProperties()
            if props:
                VSPersistableSystemOption.configurableProps = {} 
                for cp in props:
                    VSPersistableSystemOption.configurableProps[cp.getPropertyName()] = cp

    @staticmethod
    def getConfigurableProperties():
        result = []
        for dbo in DbConfigurableProperty.objects.all().exclude('deleteFlag=True'):
            result.append(ConfigurableProperty(dbo))
        return result

              
class Address(BusinessObject):
    
    CAME_FROM = "cameFromAddress"
    STREET_LENGTH = 255
    ADDRESS_LINE2_LENGTH = 255
    CITY_LENGTH = 50
    STATE_LENGTH = 2
    ZIP_LENGTH = 10
    PHONE_LENGTH = 20
    EMAIL_LENGTH = 255
    
    def __init__(self, myDb=None):
        super().__init__()
        
        self.addressID = IntegerAttribute("addressID")
        self.addressOrganizationID = IntegerAttribute("addressOrganizationID")
        self.street = StringAttribute("street")
        self.addressLineTwo = StringAttribute("addressLineTwo")
        self.city = StringAttribute("city")
        self.state = StringAttribute("state")
        self.postalCode = StringAttribute("postalCode")
        self.phone = StringAttribute("phone")
        self.mobilePhone = StringAttribute("mobilePhone")
        self.fax = StringAttribute("fax")
        self.pager = StringAttribute("pager")
        self.email = StringAttribute("email")
        self.addressCreateUser = IntegerAttribute("addressCreateUser")
        self.addressUpdateUser = IntegerAttribute("addressUpdateUser")
        self.addressCreateDate = DateAttribute("addressCreateDate")
        self.addressUpdateDate = DateAttribute("addressUpdateDate")
        self.organization = None
        self.myDb = myDb
        if myDb:
            self.fromDb()
        super().setIdProperties(self.addressID)
        super().setTrackingAttributes(self.addressCreateUser,
            self.addressUpdateUser,
            self.addressCreateDate,
            self.addressUpdateDate)
        try: 
            self.street.allowInvalID = False
            self.street.setHasMaximumLength(True)
            self.street.setMaximumLength(Address.STREET_LENGTH)
    
            self.addressLineTwo.allowInvalID = False
            self.addressLineTwo.setHasMaximumLength(True)
            self.addressLineTwo.setMaximumLength(Address.ADDRESS_LINE2_LENGTH)
    
            self.city.allowInvalID = False
            self.city.setHasMaximumLength(True)
            self.city.setMaximumLength(Address.CITY_LENGTH)
    
            self.state.allowInvalID = False
            self.state.setHasMaximumLength(True)
            self.state.setMaximumLength(Address.STATE_LENGTH)
            self.state.setMixedCase(False)
    
            self.postalCode.allowInvalID = False
            self.postalCode.setHasMaximumLength(True)
            self.postalCode.setMaximumLength(Address.ZIP_LENGTH)
    
            self.phone.allowInvalID = False
            self.phone.setHasMaximumLength(True)
            self.phone.setMaximumLength(Address.PHONE_LENGTH)
    
            self.mobilePhone.allowInvalID = False
            self.mobilePhone.setHasMaximumLength(True)
            self.mobilePhone.setMaximumLength(Address.PHONE_LENGTH)
    
            self.fax.allowInvalID = False
            self.fax.setHasMaximumLength(True)
            self.fax.setMaximumLength(Address.PHONE_LENGTH)
    
            self.pager.allowInvalID = False
            self.pager.setHasMaximumLength(True)
            self.pager.setMaximumLength(Address.PHONE_LENGTH)
    
            self.email.allowInvalID = False
            self.email.setHasMaximumLength(True)
            self.email.setMaximumLength(Address.EMAIL_LENGTH)
    
            self.addressOrganizationID.allowInvalID = False
            self.addressOrganizationID.setNullAllowed(True)
            self.addressOrganizationID.setHasMinimum(True)
            self.addressOrganizationID.setMinimum(0)
            
            self.addressCreateDate.setValue(super().now())
            self.addressUpdateDate.setValue(super().now())
        except:
            logger.opt(exception=True).debug('Address constructor')
            # this only happens if the literals are set to negative values in the interface definition
    
    def getCreateUser(self):
        return self.getAddressCreateUser()
    
    def getStreet(self):
        return self.street.getValue()

    def setStreet(self, newStreet):
        self.street.setValue(newStreet)
        
    def setAddressLineTwo(self, newAddressLineTwo):
        self.addressLineTwo.setValue(newAddressLineTwo)
        
    def getAddressLineTwo(self):
        return self.addressLineTwo.getValue()

    def setCity(self, newCity):
        self.city.setValue(newCity)
        
    def getCity(self):
        return self.city.getValue()
    
    def setState(self, newState):
        self.state.setValue(newState)
        
    def getState(self):
        return self.state.getValue()

    def setPostalCode(self, newPostalCode):
        self.postalCode.setValue(newPostalCode)
        
    def getPostalCode(self):
        return self.postalCode.getValue()
    
    def setPhone(self, newPhone):
        self.phone.setValue(newPhone)
        
    def getPhone(self):
        return self.phone.getValue()
    
    def setMobilePhone(self, newMobilePhone):
        self.mobilePhone.setValue(newMobilePhone)
        
    def getMobilePhone(self):
        return self.mobilePhone.getValue()
   
    def setFax(self, newFax):
        self.fax.setValue(newFax)
        
    def getFax(self):
        return self.fax.getValue()
    
    def setPager(self, newPager):
        self.pager.setValue(newPager)
        
    def getPager(self):
        return self.pager.getValue()
    
    def setEmail(self, newEmail):
        self.email.setValue(newEmail)
        
    def getEmail(self):
        return self.email.getValue()
    
    def getAddressID(self):
        return self.addressID.getValue()
    
    def setAddressID(self, aid):
        self.addressID.setValue(aid)
        
    def setUpdateUser(self, oid):
        self.setAddressUpdateUser(oid)
        
    def getUpdateDate(self):
        return self.getAddressUpdateDate()

    def setCreateUser(self, val):
        self.setAddressCreateUser(val)
        
    def setCreateDate(self, val):
        self.setAddressCreateDate(val)
    
    def setUpdateDate(self, val):
        self.setAddressUpdateDate(val)

    def getAddressCreateDate(self):
        return self.addressCreateDate.getValue()
    
    def setAddressCreateDate(self, val):
        self.addressCreateDate.setValue(val)
    
    def getAddressUpdateDate(self):
        return self.addressUpdateDate.getValue()

    def setAddressUpdateDate(self, addressUpdateDate):
        self.addressUpdateDate.setValue(addressUpdateDate)
        
    def getAddressCreateUser(self):
        return self.addressCreateUser.getValue()

    def setAddressCreateUser(self, addressCreateUser):
        self.addressCreateUser.setValue(addressCreateUser)
        
    def getAddressUpdateUser(self):
        return self.addressUpdateUser.getValue()
    
    def setAddressUpdateUser(self, addressUpdateUser):
        self.addressUpdateUser.setValue(addressUpdateUser)
        
    def isSameState(self, add):
        result = super().isSameBaseState(add)
        if result:
            result = self.addressID == add.addressID
        elif self.street != add.street:
            result = False
        elif self.addressLineTwo != add.addressLineTwo:
            result = False
        elif self.city != add.city:
            result = False
        elif self.state != add.state:
            result = False
        elif self.postalCode != add.postalCode:
            result = False
        elif self.phone != add.phone:
            result = False
        elif self.mobilePhone != add.mobilePhone:
            result = False
        elif self.fax != add.fax:
            result = False
        elif self.pager != add.pager:
            result = False
        elif self.email != add.email:
            result = False
        elif self.addressCreateUser != add.addressCreateUser:
            result = False
        elif self.addressUpdateUser != add.addressUpdateUser:
            result = False
        elif self.addressCreateDate != add.addressCreateDate:
            result = False
        elif self.addressUpdateDate != add.addressUpdateDate:
            result = False
        return result
    
    def __str__(self):
        foundFirst = False
        result = ''
        result += "AddressImpl ["

        if super().isNotBlank(self.street):
            result += "street="
            result += self.street.getValueString()
            foundFirst = True
        
        if super().isNotBlank(self.addressLineTwo):
            if foundFirst:
                result += ", "          
            result += "addressLineTwo="
            result += self.addressLineTwo.getValueString()
            foundFirst = True
        
        if (super().isNotBlank(self.city)):
            if (foundFirst):
                result += ", "
            result += "city="
            result += self.city.getValueString()
            foundFirst = True
        
        if (super().isNotBlank(self.state)):
            if (foundFirst):
                result += ", "
            result += "state="
            result += self.state.getValueString()
            foundFirst = True
        
        if (super().isNotBlank(self.postalCode)):
            if (foundFirst):
                result += ", "            
            result += "postalCode="
            result += self.postalCode.getValueString()
            foundFirst = True
        
        if (super().isNotBlank(self.phone)):
            if (foundFirst):
                result += ", "            
            result += "phone="
            result += self.phone.getValueString()
            foundFirst = True
        
        if (super().isNotBlank(self.mobilePhone)):
            if (foundFirst):
                result += ", "            
            result += "mobilePhone="
            result += self.mobilePhone.getValueString()
            foundFirst = True
        
        if (super().isNotBlank(self.fax)):
            if (foundFirst):
                result += ", "            
            result += "fax="
            result += self.fax.getValueString()
            foundFirst = True
        
        if (super().isNotBlank(self.pager)):
            if (foundFirst):
                result += ", "            
            result += "pager="
            result += self.pager.getValueString()
            foundFirst = True
        
        if (super().isNotBlank(self.email)):
            if (foundFirst):
                result += ", "            
            result += "email="
            result += self.email.getValueString()
            foundFirst = True
        
        result += "]"
        return result
    
    def getLastUpdateUser(self):
        return self.getAddressUpdateUser()
    
    def toDb(self):
        for name, att in self.__dict__.items():
            a = att
            if isinstance(att, Attribute):
                a = att.value
            self.myDb.__dict__[name] = a
            # print(\n + str(name) +  =  ) print(type(a))
    
    def fromDb(self):
        for name, att in self.myDb.__dict__.items():
            myAtt = self.__dict__.get(name)
            if not myAtt: 
                self.__dict__[name] = att
            else:
                a = att
                if isinstance(att, bytes):
                    a = att.decode()
                if isinstance(myAtt, Attribute):
                    myAtt.value = a
                else:
                    myAtt = a
                self.__dict__[name] = myAtt

                # print(name)print(a)   
        # print(self.__dict__)
    def validate(self):
        atts = self.getAttributeList()
        BusinessObjectBase.validateAttributes(atts)
        
    def save(self):
            self.toDb()
            self.myDb.save()
            self.fromDb()
  
    def remove(self):
            self.myDb.delete()
              
    def delete(self):
        self.myDb.deleteFlag = True
        self.myDb.save()
       
    def getAttributeList(self): 
        atts = [
        self.addressID,
        self.street,
        self.addressLineTwo,
        self.city,
        self.state,
        self.postalCode,
        self.phone,
        self.mobilePhone,
        self.fax,
        self.pager,
        self.email,
        self.addressCreateUser,
        self.addressUpdateUser,
        self.addressCreateDate,
        self.addressUpdateDate
        ]
        return atts 


class AuthorizationManager(VSBase):

    @staticmethod
    def isAuthorized(request, login):
        result = False
        if Utils.notBlank(request):
            securityGroups = login.getSecurityGroups()
            for sg in securityGroups:
                for priv in sg.getPrivileges():
                    if request == priv.getPrivilegeName():
                        result = True
                        break
                if result:
                    break
        return result
    
    @staticmethod
    def isVolunteerUser(login):
        result = False
        if login and isinstance(login, Login):
            securityGroups = login.getSecurityGroups()
            if securityGroups and len(securityGroups) == 1:
                sg = securityGroups[0]
                if Constants.SECURITY_GROUP_VOLUNTEER.casefold() == sg.getSecurityGroupName().casefold():
                    result = True
        return result

    
class SecurityUtils(VSBase):
    adminIds = None
    ResourceNames = []

    @staticmethod
    def isAuthorized(login, _type):
        result = False
        if login:
            result = SecurityUtils.isAdmin(_type)
            if not result:
                result = SecurityUtils.isAdmin(login)
                if not result:
                    result = AuthorizationManager.isAuthorized(_type, login)
        return result
    
    @staticmethod
    def isAdmin(login):
        result = False
        name = login.getLogin()
        if Utils.notBlank(name):
            adIds = SecurityUtils.getAdminIds()
            if adIds:
                for nm in adIds:
                    if nm == name:
                        result = True
                        break
        return result

    @staticmethod
    def isVolunteerUser(login):
        return AuthorizationManager.isVolunteerUser(login)
    
    @staticmethod
    def getAdminIds():
        result = []
        s = VSSystemOption().get(Constants.SECURITY_ADMIN_PROP)
        if Utils.notBlank(s):
            result = s.split(",")
        return result
    
    @staticmethod
    def getResourceNames():
        result = SecurityUtils.ResourceNames
        if not result:
            s = VSSystemOption.get(Constants.SECURITY__PROP)
            if Utils.notBlank(s):
                SecurityUtils.ResourceNames = s.split(",")
                result = SecurityUtils.ResourceNames
        return result
    
    @staticmethod
    def isAdminType(_type):
        result = False
        if _type and Utils.notBlank(_type.strip()):
            for n in SecurityUtils.getResourceNames():
                if n == _type: 
                    result = True
                    break     
        return result

                
class Login(BusinessObject):
    encrypter = Encrypter()
    maxFailedLogins = 3
    passwordExpireDays = 0
    
    LOGIN_MAX_SIZE = 255
    LOGIN_MIN_SIZE = 1
    LOGIN_NAME_MAX_SIZE = 255
    PASSWORD_MAX_SIZE = 40
    PASSWORD_MIN_SIZE = 1  # set low - will be overridden by configurable properties
    PASSWORD_MAX_ENCRYPTED_SIZE = 255
    SECRET_MAX_SIZE = 40
    SECRET_MAX_ENCRYPTED_SIZE = 255
    
    @classmethod
    def getMaxFailedLogins(cls):
        return cls.maxFailedLogins

    @classmethod
    def getPasswordExpireDays(cls):
        return cls.passwordExpireDays
       
    def __init__(self, myDbArg=None):
        super().__init__()
        self.loginID = IntegerAttribute("loginID", allowInvalid=False,)
        self.loginOrganizationID = IntegerAttribute("loginOrganizationID")
        self.login = StringAttribute("login")
        self.loginName = StringAttribute("loginName")
        self.lastChange = DateAttribute("lastChange")
        self.secret = StringAttribute("secret")
        self.loginStatusID = IntegerAttribute("loginStatusID")
        self.loginCreateUser = IntegerAttribute("loginCreateUser")
        self.loginUpdateUser = IntegerAttribute("loginUpdateUser")
        self.loginCreateDate = DateAttribute("loginCreateDate")
        self.loginUpdateDate = DateAttribute("loginUpdateDate")
        self.deleteFlag = BooleanAttribute('deleteFlag')
        self.failures = IntegerAttribute('failures')
        self.loggedIn = False
        self.organization = None
        self.loginStatus = None
        self.securityGroups = []
        self.passwords = []
        self.password = None
        super().setIdProperties(self.loginID)        
        super().setTrackingAttributes(
                self.loginCreateUser,
                self.loginUpdateUser,
                self.loginCreateDate,
                self.loginUpdateDate)

        self.login.allowInvalID = False
        self.login.hasMaximumLength = True
        self.login.hasMinimumLength = True
        self.login.allSpacesAllowed = False
        self.login.nullStringAllowed = False
        self.login.nullAllowed = False
        self.login.maximumLength = Login.LOGIN_MAX_SIZE
        self.login.MinimumLength = Login.LOGIN_MIN_SIZE

        self.loginName.allowInvalID = False
        self.loginName.hasMaximumLength = True
        self.loginName.allSpacesAllowed = False
        self.loginName.nullStringAllowed = False
        self.loginName.nullAllowed = False
        self.loginName.maximumLength = Login.LOGIN_NAME_MAX_SIZE

        self.loginOrganizationID.allowInvalID = False
        self.login.nullAllowed = False
        self.loginOrganizationID.hasMinimum = True
        self.loginOrganizationID.minimum = 0

        self.failures.allowInvalID = False
        self.failures.nullAllowed = False
        self.failures.hasMinimum = True
        self.failures.minimum = 0

        self.lastChange.allowInvalID = False
        self.lastChange.nullAllowed = True
        self.lastChange.durationRequired = False

        self.secret.allowInvalID = False
        self.secret.hasMaximumLength = True
        self.secret.allSpacesAllowed = False
        self.secret.nullStringAllowed = False
        self.secret.nullAllowed = False
        self.secret.maximumLength = Login.SECRET_MAX_ENCRYPTED_SIZE
        
        self.loginStatusID.allowInvalID = False
        self.loginStatusID.nullAllowed = False
        self.loginStatusID.minimum = LoginStatusLoader.MINIMUM
        self.loginStatusID.hasMaximum = False
        self.loginStatusID.hasMinimum = True
        self.loginStatusID.value = LoginStatusLoader.READY
        
        self.deleteFlag.allowInvalID = False
        self.deleteFlag.nullAllowed = False
        self.deleteFlag.value = False
        
        super().setIdProperties(self.loginID)
        super().setTrackingAttributes(self.loginCreateUser,
                self.loginUpdateUser,
                self.loginCreateDate,
                self.loginUpdateDate)
        if myDbArg:
            self.myDb = myDbArg
            self.fromDb()
        else:
            self.myDb = DbLogin()
            
    def clone(self, li): 
        try:
            if li: 
                if li.getLoginOrganizationID():
                    self.loginOrganizationID.setValue(li.getLoginOrganizationID())
                self.login.setValue(li.getLogin())
                self.loginName.setValue(li.getLoginName())
                self.passwords = li.getPasswords()
                self.password = self.passwords[0] if self.passwords else None
                self.lastChange.setValue(li.getLastChange())
                self.secret.setValue(li.getSecret())
                self.loginStatusID.setValue(li.getLoginStatusID())
                self.loginCreateUser.setValue(li.getLoginCreateUser())
                self.loginUpdateUser.setValue(li.getLoginUpdateUser())
                self.loginCreateDate.setValue(li.getLoginCreateDate())
                self.loginUpdateDate.setValue(li.getLoginUpdateDate())
                self.failures = li.failures
                self.loggedIn = li.loggedIn
                self.organization = li.organization
                self.loginStatus = li.loginStatus 
                self.securityGroups = li.getSecurityGroups()
            #print(li)
        except Exception as e:
            super().handleException("", e)
        return self
        
    def isSameState(self, impl):
        result = True
        if not isinstance(impl, Login):
            result = False
        elif not super().isSameBaseState(impl):
            result = False
        
        if result:
            result = self.getLoginID() == impl.getLoginID()
        
        if result:
            result = self.getLogin() == impl.getLogin()
        
        if result:
            result = self.getLoginName() == impl.getLoginName()
        
        if result:
            result = self.getPassword() == impl.getPassword()
        
        if result:
            result = self.getSecret() == impl.getSecret()
        
        if result:
            result = self.getLoginStatusID() == impl.getLoginStatusID()
        
        if result:
            result = self.getFailures() == impl.getFailures()
        
        if result:
            result = self.getLastChange() == impl.getLastChange()
        
        if result:
            result = self.getLoginCreateDate() == impl.getLoginCreateDate()
        
        if result:
            result = self.getLoginUpdateDate() == impl.getLoginUpdateDate()
        
        if result:
            result = self.getLoginCreateUser() == impl.getLoginCreateUser()
        
        if result:
            result = self.getLoginUpdateUser() == impl.getLoginUpdateUser()
        
        if result:
            oi1 = self.getOrganization()
            oi2 = impl.getOrganization()
            if oi1 is not None and oi2 is None:
                result = False
            elif oi1 is None and oi2 is not None: 
                result = False
            elif oi1 is None and oi2 is None:
                result = False
            elif oi1 is not None and oi2 is not None:
                result = oi1.isSameState(oi2)
        return result

    def getLoginOrganizationID(self):
        return self.loginOrganizationID.getValue()
    
    def setLoginOrganizationID(self, oid):
        self.loginOrganizationID.setValue(oid)

    def getStatusType(self):
        return self.getLoginStatus().getLoginStatusType()

    def setOrganization(self, newOrg):
        self.organization = newOrg
        if not newOrg:
            self.organization_ID = None
            self.loginOrganizationID.value = None
        elif isinstance(newOrg, DbOrganization):
            self.loginOrganizationID.value = newOrg.organizationID    
        elif isinstance(newOrg, Organization):
            self.loginOrganizationID.value = newOrg.organizationID.value
            
    def getOrganization(self):
        return self.organization
    
    def attempt(self, pwd):
        result = False
        if not pwd or not isinstance(pwd, str) or len(pwd.strip()) == 0:
            raise InvalidPasswordException()
        elif (self.isLocked()):
            raise AccountLockedException()
        elif self.isDeleted():
            raise AccountDeletedException() 
        elif self.isExpired() and not self.isAdmin():
            raise AccountExpiredException()
        
        encodedPwd = self.getPassword().password.value
        decodedPwd = Login.encrypter.decrypt(encodedPwd)
        if pwd != decodedPwd:
            # print(str(type(encodedPwd)) + ' ' + str(type(pwd)))
            #print('decodedPwd "' + decodedPwd + '"  "' + pwd + '"')
            self.fail()
            raise InvalidPasswordException()
        elif not self.isDeleted():
            encodedPwd = Login.encrypter.encrypt(pwd)
            if encodedPwd == self.getPassword():
                result = True
                self.succeed()
            else:
                self.fail()
        else:
            self.fail()
        return result

    def getLoginID(self):
        return self.loginID.getValue()
    
    def setLoginID(self, lid):
        self.loginID.setValue(lid)

    def getLogin(self):
        return self.login.getValue()
    
    def setLogin(self, login):
        self.login.setValue(login)
    
    def getLoginName(self):
        return self.loginName.getValue()
    
    def setLoginName(self, login):
        self.loginName.setValue(login)
        
    def getPasswords(self):
        result = []
        if len(self.passwords) == 0:
            for obj in ObjectFactory().getPasswords(login=self):
                result.append(obj)
            self.passwords = result
        return result
        
    def getPassword(self):
        pwd = self.password
        if not pwd:
            pwd = Password (
            self.myDb.passwords
            .order_by('-passwordID')
            .first())
            self.password = pwd
        return pwd
    
    def setPassword(self, txt, loginID=1):
        self.validatePassword(txt)
        self.save()
        encodedPwd = Login.encrypter.encrypt(txt)
        dbo = DbPassword()
        dbo.password = encodedPwd
        dbo.login = self.myDb
        if not loginID:
            dbo.passwordCreateUser = 1
            dbo.passwordUpdateUser = 1
        else:
            dbo.passwordCreateUser = loginID
            dbo.passwordUpdateUser = loginID
        dbo.save()
        pwd = Password(dbo)
        self.passwords.append(pwd)
        self.password = pwd

    def setValidatedPassword(self, pwd):
        self.passwords.append(pwd)

    def getLastChange(self):
        return self.lastChange.getValue()
        
    def setLastChange(self, newV):
        if newV is None:
            self.lastChange.setValue(None)
        elif isinstance(newV, DT):
            self.lastChange.setValue(newV.date())
        elif isinstance(newV, date):
            self.lastChange.setValue(newV)
        elif isinstance(newV, str):
            dt = DT.strptime(newV, "%Y-%m-%d").date()
            self.lastChange.setValue(dt)
        else:
            raise InvalidAttributeValueException(AttributeMessageFactory.dateFormatError(newV))
   
    def setLoggedIn(self, loggedIn):
        self.loggedIn = loggedIn
   
    def succeed(self):
        self.failures.value = 0
        self.loggedIn = True
        self.setLoginStatusID(LoginStatusLoader.READY)
        ValuesHolder.setCurrentLogin(self) 
        self.save()
        
    def lock(self):
            self.setLoginStatusID(LoginStatusLoader.LOCKED)
            self.save()

    def isLocked(self):
        return self.getLoginStatusID() == LoginStatusLoader.LOCKED
    
    def isDeleted(self):
        return self.deleteFlag.value

    def fail(self):
        self.failures.value += 1
        if self.failures.value >= Login.getMaxFailedLogins():
            self.lock()  # lock() saves the login
            raise AccountLockedException()
        else: 
            try:
                self.save()
            except Exception as pe:
                super().handleException("Couldn't save failed Login", pe)
                raise pe
        
    def isExpired(self):
        result = False
        ls = self.getLoginStatus()
        if isinstance(ls, DbLoginStatus):
            ls = LoginStatus(ls)
            self.setLoginStatus(ls)
        if ls and ls.getLoginStatusType() == LoginStatusLoader.EXPIRED:
            result = True
        else: 
            if not SecurityUtils.isAdmin(self) and self.passwordExpireDays > 0:
                lc = self.lastChange.getValue()
                today = DT.now() 
                delta = today - lc
                if delta.days >= self.passwordExpireDays:
                    result = True 
                    ls = ValueTableManager().get(LoginStatus, LoginStatus.STATUS_EXPIRED)
                    if ls:
                        self.setLoginStatus(ls)
        return result
    
    def changePassword(self, secret, newPwd):
        encodedSecret = Login.encrypter.encrtpt(secret)
        if (encodedSecret != self.getSecret()):
            raise InvalidPasswordException(VSMessages.invalidSecretText(secret))      
        self.validatePassword(newPwd)
        try:
            encodedNewPwd = Login.encrypter.encrypt(newPwd)
            self.setValidatedPassword(encodedNewPwd)
        except InvalidAttributeValueException as e:
            raise InvalidPasswordException(VSMessages.invalidPassword(), e)

    def getSecret(self):
        return self.secret.getValue()

    def setSecret(self, secret):
        encodedSecret = Login.encrypter.encrypt(secret)
        self.setSecretEncoded(encodedSecret)
    
    def getSecretEncoded(self):
        return self.secret.getValue()
    
    def setSecretEncoded(self, newV):
        self.secret.setValue(newV)
        
    def reset(self):
        vt = ValueTableManager()
        # for key in ValueTableManager.tables:
        #   print(str(type(key)) +   + str(key))
        keyVal = int(LoginStatus.STATUS_RESET)
        ls = vt.getValue(table='LoginStatus', key=keyVal)
        if ls:
            self.setLoginStatus(ls)
            self.loginStatusID = LoginStatus.STATUS_RESET
            self.save()
        else:
            raise Exception("didnt get login status for " + str(keyVal))
            
    def isReset(self):
        # print(str(self.loginStatus.loginStatusID) +  :  + str(self.loginStatusID))
        return int(self.loginStatusID.value) == int(LoginStatusLoader.RESET)

    def getLoginStatusID(self):
        return self.loginStatusID.getValue()
    
    def setLoginStatusID(self, oid):
        self.loginStatusID.setValue(oid)
    
    def getMinimumPasswordLength(self):
        return PropertiesManager().getDefaultedProperty(Login.PASSWORD_MIN_LENGTH_PROP, 0)
    
    def getMinimumSecretLength(self):
        return PropertiesManager().getDefaultedProperty(Login.SECRET_MIN_LENGTH_PROP, 0)
    
    def isAdmin(self):
        return "admin" == self.login.value.lower()
    
    def getLoggedIn(self): 
        return str(self.loggedIn)

    def isReady(self):
        return self.getLoginStatusID() == LoginStatusLoader.READY
    
    def setUpdateUser(self, uid):
        self.setLoginUpdateUser(uid)
    
    def getUpdateDate(self):
        return self.getLoginUpdateDate()
    
    def setCreateUser(self, uid):
        self.setLoginCreateUser(uid)
        
    def setCreateDate(self, d):
        self.setLoginCreateDate(d)
        
    def setUpdateDate(self, d):
        self.setLoginUpdateDate(d)
    
    def getLoginCreateDate(self):
        return self.loginCreateDate.getValue()

    def setLoginCreateDate(self, lcd):
        self.loginCreateDate.setValue(lcd)

    def getLoginUpdateDate(self):
        return self.loginUpdateDate.getValue()

    def setLoginUpdateDate(self, loginUpdateDate):
        self.loginUpdateDate.setValue(loginUpdateDate)
    
    def getLoginCreateUser(self):
        return self.loginCreateUser.getValue()
    
    def setLoginCreateUser(self, loginCreateUser):
        self.loginCreateUser.setValue(loginCreateUser)

    def getLoginUpdateUser(self):
        return self.loginUpdateUser.getValue()

    def setLoginUpdateUser(self, loginUpdateUser):
        self.loginUpdateUser.setValue(loginUpdateUser)
        
    def setDeleteFlag(self, flag):
        self.deleteFlag.setValue(flag)
        
    def getDeleteFlag(self):
        return self.deleteFlag.getValue()
    
    def getSecurityGroups(self):
        return self.securityGroups
    
    def setSecurityGroups(self, securityGroups):
        if (securityGroups != None):
            self.securityGroups = securityGroups

    def addSecurityGroup(self, secGrp):
        if isinstance(secGrp, SecurityGroup):
            secGrp = secGrp.myDb
        elif not isinstance(secGrp, DbSecurityGroup):
            raise InvalidArgumentException(str(type(secGrp)) + 'is not a security group')
        self.securityGroups.add(secGrp)
            
    def removeSecurityGroup(self, sg):
        result = False
        if sg != None:
            try:
                result = self.securityGroups.remove(sg)
                result = True
                
            except:
                pass
        return result
    
    def getFailures(self):
        return self.failures.value

    def setFailures(self, failures):
        self.failures.value = failures
    
    def getLastUpdateUser(self):
        return self.getLoginUpdateUser()
    
    def getCreateUser(self):
        return self.getLoginCreateUser()

    def validatePassword(self, pwd):
        if pwd:  # let attribute validation handle case where value is None so we dont get NPE
            # regEx = r"^.*(?=.{8,)(?=.*\\d)(?=.*[a-z])(?=.*[A-Z]).*$"

            if len(pwd) > int(Login.PASSWORD_MAX_SIZE) or len(pwd) < int(Login.PASSWORD_MIN_SIZE):
                    # or not re.fullmatch(regEx, pwd))
                raise InvalidPasswordValueException(VSMessageFactory.getInvalidPasswordError(),)
            for opwd in self.myDb.passwords.all():
                dec = Login.encrypter.decrypt(opwd.password)
                # print(dec)
                if dec == pwd:
                    raise PasswordAlreadyUsedException(msg=pwd)
        else:
            raise InvalidPasswordValueException(VSMessageFactory.getInvalidPasswordError(),)

    def getLoginStatus(self):
        return self.loginStatus

    def setLoginStatus(self, ls):
        # print(ls)
        self.loginStatus = ls
        if ls:
            val = ls.getLoginStatusID()
        else:
            val = None
        self.setLoginStatusID(val)
        
    def __str__(self):
        s = "Login{loginID=" 
        if self.loginID and self.loginID.value:
            s += str(self.loginID.value)
        else:
            s += 'None' 
        s += ", login=" 
        if self.loginID and self.loginID.value:
            s += str(self.login.value)
        else:
            s += 'None' 
        s += ", loginName=" 
        if self.loginName and self.loginName.value:
            s += str(self.loginName.value)
        else:
            s += 'None' 
        s += ", password="
        if self.password and self.password.getValue():
            s +- str(Encrypter().decrypt(self.password.getValue()))
        else:
            s += 'None' 
        s += ", lastChange=" 
        if self.lastChange and self.lastChange.value:
            s += self.lastChange.value.strftime('%m/%d/%Y') 
        else:
            s += 'None' 
        s += ", secret=" 
        if self.secret and self.secret.getValue():
            s += str(Encrypter().decrypt(self.secret.getValue()))
        else:
            s += 'None' 
        s += ", loginStatusID=" 
        if self.loginStatusID and self.loginStatusID.value:
            s += str(self.loginStatusID.value) 
        else:
            s += 'None' 
        s += ", loginCreateUser=" 
        if self.loginCreateUser and self.loginCreateUser.value:
            s+= str(self.loginCreateUser.value) 
        else:
            s += 'None' 
        s += ", loginUpdateUser=" 
        if self.loginUpdateUser and self.loginUpdateUser.value:
            s += str(self.loginUpdateUser.value)
        else:
            s += 'None' 
        s += ", loginCreateDate=" 
        if self.loginCreateDate and self.loginCreateDate.value:
            s += str(self.loginCreateDate.value.strftime('%m/%d/%Y'))
        else:
            s += 'None' 
        s += ", loginUpdateDate=" 
        if self.loginUpdateDate and self.loginUpdateDate.value:
            s += str(self.loginUpdateDate.value.strftime('%m/%d/%Y'))
        else:
            s += 'None' 
        s += ", failures=" 
        if self.failures and self.failures.value:
            s += str(self.failures.value)
        else:
            s += 'None' 
        s += ", loggedIn=" 
        if self.loggedIn:
            s += str(self.loggedIn)
        else:
            s += 'None' 
        if self.loginStatus:
            try:
                s += ", loginStatus=" + str(self.loginStatus)
            except: 
                s += ", loginStatus=None"    
        else:
            s += ", loginStatus=None"
        if self.securityGroups:
            s += ", securityGroups=" + str(self.securityGroups) 
        else:
            s += ", securityGroups=None" 
        s += '}'
        return s
    
    def toDb(self):
        self.myDb.loginID = self.loginID.getValue()
        self.myDb.login = self.login.getValue()
        self.myDb.loginName = self.loginName.getValue()
        if self.failures and self.failures.value:
            self.myDb.failures = self.failures.getValue()
        else:
            self.myDb.failures = 0
        self.myDb.lastChange = self.lastChange.getValue()
        self.myDb.secret = self.secret.getValue()
        self.myDb.loginCreateUser = self.loginCreateUser.getValue()
        self.myDb.loginUpdateUser = self.loginUpdateUser.getValue()
        self.myDb.loginCreateDate = self.loginCreateDate.getValue()
        self.myDb.loginUpdateDate = self.loginUpdateDate.getValue()
        self.myDb.deleteFlag = self.deleteFlag.getValue()
        if self.loginID.value and self.loginID.value > 0:
            # print(self.loginID.value)
            self.myDb.login = self.login.value
            if self.loginStatus:
                if isinstance(self.loginStatus, LoginStatus) and self.loginStatus.myDb:
                    self.myDb.loginStatus = self.loginStatus.myDb
                elif isinstance(self.loginStatus, DbLoginStatus):
                    self.myDb.loginStatus = self.loginStatus
                # else:
                #    logger.debug('invalID login status')
                    # print(type(self.loginStatus))    
            if self.securityGroups and self.loginID.value:
                self.myDb.securityGroups.clear()
                for secGrp in self.securityGroups:
                    self.myDb.securityGroups.add(secGrp.myDb)
        self.myDb.organization = None
        if self.organization:
            if isinstance(self.organization, Organization): 
                self.myDb.organization = self.organization.myDb
        
    def fromDb(self):
        if self.myDb.loginID:
            self.loginID.setValue(self.myDb.loginID)
            self.securityGroups = []
            for sg in self.myDb.securityGroups.all():
                self.securityGroups.append(SecurityGroup(sg))
            self.setOrganization(Organization(self.myDb.organization))
            if self.myDb.loginStatus:
                self.loginStatus = LoginStatus(self.myDb.loginStatus)
        val = self.myDb.login
        if val and isinstance(val, bytes):
            val = val.decode()
        self.login.setValue(val)
        val = self.myDb.loginName
        if val and isinstance(val, bytes):
            val = val.decode()
        self.loginName.setValue(val)
        val = self.myDb.secret
        if val and isinstance(val, bytes):
            val = val.decode()
        self.secret.setValue(val)
        self.failures.setValue(self.myDb.failures)
        self.lastChange.setValue(self.myDb.lastChange)
        self.loginCreateUser.setValue(self.myDb.loginCreateUser)
        self.loginUpdateUser.setValue(self.myDb.loginUpdateUser)
        self.loginCreateDate.setValue(self.myDb.loginCreateDate)
        self.loginUpdateDate.setValue(self.myDb.loginUpdateDate)
        self.deleteFlag.setValue(self.myDb.deleteFlag)
    
    def validate(self):
        for att in self.getAttributeList():
            att.validate()   
        
    def getAttributeList(self, includeSuperClasses=False):
        atts = [            
            self.loginID,
            self.login,
            self.loginName,
            self.password,
            self.failures,
            self.lastChange,
            self.secret,
            self.self.loginCreateUser,
            self.loginUpdateUser,
            self.loginCreateDate,
            self.loginUpdateDate,
            self.deleteFlag
        ]
        if includeSuperClasses:
            atts.append(super().getAttributeList())    
        return atts
        
    def save(self):
        if not self.secret:
            self.setSecret('secret123')
        self.toDb()
        self.myDb.save()
        #print(self.myDb)
        self.fromDb()      
  
    def remove(self):
            self.myDb.delete()
              
    def delete(self):
        self.myDb.deleteFlag = True
        self.myDb.save()
        
    @staticmethod
    def doOrDie(loginID, password):
        
        dbl = DbLogin.objects.get(login=loginID).exclude(deleteFlag=True)
        li = Login(dbl)
        li.attemptToLogin(password)
        ValuesHolder.setCurrentLogin(li) 

     
class Privilege(BusinessObject):

    NAME_LENGTH = 40

    def __init__(self, myDb=None):
        super().__init__()
        self.myDb = myDb
        self.privilegeID = IntegerAttribute("privilegeID")
        self.privilegeName = StringAttribute("privilegeName")
        self.privilegeCreateDate = DateAttribute("privilegeCreateDate")
        self.privilegeUpdateDate = DateAttribute("privilegeUpdateDate")
        self.privilegeCreateUser = IntegerAttribute("privilegeCreateUser")
        self.privilegeUpdateUser = IntegerAttribute("privilegeUpdateUser")
        
        super().setIdProperties(self.privilegeID)
        super().setTrackingAttributes(
                self.privilegeCreateUser,
                self.privilegeUpdateUser,
                self.privilegeCreateDate,
                self.privilegeUpdateDate)

        self.privilegeName.setHasMaximumLength(True)
        self.privilegeName.setMaximumLength(Privilege.NAME_LENGTH)
        self.privilegeName.setNullAllowed(False)
        self.privilegeName.setNullStringAllowed(False)
        self.privilegeName.setAllSpacesAllowed(False)
        if myDb:
            self.fromDb()

    def isSameState(self, impl):
        result = super().isSameBaseState(impl)
        
        if result:
            s1 = self.getPrivilegeID()
            s2 = impl.getPrivilegeID()
            result = s1 == s2
        
        if result:
            s1 = self.getPrivilegeName()
            s2 = impl.getPrivilegeName()
            result = s1 == s2
        
        if result:
            result = self.getPrivilegeCreateDate() == impl.getPrivilegeCreateDate()
        
        if result:
            result = self.getPrivilegeUpdateDate() - -impl.getPrivilegeUpdateDate()
        
        if result:
            s1 = self.getPrivilegeCreateUser()
            s2 = impl.getPrivilegeCreateUser()
            result = s1 == s2
        
        if result:
            s1 = self.getPrivilegeUpdateUser()
            s2 = impl.getPrivilegeUpdateUser()
            result = s1 == s2
        
        return result

    def __sstr__(self):
        return self.getDisplayString()
    
    def getDisplayString(self):
        return self.getPrivilegeName()
    
    def getPrivilegeName(self):
        return self.privilegeName.getValue()

    def setPrivilegeName(self, name):
        if not name == self.getPrivilegeName():
            self.privilegeName.setValue(name)

    def setPrivilegeID(self, uid):
        if not uID == self.privilegeID:
            self.privilegeID.setValue(uid)
        
    def getPrivilegeID(self):
        return self.privilegeID.getValue()
    
    def getPrivilegeCreateDate(self):
        return self.privilegeCreateDate.getValue()

    def setPrivilegeCreateDate(self, privilegeCreateDate):
        self.privilegeCreateDate.setValue(privilegeCreateDate)

    def getPrivilegeUpdateDate(self):
        return self.privilegeUpdateDate.getValue()

    def setPrivilegeUpdateDate(self, privilegeUpdateDate):
        self.privilegeUpdateDate.setValue(privilegeUpdateDate)
    
    def getPrivilegeCreateUser(self):
        return self.privilegeCreateUser.getValue()

    def setPrivilegeCreateUser(self, privilegeCreateUser):
        self.privilegeCreateUser.setValue(privilegeCreateUser)
        
    def getPrivilegeUpdateUser(self):
        return self.privilegeUpdateUser.getValue()

    def setPrivilegeUpdateUser(self, privilegeUpdateUser):
        self.privilegeUpdateUser.setValue(privilegeUpdateUser)
    
    def toDb(self):
        for name, att in self.__dict__.items():
            a = att
            if isinstance(att, Attribute):
                a = att.value
            self.myDb.__dict__[name] = a
            # print(\n + str(name) +  =  ) print(type(a))
    
    def fromDb(self):
        for name, att in self.myDb.__dict__.items():
            myAtt = self.__dict__.get(name)
            if not myAtt: 
                self.__dict__[name] = att
            else:
                a = att
                if isinstance(att, bytes):
                    a = att.decode()
                if isinstance(myAtt, Attribute):
                    myAtt.value = a
                else:
                    myAtt = a
                self.__dict__[name] = myAtt
        # print(self.__dict__)
        
    def validate(self):
        atts = self.getAttributeList()
        BusinessObjectBase.validateAttributes(atts)
        
    def save(self):
        self.toDb()
        self.myDb.save()
        self.fromDb()
  
    def remove(self):
            self.myDb.delete()
              
    def delete(self):
        self.myDb.deleteFlag = True
        self.myDb.save()
    
    def getAttributeList(self): 
        return [
            self.privilegeID,
            self.privilegeName,
            self.privilegeCreateDate,
            self.privilegeUpdateDate,
            self.privilegeCreateUser,
            self.privilegeUpdateUser
        ]

        
class Password(BusinessObject):
    encrypter = Encrypter()

    def __init__(self, myDb=None):
        super(). __init__()
        self.myDb = myDb
        self.passwordID = IntegerAttribute("passwordID")
        self.passwordLoginID = IntegerAttribute("passwordLoginID")
        self.password = StringAttribute("password")
        self.passwordCreateDate = DateAttribute("passwordCreateDate")
        self.passwordUpdateDate = DateAttribute("passwordUpdateDate")
        self.passwordCreateUser = IntegerAttribute("passwordCreateUser")
        self.passwordUpdateUser = IntegerAttribute("passwordUpdateUser")
        super().setIdProperties(self.passwordID)        
        super().setTrackingAttributes(
                self.passwordCreateUser,
                self.passwordUpdateUser,
                self.passwordCreateDate,
                self.passwordUpdateDate)
        super().setIdProperties(self.passwordLoginID)        
        self.passwordLoginID.setNullAllowed(False)

        self.password.allowInvalID = False
        self.password.setHasMaximumLength(True)
        self.password.setMaximumLength(Login.PASSWORD_MAX_ENCRYPTED_SIZE)
        self.password.setNullAllowed(False)
        self.password.setNullStringAllowed(False)
        self.passwordCreateDate.allowInvalID = False
        self.passwordCreateDate.setNullAllowed(False)

        self.passwordUpdateDate.allowInvalID = False
        self.passwordUpdateDate.setNullAllowed(False)
        if self.myDb:
            self.fromDb()
    
    def isSameState(self, impl):
        result = super().isSameBaseState(impl)
        
        if result:
            s1 = self.getPasswordID()
            s2 = impl.getPasswordID()
            result = s1 == s2
        
        if result:
            s1 = self.getPassword()
            s2 = impl.getPassword()
            result = s1 == s2
        
        if result:
            result = self.getPasswordCreateDate() == impl.getPasswordCreateDate()
        
        if result:
            result = self.getPasswordUpdateDate() == impl.getPasswordUpdateDate()
        
        if result:
            s1 = self.getPasswordCreateUser()
            s2 = impl.getPasswordCreateUser()
            result = s1 == s2
        
        if result:
            s1 = self.getPasswordUpdateUser()
            s2 = impl.getPasswordUpdateUser()
            result = s1 == s2
        
        return result
    
    def __str__(self):
        return self.getDisplayString()
        
    def getDisplayString(self):
        return 'Password{passwordId=' + \
            str(self.passwordID.value) + \
            ', password=' + \
            Login.encrypter.decrypt(self.getPassword()) \
            +', passwordCreateDate=' + str(self.passwordCreateDate.value)
    
    def getPassword(self):
        return self.password.getValue()

    def setValidatedPassword(self, txt):
        self.password.setValue(txt)
        
    def setPassword(self, txt):
        if not txt or not Utils.notBlank(txt):
            raise InvalidArgumentException('Argument not a string')
        encTxt = Password.encrypter.encrypt(txt)
        self.password.setValue(encTxt)
        # print(str(len(encTxt)) +  =  + encTxt )

    def setPasswordID(self, uid):
        self.passwordID.setValue(uid)

    def getPasswordID(self):
        return self.passwordID.getValue()

    def setPasswordLoginID(self, uid):
        self.passwordLoginID.setValue(uid)

    def getPasswordLoginID(self):
        return self.passwordLoginID.getValue()
    
    def setUpdateUser(self, uid):
        self.setPasswordUpdateUser(uid)
    
    def getUpdateDate(self):
        return self.getPasswordUpdateDate()

    def setCreateUser(self, uid):
        self.setPasswordCreateUser(uid)
    
    def setCreateDate(self, date):
        self.setPasswordCreateDate(date)
    
    def setUpdateDate(self, date):
        self.setPasswordUpdateDate(date)

    def getPasswordCreateDate(self):
        return self.passwordCreateDate.getValue()
    
    def setPasswordCreateDate(self, passwordCreateDate):
        self.passwordCreateDate.setValue(passwordCreateDate)

    def getPasswordUpdateDate(self):
        return self.passwordUpdateDate.getValue()
    
    def setPasswordUpdateDate(self, passwordUpdateDate):
        self.passwordUpdateDate.setValue(passwordUpdateDate)
    
    def getPasswordCreateUser(self):
        return self.passwordCreateUser.getValue()
    
    def setPasswordCreateUser(self, passwordCreateUser):
        self.passwordCreateUser.setValue(passwordCreateUser)
    
    def getPasswordUpdateUser(self):
        return self.passwordUpdateUser.getValue()
    
    def setPasswordUpdateUser(self, passwordUpdateUser):
        self.passwordUpdateUser.setValue(passwordUpdateUser)

    def getLastUpdateUser(self):
        return self.getPasswordUpdateUser()
    
    def getCreateUser(self):
        return self.getPasswordCreateUser()
      
    def toDb(self):
        for name, att in self.__dict__.items():
            a = att
            if isinstance(att, Attribute):
                a = att.value
            self.myDb.__dict__[name] = a
            # print(\n + str(name) +  =  + str(a) +   + str(type(a)))
    
    def fromDb(self):
        for name, att in self.myDb.__dict__.items():
            myAtt = self.__dict__.get(name)
            if not myAtt: 
                self.__dict__[name] = att
            else:
                a = att
                if isinstance(att, bytes):
                    a = att.decode()
                if isinstance(myAtt, Attribute):
                    myAtt.value = a
                else:
                    myAtt = a
                self.__dict__[name] = myAtt
        if self.myDb.login:
            self.passwordLoginID.value = self.myDb.login.loginID 
        # print(self.__dict__)
        
    def validate(self):
        atts = self.getAttributeList()
        BusinessObjectBase.validateAttributes(atts)
        
    def save(self):
        self.validate()
        self.toDb()
        self.myDb.save()
        self.fromDb()
  
    def remove(self):
            self.myDb.delete()
              
    def delete(self):
        self.myDb.deleteFlag = True
        self.myDb.save()
    
    def getAttributeList(self): 
        return [
            self.passwordID,
            self.password,
            self.passwordCreateDate,
            self.passwordUpdateDate,
            self.passwordCreateUser,
            self.passwordUpdateUser
        ]       


class SecurityGroup(BusinessObject): 

    DESCRIPTION_LENGTH = 250
    NAME_LENGTH = 40

    def __init__(self, myDb=None,sg=None):
        super().__init__()
        self.myDb = myDb
        self.securityGroupID = IntegerAttribute("securityGroupID")
        self.securityGroupName = StringAttribute("securityGroupName")
        self.level = IntegerAttribute("level")
        self.securityGroupDescription = StringAttribute("securityGroupDescription")
        self.securityGroupCreateDate = DateAttribute("securityGroupCreateDate")
        self.securityGroupUpdateDate = DateAttribute("securityGroupUpdateDate")
        self.securityGroupCreateUser = IntegerAttribute("securityGroupCreateUser")
        self.securityGroupUpdateUser = IntegerAttribute("securityGroupUpdateUser")
        self.organization = None
        self.privileges = []
        super().setIdProperties(self.securityGroupID)
        super().setTrackingAttributes(
                self.securityGroupCreateUser,
                self.securityGroupCreateUser,
                self.securityGroupCreateDate,
                self.securityGroupUpdateDate)

        self.securityGroupName.allowInvalID = False
        self.securityGroupName.setHasMaximumLength(True)
        self.securityGroupName.setMaximumLength(SecurityGroup.NAME_LENGTH)
        self.securityGroupName.setNullAllowed(False)
        self.securityGroupName.setNullStringAllowed(False)
        
        self.securityGroupDescription.allowInvalID = False
        self.securityGroupDescription.setHasMaximumLength(True)
        self.securityGroupDescription.setMaximumLength(SecurityGroup.DESCRIPTION_LENGTH)
        self.securityGroupDescription.setNullAllowed(False)
        self.securityGroupDescription.setNullStringAllowed(False)
        self.level.setNullAllowed(False)
        self.level.setHasMinimum(True)
        self.level.setMinimum(1)
        if myDb:
            self.fromDb()
        now = DT.now().date()
        self.setSecurityGroupCreateDate(now)
        self.setSecurityGroupUpdateDate(now)
        if sg:
            self.clone(sg)
        
    def clone(self, sg):
        self.securityGroupName = sg.securityGroupName
        self.level = sg.level
        self.securityGroupDescription = sg.securityGroupDescription
        #print(sg)
        self.securityGroupCreateDate = sg.securityGroupCreateDate
        self.securityGroupUpdateDate = sg.securityGroupUpdateDate
        self.securityGroupCreateUser = sg.securityGroupCreateUser
        self.securityGroupUpdateUser = sg.securityGroupUpdateUser
        self.organization = sg.organization
        self.privileges = sg.privileges
        return self
    
    def getOrganization(self):
        return self.organization

    def setOrganization(self, org):
        if org:
            if isinstance(org, DbOrganization):
                org = Organization(org)
                org.fromDb()
        self.organization = org
    
    def getDisplayString(self):
        return self.getSecurityGroupName()

    def getSecurityGroupName(self):
        return self.securityGroupName.getValue()
    
    def setSecurityGroupName(self, name):
        self.securityGroupName.setValue(name)
    
    def getSecurityGroupDescription(self):
        return self.securityGroupDescription.getValue()
    
    def setSecurityGroupDescription(self, desc):
        self.securityGroupDescription.setValue(desc)
                        
    def setSecurityGroupID(self, uid):
        self.securityGroupID.setValue(uid)

    def setLevel(self, level):
        self.level.setValue(level)
        
    def getLevel(self):
        return self.level.getValue()

    def getSecurityGroupID(self):
        return self.securityGroupID.getValue()

    def setSecurityGroupOrganizationID(self, uid):
        self.securityGroupOrganizationID.setValue(uid)
        
    def getSecurityGroupOrganizationID(self):
        return self.securityGroupOrganizationID.getValue()
        
    def setUpdateUser(self, uid):
        self.setSecurityGroupUpdateUser(uid)
    
    def getUpdateDate(self):
        return self.getSecurityGroupUpdateDate()
        
    def setCreateUser(self, uid):
        self.setSecurityGroupCreateUser(uid)
        
    def setCreateDate(self, d):
        self.setSecurityGroupCreateDate(d)
        
    def setUpdateDate(self, d):
        self.setSecurityGroupUpdateDate(d)
    
    def getSecurityGroupCreateDate(self):
        return self.securityGroupCreateDate.getValue()
    
    def setSecurityGroupCreateDate(self, createDate):
        self.securityGroupCreateDate.setValue(createDate)
    
    def getSecurityGroupUpdateDate(self):
        return self.securityGroupUpdateDate.getValue()
    
    def setSecurityGroupUpdateDate(self, updateDate):
        self.securityGroupUpdateDate.setValue(updateDate)
    
    def getSecurityGroupCreateUser(self):
        return self.securityGroupCreateUser.getValue()

    def setSecurityGroupCreateUser(self, updateUser):
        self.securityGroupCreateUser.setValue(updateUser)
    
    def getSecurityGroupUpdateUser(self):
        return self.securityGroupUpdateUser.getValue()

    def setSecurityGroupUpdateUser(self, updateUser):
        self.securityGroupUpdateUser.setValue(updateUser)
    
    def getPrivileges(self):
        return self.privileges
    
    def setPrivileges(self, privileges):
        self.privileges = privileges
    
    def addPrivilege(self, p):
        if self.privileges.contains(p) == False:
            self.privileges.append(p)
        
    def removePrivilege(self, p):
        self.privileges.remove(p)
        
    def getLastUpdateUser(self):
        return self.getSecurityGroupUpdateUser()
    
    def getCreateUser(self):
        return self.getSecurityGroupCreateUser()    
    
    def __str__(self):
        s = 'SecurityGroup{securityGroupID: '
        s += str(self.securityGroupID.value)
        s += ' securityGroupName: '
        s += str(self.securityGroupName.value)
        s += ' securityGroupDescription: '
        s += str(self.securityGroupDescription.value)
        s += ' privileges '
        s += str(self.getPrivileges())
        s += '}'
        return s
  
    def toDb(self):
        for name, att in self.__dict__.items():
            a = att
            if isinstance(att, Attribute):
                a = att.value
            self.myDb.__dict__[name] = a
            # print(\n + str(name) +  =  + str(a) +   + str(type(a)))
    
    def fromDb(self):
        for name, att in self.myDb.__dict__.items():
            myAtt = self.__dict__.get(name)
            if not myAtt: 
                self.__dict__[name] = att
            else:
                a = att
                if isinstance(att, bytes):
                    a = att.decode()
                if isinstance(myAtt, Attribute):
                    myAtt.value = a
                else:
                    myAtt = a
                self.__dict__[name] = myAtt
        # print(self.__dict__)
        
    def validate(self):
        atts = self.getAttributeList()
        BusinessObjectBase.validateAttributes(atts)
        
    def save(self):
        self.validate()
        self.toDb()
        self.myDb.save()
        self.fromDb()
  
    def remove(self):
            self.myDb.delete()
              
    def delete(self):
        self.myDb.deleteFlag = True
        self.myDb.save()
    
    def getAttributeList(self): 
        return [
            self.securityGroupID,
            self.securityGroupName,
            self.level,
            self.securityGroupDescription,
            self.securityGroupCreateDate,
            self.securityGroupUpdateDate,
            self.securityGroupCreateUser,
            self.securityGroupUpdateUser
        ]       


class WorkAddress(BusinessObject):

    def __init__(self, myDb=None, addr=None):

        super().__init__()

        self.workAddressID = IntegerAttribute("workAddressID")
        self.waAddressID = IntegerAttribute("waAddressID")
        self.employer = StringAttribute("employer")
        self.jobTitle = StringAttribute("jobTitle")
        self.waCreateUser = IntegerAttribute("waCreateUser")
        self.waUpdateUser = IntegerAttribute("waUpdateUser")
        self.waCreateDate = DateAttribute("waCreateDate")
        self.waUpdateDate = DateAttribute("waUpdateDate")
        self.address = None
        self.myDb = myDb
        if myDb:
            self.fromDb()
        super().setIdProperties(self.workAddressID)
        super().setTrackingAttributes(self.waCreateUser,
                self.waUpdateUser,
                self.waCreateDate,
                self.waUpdateDate)
        
        self.employer.allowInvalID = False
        self.employer.setHasMaximumLength(True)
        self.employer.setMaximumLength(Constants.EMPLOYER_LENGTH)

        self.jobTitle.allowInvalID = False
        self.jobTitle.setHasMaximumLength(True)
        self.jobTitle.setMaximumLength(Constants.JOB_TITLE_LENGTH)
        
        if addr:
            self.address = addr
        else:
            self.address = Address()
    
    def isSameState(self, impl):
        result = super().isSameBaseState(impl)
        if result: 
            ai1 = self.getAddress()
            ai2 = impl.getAddress()
            if (ai1 != None and ai2 == None):
                result = False
            elif (ai1 == None and ai2 != None):
                result = False
            elif (ai1 != None and ai2 != None):
                result = ai1.isSameState(ai2)
        
        if result:
            s1 = self.getWorkAddressID()
            s2 = impl.getWorkAddressID()
            result = s1 == s2
        
        if result:
            s1 = self.getWaAddressID()
            s2 = impl.getWaAddressID()
            result = s1 == s2
        
        if result:
            s1 = self.getEmployer()
            s2 = impl.getEmployer()
            result = s1 == s2
        
        if result:
            s1 = self.getJobTitle()
            s2 = impl.getJobTitle()
            result = s1 == s2
        
        if result:
            result = self.getWaCreateDate() == impl.getWaCreateDate()
        
        if result:
            result = self.getWaUpdateDate() == impl.getWaUpdateDate()
        
        if result:
            s1 = self.getWaCreateUser()
            s2 = impl.getWaCreateUser()
            result = s1 == s2
        
        if result:
            s1 = self.getWaUpdateUser()
            s2 = impl.getWaUpdateUser()
            result = s1 == s2
        
        return result
    
    def getAddress(self):
        if not self.address:
            dbo = DbAddress()
            self.address = Address(dbo)    
    
    def dropAddress(self):
        self.address.delete()
        self.address = None
    
    def getDisplayString(self):
        return self.toString()
    
    def getEmployer(self):
        return self.employer.getValue()
    
    def setEmployer(self, newEmployer):
        self.employer.setValue(newEmployer)
        
    def setJobTitle(self, newJobTitle):
        self.jobTitle.setValue(newJobTitle)
        
    def getJobTitle(self):
        return self.jobTitle.getValue()

    def setAddress(self, newAddress):
        self.address = newAddress
        
        if self.address:
            self.setWaAddressID(self.address.getAddressID())

    def getStreet(self):
        return self.getAddress().getStreet()

    def getAddressLineTwo(self):
        return self.getAddress().getAddressLineTwo()
    
    def getCity(self):
        return self.getAddress().getCity()
    
    def getState(self):
        return self.getAddress().getState()
    
    def getPostalCode(self):
        return self.getAddress().getPostalCode()
    
    def getPhone(self):
        return self.getAddress().getPhone()
    
    def getMobilePhone(self):
        return self.getAddress().getMobilePhone()
    
    def getFax(self):
        return self.getAddress().getFax()
    
    def getPager(self):
        return self.getAddress().getPager()
    
    def getEmail(self):
        return self.getAddress().getEmail()

    def getWorkAddressID(self):
        return self.workAddressID.getValue()
    
    def setWorkAddressID(self, aid):
        self.workAddressID.setValue(aid)
    
    def getWaAddressID(self):
        return self.waAddressID.getValue()
   
    def setWaAddressID(self, wid):
        self.waAddressID.setValue(wid)

    def setUpdateUser(self, wid):
        self.setWaUpdateUser(wid)
        if self.address:
            self.address.setUpdateUser(wid)
    
    def getUpdateDate(self):
        return self.getWaUpdateDate()
    
    def setCreateUser(self, uid):
        self.setWaCreateUser(uid)
        if self.address:
            self.address.setCreateUser(uid)

    def setCreateDate(self, d):
        self.setWaCreateDate(d)

    def setUpdateDate(self, d):
        self.setWaUpdateDate(d)
        if self.address:
            self.address.setAddrressUpdateDate(d)
        
    def getWaCreateDate(self):
        return self.waCreateDate.getValue()
    
    def setWaCreateDate(self, waCreateDate):
        self.waCreateDate.setValue(waCreateDate)
    
    def setAddressCreateUser(self, oid):
        self.address.setCreateUser(oid)
    
    def setAddressUpdateUser(self, oid):
        self.address.setUpdateUser(oid)

    def getWaUpdateDate(self):
        return self.waUpdateDate.getValue()
    
    def setWaUpdateDate(self, waUpdateDate):
        self.waUpdateDate.setValue(waUpdateDate)
    
    def getWaCreateUser(self):
        return self.waCreateUser.getValue()
    
    def setWaCreateUser(self, waCreateUser):
        self.waCreateUser.setValue(waCreateUser)

    def getWaUpdateUser(self):
        return self.waUpdateUser.getValue()

    def setWaUpdateUser(self, waUpdateUser):
        self.waUpdateUser.setValue(waUpdateUser)

    def setStreet(self, newStreet):
        self.address.setStreet(newStreet)

    def setAddressLineTwo(self, newAddressLineTwo):
        self.address.setAddressLineTwo(newAddressLineTwo)

    def setCity(self, newCity):
        self.address.setCity(newCity)

    def setState(self, newState):
        self.address.setState(newState)

    def setPostalCode(self, newPostalCode):
        self.address.setPostalCode(newPostalCode)

    def setPhone(self, newPhone):
        self.address.setPhone(newPhone)

    def setMobilePhone(self, newMobilePhone):
        self.address.setMobilePhone(newMobilePhone)

    def setFax(self, newFax):
        self.address.setFax(newFax)
        
    def setPager(self, newPager):
        self.address.setPager(newPager)
        
    def setEmail(self, newEmail):
        self.address.setEmail(newEmail)
        
    def __str__(self):
        base = 'WorkAddress ['
        if self.address:
            base += str(self.address)
            foundFirst = False        
        if Utils.notBlank(self.employer.getValue()):
            base += "employer="
            base += self.employer.getValue()
            foundFirst = True
        
        if Utils.notBlank(self.jobTitle.getValue()):
            if foundFirst:
                base += ", "            
            base += "jobTitle="
            base += self.jobTitle.getValue()
            foundFirst = True
        if self.address:
            base += str(self.address)
        base += "]"
        return base
    
    def toDb(self):
        for name, att in self.__dict__.items():
            a = att
            if isinstance(att, Attribute):
                a = att.value
            self.myDb.__dict__[name] = a
            # print(\n + str(name) +  =  ) print(type(a))
    
    def fromDb(self):
        for name, att in self.myDb.__dict__.items():
            myAtt = self.__dict__.get(name)
            if not myAtt: 
                self.__dict__[name] = att
            else:
                a = att
                if isinstance(att, bytes):
                    a = att.decode()
                if isinstance(myAtt, Attribute):
                    myAtt.value = a
                else:
                    myAtt = a
                self.__dict__[name] = myAtt

                # print(name)print(a)   
        # print(self.__dict__)
    def validate(self):
        atts = self.getAttributeList()
        BusinessObject.validateAttributes(atts)
        
    def save(self):
        if self.workAddressID.value:
            if super().isDirty():
                self.toDb()
                self.myDb.save()
                self.fromDb()
        else:
            self.toDb()
            self.myDb.save()
            self.fromDb()
  
    def remove(self):
            self.myDb.delete()
              
    def delete(self):
        self.myDb.deleteFlag = True
        self.myDb.save()
       
    def getAttributeList(self): 
        atts = [
            self.workAddressID,
            self.waAddressID,
            self.employer,
            self.jobTitle,
            self.waCreateUser,
            self.waUpdateUser,
            self.waCreateDate,
            self.waUpdateDate
        ]    
        return atts

    
class Organization(BusinessObject):
    CAME_FROM = "cameFromOrganization"
    NAME_LENGTH = 255
 
    def __init__(self, myDb=None):
        self.organizationID = IntegerAttribute("organizationID")
        self.organizationAddressID = IntegerAttribute("organizationAddressID")
        self.organizationName = StringAttribute("organizationName")
        self.organizationCreateUser = IntegerAttribute("organizationCreateUser")
        self.organizationUpdateUser = IntegerAttribute("organizationUpdateUser")
        self.organizationCreateDate = DateAttribute("organizationCreateDate")
        self.organizationUpdateDate = DateAttribute("organizationUpdateDate")
        self.address = None
        super().__init__()
        super().setIdProperties(self.organizationID)
        super().setTrackingAttributes(self.organizationCreateUser,
                self.organizationUpdateUser,
                self.organizationCreateDate,
                self.organizationUpdateDate)

        try:
            self.organizationName.allowInvalID = False
            self.organizationName.setNullAllowed(False)
            self.organizationName.setNullStringAllowed(False)
            self.organizationName.setAllSpacesAllowed(False)
            self.organizationName.setMixedCase(True)
            self.organizationName.setHasMaximumLength(True)
            self.organizationName.setMaximumLength(Organization.NAME_LENGTH)

            self.organizationAddressID.allowInvalID = False
            self.organizationAddressID.setNullAllowed(True)
            self.organizationAddressID.setHasMinimum(True)
            self.organizationAddressID.setMinimum(0)
            
            self.organizationCreateDate.setValue(super().now())
            self.organizationUpdateDate.setValue(super().now())
        except:
            logger.opt(exception=True).debug('failure setting up Organization')
        self.myDb = myDb
        if myDb:
            self.fromDb()
             
    def isSameState(self, vsp):
        result = True
        if not vsp or not isinstance(vsp, Organization):
            result = False
        
        if result:
            result = super().isSameBaseState(vsp)
        
        if result:
            result = self.getOrganizationID() == vsp.getOrganizationID()
        
        if result:
            s1 = self.getOrganizationName()
            s2 = vsp.getOrganizationName()
            result = s1 == s2
        
        if result:
            result = self.getOrganizationCreateDate() == vsp.getOrganizationCreateDate()
        
        if result:
            result = self.getOrganizationUpdateDate() == vsp.getOrganizationUpdateDate()
        
        if result:
            result = self.getOrganizationCreateUser() == vsp.getOrganizationCreateUser()
        
        if result:
            result = self.getOrganizationUpdateUser() == vsp.getOrganizationUpdateUser()
        
        if result:
            result = self.getOrganizationAddressID() == vsp.getOrganizationAddressID()
        
        ai1 = self.getAddress()
        ai2 = vsp.getAddress()
        if result:
            if not ai1 and not ai2:
                pass
            elif (ai1 and not ai2):
                result = False
            elif (not ai1 and ai2 != None):
                result = False
            elif (ai1 != None and ai2 != None):
                result = ai1.isSameState(ai2)
        return result
    
    def compareTo(self, o):
        result = -1
        if not o:
            result = 1
        elif isinstance(o, Organization):
            oKey = o.getOrganizationName()
            key = self.getOrganizationName()
            result = Utils.compareTo(key, oKey)
        else:
            raise InvalidArgumentException("Object " + o + "is not an instance of Organization")
        return result

    def setAddress(self, ai):
        self.address = ai
        if ai:
            self.setOrganizationAddressID(ai.addressID.value)
        else:
            self.setOrganizationAddressID(None)
    
    def getAddress(self):
        return self.address
    
    def getOrganizationID(self):
        return self.organizationID.getValue()

    def setOrganizationID(self, oid):
        if oid:
            self.organizationID.setValue(oid)
        else:
            self.organizationID.setValue(0)

    def getOrganizationAddressID(self):
        return self.organizationAddressID.getValue()
    
    def setOrganizationAddressID(self, oid):
        self.organizationAddressID.setValue(oid)
        
    def getOrganizationName(self):
        return self.organizationName.getValue()
    
    def setOrganizationName(self, name):
        self.organizationName.setValue(name)

    def setName(self, name):
        self.setOrganizationName(name)
        
    def getName(self):
        return self.getOrganizationName()

    def getAddressForUpdate(self):
        result = self.address
        if not result:
            dba = self.myDb.address
            if not dba:
                dba = DbAddress()
            dba.addressCreateDate = super().now()
            dba.addressUpdateDate = super().now()
            dba.addressCreateUser = self.organizationUpdateUser.value
            dba.addressUpdateUser = self.organizationUpdateUser.value
            dba.save() 
            result = Address(dba)
            self.myDb.address = dba
            result.setAddressCreateUser(self.getOrganizationCreateUser())
            result.setAddressUpdateUser(self.getOrganizationUpdateUser())
            result.save()
            result.setAddressID(result.myDb.addressID)
            self.setAddress(result)
            
        return result
    
    def getEmail(self):
        result = None
        if self.getAddress():
            result = self.getAddress().getEmail()
        return result
    
    def setEmail(self, add):
        if add and not add.strip() == '':
            self.getAddressForUpdate().setEmail(add)
    
    def getPhone(self):
        result = None
        if self.address:
            result = self.getAddress().getPhone()        
        return result

    def setPhone(self, add):
        if add and not add.strip() == '':
            self.getAddressForUpdate().setPhone(add)

    def getPager(self):
        result = None
        if self.getAddress():
            result = self.getAddress().getPager()
        return result
    
    def setPager(self, add):
        if add and not add.strip() == '':
            self.getAddressForUpdate().setPager(add)
    
    def getMobilePhone(self):
        result = None
        if self.getAddress():
            result = self.getAddress().getMobilePhone()        
        return result
    
    def setMobilePhone(self, add):
        if add and not add.strip() == '':
            self.getAddressForUpdate().setMobilePhone(add)
            
    def getFax(self):
        result = None
        if self.getAddress():
            result = self.getAddress().getFax()
        return result
    
    def setFax(self, add):
        if add and not add.strip() == '':
            self.getAddressForUpdate().setFax(add)
    
    def getPostalCode(self):
        result = None
        if self.getAddress():
            result = self.getAddress().getPostalCode()
        return result

    def setPostalCode(self, add):
        if add and not add.strip() == '':
            self.getAddressForUpdate().setPostalCode(add)

    def getState(self):
        result = None
        if  self.getAddress():
            result = self.getAddress().getState()
        return result
   
    def setState(self, add):
        if add and not add.strip() == '':
            self.getAddressForUpdate().setState(add)
    
    def getCity(self):
        result = None
        if  self.getAddress():
            result = self.getAddress().getCity()
        return result

    def setCity(self, add):
        if add and not add.strip() == '':
            self.getAddressForUpdate().setCity(add)
    
    def getAddressLineTwo(self):
        result = None
        if  self.getAddress():
            result = self.getAddress().getAddressLineTwo()
        return result

    def setAddressLineTwo(self, add):
        if add and not add.strip() == '':
            self.getAddressForUpdate().setAddressLineTwo(add)

    def getStreet(self):
        result = None
        if  self.getAddress():
            result = self.getAddress().getStreet()        
        return result
    
    def setStreet(self, add):
        if Utils.notBlank(add):
            self.getAddressForUpdate().setStreet(add)
            
    def getDisplayString(self):
        if self.organizationName and self.organizationName.getValue():
            return self.organizationName.getValue().strip() 
        else:
            return 
    
    def setUpdateUser(self, uid):
        if isinstance(uid, int):
            self.setOrganizationUpdateUser(uid)
        else:
            raise InvalidArgumentException()

    def getUpdateDate(self):
        return self.getOrganizationUpdateDate()
    
    def setCreateUser(self, uid):
        if isinstance(uid, int):
            self.setOrganizationCreateUser(uid)
        else:
            raise InvalidArgumentException()
        
    def setCreateDate(self, date):
        self.setOrganizationCreateDate(date)
    
    def setUpdateDate(self, date):
        self.setOrganizationUpdateDate(date)
    
    def getOrganizationCreateDate(self):
        return self.organizationCreateDate.getValue()

    def setOrganizationCreateDate(self, dt):
        self.organizationCreateDate.setValue(dt)
    
    def getOrganizationUpdateDate(self):
        return self.organizationUpdateDate.getValue()

    def setOrganizationUpdateDate(self, dt):
        self.organizationUpdateDate.setValue(dt)
    
    def getOrganizationCreateUser(self):
        return self.organizationCreateUser.getValue()

    def setOrganizationCreateUser(self, organizationCreateUser):
        self.organizationCreateUser.setValue(organizationCreateUser)
    
    def getOrganizationUpdateUser(self):
        return self.organizationUpdateUser.getValue()

    def setOrganizationUpdateUser(self, organizationUpdateUser):
        self.organizationUpdateUser.setValue(organizationUpdateUser)
     
    def getLastUpdateUser(self):
        return self.getOrganizationUpdateUser()
    
    def getCreateUser(self):
        return self.getOrganizationCreateUser()
    
    def toDb(self):
        for name, att in self.__dict__.items():
            if name == 'organizationID' and not att:
                print('skipped ' + str(att))
                continue
            a = att
            if isinstance(att, Attribute):
                a = att.value
            self.myDb.__dict__[name] = a
            if self.address:
                self.myDb.save()
                self.address.save()
                self.myDb.address = self.address.myDb
            # print(\n + str(name) +  =  ) print(type(a))
    
    def fromDb(self):
        for name, att in self.myDb.__dict__.items():
            myAtt = self.__dict__.get(name)
            if not myAtt: 
                self.__dict__[name] = att
            else:
                a = att
                if isinstance(att, bytes):
                    a = att.decode()
                if isinstance(myAtt, Attribute):
                    myAtt.value = a
                else:
                    myAtt = a
                self.__dict__[name] = myAtt
                # print(self.organizationID)
        if self.myDb.address:
            self.address = Address(self.myDb.address)
            # print('1st IF')
            
        if self.address and isinstance(self.address, DbAddress):
            self.address = Address(self.myDb.address)
            # print('2nd IF')
        
    def validate(self):
        atts = self.getAttributeList()
        BusinessObjectBase.validateAttributes(atts)
        
    def save(self):
        self.toDb()
        self.myDb.save()
        self.organizationID.setValue(self.myDb.organizationID)
  
    def remove(self):
            self.myDb.delete()
              
    def delete(self):
        self.myDb.deleteFlag = True
        self.myDb.save()
    
    def getAttributeList(self): 
        return [
            self.organizationID,
        self.organizationAddressID,
        self.organizationName,
        self.organizationCreateUser,
        self.organizationUpdateUser,
        self.organizationCreateDate,
        self.organizationUpdateDate]
    
    def __str__(self):
        result = self.getOrganizationName() + ' id='
        result += str(self.getOrganizationID())
        if self.address:
            result += (' ' + str(self.address))
        return result

  
class ConfigurationSet(BusinessObject):
   
    def __init__(self, myDb=None):
        self.myDb = myDb
        self.configurationSetID = IntegerAttribute("configurationSetID")
        self.configurationSetName = StringAttribute("configurationSetName")
        self.configurationSetOrganizationID = IntegerAttribute("configurationSetOrganizationID")
        self.configurationSetCreateUser = IntegerAttribute("configurationSetCreateUser")
        self.configurationSetUpdateUser = IntegerAttribute("configurationSetUpdateUser")
        self.configurationSetCreateDate = DateAttribute("configurationSetCreateDate")
        self.configurationSetUpdateDate = DateAttribute("configurationSetUpdateDate")
        self.organization = None
        self.properties = []
        super().__init__()
        super().setIdProperties(self.configurationSetID)
        super().setTrackingAttributes(
            self.configurationSetCreateUser,
            self.configurationSetUpdateUser,
            self.configurationSetCreateDate,
            self.configurationSetUpdateDate)
        if myDb:
            self.fromDb()
    
    def clone(self, cs):
        try:
            self.setConfigurationSetName(cs.getConfigurationSetName())
            self.setOrganization(cs.getOrganization())
            self.setConfigurationSetOrganizationID(cs.getConfigurationSetOrganizationID())
            self.setConfigurationSetCreateUser(cs.getConfigurationSetCreateUser())
            self.setConfigurationSetUpdateUser(cs.getConfigurationSetUpdateUser())
            self.setConfigurationSetCreateDate(cs.getConfigurationSetCreateDate())
            self.setConfigurationSetUpdateDate(cs.getConfigurationSetUpdateDate())
            for cp in cs.getProperties():
                cpNew = ConfigurableProperty().clone(cp)
                self.addProperty(cpNew)            
        except InvalidAttributeValueException as unlikely:
            super().handleException(unlikely)
            
    def getConfigurableProperties(self):
        return self.properties

    def getConfigurationSetID(self):
        return self.configurationSetID.getValue()

    def setConfigurationSetID(self, configurationSetID):
        self.configurationSetID.setValue(configurationSetID)

    def getConfigurationSetName(self):
        return self.configurationSetName.getValue()

    def setConfigurationSetName(self, configurationSetName):
        self.configurationSetName.setValue(configurationSetName)

    def getConfigurationSetOrganizationID(self):
        return self.configurationSetOrganizationID.getValue()
    
    def setConfigurationSetOrganizationID(self, configurationSetOrganizationID):
        self.configurationSetOrganizationID.setValue(configurationSetOrganizationID)

    def getConfigurationSetCreateUser(self):
        return self.configurationSetCreateUser.getValue()
    
    def setConfigurationSetCreateUser(self, configurationSetCreateUser):
        self.configurationSetCreateUser.setValue(configurationSetCreateUser)

    def getConfigurationSetUpdateUser(self):
        return self.configurationSetUpdateUser.getValue()

    def setConfigurationSetUpdateUser(self, configurationSetUpdateUser):
        self.configurationSetUpdateUser.setValue(configurationSetUpdateUser)    

    def getConfigurationSetCreateDate(self):
        return self.configurationSetCreateDate.getValue()

    def setConfigurationSetCreateDate(self, configurationSetCreateDate):
        self.configurationSetCreateDate.setValue(configurationSetCreateDate)    

    def getConfigurationSetUpdateDate(self):
        return self.configurationSetUpdateDate.getValue()

    def setConfigurationSetUpdateDate(self, configurationSetUpdateDate):
        self.configurationSetUpdateDate.setValue(configurationSetUpdateDate)

    def getOrganization(self):
        return self.organization    

    def setOrganization(self, org):
        try:
            self.organization = org
            if not org:
                self.setConfigurationSetOrganizationID(None)
            else:
                if isinstance(org, Organization) and not org.myDb:
                    org.myDb = DbOrganization()
                    org.toDb()
                self.myDb.organization_ID = org.getOrganizationID()
                self.setConfigurationSetOrganizationID(org.getOrganizationID())
                        
        except InvalidAttributeValueException as unlikely:
            super().handleException("setOrganization", unlikely)

    def getProperties(self):
        return self.properties
    
    def setProperties(self, properties):
        self.properties = properties
    
    def addProperty(self, prop):
        if prop and prop not in self.properties:
            self.properties.append(prop)
        
    def removeProperty(self, prop):
        if prop and prop in self.properties:
            self.properties.remove(prop)

    def setUpdateDate(self, d):
        self.setConfigurationSetUpdateDate(d)
    
    def setCreateDate(self, d):
        self.setConfigurationSetCreateDate(d)

    def setUpdateUser(self, uid):
        self.setConfigurationSetUpdateUser(uid)
    
    def setCreateUser(self, uid):
        self.setConfigurationSetCreateUser(uid)
        
    def __str__(self):
        result = "\nConfigurationSet{configurationSetID="
        if self.configurationSetID.value:
            result += str(self.configurationSetID.value)
        else:
            result += None 
            
        result += ", configurationSetName=" 
        if self.configurationSetName.value:
            result += self.configurationSetName.value
        else:
            result += None
             
        result += ", configurationSetOrganizationID="        
        if self.configurationSetOrganizationID:
            result += str(self.configurationSetOrganizationID.value)
        else:
            result += None
             
        result += ", configurationSetCreateUser=" 
        if self.configurationSetCreateUser: 
            result += str(self.configurationSetCreateUser.value)
        else:
            result += None
             
        result += ", configurationSetUpdateUser=" 
        if self.configurationSetUpdateUser: 
            result += str(self.configurationSetUpdateUser.value)
        else:
            result += None
             
        result += ", configurationSetCreateDate="
        if self.configurationSetCreateDate:
            result += str(self.configurationSetCreateDate.value)
        else:
            result += None
             
        result += ", configurationSetUpdateDate=" 
        if self.configurationSetUpdateDate:
            result += str(self.configurationSetUpdateDate.value)
        else:
            result += None
        if self.properties and len(self.properties): 
            for cp in self.properties:
                if cp:
                    # print(type(cp))
                    result += ' ' 
                    result += (str(cp))
                else:
                    result += ' cp was null'
        else:
            result += ' no properties'
            if self.myDb.properties and len(self.myDb.properties.all()):
                result += '-------'
                result += str(len(self.myDb.properties.all()))
                result += '-------'    
                for cp in self.myDb.properties.all():
                    if cp:
                        # print(type(cp))
                        result += (str(cp))
                    else:
                        result += 'myDb cp was null'
            else:
                result += 'myDb no properties'
        if self.organization:
            result += ', ' 
            result += str(self.organization)
        else:
            result += ' no organization'
        result += ' '
        return result

    def getDisplayString(self):
        return self.__str__()
    
    def toDb(self):
        for name, att in self.__dict__.items():
            a = att
            if isinstance(att, Attribute):
                a = att.value
            self.myDb.__dict__[name] = a
        if self.organization:
            self.myDb.organization = self.organization.myDb
            self.myDb.organization_ID = self.organization.getOrganizationID()
        for cp in self.properties:
            self.myDb.properties.add(cp.myDb)
        # print(\n + str(name) +  =  ) print(type(a))
    
    def fromDb(self):
        for name, att in self.myDb.__dict__.items():
            myAtt = self.__dict__.get(name)
            if not myAtt: 
                self.__dict__[name] = att
            else:
                a = att
                if isinstance(att, bytes):
                    a = att.decode()
                if isinstance(myAtt, Attribute):
                    myAtt.value = a
                else:
                    myAtt = a
                self.__dict__[name] = myAtt
        dbOrg = self.myDb.organization
        if dbOrg:
            o = Organization(dbOrg)
            self.setOrganization(o)
            self.configurationSetOrganizationID.value = self.organization.organizationID.value
        self.properties = []
        if self.myDb.configurationSetID:
            try:
                for idx, dbcp in enumerate(self.myDb.properties.all()):
                    self.trash = idx
                    if isinstance(dbcp, DbConfigurableProperty):
                        cpo = ConfigurableProperty(dbcp)
                        self.properties.append(cpo)
            except:
                logger.opt(exception=True). debug('fromDb(self)')

                # ValueError is expected if not saved 
                # print(name)print(a)   
                # print(str(self.myDb.__dict__))
    def validate(self):
        atts = self.getAttributeList()
        BusinessObject.validateAttributes(atts)
        
    def save(self):
        if self.configurationSetID.value:
            self.toDb()
            self.myDb.save()
        else:
            self.toDb()
            self.myDb.save()
        for cp in self.properties:
            if isinstance(cp, DbConfigurableProperty):
                self.myDb.properties.add(cp)
            else:
                self.myDb.properties.add(cp.myDb)                
        self.fromDb()
  
    def remove(self):
            self.myDb.delete()
              
    def delete(self):
        self.myDb.deleteFlag = True
        self.myDb.save()
    
    def getAttributeList(self): 
        return [
            self.configurationSetID,
            self.configurationSetName,
            self.configurationSetOrganizationID,
            self.configurationSetCreateUser,
            self.configurationSetUpdateUser,
            self.configurationSetCreateDate,
            self.configurationSetUpdateDate
        ]


class Location(BusinessObject):
    NAME_LENGTH = 255

    def __init__(self, myDb=None):
        super().__init__()
        
        self.locationID = IntegerAttribute("locationID")
        self.locationName = StringAttribute("locationName")
        self.locationOrganizationID = IntegerAttribute("locationOrganizationID")
        self.locationCreateUser = IntegerAttribute("locationCreateUser")
        self.locationUpdateUser = IntegerAttribute("locationUpdateUser")
        self.locationCreateDate = DateAttribute("locationCreateDate")
        self.locationUpdateDate = DateAttribute("locationUpdateDate")
        self.organization = None
        super().setIdProperties(self.locationID)
        super().setTrackingAttributes(
                self.locationCreateUser,
                self.locationUpdateUser,
                self.locationCreateDate,
                self.locationUpdateDate)

        try:
            self.locationName.allowInvalID = False
            self.locationName.setNullAllowed(False)
            self.locationName.setNullStringAllowed(False)
            self.locationName.setAllSpacesAllowed(False)
            self.locationName.setMixedCase(True)
            self.locationName.setHasMaximumLength(True)
            self.locationName.setMaximumLength(Location.NAME_LENGTH)

            self.locationOrganizationID.allowInvalID = False
            self.locationOrganizationID.setNullAllowed(True)
            self.locationOrganizationID.setHasMinimum(True)
            self.locationOrganizationID.setMinimum(0)
        except InvalidAttributeValueException as e:
            super().handleExveption(e)
        self.myDb = myDb
        if myDb:
            self.fromDb()
        
    def isSameState(self, vsp):
        result = super().isSameBaseState(vsp)
        
        if result:
            oi1 = self.getOrganization()
            oi2 = vsp.getOrganization()
            if (oi1 != None and oi2 == None):
                result = False
            elif (oi1 == None and oi2 != None):
                result = False
            elif (oi1 != None and oi2 != None):
                result = oi1.isSameState(oi2)
        
        if result:
            s1 = self.getLocationID()
            s2 = vsp.getLocationID()
            result = s1 == s2
        
        if result:
            s1 = self.getLocationName()
            s2 = vsp.getLocationName()
            result = s1 == s2
        
        if result:
            result = self.getLocationCreateDate() == vsp.getLocationCreateDate()
        
        if result:
            result = self.getLocationUpdateDate() == vsp.getLocationUpdateDate()
        
        if result:
            s1 = self.getLocationCreateUser()
            s2 = vsp.getLocationCreateUser()
            result = s1 == s2
        
        if result:
            s1 = self.getLocationUpdateUser()
            s2 = vsp.getLocationUpdateUser()
            result = s1 == s2
        
        return result
    
    def getLocationID(self):
        return self.locationID.getValue()

    def setLocationID(self, lid):
        self.locationID.setValue(lid)

    def getLocationName(self):
        return self.locationName.getValue()
    
    def setLocationName(self, name):
        self.locationName.setValue(name)

    def setName(self, name):
        self.setLocationName(name)
        
    def getName(self):
        return self.getLocationName()
    
    def getLocationOrganizationID(self):
        return self.locationOrganizationID.getValue()

    def setLocationOrganizationID(self, uid):
        self.locationOrganizationID.setValue(uid)
   
    def setOrganization(self, oi):
        self.organization = oi
        if not oi or not oi.getOrganizationID(): 
            oID = None
        else:
            oID = oi.getOrganizationID()
        try:
            self.setLocationOrganizationID(oid)
        except:
            logger.opt(exception=True).debug('setLocationOrganizationID(oid)')
            # super().handleException(t)
 
    def getOrganization(self):
        return self.organization

    def getDisplayString(self):
        if not self.locationName or not self.locationName.getValue():
            return None
        else: 
            return self.locationName.getValue().strip()
        
    def setUpdateUser(self, uid):
        self.setLocationUpdateUser(uid)
    
    def getUpdateDate(self):
        return self.getLocationUpdateDate()
    
    def setCreateUser(self, uid):
        self.setLocationCreateUser(uid)
   
    def setCreateDate(self, d):
        self.setLocationCreateDate(d)
    
    def setUpdateDate(self, d):
        self.setLocationUpdateDate(d)
    
    def getLocationCreateDate(self):
        return self.locationCreateDate.getValue()
    
    def setLocationCreateDate(self, lcd):
        self.locationCreateDate.setValue(lcd)
   
    def getLocationUpdateDate(self):
        return self.locationUpdateDate.getValue()
    
    def setLocationUpdateDate(self, lud):
        self.locationUpdateDate.setValue(lud)
    
    def getLocationCreateUser(self):
        return self.locationCreateUser.getValue()

    def setLocationCreateUser(self, locationCreateUser):
        self.locationCreateUser.setValue(locationCreateUser)
         
    def getLocationUpdateUser(self):
        return self.locationUpdateUser.getValue()

    def  setLocationUpdateUser(self, locationUpdateUser):
        self.locationUpdateUser.setValue(locationUpdateUser)
    
    def getLastUpdateUser(self):
        return self.getLocationUpdateUser()
    
    def getCreateUser(self):
        return self.getLocationCreateUser()
    
    def __str__(self):
        result = 'Location(locationID='
        s = self.getLocationID()
        if not s:
            result += 'None'
        else:
            result += str(s)
            
        result += ', locationName='
        s = self.getLocationName()
        if not s:
            result += 'None'
        else:
            result += str(s)
            
        result += ', locationOrganizationID='
        s = self.getLocationOrganizationID()
        if not s:
            result += 'None'
        else:
            result += str(s)
            
        result += ', locationCreateUser='
        s = self.getLocationCreateUser()
        if not s:
            result += 'None'
        else:
            result += str(s)
            
        result += ', locationUpdateUser='
        s = self.getLocationUpdateUser()
        if not s:
            result += 'None'
        else:
            result += str(s)
            
        result += ', locationCreateDate='
        s = self.getLocationCreateDate()
        if not s:
            result += 'None'
        else:
            result += str(s)
            
        result += ', locationUpdateDate='
        s = self.getLocationUpdateDate()
        if not s:
            result += 'None'
        else:
            result += str(s)
        return result
    
    def toDb(self):
        for name, att in self.__dict__.items():
            a = att
            if isinstance(att, Attribute):
                a = att.value
            self.myDb.__dict__[name] = a
        if self.organization:
            self.myDb.organization = self.organization.myDb
            self.myDb.organization_ID = self.organization.getOrganizationID()
        # print(\n + str(name) +  =  ) print(type(a))
    
    def fromDb(self):
        for name, att in self.myDb.__dict__.items():
            if isinstance(att, bytes):
                att = att.decode()
            myAtt = self.__dict__.get(name)
            if not myAtt: 
                self.__dict__[name] = att
            else:
                if isinstance(myAtt, Attribute):
                    myAtt.value = att
                else:
                    myAtt = att
                self.__dict__[name] = myAtt
        dbOrg = self.myDb.organization_id
        if dbOrg:
            o = Organization(self.myDb.organization)
            self.setOrganization(o)
            self.locationOrganizationID.value = self.organization.organizationID.value
         
            # print(name)print(a)   
            # print(str(self.myDb.__dict__))
    def validate(self):
        atts = self.getAttributeList()
        BusinessObject.validateAttributes(atts)
        
    def save(self):
        if self.locationID.value:
            self.toDb()
            self.myDb.save()
        else:
            self.toDb()
            self.myDb.save()       
        self.fromDb()
  
    def remove(self):
            self.myDb.delete()
              
    def delete(self):
        self.myDb.deleteFlag = True
        self.myDb.save()
    
    def getAttributeList(self): 
        return [
            self.locationID,
            self.locationName,
            self.locationOrganizationID,
            self.locationCreateUser,
            self.locationUpdateUser,
            self.locationCreateDate,
            self.locationUpdateDate
        ]


class Resource(BusinessObject): 

    COUNT_MINIMUM = 1
    NAME_MAXIMUM_LENGTH = 40
    NAME_SIZE = 40
    NAME = "Resource"
    
    def __init__(self, myDb=None):
        super().__init__()
        
        self.resourceID = IntegerAttribute("resourceID")
        self.resourceOrganizationID = IntegerAttribute("resourceOrganizationID")
        self.count = IntegerAttribute("count")
        self.name = StringAttribute("name")
        self.resourceCreateUser = IntegerAttribute("resourceCreateUser")
        self.resourceUpdateUser = IntegerAttribute("resourceUpdateUser")
        self.resourceCreateDate = DateAttribute("resourceCreateDate")
        self.resourceUpdateDate = DateAttribute("resourceUpdateDate")
        self.organization = None
        self.myDb = myDb
        if myDb:
            self.fromDb()
        
        super().setIdProperties(self.resourceID)
        super().setTrackingAttributes(
            self.resourceCreateUser,
            self.resourceUpdateUser,
            self.resourceCreateDate,
            self.resourceUpdateDate)

        try:
            self.count.allowInvalID = False
            self.count.setNullAllowed(False)
            self.count.setHasMinimum(True)
            self.count.setMinimum(Resource.COUNT_MINIMUM)

            self.resourceOrganizationID.allowInvalID = False
            self.resourceOrganizationID.setNullAllowed(False)
            self.resourceOrganizationID.setHasMinimum(True)
            self.resourceOrganizationID.setMinimum(Resource.COUNT_MINIMUM)

            self.name.allowInvalID = False
            self.name.setNullAllowed(False)
            self.name.setAllSpacesAllowed(False)
            self.name.setNullStringAllowed(False)
            self.name.setMixedCase(True)
            self.name.setHasMaximumLength(True)
            self.name.setMaximumLength(Resource.NAME_MAXIMUM_LENGTH)
        except InvalidAttributeValueException as e:
            super().handleException(e) 

    def isSameState(self, impl):
        result = super().isSameBaseState(impl)
        
        if result:
            s1 = self.getResourceID()
            s2 = impl.getResourceID()
            result = s1 == s2
        
        if result:
            s1 = self.getName()
            s2 = impl.getName()
            result = s1 == s2
        
        if result:
            s1 = self.getCount()
            s2 = impl.getCount()
            result = s1 == s2
        
        if result:
            result = self.getResourceCreateDate() == impl.getResourceCreateDate()
        
        if result:
            result = self.getResourceUpdateDate() == impl.getResourceUpdateDate()
        
        if result:
            s1 = self.getResourceCreateUser()
            s2 = impl.getResourceCreateUser()
            result = s1 == s2
        
        if result:
            s1 = self.getResourceUpdateUser()
            s2 = impl.getResourceUpdateUser()
            result = s1 == s2
        
        return result

    def getDisplayString(self):
        return str(self.getName()) + " : " + str(self.getCount())

    def getResourceID(self):
        if not self.resourceID.value:
            return None
        else:
            return self.resourceID.getValue()
    
    def setResourceID(self, resourceID):
        self.resourceID.setValue(resourceID)
    
    def getResourceOrganizationID(self):
        if not self.resourceOrganizationID.value:
            return None
        else:
            return self.resourceOrganizationID.getValue()

    def setResourceOrganizationID(self, resourceID):
        self.resourceOrganizationID.setValue(resourceID)
    
    def getOrganization(self):
        return self.organization    

    def setOrganization(self, organization):
        self.organization = organization
        if organization:
            self.setResourceOrganizationID(organization.getOrganizationID())
       
    def setUpdateUser(self, uid):
        self.setResourceUpdateUser(uid)

    def getUpdateDate(self):
        return self.getResourceUpdateDate()
    
    def setCreateUser(self, uid):
        self.setResourceCreateUser(uid)
    
    def setCreateDate(self, d):
        self.setResourceCreateDate(d)
    
    def setUpdateDate(self, d):
        self.setResourceUpdateDate(d)
    
    def getResourceCreateDate(self):
        return self.resourceCreateDate.getValue()
    
    def setResourceCreateDate(self, resourceCreateDate):
        self.resourceCreateDate.setValue(resourceCreateDate)

    def getResourceUpdateDate(self):
        return self.resourceUpdateDate.getValue()
    
    def setResourceUpdateDate(self, resourceUpdateDate):
        self.resourceUpdateDate.setValue(resourceUpdateDate)
    
    def getResourceCreateUser(self):
        return self.resourceCreateUser.getValue()

    def setResourceCreateUser(self, resourceCreateUser):
        self.resourceCreateUser.setValue(resourceCreateUser)
        
    def getResourceUpdateUser(self):
        return self.resourceUpdateUser.getValue()

    def setResourceUpdateUser(self, resourceUpdateUser):
        self.resourceUpdateUser.setValue(resourceUpdateUser)
    
    def getCount(self):
        return self.count.getValue()
    
    def setCount(self, ct):
        self.count.setValue(ct)
    
    def getName(self):
        return self.name.getValue()
    
    def setName(self, nm):
        self.name.setValue(nm)
    
    def getLastUpdateUser(self):
        return self.getResourceUpdateUser()
    
    def getCreateUser(self):
        return self.getResourceCreateUser()
    
    def __str__(self):
        return self.getName() + " count " + str(self.getCount())
    
    def toDb(self):
        for name, att in self.__dict__.items():
            a = att
            if isinstance(att, Attribute):
                a = att.value
            self.myDb.__dict__[name] = a
        if self.organization:
            self.myDb.organization = self.organization.myDb
            self.myDb.organization_ID = self.organization.getOrganizationID()
        # print(\n + str(name) +  =  ) print(type(a))
    
    def fromDb(self):
        for name, att in self.myDb.__dict__.items():
            if isinstance(att, bytes):
                att = att.decode()
            myAtt = self.__dict__.get(name)
            if not myAtt: 
                self.__dict__[name] = att
            else:
                if isinstance(myAtt, Attribute):
                    myAtt.value = att
                else:
                    myAtt = att
                self.__dict__[name] = myAtt
        dbOrg = self.myDb.organization
        if dbOrg:
            o = Organization(dbOrg)
            self.setOrganization(o)
            self.resourceOrganizationID.value = self.organization.organizationID.value
         
            # print(name)print(a)   
            # print(str(self.myDb.__dict__))
    def validate(self):
        atts = self.getAttributeList()
        BusinessObject.validateAttributes(atts)
        
    def save(self):
        if self.resourceID.value:
            self.toDb()
            self.myDb.save()
        else:
            self.toDb()
            self.myDb.save()       
        self.fromDb()
  
    def remove(self):
            self.myDb.delete()
              
    def delete(self):
        self.myDb.deleteFlag = True
        self.myDb.save()
    
    def getAttributeList(self): 
        return [
            self.resourceID,
            self.resourceOrganizationID,
            self.count,
            self.name,
            self.resourceCreateUser,
            self.resourceUpdateUser,
            self.resourceCreateDate,
            self.resourceUpdateDate,
            self.organization
        ]


class ResourceUsage(Resource):

    def __init__(self, myDb=None,resource=None):
        super().__init__()
        self.myDb = myDb
        try:
            if myDb:
                super().fromDb()
            super().count.setMinimum(0)
            if resource:
                super().setName(resource.getName())
                super().setResourceID(resource.getResourceID())
                super().setID(resource.getID())
        except:
            pass
    
    def __str__(self):
        return super().getName() + " count " + str(super().getCount())


class SkillRelationship(BusinessObject):
    
    NAME_SIZE = 25

    def __init__(self, myDb=None):
        self.skillRelationshipTypeID = IntegerAttribute("skillRelationshipTypeID")
        self.skillOneID = IntegerAttribute("skillOneID")
        self.skillTwoID = IntegerAttribute("skillTwoID")
        self.skillRelationshipID = IntegerAttribute("skillRelationshipID")
        self.skillRelationshipCreateUser = IntegerAttribute("skillRelationshipCreateUser")
        self.skillRelationshipUpdateUser = IntegerAttribute("skillRelationshipUpdateUser")
        self.skillRelationshipCreateDate = DateAttribute("skillRelationshipCreateDate")
        self.skillRelationshipUpdateDate = DateAttribute("skillRelationshipUpdateDate")
        self.type = None
        self.organization = None
        super().__init__()
        super().setIdProperties(self.skillRelationshipID)
        super().setTrackingAttributes(self.skillRelationshipCreateUser,
                self.skillRelationshipUpdateUser,
                self.skillRelationshipCreateDate,
                self.skillRelationshipUpdateDate)

        self.skillRelationshipTypeID.allowInvalID = False
        self.skillRelationshipTypeID.setNullAllowed(False)
        self.skillRelationshipTypeID.setHasMaximum(True)
        self.skillRelationshipTypeID.setHasMinimum(True)
        self.skillRelationshipTypeID.setMaximum(SkillRelationshipType.MAXIMUM_TYPE)
        self.skillRelationshipTypeID.setMinimum(SkillRelationshipType.MINIMUM_TYPE)

        self.skillOneID.allowInvalID = False
        self.skillOneID.setNullAllowed(False)
        self.skillOneID.setHasMinimum(True)
        self.skillOneID.setMinimum(0)

        self.skillTwoID.allowInvalID = False
        self.skillTwoID.setNullAllowed(False)
        self.skillTwoID.setHasMinimum(True)
        self.skillTwoID.setMinimum(0)
        self.myDb = myDb
        if myDb:
            self.fromDb()

    def isSameState(self, impl):
        result = True
        if not impl:
            result = False
        else:
            s1 = self.getSkillOneID()
            s2 = impl.getSkillOneID()
            result = s1 == s2
            
            if result:
                s1 = self.getSkillTwoID()
                s2 = impl.getSkillTwoID()
                result = s1 == s2
            
            if result:
                s1 = self.getSkillRelationshipID()
                s2 = impl.getSkillRelationshipID()
                result = s1 == s2
            
            if result:
                s1 = self.getSkillRelationshipTypeID()
                s2 = impl.getSkillRelationshipTypeID()
                result = s1 == s2
            
            if result:
                result = self.getSkillRelationshipCreateDate() == impl.getSkillRelationshipCreateDate()
            
            if result:
                result = self.getSkillRelationshipUpdateDate() == impl.getSkillRelationshipUpdateDate()
            
            if result:
                s1 = self.getSkillRelationshipCreateUser()
                s2 = impl.getSkillRelationshipCreateUser()
                result = s1 == s2
            
            if result:
                s1 = self.getSkillRelationshipUpdateUser()
                s2 = impl.getSkillRelationshipUpdateUser()
                result = s1 == s2 
        return result

    def getDisplayString(self):
        typeStr = ''
        if self.skillRelationshipTypeID  and self.skillRelationshipTypeID.getValue():
            typeStr = self.getRelationshipTypeNameForId(self.getSkillRelationshipTypeID())
        return '\n id: ' + str(self.getSkillRelationshipID()) + ' ' +\
            str(self.skillOne) + " + " + str(self.skillTwo) + " " + typeStr

    def getSkillRelationshipTypeID(self):
        if not self.skillRelationshipTypeID or not self.skillRelationshipTypeID.getValue():
            return -1
        else:
            return self.skillRelationshipTypeID.getValue()
    
    def setSkillRelationshipTypeID(self, newType):
        self.skillRelationshipTypeID.setValue(newType)

    def __str__(self):
        return self.getDisplayString()
    
    def getSkillRelationshipID(self):
        return self.skillRelationshipID.getValue()
    
    def setSkillRelationshipID(self, val):
        self.skillRelationshipID.setValue(val)
    
    def getSkillOneID(self):
        return self.skillOneID.getValue()
    
    def setSkillOneID(self, uid):
        self.skillOneID.setValue(uid)
    
    def getSkillTwoID(self):
        return self.skillTwoID.getValue()

    def setSkillTwoID(self, uid):
        self.skillTwoID.setValue(uid)
    
    def setUpdateUser(self, uid):
        self.setSkillRelationshipUpdateUser(uid)
    
    def getUpdateDate(self):
        return self.getSkillRelationshipUpdateDate()
    
    def setCreateUser(self, uid):
        self.setSkillRelationshipCreateUser(uid)
    
    def setCreateDate(self, d):
        self.setSkillRelationshipCreateDate(d)
    
    def setUpdateDate(self, d):
        self.setSkillRelationshipUpdateDate(d)
    
    def getSkillRelationshipCreateDate(self):
        return self.skillRelationshipCreateDate.getValue()
       
    def setSkillRelationshipCreateDate(self, d):
        self.skillRelationshipCreateDate.setValue(d)
    
    def getSkillRelationshipUpdateDate(self):
        return self.skillRelationshipUpdateDate.getValue()
    
    def setSkillRelationshipUpdateDate(self, d):
        self.skillRelationshipUpdateDate.setValue(d)
    
    def getSkillRelationshipCreateUser(self):
        return self.skillRelationshipCreateUser.getValue()
    
    def setSkillRelationshipCreateUser(self, skillRelationshipCreateUser):
        self.skillRelationshipCreateUser.setValue(skillRelationshipCreateUser)
      
    def getSkillRelationshipUpdateUser(self):
        return self.skillRelationshipUpdateUser.getValue()
    
    def setSkillRelationshipUpdateUser(self, skillRelationshipUpdateUser):
        self.skillRelationshipUpdateUser.setValue(skillRelationshipUpdateUser)
    
    def isAllowed(self):
        result = True
        if self.getSkillRelationshipTypeID() == SkillRelationshipType.SEPARATE_REQUIRED_VAL:
            result = False
        return result
    
    def getLastUpdateUser(self):
        return self.getSkillRelationshipUpdateUser()
    
    def getCreateUser(self):
        return self.getSkillRelationshipCreateUser()
    
    def getType(self):
        return self.type
    
    def setType(self, typ):
        self.type = typ
        if typ:
            self.setSkillRelationshipTypeID(typ.getSkillRelationshipTypeID())
            
    def setSkillOne(self, skill):
        self.skillOne = skill
        self.setSkillOneID(skill.skillID)
            
    def setSkillTwo(self, skill):
        self.skillTwo = skill
        self.setSkillTwoID(skill.skillID)
                
    def toDb(self):
        for name, att in self.__dict__.items():
            a = att
            if isinstance(att, Attribute):
                a = att.value
            self.myDb.__dict__[name] = a
            # print(\n + str(name) +  =  ) print(type(a))
    
    def fromDb(self):
        for name, att in self.myDb.__dict__.items():
            myAtt = self.__dict__.get(name)
            if not myAtt: 
                self.__dict__[name] = att
            else:
                a = att
                if isinstance(att, bytes):
                    a = att.decode()
                if isinstance(myAtt, Attribute):
                    myAtt.value = a
                else:
                    myAtt = a
                self.__dict__[name] = myAtt
        if self.myDb.skillOne:
            self.setSkillOne(self.myDb.skillOne)
        if self.myDb.skillTwo:
            self.setSkillTwo(self.myDb.skillTwo)
        # print(self.__dict__)
        
    def validate(self):
        atts = self.getAttributeList()
        BusinessObjectBase.validateAttributes(atts)
        self.validate2()
        
    def validate2(self):
        isValID = True
        msg = None
        
        if isValID and self.getSkillOneID() == self.getSkillTwoID():
            isValID = False
            errMsg = VSMessageFactory.getRelationshipSameSkillsError()
            msg = errMsg
        if not isValid:
            raise InvalidAttributeValueException(msg, 'SkillRelationship')
        
    def save(self):
        self.toDb()
        self.myDb.save()
        self.fromDb()
  
    def remove(self):
            self.myDb.delete()
              
    def delete(self):
        self.myDb.deleteFlag = True
        self.myDb.save()
    
    def getAttributeList(self): 
        return [
            self.skillRelationshipTypeID,
            self.skillOneID,
            self.skillTwoID,
            self.skillRelationshipID,
            self.skillRelationshipCreateUser,
            self.skillRelationshipUpdateUser,
            self.skillRelationshipCreateDate,
            self.skillRelationshipUpdateDate
            ]


class Project(BusinessObject):

    CAME_FROM = "cameFromProject"
    NAME_LENGTH = 255

    def __init__(self, myDb=None):
        self.projectID = IntegerAttribute("projectID")
        self.projectOrganizationID = IntegerAttribute("projectOrganizationID")
        self.projectStatusID = IntegerAttribute("projectStatusID")
        self.projectName = StringAttribute("projectName")
        self.projectStartDate = DateAttribute("projectStartDate")
        self.projectFinishDate = DateAttribute("projectFinishDate")
        self.projectCreateUser = IntegerAttribute("projectCreateUser")
        self.projectUpdateUser = IntegerAttribute("projectUpdateUser")
        self.projectCreateDate = DateAttribute("projectCreateDate")
        self.projectUpdateDate = DateAttribute("projectUpdateDate")
        self.organization = None
        self.subprojects = []
        self.tasks = []
        self.teams = []
        self.status = None
        self.myDb = myDb
        super().__init__()

        super().setIdProperties(self.projectID)
        super().setTrackingAttributes(
                self.projectCreateUser,
                self.projectUpdateUser,
                self.projectCreateDate,
                self.projectUpdateDate)

        self.projectName.allowInvalID = False
        self.projectName.setNullAllowed(False)
        self.projectName.setNullStringAllowed(False)
        self.projectName.setAllSpacesAllowed(False)
        self.projectName.setMixedCase(True)
        self.projectName.setHasMaximumLength(True)
        self.projectName.setMaximumLength(Project.NAME_LENGTH)        

        self.projectOrganizationID.allowInvalID = False
        self.projectOrganizationID.setNullAllowed(False)
        self.projectOrganizationID.setHasMinimum(True)
        self.projectOrganizationID.setMinimum(1)
        
        self.projectStartDate.allowInvalID = False
        self.projectStartDate.setNullAllowed(False)
        if myDb:
            self.fromDb()
    
    def getCost(self):
        result = 0
        for sub in self.subprojects:
            result += sub.getCost()
        for task in self.tasks:
            result += task.getCost()
        return result

    def getStartDate(self):
        result = None
        for t in self.tasks:
            if not result:
                result = t.getStartDate()
            elif t.getStartDate():
                if t.getStartDate() > result:
                    result = t.getStartDate()
        return result

    def getEndDate(self):
        result = None
        for t in self.tasks:
            if not result:
                result = t.getEndDate()
            elif t.getEndDate():
                if t.getEndDate() < result:
                    result = t.getEndDate().getTime()
        return result    
    
    def getStatus(self):
        return self.status
    
    def setStatus(self, status):
        self.status = status
        sID = None
        if status:
            sID = status.getProjectStatusID()
        self.setProjectStatusID(sid)
        #print(str(status) + ' sid= ' + str(sid))
    
    def getTasks(self):
        return self.tasks
    
    def setTasks(self, tasks):
        self.tasks = tasks
    
    def addTask(self, t):
        if not t in self.tasks:
            self.tasks.append(t)
            t.setTaskProjectID(self.getProjectID())
    
    def getSubprojects(self):
        return self.subprojects
    
    def setSubprojects(self, subprojects):
        self.subprojects = subprojects
    
    def addSubproject(self, t):
        if t not in self.subprojects:
            self.subprojects.append(t)
            
    def removeSubproject(self, p):
        try: 
            self.subprojects.remove(p)
        except ValueError:
            pass

    def removeTask(self, t):
        try:
            self.tasks.remove(t)
        except ValueError:
            pass

    def removeTeam(self, t):
        try:
            self.teams.remove(t)
        except ValueError:
            pass
    
    def getTeams(self):
        return self.teams
    
    def addTeam(self, t):
        if t not in self.teams:
            self.teams.append(t)
    
    def setTeams(self, teams):
        self.teams = teams
    
    def isSameState(self, impl):
        result = True
        if not impl or not isinstance(impl, Project):
            result = False
        if result:
            result = super().isSameBaseState(impl)
        
        if result:
            s1 = self.getProjectOrganizationID()
            s2 = impl.getProjectOrganizationID()
            result = s1 == s2
        
        if result:
            s1 = self.getProjectID()
            s2 = impl.getProjectID()
            result = s1 == s2
        
        if result:
            s1 = self.getProjectName()
            s2 = impl.getProjectName()
            result = s1 == s2
        
        if result:
            result = self.getProjectCreateDate() == impl.getProjectCreateDate()
        
        if result:
            result = self.getProjectUpdateDate() == impl.getProjectUpdateDate()
        
        if result:
            s1 = self.getProjectCreateUser()
            s2 = impl.getProjectCreateUser()
            result = s1 == s2
        
        if result:
            s1 = self.getProjectUpdateUser()
            s2 = impl.getProjectUpdateUser()
            result = s1 == s2
        
        return result

    def getOrganization(self):
        return self.organization
    
    def setOrganization(self, org):
        self.organization = org
        if org:
            self.setProjectOrganizationID(org.getOrganizationID())

    def getProjectOrganizationID(self):
        return self.projectOrganizationID.getValue()   

    def setProjectOrganizationID(self, i):
        self.projectOrganizationID.setValue(i)

    def getProjectStatusID(self):
        return self.projectStatusID.getValue()
    
    def setProjectStatusID(self, d):
        if isinstance(d, Attribute):
            d = d.value
        self.projectStatusID.setValue(d)
        
    def getProjectID(self):
        return self.projectID.getValue()
    
    def setProjectID(self, pid):
        if pid:
            self.projectID.setValue(pid)
        else:
            self.projectID.setValue(0)
        
    def getProjectName(self):
        return self.projectName.getValue()
  
    def setName(self, name):
        self.setProjectName(name)
    
    def getName(self):
        return self.getProjectName()

    def getStyle(self):
        result = ''
        if self.status:
            ver = self.status.getKey()
            match ver:
                case "1":
                    result = "class=listTable"
                case "2":
                    result = "class=listTable"
                case "3":
                    result = "class=assigned"
                case "4":
                    result = "class=active"
                case "5":
                    result = "class=complete"
                case "6":
                    result = "class=canceled"
                case _:
                    result = "class=listTable"
        return result
    
    def getDisplayString(self):
        result = '' 
        if self.projectName and self.projectName.getValue():
            result = self.projectName.getValue().strip()
        return result

    def setUpdateUser(self, uid):
        self.setProjectUpdateUser(uid)
    
    def getUpdateDate(self):
        return self.getProjectUpdateDate()
    
    def setCreateUser(self, d):
        self.setProjectCreateUser(d)
    
    def setCreateDate(self, d):
        self.setProjectCreateDate(d)
    
    def setUpdateDate(self, d):
        self.setProjectUpdateDate(d)
    
    def getProjectCreateDate(self):
        return self.projectCreateDate.getValue()
    
    def getProjectStartDate(self):
        result = self.projectStartDate.getValue()
        return result
    
    def setProjectStartDate(self, projectStartDate):
        self.projectStartDate.setValue(projectStartDate)
    
    def getProjectFinishDate(self):
        result = self.projectFinishDate.getValue()
        return result
    
    def setProjectFinishDate(self, projectFinishDate):
        self.projectFinishDate.setValue(projectFinishDate)
    
    def setProjectCreateDate(self, projectCreateDate):
        self.projectCreateDate.setValue(projectCreateDate)
    
    def getProjectUpdateDate(self):
        return self.projectUpdateDate.getValue()
    
    def setProjectUpdateDate(self, projectUpdateDate):
        self.projectUpdateDate.setValue(projectUpdateDate)
    
    def getProjectCreateUser(self):
        return self.projectCreateUser.getValue()
    
    def setProjectCreateUser(self, projectCreateUser):
        self.projectCreateUser.setValue(projectCreateUser)
    
    def getProjectUpdateUser(self):
        return self.projectUpdateUser.getValue()
    
    def setProjectUpdateUser(self, projectUpdateUser):
        self.projectUpdateUser.setValue(projectUpdateUser)
    
    def getLastUpdateUser(self):
        return self.getProjectUpdateUser()
    
    def getCreateUser(self):
        return self.getProjectCreateUser()

    def setID(self, d):
        self.setProjectID(d)

    def getID(self):
        return self.getProjectID().longValue()

    def toString(self):
        return self.getDisplayString()   
       
    def __str__(self):
        return self.getDisplayString()
    
    def toDb(self):
        for name, att in self.__dict__.items():
            a = att
            if isinstance(att, Attribute):
                a = att.value
            self.myDb.__dict__[name] = a
        if self.organization:
            self.myDb.organization = self.organization.myDb
            self.myDb.organization_ID = self.organization.getOrganizationID()
        # print(\n + str(name) +  =  ) print(type(a))
    
    def fromDb(self):
        for name, att in self.myDb.__dict__.items():
            if isinstance(att, bytes):
                att = att.decode()
            myAtt = self.__dict__.get(name)
            if not myAtt: 
                self.__dict__[name] = att
            else:
                if isinstance(myAtt, Attribute):
                    myAtt.value = att
                else:
                    myAtt = att
                self.__dict__[name] = myAtt
        dbOrg = self.myDb.organization
        if dbOrg:
            o = Organization(dbOrg)
            self.setOrganization(o)
            self.projectOrganizationID.value = self.organization.organizationID.value

    def validate(self):
        atts = self.getAttributeList()
        BusinessObject.validateAttributes(atts)
        
    def save(self):
        self.toDb()
        self.myDb.save()       
        self.fromDb()
  
    def remove(self):
            self.myDb.delete()
              
    def delete(self):
        self.myDb.deleteFlag = True
        self.myDb.save()
    
    def getAttributeList(self): 
        return [
            self.projectID,
            self.projectOrganizationID,
            self.projectStatusID,
            self.projectName,
            self.projectStartDate,
            self.projectFinishDate,
            self.projectCreateUser,
            self.projectUpdateUser,
            self.projectCreateDate,
            self.projectUpdateDate
        ]      


class Skill(BusinessObject):
    NAME_SIZE = 255
    
    def __init__(self, myDb=None):
        self.myDb = myDb
        super().__init__()
        self.skillID = IntegerAttribute("skillID")
        self.skillOrganizationID = IntegerAttribute("skillOrganizationID")
        self.skillName = StringAttribute('skillName')
        self.skillCreateUser = IntegerAttribute("skillCreateUser")
        self.skillUpdateUser = IntegerAttribute("skillUpdateUser")
        self.skillCreateDate = DateAttribute("skillCreateDate")
        self.skillUpdateDate = DateAttribute("skillUpdateDate")
        self.relationships = []
        self.organization = None
        super().setIdProperties(self.skillID)
        super().setTrackingAttributes(
            self.skillCreateUser,
            self.skillUpdateUser,
            self.skillCreateDate,
            self.skillUpdateDate)

        self.skillName.allowInvalID = False
        self.skillName.setHasMaximumLength(True)
        self.skillName.setAllSpacesAllowed(False)
        self.skillName.setNullStringAllowed(False)
        self.skillName.setNullAllowed(False)
        self.skillID.setName("skillID")
        self.skillOrganizationID.setName("skillOrganizationID")
        self.skillName.setMaximumLength(Skill.NAME_SIZE)
        if myDb:
            self.fromDb()
            
    def isSameState(self, impl):
        result = True
        
        if result:
            result = super().isSameBaseState(impl)
        
        if result:
            s1 = self.getSkillName()
            s2 = impl.getSkillName()
            result = s1 == s2
        
        if result:
            s1 = self.getSkillID()
            s2 = impl.getSkillID()
            result = s1 == s2
        
        if result:
            result = self.getSkillCreateDate() == impl.getSkillCreateDate()
        
        if result: result = self.getSkillUpdateDate() == impl.getSkillUpdateDate()
        
        if result:
            s1 = self.getSkillCreateUser()
            s2 = impl.getSkillCreateUser()
            result = s1 == s2
        
        if result:
            s1 = self.getSkillUpdateUser()
            s2 = impl.getSkillUpdateUser()
            result = s1 == s2
        
        if result:
            result = self.getRelationships().size() == impl.getRelationships().size()
        
        return result
    
    def getSkillOrganizationID(self):
        return self.skillOrganizationID.getValue()
    
    def setSkillOrganizationID(self, skillOrganizationID):
        self.skillOrganizationID.setValue(skillOrganizationID)
       
    def getOrganization(self):
        return self.organization 

    def setOrganization(self, organization):
        self.organization = organization
        if organization:
            self.setSkillOrganizationID(organization.getOrganizationID())
        
    def getSkillName(self):
        return self.skillName.getValue()
     
    def setSkillName(self, newName):
        self.skillName.setValue(newName)
        
    def getDisplayString(self):
        return self.getSkillName()

    def __str__(self):
        return self.getDisplayString()
    
    def isAllowedWith(self, skill):
        result = False
        sID = skill.getSkillID()
        myID = self.getSkillID()
        rels = ObjectFactory().getRelationshipsForSkill(skill)
        for sr in rels:
            if sr.isAllowed():
                sid1 = sr.getSkillOneID()
                oID = None
                if sid1 == sid: 
                    oID = sr.getSkillTwoID()
                else: 
                    oID = sr.getSkillOneID()
                if oID == myId:
                    result = True
                    break
        return result
    
    def getSkillID(self):
        return self.skillID.getValue()
    
    def setSkillID(self, uid):
        self.skillID.setValue(uid)

    def getID(self):
        return self.getSkillID()
    
    def setID(self, uid):
        self.setSkillID(uid)
        
    def setUpdateUser(self, uid):
        self.setSkillUpdateUser(uid)
    
    def getUpdateDate(self):
        return self.getSkillUpdateDate()
    
    def setCreateUser(self, uid):
        self.setSkillCreateUser(uid)
    
    def setCreateDate(self, d):
        self.setSkillCreateDate(d)
    
    def setUpdateDate(self, d):
        self.setSkillUpdateDate(d)
    
    def getSkillCreateDate(self):
        return self.skillCreateDate.getValue()
    
    def setSkillCreateDate(self, skillCreateDate):
        skillCreateDate.setValue(skillCreateDate)
    
    def getSkillUpdateDate(self):
        return self.skillUpdateDate.getValue()
    
    def setSkillUpdateDate(self, skillUpdateDate):
        self.skillUpdateDate.setValue(skillUpdateDate)

    def getSkillCreateUser(self):
        return self.skillCreateUser.getValue()

    def setSkillCreateUser(self, skillCreateUser):
        self.skillCreateUser.setValue(skillCreateUser)
    
    def getSkillUpdateUser(self):
        return self.skillUpdateUser.getValue()
  
    def setSkillUpdateUser(self, skillUpdateUser):
        self.skillUpdateUser.setValue(skillUpdateUser)
 
    def getLastUpdateUser(self):
        return self.getSkillUpdateUser()

    def getCreateUser(self):
        return self.getSkillCreateUser()

    def getRelationships(self):
        return self.relationships

    def setRelationships(self, relationships):
        self.relationships = relationships

    def addRelationship(self, relationship):
        if relationship and not relationship in self.relationships:
            self.relationships.append(relationship)
            
    def removeRelationship(self, relationship):
        if relationship in self.relationships:
            self.relationships.remove(relationship)
                
    def toDb(self):
        for name, att in self.__dict__.items():
            a = att
            if isinstance(att, Attribute):
                a = att.value
            self.myDb.__dict__[name] = a
            # print(\n + str(name) +  =  ) print(type(a))
    
    def fromDb(self):
        for name, att in self.myDb.__dict__.items():
            myAtt = self.__dict__.get(name)
            if not myAtt: 
                self.__dict__[name] = att
            else:
                a = att
                if isinstance(att, bytes):
                    a = att.decode()
                if isinstance(myAtt, Attribute):
                    myAtt.value = a
                else:
                    myAtt = a
                self.__dict__[name] = myAtt
        if  hasattr(self.myDb,'organization'):
            mydbo = self.myDb.organization
            if mydbo:
                self.setOrganization(Organization(mydbo))
            # print(self.__dict__)
        
    def validate(self):
        atts = self.getAttributeList()
        BusinessObject.validateAttributes(atts)
        self.validate2()
        
    def validate2(self):
        isValID = True
        msg = None
        
        if isValID and self.getSkillOneID() == self.getSkillTwoID():
            isValID = False
            errMsg = VSMessageFactory.getRelationshipSameSkillsError()
            msg = errMsg
        if not isValid:
            raise InvalidAttributeValueException(msg, 'SkillRelationship')
        
    def save(self):
        self.toDb()
        self.myDb.save()
        self.fromDb()
  
    def remove(self):
            self.myDb.delete()
              
    def delete(self):
        self.myDb.deleteFlag = True
        self.myDb.save()
    
    def getAttributeList(self): 
        return [
            self.skillID,
            self.skillOrganizationID,
            self.skillCreateUser,
            self.skillUpdateUser,
            self.skillCreateDate,
            self.skillUpdateDate
        ]

class EventJoinToResource(BusinessObject):
    
    def __init__(self, myDb=None):
        self.myDb = myDb
        super().__init__()
        self.eventID = IntegerAttribute("eventID")
        self.resourceID = IntegerAttribute("resourceID")
        self.count = IntegerAttribute("count")
        self.createUser = IntegerAttribute("createUser")
        self.updateUser = IntegerAttribute("updateUser")
        self.createDate = DateAttribute("createDate")
        self.updateDate = DateAttribute("updateDate")
        if myDb:
            self.fromDb()
        
    def __str__(self):
        return 'EventJoinToResource {eventID: ' + str(self.eventID) +\
            ' resourceID: ' + str(self.resourceID) +\
            ' count ' + str(self.count) + '}'
            
    def validate(self):
        pass
    
    def getEventID(self):
        return self.eventID.getValue()
    
    def setEventID(self, uid):
        self.eventID.setValue(uid)

    def getResourceID(self):
        return self.resourceID.getValue()
    
    def setResourceID(self, uid):
        self.resourceID.setValue(uid)
        
    def setUpdateUser(self, uid):
        self.updateUser.setValue(uid)
    
    def getUpdateDate(self):
        return self.updateDate.getValue()
    
    def setCreateUser(self, uid):
        self.createUser.setValue(uid)
    
    def setCreateDate(self, d):
        self.createDate.setValue(d)
    
    def setUpdateDate(self, d):
        self.updateDate.setValue(d)
    
    def toDb(self):
        for name, att in self.__dict__.items():
            a = att
            if isinstance(att, Attribute):
                a = att.value
            self.myDb.__dict__[name] = a
            # print(\n + str(name) +  =  ) print(type(a))
    
    def fromDb(self):
        for name, att in self.myDb.__dict__.items():
            myAtt = self.__dict__.get(name)
            if not myAtt: 
                self.__dict__[name] = att
            else:
                a = att
                if isinstance(att, bytes):
                    a = att.decode()
                if isinstance(myAtt, Attribute):
                    myAtt.value = a
                else:
                    myAtt = a
                self.__dict__[name] = myAtt
            # print(self.__dict__)
        
    def save(self):
        self.toDb()
        self.myDb.save()
        self.fromDb()
  
    def remove(self):
            self.myDb.delete()
              
    def delete(self):
        self.myDb.delete()
    
    def getAttributeList(self): 
        return [
            self.eventID,
            self.resourceID,
            self.count,
            self.createUser,
            self.updateUser,
            self.createDate,
            self.updateDate
        ]



class Task(BusinessObject):
    
    NAME_LENGTH = 255

    def __init__(self, myDb=None):
        self.taskID = IntegerAttribute("taskID")
        self.taskProjectID = IntegerAttribute("taskProjectID")
        self.taskStatusID = IntegerAttribute("taskStatusID")
        self.taskName = StringAttribute("taskName")
        self.taskSequence = IntegerAttribute("taskSequence")
        self.plannedTaskStart = DateAttribute("plannedTaskStart")
        self.actualTaskStart = DateAttribute("actualTaskStart")
        self.estimatedTaskEffort = IntegerAttribute("actualTaskEffort")
        self.actualTaskEffort = IntegerAttribute("estimatedTaskEffort")
        self.plannedTaskFinish = DateAttribute("plannedTaskFinish")
        self.actualTaskFinish = DateAttribute("actualTaskFinish")
        self.taskCreateUser = IntegerAttribute("taskCreateUser")
        self.taskUpdateUser = IntegerAttribute("taskUpdateUser")
        self.taskCreateDate = DateAttribute("taskCreateDate")
        self.taskUpdateDate = DateAttribute("taskUpdateDate")
        self.deleteFlag = BooleanAttribute('deleteFlag')
        self.activities = []
        self.subtasks = []
        self.resources = []
        self.skills = []
        self.teams = []
        self.volunteers = []
        self.taskStatus = None
        self.project = None
        self.parent = None
        super().__init__()
        self.myDb = myDb
        super().setIdProperties(self.taskID)
        super().setTrackingAttributes(
            self.taskCreateUser,
            self.taskUpdateUser,
            self.taskCreateDate,
            self.taskUpdateDate)

        self.taskName.allowInvalID = False
        self.taskName.setNullAllowed(False)
        self.taskName.setNullStringAllowed(False)
        self.taskName.setAllSpacesAllowed(False)
        self.taskName.setMixedCase(True)
        self.taskName.setHasMaximumLength(True)
        self.taskName.setMaximumLength(Task.NAME_LENGTH)

        self.taskProjectID.allowInvalID = False
        self.taskProjectID.setNullAllowed(False)
        self.taskProjectID.setHasMinimum(True)
        self.taskProjectID.setMinimum(1)

        self.taskSequence.allowInvalID = False
        self.taskSequence.setNullAllowed(False)
        self.taskSequence.setHasMinimum(True)
        self.taskSequence.setMinimum(1)
        self.taskSequence.setValue(1)
        
        self.taskStatusID.allowInvalID = False
        self.taskStatusID.setNullAllowed(False)
        self.taskStatusID.setHasMinimum(True)
        self.taskStatusID.setMinimum(1)
        if myDb:
            self.fromDb()
        
    def getParent(self):
        return self.parent
    
    def setParent(self, p):
        self.parent = p
        
    def getProject(self):
        return self.project
    
    def setProject(self, p):
        self.project = p
        if p:
            self.setProjectID(p.projectID)
        else:
            self.setProjectID(None)
    def getCost(self):
        result = 0
        for sub in self.subtasks:
            result += sub.getCost()
        for activity in self.activities:
            result += activity.getCost()
        return result
    
    def getStartDate(self):
        result = None
        if self.actualTaskStart.getValue():
            result = self.actualTaskStart.getValue()
        elif self.plannedTaskStart.getValue():
            result = self.plannedTaskStart.getValue()
        return result

    def getEndDate(self):
        result = None
        if self.actualTaskFinish.getValue():
            result = self.actualTaskFinish.getValue()
        elif self.plannedTaskFinish.getValue():
            result = self.plannedTaskFinish.getValue()    
        return result
    
    def getStyle(self):
        result = ""
        if self.taskStatus:
            match self.taskStatus.getKey():
                case "1":
                    result = "class=listTable"
                case "2":
                    result = "class=listTable"
                case "3":
                    result = "class=assigned"
                case "4":
                    result = "class=active"
                case "5":
                    result = "class=complete"
                case "6":
                    result = "class=canceled"
                case _:
                    result = "class=listTable"
        return result

    def getPlannedTaskStart(self):
        return self.plannedTaskStart.getValue()

    def setPlannedTaskStart(self, plannedTaskStart):
        self.plannedTaskStart.setValue(plannedTaskStart)
    
    def getActualTaskStart(self):
        return self.actualTaskStart.getValue()
    
    def setActualTaskStart(self, actualTaskStart):
        self.actualTaskStart.setValue(actualTaskStart)
    
    def getEstimatedTaskEffort(self):
        return self.estimatedTaskEffort.getValue()
    
    def setEstimatedTaskEffort(self, estimatedTaskEffort):
        self.estimatedTaskEffort.setValue(estimatedTaskEffort)
    
    def getActualTaskEffort(self):
        return self.actualTaskEffort.getValue()
    
    def setActualTaskEffort(self, actualTaskEffort):
        self.actualTaskEffort.setValue(actualTaskEffort)
    
    def getPlannedTaskFinish(self):
        return self.plannedTaskFinish.getValue()    

    def setPlannedTaskFinish(self, plannedTaskFinish):
        self.plannedTaskFinish.setValue(plannedTaskFinish)
    
    def getActualTaskFinish(self):
        return self.actualTaskFinish.getValue()
    
    def setActualTaskFinish(self, actualTaskFinish):
        self.actualTaskFinish.setValue(actualTaskFinish)
    
    def getTaskStatus(self):
        return self.taskStatus
    
    def setTaskStatus(self, taskStatus):
        self.taskStatus = taskStatus
        self.taskStatusID.setValue(taskStatus.getTaskStatusID())
    
    def getTaskStatusID(self):
        return self.taskStatusID.getValue()
    
    def setTaskStatusID(self, taskStatusID):
        self.taskStatusID.setValue(taskStatusID)

    def getSkills(self):
        return self.skills

    def setSkills(self, skills):
        self.skills = skills
    
    def addSkill(self, a):
        if a and not a in self.skills:
            self.skills.append(a)
            
    def getTeams(self):
        return self.teams
    
    def setTeams(self, teams):
        self.teams = teams
    
    def addTeam(self, a):
        if a and not a in self.teams:
            self.teams.append(a)

    def getVolunteers(self):
        return self.volunteers

    def addVolunteer(self, v):
        if v and v not in self.volunteers:
            self.volunteers.append(v)

    def setVolunteers(self, volunteers):
        self.volunteers = volunteers
    
    def getResources(self):
        return self.resources
    
    def setResources(self, resources):
        self.resources = resources
    
    def addResource(self, a):
        if a and a not in self.resources:
            self.resources.append(a)
            
    def copyState(self, t):
        super.copyState(t)
        self.activities = t.activities
        self.resources = t.resources
        self.skills = t.skills
        self.subtasks = t.subtasks
        self.teams = t.teams
        self.volunteers = t.volunteers

    def getSubtasks(self):
        return self.subtasks
    
    def addSubtask(self, a):
        if a and a not in self.subtasks:
            self.subtasks.append(a)
            try:
                a.setTaskProjectID(self.getTaskProjectID())
            except InvalidAttributeValueException as e:
                super().handleException(e)
            
    def setSubtasks(self, subtasks):
        self.subtasks = subtasks
    
    def getActivities(self):
        return self.activities    

    def setActivities(self, activities):
        coll = []
        for a in activities:
            if a.isDeleted():
                continue
            coll.append(a)       
        self.activities = coll
    
    def addActivity(self, a):
        if a and a not in self.activities:
            self.activities.append(a)

    def getTaskSequence(self):
        return self.taskSequence.getValue()
    
    def setTaskSequence(self, val):
        self.taskSequence.setValue(val)
    
    def removeSkill(self, a):
        result = None
        if a and isinstance(a, Skill):
            result = next((u for u in self.skills if u["skillID"] == a.skillID), None)
            self.skills.remove(a)
        return result

    def removeActivity(self, a):
        result = None
        if a and isinstance(a, Activity):
            result = next((u for u in self.activities if u["activityID"] == a.activityID), None)
            if result:
                self.activities.remove(a)
        return result
    
    def removeProjectResource(self, pr):
        result = None
        if pr and isinstance(pr, ProjectResource):
            result = next((u for u in self.projectResources if u["orojectResourceID"] == pr.projectResourceID), None)
            if result:
                self.projectResources.remove(pr)
        return result

    def removeTeam(self, t):
        result = None
        if t and isinstance(t, Team):
            result = next((u for u in self.teams if u["teamID"] == t.teamID), None)
            if result:
                self.teams.remove(t)
        return result

    def removeVolunteer(self, v):
        result = None
        if v and isinstance(v, Volunteer):
            result = next((u for u in self.volunteers if u["volunteerID"] == v.volunteerID), None)
            if result:
                self.volunteers.remove(v)
        return result
    
    def removeTask(self, t):
        result = None
        if t and isinstance(t, Task):
            result = next((u for u in self.tasks if u["taskID"] == t.taskID), None)
            if result:
                self.tasks.remove(t)
        return result

    def getTaskID(self):
        return self.taskID.getValue()
    
    def setTaskID(self, tid):
        self.taskID.setValue(tid)

    def getTaskProjectID(self):
        return self.taskProjectID.getValue()
    
    def setTaskProjectID(self, tid):
        self.taskProjectID.setValue(tid)
    
    def getTaskName(self):
        return self.taskName.getValue()
    
    def setTaskName(self, task):
        self.taskName.setValue(task)
    
    def getTaskCreateUser(self):
        return self.taskCreateUser.getValue()

    def getTaskUpdateUser(self):
        return self.taskUpdateUser.getValue()
    
    def getTaskCreateDate(self):
        return self.taskCreateDate.getValue()
    
    def setTaskCreateDate(self, taskCreateDate):
        self.taskCreateDate.setValue(taskCreateDate)
    
    def getTaskUpdateDate(self):
        return self.taskUpdateDate.getValue()
    
    def setTaskUpdateDate(self, taskUpdateDate):
        self.taskUpdateDate.setValue(taskUpdateDate)
       
    def getCreateUser(self):
        return self.getTaskCreateUser()
    
    def setUpdateDate(self, date):
        self.setTaskUpdateDate(date)
    
    def setCreateDate(self, date):
        self.setTaskCreateDate(date)
    
    def setDatabaseID(self, dbid):
        self.setTaskID(dbid)
        
    def setUpdateUser(self, uid):
        self.setTaskUpdateUser(uid)
    
    def setCreateUser(self, uid):
        self.setTaskCreateUser(uid)
    
    def setID(self, uid):
        self.setTaskID(uid)

    def getID(self):
        return self.getTaskID()    
    
    def equals(self, obj):
        result = True
        if not obj:
            result = False
        elif self.taskID != obj.taskID:
            result = False
        elif self.taskProjectID != obj.taskProjectID:
            result = False
        elif self.taskStatusID != obj.taskStatusID:
            result = False
        elif self.taskName != obj.taskName:
            result = False
        elif self.taskSequence != obj.taskSequence:
            result = False
        elif self.plannedTaskStart != obj.plannedTaskStart:
            result = False
        elif self.actualTaskStart != obj.actualTaskStart:
            result = False
        elif self.estimatedTaskEffort != obj.estimatedTaskEffort:
            result = False
        elif self.actualTaskEffort != obj.actualTaskEffort:
            result = False
        elif self.plannedTaskFinish != obj.plannedTaskFinish:
            result = False
        elif self.actualTaskFinish != obj.actualTaskFinish:
            result = False
        elif self.taskCreateUser != obj.taskCreateUser:
            result = False
        elif self.taskUpdateUser != obj.taskUpdateUser:
            result = False
        elif self.taskCreateDate != obj.taskCreateDate:
            result = False
        elif self.taskUpdateDate != obj.taskUpdateDate:
            result = False
        elif self.activities != obj.activities:
            result = False
        elif self.subtasks != obj.subtasks:
            result = False
        elif self.resources != obj.resources:
            result = False
        elif self.teams != obj.teams:
            result = False
        elif self.volunteers != obj.volunteers:
            result = False
        elif self.taskStatus != obj.taskStatus:
            result = False
        return result
    
    def isSameState(self, vsp):
        return self.equals(vsp)
        
    def compareTo(self, o):
        result = 0
        if o == None:
            result = 1
        elif isinstance(o, Task):
            oKey = o.getTaskName()
            key = self.getTaskName()
            if key < oKey:
                result = -1
            elif key > oKey:
                result = 1                 
        else:
            raise ClassCastException("Object " + o + "is not an instance of Task")
        return result
    
    def toString(self):
        return str(self.taskSequence.value) + " | " + str(self.getTaskName())
    
    def __str__(self):
        return self.toString()
    
    def toDb(self):
        for name, att in self.__dict__.items():
            a = att
            if isinstance(att, Attribute):
                a = att.value
            self.myDb.__dict__[name] = a
        if self.taskID.value:
            if self.project:
                self.myDb.project = self.project.myDb
            else:
                if self.myDb.project:
                    self.myDb.project.delete()
                    
            if self.parent:
                self.myDb.parent = self.parent.myDb  
            else:
                if self.myDb.parent:
                    self.myDb.parent.clear()
                    
            self.myDb.activities.clear()
            if self.activities and len(self.activities) > 0:
                for a in self.activities:
                    self.myDb.activities.add(a.MyDb)
                    
            self.myDb.teams.clear()
            if self.teams and len(self.teams) > 0:
                for a in self.teams:
                    self.myDb.teams.add(a.MyDb)
                    
            self.myDb.resources.clear()
            if self.resources and len(self.resources) > 0:
                for a in self.resources:
                    self.myDb.resources.add(a.MyDb)
                    
            self.myDb.skills.clear()
            if self.skills and len(self.skills) > 0:
                for a in self.skills:
                    self.myDb.skills.add(a.MyDb)
                    
            self.myDb.volunteers.clear()
            if self.volunteers and len(self.volunteers) > 0:
                for a in self.volunteers:
                    self.myDb.volunteers.add(a.myDb)
                    
            if self.taskStatus:
                self.myDb.taskStatus = self.taskStatus.myDb  
            else:
                if self.myDb.taskStatus:
                    self.myDb.taskStatus.clear()
        
    def fromDb(self):
        for name, att in self.myDb.__dict__.items():
            if isinstance(att, bytes):
                att = att.decode()
            myAtt = self.__dict__.get(name)
            if not myAtt: 
                self.__dict__[name] = att
            else:
                if isinstance(myAtt, Attribute):
                    myAtt.value = att
                else:
                    myAtt = att
        if self.myDb:
            self.activities = []
            self.subtasks = []
            self.resources = []
            self.skills = []
            self.teams = []
            self.volunteers = []
            if self.myDb.taskID:
                if self.myDb.project:
                    self.project = Project(self.myDb.project)            
                if self.myDb.taskStatus:
                    self.taskStatus = TaskStatus(self.myDb.taskStatus)
                if self.myDb.activities:
                    for dbo in self.myDb.activities.all():
                        self.activities.append(Activity(dbo))
                if self.myDb.subtasks:
                    for dbo in self.myDb.subtasks.all():
                        self.subtasks.append(Task(dbo))
                if self.myDb.resources:
                    for dbo in self.myDb.resources.all():
                        self.resources.append(ProjectResource(dbo))
                if self.myDb.skills:
                    for dbo in self.myDb.skills.all():
                        self.skills.append(Skill(dbo))
                if self.myDb.teams:
                    for dbo in self.myDb.teams.all():
                        self.teams.append(Team(dbo))
                if self.myDb.volunteers:
                    for dbo in self.myDb.volunteers.all():
                        self.volunteers.append(Volunteer(dbo))

    def validate(self):
        atts = self.getAttributeList()
        BusinessObject.validateAttributes(atts)
        
    def save(self):
        self.toDb()
        needTwice = not self.getTaskID()
        self.myDb.save()       
        self.fromDb()
        if needTwice: #do fhise because joins require an object OD
            self.toDb()
            self.myDb.save()       
            self.fromDb()
  
    def remove(self):
            self.myDb.delete()
              
    def delete(self):
        self.myDb.deleteFlag = True
        self.myDb.save()
    
    def getAttributeList(self): 
        return [
            self.taskID,
            self.taskProjectID,
            self.taskStatusID,
            self.taskName,
            self.taskSequence,
            self.plannedTaskStart,
            self.actualTaskStart,
            self.estimatedTaskEffort,
            self.actualTaskEffort,
            self.plannedTaskFinish,
            self.actualTaskFinish,
            self.taskCreateUser,
            self.taskUpdateUser,
            self.taskCreateDate,
            self.taskUpdateDate,
            self.deleteFlag
        ]

        
class Team(BusinessObject):

    NAME_LENGTH = 255
    
    def __init__(self, myDb=None,org=None):
        super().__init__()
        self.teamID = IntegerAttribute("teamID")
        self.teamName = StringAttribute("teamName")
        self.teamCreateUser = IntegerAttribute("teamCreateUser")
        self.teamUpdateUser = IntegerAttribute("teamUpdateUser")
        self.teamCreateDate = DateAttribute("teamCreateDate")
        self.teamUpdateDate = DateAttribute("teamUpdateDate")
        self.organization = None
        self.volunteers = []
        self.tasks = []
        super().setIdProperties(self.teamID)
        super().setTrackingAttributes(self.teamCreateUser,
                    self.teamUpdateUser,
                    self.teamCreateDate,
                    self.teamUpdateDate)
    
        self.teamName.allowInvalID = False
        self.teamName.setNullAllowed(False)
        self.teamName.setNullStringAllowed(False)
        self.teamName.setAllSpacesAllowed(False)
        self.teamName.setMixedCase(True)
        self.teamName.setHasMaximumLength(True)
        self.teamName.setMaximumLength(Team.NAME_LENGTH)
        
        self.myDb = myDb
        if myDb:
            myDb.teamCreateUser=1
            myDb.teamUpdateUser=1
            myDb.save()
            self.fromDb()
        self.organization = org
        if org:
            self.myDb.organization = org.myDb
    
    def getHourlyCost(self):
        result = 0
        for vol in self.volunteers:
            result += vol.getCost()
        return result
    
    def getStyle(self):
        result = "class=listTable"
        return result
    
    def getTeamID(self):
        return self.teamID.getValue()
    
    def setTeamID(self, i):
        self.teamID.setValue(i)
    
    def getOrganization(self):
        return self.organization
    
    def setOrganization(self, org):
        self.organization = org
           
    def getVolunteers(self):
        return self.volunteers
    
    def addVolunteer(self, vol):
        if not self.volunteers.contains(vol):
            self.volunteers.append(vol)
            
    def removeVolunteer(self, vol):
        if self.volunteers.contains(vol):
            self.volunteers.remove(vol)
            
    def setVolunteers(self, volunteers):
        self.volunteers = volunteers
    
    def getTasks(self):
        return self.tasks
    
    def setTasks(self, tasks):
        self.tasks = tasks
    
    def addTask(self, t):
        if not self.tasks.contains(t):
            self.tasks.append(t)

    def removeTask(self, t):
        if self.tasks.contains(t):
            self.tasks.remove(t)
           
    def getTeamName(self):
        return self.teamName.getValue()
    
    def setTeamName(self, s):
        self.teamName.setValue(s)
            
    def getTeamCreateUser(self):
        return self.teamCreateUser.getValue()
    
    def setTeamCreateUser(self, teamCreateUser):
        self.teamCreateUser.setValue(teamCreateUser)

    def getTeamUpdateUser(self):
        return self.teamUpdateUser.getValue()
    
    def setTeamUpdateUser(self, teamUpdateUser):
        self.teamUpdateUser.setValue(teamUpdateUser)
    
    def getTeamCreateDate(self):
        return self.teamCreateDate.getValue()
    
    def setTeamCreateDate(self, teamCreateDate):
        self.teamCreateDate.setValue(teamCreateDate)
    
    def getTeamUpdateDate(self):
        return self.teamUpdateDate.getValue()
    
    def setTeamUpdateDate(self, teamUpdateDate):
        self.teamUpdateDate.setValue(teamUpdateDate)
    
    def getCreateUser(self):
        return self.getTeamCreateUser()
    
    def setUpdateDate(self, date):
        self.setTeamUpdateDate(date)
    
    def setCreateDate(self, date):
        self.setTeamCreateDate(date)
    
    def setDatabaseID(self, i):
        self.setTeamID(i)
            
    def setUpdateUser(self, d):
        self.setTeamUpdateUser(d)
        
    def setCreateUser(self, d):
        self.setTeamCreateUser(d)
    
    def setID(self, d):
        self.setTeamID(d)
        
    def getID(self):
        return self.getTeamID()    
    
    def equals(self, obj):
        if not obj:
            result = False        
        elif self.__class__.__name__ != obj.__class__.__name__:
            result = False
        elif not self.teamID == obj.teamID:
            result = False
        elif not self.teamOrganizationID == obj.teamOrganizationID: 
            result = False
        elif not self.teamName == obj.teamName:
            result = False
        elif not self.teamCreateUser == obj.teamCreateUser:
            result = False
        elif not self.teamUpdateUser == obj.teamUpdateUser:
            result = False
        elif not self.organization == obj.organization:
            result = False
        elif not self.volunteers == obj.volunteers:
            result = False
        elif not self.tasks == obj.tasks:
            result = False
        return result
    
    def isSameState(self, vsp):
        return self.equals(vsp)
        
    def compareTo(self, o):
        result = 0
        if not o:
            result = 1
        elif isinstance(o, Team):
            okey = o.getTeamName()
            key = self.getTeamName()
            if key < okey:
                result = -1
            elif key > okey:
                result = 1 
        else:
            raise ClassCastException("Object " + str(o) + "is not an instance of Team")
        return result
    
    def toString(self, obj):
        result = self.taskSequence.getValue()
        if result:
            result = str(result)
        else:
            result = 'None' 
        result += "|" 
        s = self.getTaskName()
        if s:
            result += s
        else: 
            result += 'None'

    def __str__(self):
        return self.toString()
    
    def toDb(self):
        for name, att in self.__dict__.items():
            a = att
            if isinstance(att, Attribute):
                a = att.value
            self.myDb.__dict__[name] = a
        if self.organization:
            self.myDb.organization = self.organization.myDb
            self.myDb.organization_ID = self.organization.getOrganizationID()
        if self.myDb.volunteers:
            self.myDb.volunteers.clear()
            for vol in self.volunteers:
                self.myDb.volunteers.add(vol.myDb)
        if self.myDb.tasks:
            self.myDb.tasks.clear()
            for t in self.tasks:
                self.myDb.tasks.add(t.myDb)
    
    def fromDb(self):
        for name, att in self.myDb.__dict__.items():
            if isinstance(att, bytes):
                att = att.decode()
            myAtt = self.__dict__.get(name)
            if not myAtt: 
                self.__dict__[name] = att
            else:
                if isinstance(myAtt, Attribute):
                    myAtt.value = att
                else:
                    myAtt = att
                self.__dict__[name] = myAtt
        dbOrg = self.myDb.organization
        if dbOrg:
            o = Organization(dbOrg)
            self.setOrganization(o)
        dbTasks = self.myDb.tasks
        self.tasks.clear()
        if dbTasks: 
            for dbt in dbTasks.all():
                self.tasks.append(Task(dbt))
        self.volunteers.clear()
        dbVols = self.myDb.volunteers
        if dbVols:
            for dbv in dbVols.all():
                self.volunteers.appent(Volunteer(dbv))
                
    def validate(self):
        atts = self.getAttributeList()
        BusinessObject.validateAttributes(atts)
        
    def save(self):
        self.toDb()
        self.myDb.save()  
        self.fromDb()
  
    def remove(self):
            self.myDb.delete()
              
    def delete(self):
        self.myDb.deleteFlag = True
        self.myDb.save()
    
    def getAttributeList(self): 
        return [
            self.teamID,
            self.teamOrganizationID,
            self.teamName,
            self.teamCreateUser,
            self.teamUpdateUser,
            self.teamCreateDate,
            self.teamUpdateDate,
        ]


class ProjectResource(Resource):

    def __init__(self, myDb=None,org=None):
        self.reusable = BooleanAttribute('reusable')
        self.cost = CurrencyAttribute("cost")
        self.resourceID = IntegerAttribute("resourceID")
        self.resourceOrganizationID = IntegerAttribute("resourceOrganizationID")
        self.count = IntegerAttribute("count")
        self.name = StringAttribute("name")
        self.resourceCreateUser = IntegerAttribute("resourceCreateUser")
        self.resourceUpdateUser = IntegerAttribute("resourceUpdateUser")
        self.resourceCreateDate = DateAttribute("resourceCreateDate")
        self.resourceUpdateDate = DateAttribute("resourceUpdateDate")
        self.organization = org
        self.myDb = myDb
        if myDb:
            self.fromDb()
        super().setIdProperties(self.resourceID)
        super().setTrackingAttributes(self.resourceCreateUser,
                self.resourceUpdateUser,
                self.resourceCreateDate,
                self.resourceUpdateDate)
        self.count.setValue(1)
        self.count.allowInvalID = False
        self.count.setNullAllowed(False)
        self.count.setHasMinimum(True)
        self.count.setMinimum(0)
        
        self.cost.setNullAllowed(False)
        self.cost.setHasMinimum(True)
        self.cost.setMinimum(0.0)
        self.cost.setValue(0.0)
        
        self.resourceOrganizationID.allowInvalID = False
        self.resourceOrganizationID.setNullAllowed(False)
        self.resourceOrganizationID.setHasMinimum(True)
        self.resourceOrganizationID.setMinimum(ProjectResource.COUNT_MINIMUM)
        
        self.name.allowInvalID = False
        self.name.setNullAllowed(False)
        self.name.setAllSpacesAllowed(False)
        self.name.setNullStringAllowed(False)
        self.name.setMixedCase(True)
        self.name.setHasMaximumLength(True)
        self.name.setMaximumLength(ProjectResource.NAME_MAXIMUM_LENGTH)
    
        self.reusable.value = False
        
    def getCost(self):
        return self.cost.getValue()
    
    def setCost(self, val):
        self.cost.setValue(val)

    def isReusable(self):
        return self.reusable
    
    def getReusable(self):
        return self.reusable
    
    def setReusable(self, reusable):
        self.reusable = reusable
    
    def toString(self):
        return self.getName() + " count " + str(self.getCount())
    
    def getDisplayString(self):
        return self.toString
    
    def isSameState(self, impl):
        result = True
        if not isinstance(impl, ProjectResource):
            result = False
        if result:
            result = super().isSameBaseState(impl)
        if result:
            s1 = self.getResourceID()
            s2 = impl.getResourceID()
            result = s1 == s2
        if result:
            s1 = self.getName()
            s2 = impl.getName()
            result = s1 == s2
        if result:
            s1 = self.getCount()
            s2 = impl.getCount()
            result = s1 == s2
        if result:
            result = self.getResourceCreateDate() == impl.getResourceCreateDate()
        if result:
            result = self.getResourceUpdateDate() == impl.getResourceUpdateDate()
        if result:
            s1 = self.getResourceCreateUser()
            s2 = impl.getResourceCreateUser()
            result = s1 == s2
        if result:
            s1 = self.getResourceUpdateUser()
            s2 = impl.getResourceUpdateUser()
            result = s1 == s2
        return result
    
    def getResourceID(self):
        return self.resourceID.value
    
    def setResourceID(self,resourceID):
        self.resourceID.setValue(resourceID)
    
    def getResourceOrganizationID(self):
        return self.resourceOrganizationID
    
    def setResourceOrganizationID(self, resourceID):
        self.resourceOrganizationID.setValue(resourceID)
    
    def getID(self):
        return self.getResourceID()
    
    def setID(self, oid):
        self.setResourceID(oid)
        
    def getOrganization(self):
        return self.organization
    
    def setOrganization(self, organization):
        self.organization = organization
        if organization:
            self.setResourceOrganizationID(organization.getOrganizationID())
        
    def setUpdateUser(self, oid):
        self.setResourceUpdateUser(oid)
    
    def getUpdateDate(self):
        return self.getResourceUpdateDate()
    
    def setCreateUser(self, d):
        self.setResourceCreateUser(d)
    
    def setCreateDate(self, d):
        self.setResourceCreateDate(d)
    
    def setUpdateDate(self, d):
        self.setResourceUpdateDate(d)
    
    def getResourceCreateDate(self):
        return self.resourceCreateDate.getValue()
    
    def setResourceCreateDate(self, resourceCreateDate):
        self.resourceCreateDate.setValue(resourceCreateDate)
    
    def getResourceUpdateDate(self):
        return self.resourceUpdateDate.getValue()
    
    def setResourceUpdateDate(self, resourceUpdateDate):
        self.resourceUpdateDate.setValue(resourceUpdateDate)
    
    def getResourceCreateUser(self):
        return self.resourceCreateUser.getValue()
    
    def setResourceCreateUser(self, resourceCreateUser):
        self.resourceCreateUser.setValue(resourceCreateUser)
    
    def getResourceUpdateUser(self):
        return self.resourceUpdateUser.getValue()
    
    def setResourceUpdateUser(self, resourceUpdateUser):
        self.resourceUpdateUser.setValue(resourceUpdateUser)
    
    def getCount(self):
        return self.count.getValue()
    
    def setCount(self, ct):
        self.count.setValue(ct)
    
    def getName(self):
        return self.name.getValue()
    
    def setName(self, nm):
        self.name.setValue(nm)
        
    def getLastUpdateUser(self):
        return self.getResourceUpdateUser()
    
    def getCreateUser(self):
        return self.getResourceCreateUser()
    
    def __str__(self)->str:
        return self.toString()
    
    def toDb(self):
        for name, att in self.__dict__.items():
            a = att
            if isinstance(att, Attribute):
                a = att.value
            self.myDb.__dict__[name] = a
        if self.getOrganization():
            self.myDb._organization = self.getOrganization().myDb
    
    def fromDb(self):
        for name, att in self.myDb.__dict__.items():
            if isinstance(att, bytes):
                att = att.decode()
            myAtt = self.__dict__.get(name)
            if not myAtt: 
                self.__dict__[name] = att
            else:
                if isinstance(myAtt, Attribute):
                    myAtt.value = att
                else:
                    myAtt = att
                self.__dict__[name] = myAtt
            if self.myDb.organization:
                self.setOrganization(Organization(self.myDb.organization))

    def validate(self):
        result = True
        atts = self.getAttributeList()
        try:
            BusinessObject.validateAttributes(atts)
        except InvalidAttributeValueException as e:
            super().addMessage(e.getMsg())
            result = False
        return result
        
    def save(self):
        self.toDb()
        self.myDb.save()       
        self.fromDb()
  
    def remove(self):
            self.myDb.delete()
              
    def delete(self):
        self.myDb.deleteFlag = True
        self.myDb.save()
    
    def getAttributeList(self): 
        return [    
            self.reusable,
            self.cost,
            self.resourceID,
            self.resourceOrganizationID,
            self.count,
            self.name,
            self.resourceCreateUser,
            self.resourceUpdateUser,
            self.resourceCreateDate,
            self.resourceUpdateDate
        ]
   
    
class Household(BusinessObject):
    FIRST_NAME_LENGTH = 255
    LAST_NAME_LENGTH = 255
    
    def __init__(self, myDb=None, address=None, org=None, uid=None):
        self.householdID = IntegerAttribute("householdID")
        self.householdAddressID = IntegerAttribute("householdAddressID")
        self.householdOrganizationID = IntegerAttribute("householdOrganizationID")
        self.householdFirstName = StringAttribute("householdFirstName")
        self.householdLastName = StringAttribute("householdLastName")
        self.householdCreateUser = IntegerAttribute("householdCreateUser")
        self.householdUpdateUser = IntegerAttribute("householdUpdateUser")
        self.householdCreateDate = DateAttribute("householdCreateDate")
        self.householdUpdateDate = DateAttribute("householdUpdateDate")
        if address:
            self.setAddress(address)
        else:
            add = Address(DbAddress())
            self.setAddress(add)
        if uid:
            add.setAddressCreateUser(uid)
            add.setAddressUpdateUser(uid)
        elif self.getHouseholdUpdateUser():
            add.setAddressCreateUser(self.getHouseholdUpdateUser())
            add.setAddressUpdateUser(self.getHouseholdUpdateUser())
        else:
            add.setAddressCreateUser(1)
            add.setAddressUpdateUser(1)
        add.save()
        self.setAddress(add)
        if org:
            self.setOrganization(org)
        super().__init__()
        super().setIdProperties(self.householdID)
        super().setTrackingAttributes(self.householdCreateUser,
                self.householdUpdateUser,
                self.householdCreateDate,
                self.householdUpdateDate)
        self.householdLastName.allowInvalID = False
        self.householdLastName.setAllSpacesAllowed(False)
        self.householdLastName.setNullAllowed(False)
        self.householdLastName.setNullStringAllowed(False)
        self.householdLastName.setHasMaximumLength(True)
        self.householdLastName.setMaximumLength(Household.LAST_NAME_LENGTH)

        self.householdFirstName.allowInvalID = False
        self.householdFirstName.setAllSpacesAllowed(False)
        self.householdFirstName.setNullAllowed(False)
        self.householdFirstName.setNullStringAllowed(False)
        self.householdFirstName.setHasMaximumLength(True)
        self.householdFirstName.setMaximumLength(Household.FIRST_NAME_LENGTH)

        self.householdAddressID.allowInvalID = False
        self.householdAddressID.setNullAllowed(True)
        self.householdAddressID.setHasMinimum(True)
        self.householdAddressID.setMinimum(0)

        self.householdOrganizationID.allowInvalID = False
        self.householdOrganizationID.setNullAllowed(True)
        self.householdOrganizationID.setHasMinimum(True)
        self.householdOrganizationID.setMinimum(0)

        if address:
            self.setAddress(address)
        if org:
            self.setOrganization(org)
        self.myDb = myDb
        if myDb:
            self.fromDb() 
            
    def isSameState(self, impl):
        result = True
        if not impl or not isinstance(impl, Household):
            result = False
        if result:
            result = super().isSameBaseState(impl)
        
        ai1 = self.getAddress(True)
        ai2 = impl.getAddress(True)
        if ai1 != None and ai2 == None:
            result = False
        elif (ai1 == None and ai2 != None):
            result = False
        elif (ai1 != None and ai2 != None):
            result = ai1.isSameState(ai2)
        
        oi1 = self.getOrganization()
        oi2 = impl.getOrganization()
        if (oi1 != None and oi2 == None):
            result = False
        elif (oi1 == None and oi2 != None):
            result = False
        elif (oi1 != None and oi2 != None):
            result = oi1.isSameState(oi2)
        
        if result:
            s1 = self.getHouseholdID()
            s2 = impl.getHouseholdID()
            result = s1 == s2
        
        
        if result:
            s1 = self.getHouseholdFirstName()
            s2 = impl.getHouseholdFirstName()
            result = s1 == s2
        
        if result:
            s1 = self.getHouseholdLastName()
            s2 = impl.getHouseholdLastName()
            result = s1 == s2
        
        if result:
            result = self.getHouseholdCreateDate() == impl.getHouseholdCreateDate()
        
        if result:
            result = self.getHouseholdUpdateDate() == impl.getHouseholdUpdateDate()
        
        if result:
            s1 = self.getHouseholdCreateUser()
            s2 = impl.getHouseholdCreateUser()
            result = s1 == s2
        
        if result:
            s1 = self.getHouseholdUpdateUser()
            s2 = impl.getHouseholdUpdateUser()
            result = s1 == s2
        
        return result
    
    def getDisplayString(self):
        return str(self.getHouseholdID()) + ' ' +\
    self.getHouseholdFirstName() + " " + self.getHouseholdLastName()

    def toString(self):
        return self.getDisplayString()
    
    def setHouseholdFirstName(self, newName):
        self.householdFirstName.setValue(newName)
    
    def getHouseholdFirstName(self):
        return self.householdFirstName.getValue()
    
    def setHouseholdLastName(self, newName):
        self.householdLastName.setValue(newName)
    
    def getHouseholdLastName(self):
        return self.householdLastName.getValue()
    
    def setAddress(self, newAddress):
        self.address = newAddress

    def getAddress(self, allowNone=False):
        if not allowNone and not self.address:
            dbo = DbAddress()
            dbo.save()
            self.setAddress(Address(dbo))
        if self.address and isinstance(self.address, DbAddress):
            self.address = Address(self.address)
        elif self.address and not isinstance(self.address, Address):
            self.address = Address(DbAddress())
        if not self.address.myDb:
            self.address.myDb = DbAddress()
        #print(self.address)
        return self.address
    
    def setOrganization(self, newOrganization):
        self.organization = newOrganization
         
    def getOrganization(self):
        return self.organization
    
    def getStreet(self):
        return self.getAddress().getStreet()
    
    def setStreet(self, newStreet):
        add = self.getAddress()
        #print(add.__class__.__name__)
        add.setStreet(newStreet)
    
    def setAddressLineTwo(self, newAddressLineTwo):
        self.getAddress().setAddressLineTwo(newAddressLineTwo)
    
    def getAddressLineTwo(self):
        return self.getAddress().getAddressLineTwo()
    
    def setCity(self, newCity):
        self.getAddress().setCity(newCity)
    
    def getCity(self):
        return self.getAddress().getCity()
    
    def setState(self, newState):
        self.getAddress().setState(newState)
    
    def getState(self):
        return self.getAddress().getState()
    
    def setPostalCode(self, newPostalCode):
        self.getAddress().setPostalCode(newPostalCode)
    
    def getPostalCode(self):
        return self.getAddress().getPostalCode()
    
    def setPhone(self, newPhone):
        self.getAddress().setPhone(newPhone)
    
    def getPhone(self):
        return self.getAddress().getPhone()
    
    def setMobilePhone(self, newMobilePhone):
        self.getAddress().setMobilePhone(newMobilePhone)
    
    def getMobilePhone(self):
        return self.getAddress().getMobilePhone()
    
    def setFax(self, newFax):
        self.getAddress().setFax(newFax)
    
    def getFax(self):
        return self.getAddress().getFax()
    
    def setPager(self, newPager):
        self.getAddress().setPager(newPager)
    
    def getPager(self):
        return self.getAddress().getPager()
    
    def setEmail(self, newEmail):
        self.getAddress().setEmail(newEmail)
    
    def getEmail(self):
        return self.getAddress().getEmail()

    def getHouseholdID(self):
        return self.householdID.getValue()
    
    def setHouseholdID(self, d):
        self.householdID.setValue(d)
    
    def setID(self, d): 
        self.setHouseholdID(d)

    def getID(self):
        return self.householdID()

    def setDatabaseID(self, oid):
        self.setHouseholdID(oid)

    def setUpdateUser(self, d):
        self.setHouseholdUpdateUser(d)
    
    def getUpdateDate(self):
        return self.getHouseholdUpdateDate()
    
    def setCreateUser(self, d):
        self.setHouseholdCreateUser(d)
    
    def setCreateDate(self, d):
        self.setHouseholdCreateDate(d)
    
    def setUpdateDate(self, d):
        self.setHouseholdUpdateDate(d)
    
    def getHouseholdCreateDate(self):
        return self.householdCreateDate.getValue()
    
    def setHouseholdCreateDate(self, householdCreateDate):
        self.householdCreateDate.setValue(householdCreateDate)
 
    def getHouseholdUpdateDate(self):
        return self.householdUpdateDate.getValue()
    
    def setHouseholdUpdateDate(self, householdUpdateDate):
        self.householdUpdateDate.setValue(householdUpdateDate)
    
    def getHouseholdCreateUser(self):
        return self.householdCreateUser.getValue()
    
    def setHouseholdCreateUser(self, householdCreateUser):
        self.householdCreateUser.setValue(householdCreateUser)
    
    def getHouseholdUpdateUser(self):
        return self.householdUpdateUser.getValue()
    
    def setHouseholdUpdateUser(self, householdUpdateUser):
        self.householdUpdateUser.setValue(householdUpdateUser)
    
    def getLastUpdateUser(self):
        return self.getHouseholdUpdateUser()
    
    def getCreateUser(self):
        return self.getHouseholdCreateUser()
    
    def __str__(self)->str:
        return self.getDisplayString()
    
    def toDb(self):
        if not self.myDb or not isinstance(self.myDb, DbHousehold):
            self.myDb = DbHousehold()
        for name, att in self.__dict__.items():
            a = att
            if isinstance(att, Attribute):
                a = att.value
            self.myDb.__dict__[name] = a
        if self.address and not self.myDb.address:
            self.myDb.address = self.address.myDb 
        if self.organization and not self.myDb.organization:
            self.myDb.organization = self.organization.myDb
    
    def fromDb(self):
        for name, att in self.myDb.__dict__.items():
            if isinstance(att, bytes):
                att = att.decode()
            myAtt = self.__dict__.get(name)
            if not myAtt: 
                self.__dict__[name] = att
            else:
                if isinstance(myAtt, Attribute):
                    myAtt.value = att
                else:
                    myAtt = att
                self.__dict__[name] = myAtt
            
        if hasattr(self.myDb,'address'):
            self.setAddress(Address(self.myDb.address))
        else:
            self.setAddress(Address(DbAddress()))
        if hasattr(self.myDb,'organization'):
            self.setOrganization(Organization(self.myDb.organization))
            
    def validate(self):
        if self.address:
            ai = self.address
            if not ai.getAddressCreateUser():
                ai.setAddressCreateUser(self.getHouseholdCreateUser())
            if not ai.getAddressUpdateUser():
                ai.setAddressUpdateUser(self.getHouseholdUpdateUser())
        result = True
        atts = self.getAttributeList()
        try:
            BusinessObject.validateAttributes(atts)
        except InvalidAttributeValueException as e:
            super().addMessage(e.getMsg())
            result = False
        if result:
            result = self.validate2()
        return result
        
    def save(self):
        add = self.getAddress()
        if not add:
            add = ObjectFactory().getNewAddress(self.getAddressUpdateUser())
            self.setAddress(add)
        uID = self.myDb.householdUpdateUser
        if not uid:
            uID = 1
        if not add.getAddressCreateUser():
            add.setAddressCreateUser(uid)
        if not add.getAddressUpdateUser():
            add.setAddressUpdateUser(uid)
        add.save()
        self.toDb()
        self.myDb.save()       
        self.fromDb()
  
    def remove(self):
            self.myDb.delete()
              
    def delete(self):
        self.myDb.deleteFlag = True
        self.myDb.save()
    
    def getAttributeList(self): 
        return [         
            self.householdID,
            self.householdAddressID,
            self.householdOrganizationID,
            self.householdFirstName,
            self.householdLastName,
            self.householdCreateUser,
            self.householdUpdateUser,
            self.householdCreateDate,
            self.householdUpdateDate
        ]


class Availability(BusinessObject):

    def __init__(self, myDb=None): 
        self.availabilityID = IntegerAttribute("availabilityID")
        self.availabilityVolunteerID = IntegerAttribute("availabilityVolunteerID")
        self.availabilityStartDate = DateAttribute("availabilityStartDate")
        self.availabilityEndDate = DateAttribute("availabilityEndDate")
        self.availabilityCreateDate = DateAttribute("availabilityCreateDate")
        self.availabilityUpdateDate = DateAttribute("availabilityUpdateDate")
        self.availabilityCreateUser = IntegerAttribute("availabilityCreateUser")
        self.availabilityUpdateUser = IntegerAttribute("availabilityUpdateUser")
        super().__init__()
        super().setIdProperties(self.availabilityID)
        super().setTrackingAttributes(self.availabilityCreateUser,
                self.availabilityUpdateUser,
                self.availabilityCreateDate,
                self.availabilityUpdateDate)
        
        self.myDb = myDb
        if myDb:
            self.fromDb()

    def getDisplayString(self):
        return self.toString()
    
    def isSameState(self, impl):
        result = True
        if impl:
            result = super().isSameBaseState(impl)
        else:
            result = False
        if result:
            result = self.getAvailabilityStartDate() == impl.getAvailabilityStartDate()
        if result: 
            result = self.getAvailabilityEndDate() == impl.getAvailabilityEndDate()
        if result:
            s1 = self.getAvailabilityID()
            s2 = impl.getAvailabilityID()
            result = s1 == s2
        if result:
            result = self.getAvailabilityCreateDate() == impl.getAvailabilityCreateDate()
        if result:
            result = self.getAvailabilityUpdateDate() == impl.getAvailabilityUpdateDate()
        if result:
            s1 = self.getAvailabilityCreateUser()
            s2 = impl.getAvailabilityCreateUser()
            result = s1 == s2
        if result:
            s1 = self.getAvailabilityUpdateUser()
            s2 = impl.getAvailabilityUpdateUser()
            result = s1 == s2
        return result
    
    def __str__(self):
        return self.totring()

    def getAvailabilityStartDate(self):
        return self.availabilityStartDate
    
    def setAvailabilityID(self, availabilityID):
        self.availabilityID.setValue(availabilityID)
    
    def setAvailabilityStartDate(self, newStartDate):
        if newStartDate and not isinstance(newStartDate, DT):
            raise InvalidArgumentException('not a datetime')
        self.availabilityStartDate.setValue(newStartDate)
    
    def setAvailabilityEndDate(self, newEndDate):
        if newEndDate and not isinstance(newEndDate, DT):
            raise InvalidArgumentException('not a datetime')
        self.availabilityEndDate.setValue(newEndDate)
    
    def getAvailabilityEndDate(self):
        result = None
        if not self.availabilityEndDate or not self.availabilityEndDate.getValue():
            pass
        else:
            result = self.availabilityEndDate.getValue()
        return result

    def getAvailabilityID(self):
        return self.availabilityID.getValue()

    def setID(self, oid):
        self.setAvailabilityID(oid)

    def getID(self):
        return self.getAvailabilityID()
    
    def getStartDateString(self):
        result = ''
        d = self.getAvailabilityStartDate()
        if d:
            result = d.strftime("%m/%d/%Y")
        return result
    
    def getEndDateString(self):
        result = ''
        d = self.getAvailabilityEndDate(self)
        if d:
            d.strftime("%m/%d/%Y")
        return result
    
    def setUpdateUser(self, oid):
        self.setAvailabilityUpdateUser(oid)
    
    def getUpdateDate(self):
        return self.getAvailabilityUpdateDate()
    
    def setCreateUser(self, oid):
        self.setAvailabilityCreateUser(oid)
    
    def setCreateDate(self, date):
        self.setAvailabilityCreateDate(self, date)
    
    def setUpdateDate(self, date):
        self.setAvailabilityUpdateDate(date)
    
    def getAvailabilityCreateDate(self):
        return self.availabilityCreateDate.getValue()
    
    def setAvailabilityCreateDate(self, availabilityCreateDate):
        self.availabilityCreateDate.setValue(availabilityCreateDate)
    
    def getAvailabilityUpdateDate(self):
        return self.availabilityUpdateDate.getValue()
    
    def setAvailabilityUpdateDate(self, availabilityUpdateDate):
        self.availabilityUpdateDate.setValue(availabilityUpdateDate)
    
    def getAvailabilityCreateUser(self):
        return self.availabilityCreateUser.getValue()
    
    def setAvailabilityCreateUser(self, availabilityCreateUser):
        self.availabilityCreateUser.setValue(availabilityCreateUser)
    
    def  getAvailabilityUpdateUser(self):
        return self.availabilityUpdateUser.getValue()
    
    def setAvailabilityUpdateUser(self, availabilityUpdateUser):
        self.availabilityUpdateUser.setValue(availabilityUpdateUser)
    
    def getLastUpdateUser(self):
        return self.getAvailabilityUpdateUser()
    
    def getCreateUser(self):
        return self.getAvailabilityCreateUser()
    
    def toString(self):
        result = ''
        if self.startDate:
            s = self.startDate.value
            if s:
                result += s.strftime("Start: %m/%d/%Y ")
            else:
                result += 'Start: null '
        else:
            result += 'Start: null '
            
        if self.endDate:
            s = self.endDate.value
            if s:
                result += s.strftime("End: %m/%d/%Y ")
            else:
                result += 'End: null '
        else:
            result += 'End: null '
        
        if self.volunteer:
            result += str(self.volunteer)
        else:
            result += 'no volunteer'
        return result
    
    def toDb(self):
        for name, att in self.__dict__.items():
            a = att
            if isinstance(att, Attribute):
                a = att.value
            self.myDb.__dict__[name] = a
    
    def fromDb(self):
        for name, att in self.myDb.__dict__.items():
            if isinstance(att, bytes):
                att = att.decode()
            myAtt = self.__dict__.get(name)
            if not myAtt: 
                self.__dict__[name] = att
            else:
                if isinstance(myAtt, Attribute):
                    myAtt.value = att
                else:
                    myAtt = att
                self.__dict__[name] = myAtt

    def validate(self):
        result = True
        atts = self.getAttributeList()
        try:
            BusinessObject.validateAttributes(atts)
        except InvalidAttributeValueException as e:
            super().addMessage(e.getMsg())
            result = False

        if self.availabilityEndDate and self.availabilityEndDate.getValue() \
                and self.availabilityStartDate and self.availabilityStartDate.getValue()\
                and self.availabilityEndDate.value > self.availabilityStartDate.value:
            super().addMessage(VSMessageFactory.getDateSequenceError(MessageSeverity.WARNING, \
                    self.getAvailabilityStartDate(), \
                    self.getAvailabilityEndDate()))
            result = False
        
        if not result:
            raise InvalidAttributeValueException(super().getMessage(), \
                    VSMessageFactory.getDateSequenceError( \
                            MessageSeverity.WARNING, \
                            self.getAvailabilityStartDate(), \
                            self.getAvailabilityEndDate()).getText())
        
    def save(self):
        self.toDb()
        self.myDb.save()       
        self.fromDb()
  
    def remove(self):
            self.myDb.delete()
              
    def delete(self):
        self.myDb.deleteFlag = True
        self.myDb.save()
    
    def getAttributeList(self): 
        return [
            self.availabilityID,
            self.availabilityVolunteerID,
            self.availabilityStartDate,
            self.availabilityEndDate,
            self.availabilityCreateDate,
            self.availabilityUpdateDate,
            self.availabilityCreateUser,
            self.availabilityUpdateUser
        ]


class Volunteer(BusinessObject):
    
    def __init__(self, household=None, organization=None, myDb=None):
        
        super().__init__()
        self.volunteerID = IntegerAttribute("volunteerID")
        self.volunteerFirstName = StringAttribute("volunteerFirstName")
        self.volunteerLastName = StringAttribute("volunteerLastName")
        self.cost = CurrencyAttribute("cost")
        self.staff = BooleanAttribute("staff")
        self.volunteerCreateUser = IntegerAttribute("volunteerCreateUser")
        self.volunteerUpdateUser = IntegerAttribute("volunteerUpdateUser")
        self.volunteerCreateDate = DateAttribute("volunteerCreateDate")
        self.volunteerUpdateDate = DateAttribute("volunteerUpdateDate")
        self.household = Household
        self.organization = organization
        self.address = None
        self.workAddress = None
        self.login = None
        self.skills = []
        self.activities = []
        self.availability = None
        self.myDb=myDb
        if myDb:
            self.fromDb()
        super().__init__()
        super().setIdProperties(self.volunteerID)
        super().setTrackingAttributes(self.volunteerCreateUser,
                self.volunteerUpdateUser,
                self.volunteerCreateDate,
                self.volunteerUpdateDate)
            
        self.cost.setNullAllowed(False)
        self.cost.setHasMinimum(True)
        self.cost.setMinimum(0)
        self.cost.setValue(0)
        
        self.volunteerLastName.allowInvalID = False
        self.volunteerLastName.setAllSpacesAllowed(False)
        self.volunteerLastName.setNullAllowed(False)
        self.volunteerLastName.setNullStringAllowed(False)
        self.volunteerLastName.setHasMaximumLength(True)
        self.volunteerLastName.setMaximumLength(255)

        self.volunteerFirstName.allowInvalID = False
        self.volunteerFirstName.setAllSpacesAllowed(False)
        self.volunteerFirstName.setNullAllowed(False)
        self.volunteerFirstName.setNullStringAllowed(False)
        self.volunteerFirstName.setHasMaximumLength(True)
        self.volunteerFirstName.setMaximumLength(255)
        
        self.staff.allowInvalID = False
        self.staff.setValue(False)
    def isSameState(self, impl):
        result = super().isSameBaseState(self, impl)
        
        if result:
            s1 = self.getVolunteerID()
            s2 = impl.getVolunteerID()
            result = s1 == s2
        
        if result:
            s1 = self.getVolunteerHouseholdID()
            s2 = impl.getVolunteerHouseholdID()
            result = s1 == s2
        
        if result:
            s1 = self.getVolunteerAddressID()
            s2 = impl.getVolunteerAddressID()
            result = s1 == s2
        
        if result:
            s1 = self.getVolunteerWorkAddressID()
            s2 = impl.getVolunteerWorkAddressID()
            result = s1 == s2
        
        if result:
            s1 = self.getVolunteerFirstName()
            s2 = impl.getVolunteerFirstName()
            result = s1 == s2
        
        if result:
            s1 = self.getVolunteerLastName()
            s2 = impl.getVolunteerLastName()
            result = s1 == s2
        
        if result:
            result = self.getCost() == impl.getCost() 
        
        ha1 = self.hasAddress()
        ha2 = impl.hasAddress()
        if (ha1 != ha2):
            result = False
        elif (ha1 == True):
            ai1 = self.getAddress()
            ai2 = impl.getAddress()
            result = ai1.isSameState(ai2)
        
        hi1 = self.getHousehold()
        hi2 = impl.getHousehold()
        if hi1 != None and hi2 == None:
            result = False
        elif hi1 == None and hi2 != None:
            result = False
        elif hi1 != None and hi2 != None:
            result = hi1.isSameState(hi2)
        
        wai1 = self.getWorkAddress()
        wai2 = impl.getWorkAddress()
        
        if wai1 != None and wai2 == None:
            result = False
        elif wai1 == None and wai2 != None:
            result = False
        elif wai1 != None and wai2 != None:
            result = wai1.isSameState(wai2)
        
        li1 = self.getLogin()
        li2 = impl.getLogin()
        if li1 != None and li2 == None:
            result = False
        elif li1 == None and li2 != None:
            result = False
        elif li1 != None and li2 != None:
            result = li1.isSameState(li2)
        if result:
            oi1 = self.getOrganization(True)
            oi2 = impl.getOrganization(True)
            if oi1 != None and oi2 == None:
                result = False
            elif oi1 == None and oi2 != None:
                result = False
            elif oi1 != None and oi2 != None:
                result = oi1.isSameState(oi2)
        if result:
            result = Utils.compareCollections(self.getSkills(), impl.getSkills(), False)
        
        if result:
            result = self.getVolunteerCreateDate() == impl.getVolunteerCreateDate()
        
        if result:
            result = self.getVolunteerUpdateDate() == impl.getVolunteerUpdateDate()
        
        if result:
            s1 = self.getVolunteerCreateUser()
            s2 = impl.getVolunteerCreateUser()
            result = s1 == s2
        
        if result:
            s1 = self.getVolunteerUpdateUser()
            s2 = impl.getVolunteerUpdateUser()
            result = s1 == s2
        
        if result:
            result = len(self.tasks) == len(impl.tasks)
            if result and self.tasks.isEmpty() == False:
                l1 = []
                l2 = []
                l1.append(self.getTasks())
                l2.append(impl.getTasks())
                c = TaskComparator()
                Collections.sort(l1, c)
                Collections.sort(l2, c)
                for idx, t1 in enumerate(l1):
                    t2 = l2.get(idx)
                    result2 = c.compare(t1, t2) == 0
                    if result2:
                        result = False
                        break
        return result
    
    def getCost(self):
        return self.cost.getValue()
    
    def setCost(self, val):
        self.cost.setValue(val)
    
    def getTasks(self):
        return self.tasks
    
    def removeTask(self,task):
        self.tasks.remove(task)
            
    def setTasks(self, tasks):
        self.tasks.clear()
        if not tasks == None:
            self.tasks.extend(tasks)
            if len(self.tasks) > 0:
                Collections.sort(self.tasks, TaskComparator())
                
    def addTask(self, task):
        self.assign(task)
    
    def getSkills(self):
        return self.skills
    
    def removeSkill(self, skill):
        self.skills.remove(skill)
            
    def setSkills(self, skills):
        self.skills.clear()
        if skills:
            self.skills.extend(skills)
            if len(self.skills) > 1:
                Collections.sort(self.skills)
                
    def addSkill(self, skill):
        if not skill in self.skills:
            self.skills.append(skill)
            if len(self.skills) > 1:
                Collections.sort(self.skills)
    
    def getActivities(self):
        return self.activities
    
    def removeActivity(self, activity):
        self.activities.remove(activity)
            
    def setActivities(self, activities):
        self.activities.clear()
        if activities:
            self.activities.extend(activities)
            if len(self.activities) > 1:
                Collections.sort(self.activities)
                 
    def addActivity(self, activity):
        if not activity in self.activities:
            self.activities.append(activity)
            if len(self.activities) > 1:
                Collections.sort(self.activities)
    
    def assign(self, task):
        if task and not self.tasks.contains(task):
            self.tasks.append(task)        

    def getVolunteerFirstName(self):
        return self.volunteerFirstName.getValue()
    
    def setOrganization(self, newOrganization):
        self.organization = newOrganization

    def getOrganization(self, allowNone=False):
        if allowNone == False and not self.organization:
            self.setOrganization(Organization(DbOrganization()))
        return self.organization
    
    def getDisplayString(self):
        s = str(self.volunteerID) + ' '\
            + str(self.getVolunteerFirstName()) + " " \
            + str(self.getVolunteerLastName())\
            + ' create user ' + str(self.volunteerCreateUser)\
            + ' update user ' + str(self.volunteerUpdateUser)
        if self.organization:
            s += ' organization '
            s += str(self.organization)
        else:
            s += ' no org '
            s += str(self.myDb.organization_id)
        return s
    
    def setVolunteerFirstName(self, newFirstName):
        self.volunteerFirstName.setValue(newFirstName)
    
    def setVolunteerLastName(self, newLastName):
        self.volunteerLastName.setValue(newLastName)
    
    def getVolunteerLastName(self):
        return self.volunteerLastName.getValue()
    
    def setHousehold(self, newHousehold):
        self.household = newHousehold
        
    def getHousehold(self):
        return self.household
    
    def setAddress(self, newAddress):
        self.address = newAddress
        
    def hasAddress(self):
        return self.address is not None
    
    def getAnAddress(self, useHouseholdIfNone):
        if useHouseholdIfNone: 
            return self.getAddress()
        else: 
            return self.address 
    
    def getAddress(self):
        result = None
        if not self.address:
            result = self.getHousehold().getAddress()
        else:
            result = self.address
        return result
    
    def getMyAddress(self):
        return self.address
    
    def setMyAddress(self, newAddress):
        self.setAddress(newAddress)
    
    def getAddressForUpdate(self, uid):
        result = None
        if not self.address:
                result = ObjectFactory().getNewAddress(uid)
                ha = self.getHousehold().getAddress()
                result.setAddressLineTwo(ha.getAddressLineTwo())
                result.setCity(ha.getCity())
                result.setEmail(ha.getEmail())
                result.setFax(ha.getFax())
                result.setMobilePhone(ha.getMobilePhone())
                result.setPager(ha.getPager())
                result.setPhone(ha.getPhone())
                result.setPostalCode(ha.getPostalCode())
                result.setState(ha.getState())
                result.setStreet(ha.getStreet())
                result.setAddressCreateUser(uid)
                result.setAddressUpdateUser(uid)
                self.setAddress(result)         
        result = self.address
        return result

    def setWorkAddress(self, newWorkAddress):
        self.workAddress = newWorkAddress

    def getWorkAddress(self):
        return self.workAddress
    
    def getEmail(self):
        return self.getAddress().getEmail()
    
    def setEmail(self, add):
        self.getAddressForUpdate().setEmail(add)
    
    def getPhone(self):
        return self.getAddress().getPhone()
    
    def setPhone(self, add):
        self.getAddressForUpdate().setPhone(add)
    
    def getPager(self):
        return self.getAddress().getPager()
    
    def setPager(self, add):
        self.getAddressForUpdate().setPager(add)
    
    def getMobilePhone(self):
        return self.getAddress().getMobilePhone()
    
    def setMobilePhone(self, add):
        self.getAddressForUpdate().setMobilePhone(add)
    
    def getFax(self):
        return self.getAddress().getFax()
    
    def setFax(self, add):
        self.getAddressForUpdate().setFax(add)
    
    def getPostalCode(self):
        return self.getAddress().getPostalCode()
    
    def setPostalCode(self, add):
        self.getAddressForUpdate().setPostalCode(add)
    
    def getState(self):
        return self.getAddress().getState()
    
    def setState(self, add):
        self.getAddressForUpdate().setState(add)
    
    def getCity(self):
        return self.getAddress().getCity()
    
    def setCity(self, add):
        self.getAddressForUpdate().setCity(add)
    
    def getAddressLineTwo(self):
        return self.getAddress().getAddressLineTwo()
    
    def setAddressLineTwo(self, add):
        self.getAddressForUpdate().setAddressLineTwo(add)
    
    def getStreet(self):
        return self.getAddress().getStreet()
    
    def setStreet(self, add):
        self.getAddressForUpdate().setStreet(add)
    
    def compareTo(self, vol):
        result = -1
        if not vol:
            result = 1
        elif isinstance(vol, Volunteer):
            result = VolunteerComparator().compare(self, vol)
        else:
            raise ClassCastException("Object: " + vol.__class__.__name__ + ": " + str(vol) + " is not an instance of Volunteer")
        return result
    
    def setParentObject(self, parent): 
        self.household = parent

    def getVolunteerID(self):
        return self.volunteerID.getValue()
    
    def setVolunteerID(self, oid):
        self.volunteerID.setValue(oid)
    
    def getID(self):
        return self.getVolunteerID()
    
    def setID(self, d):
        self.setVolunteerID(d)

    def getVolunteerName(self):
        return str(self.getVolunteerFirstName()) + " " + str(self.getVolunteerLastName())
    
    def setDatabaseID(self, oid):
        self.setVolunteerID(oid)

    def setUpdateUser(self, oid):
        self.setVolunteerUpdateUser(oid)

    def getUpdateDate(self):
        return self.getVolunteerUpdateDate()
    
    def setCreateUser(self, d):
        self.setVolunteerCreateUser(d)
    
    def setCreateDate(self, d):
        self.setVolunteerCreateDate(d)
    
    def setUpdateDate(self, e):
        self.setVolunteerUpdateDate(e)
    
    def getVolunteerCreateDate(self):
        return self.volunteerCreateDate.getValue()
    
    def setVolunteerCreateDate(self, volunteerCreateDate):
        self.volunteerCreateDate.setValue(volunteerCreateDate)
    
    def getVolunteerUpdateDate(self):
        return self.volunteerUpdateDate.getValue()

    def setVolunteerUpdateDate(self, volunteerUpdateDate):
        self.volunteerUpdateDate.setValue(volunteerUpdateDate)
    
    def getVolunteerCreateUser(self):
        return self.volunteerCreateUser.getValue()
    
    def setVolunteerCreateUser(self, volunteerCreateUser):
        self.volunteerCreateUser.setValue(volunteerCreateUser)
    
    def getVolunteerUpdateUser(self):
        return self.volunteerUpdateUser.getValue()
    
    def setVolunteerUpdateUser(self, volunteerUpdateUser):
        self.volunteerUpdateUser.setValue(volunteerUpdateUser)
    
    def useHouseholdAddress(self):
        if self.hasAddress():
            self.address.delete()
            self.setAddress(None)
        
    def getLastUpdateUser(self):
        return self.getVolunteerUpdateUser()
    
    def getCreateUser(self):
        return self.getVolunteerCreateUser()
    
    def getLogin(self):
        return self.login
    
    def setLogin(self, li):
        self.login = li
    
    def setStaff(self, val):
        self.staff.setValue(val)
        
    def getStaff(self):
        return self.staff.getValue()
    
    def isStaff(self):
        return self.staff.getValue()
        
    def __str__(self):
        return self.getDisplayString()
    
    def toDb(self):
        if not self.myDb:
            self.myDb = DbVolunteer()
        for name, att in self.__dict__.items():
            a = att
            if isinstance(att, Attribute):
                a = att.value
            self.myDb.__dict__[name] = a
        #if self.household:
        #    self.myDb.household = self.household.myDb
        if self.address:
            self.myDb.address = self.address.myDb
        if self.workAddress:
            self.myDb.workAddress = self.workAddress.myDb
        if self.login:
            self.myDb.login = self.login.myDb
        if self.organization:
            self.myDb.organization = self.organization.myDb
        if self.skills and len(self.skills) > 0: 
            self.myDb.skills.clear()
            for skill in self.skills:
                self.myDb.skills.append(skill.myDb)
        if self.activities and len(self.activities) > 0:
            self.myDb.activities.clear()
            for a in self.activities:
                self.myDb.activities.add(a.myDb)
        if self.availability:
            self.myDb.availability = self.availability.myDb
    
    def fromDb(self):
        for name, att in self.myDb.__dict__.items():
            if isinstance(att, bytes):
                att = att.decode()
            myAtt = self.__dict__.get(name)
            if not myAtt: 
                self.__dict__[name] = att
            else:
                if isinstance(myAtt, Attribute):
                    myAtt.value = att
                else:
                    myAtt = att
                self.__dict__[name] = myAtt
        if self.getVolunteerID() and self.myDb.household: #.exists():
            self.household = Household(self.myDb.household)
        if self.getVolunteerID() and self.myDb.address:
            self.address = Address(self.myDb.address)
        if self.getVolunteerID() and self.myDb.workAddress.exists():
            self.workAddress = WorkAddress(self.myDb.workAddress)
        if self.getVolunteerID() and self.myDb.login and self.myDb.login.exists():
            self.login = Login(self.myDb.login)
        if self.getVolunteerID() and self.myDb.organization:
            self.organization = Organization(self.myDb.organization)
        if self.getVolunteerID() and self.myDb.skills.exists():
            self.skills.clear()
            for skill in self.myDb.skills.all():
                self.skiladdend(VolunteerSkill(skill))
        if self.getVolunteerID() and self.myDb.activities.exists():
            self.activities.clear()
            for a in self.myDb.activities.all():
                self.activities.append(Activity(a))
        if self.getVolunteerID() and self.myDb.availability:
            self.availability = Availability(self.myDb.availability)

    def validate(self):
        result = True
        atts = self.getAttributeList()
        try:
            BusinessObject.validateAttributes(atts)
        except InvalidAttributeValueException as e:
            super().addMessage(e.getMsg())
            result = False
        return result
        
    def save(self):
        self.toDb()
        self.myDb.save()     
        self.fromDb()
        #self.setVolunteerID(self.myDb.volunteerID)
  
    def remove(self):
            self.myDb.delete()
              
    def delete(self):
        self.myDb.deleteFlag = True
        self.myDb.save()
    
    def getAttributeList(self): 
        return [    
            self.volunteerID,
            self.volunteerFirstName,
            self.volunteerLastName,
            self.cost,
            self.staff,
            self.volunteerCreateUser,
            self.volunteerUpdateUser,
            self.volunteerCreateDate,
            self.volunteerUpdateDate
        ]


class Job(BusinessObject):

    Skill_NAME_SIZE = 20

    def __init__(self, myDb=None):
        self.expertRequired = BooleanAttribute("expertRequired")
        self.count = IntegerAttribute("count")
        self.jobID = IntegerAttribute("jobID")
        self.jobAssignmentID = IntegerAttribute("jobAssignmentID")
        self.jobSkillID = IntegerAttribute("jobSkillID")
        self.jobEventID = IntegerAttribute("jobEventID")
        self.jobCreateUser = IntegerAttribute("jobCreateUser")
        self.jobUpdateUser = IntegerAttribute("jobUpdateUser")
        self.jobCreateDate = DateAttribute("jobCreateDate")
        self.jobUpdateDate = DateAttribute("jobUpdateDate")
        self.optional = BooleanAttribute("optional")
        self.index = 0
        self.assignment = None
        self.skill = None
        super().__init__()
        super().setIdProperties(self.jobID)
        super().setTrackingAttributes(self.jobCreateUser,
                self.jobUpdateUser,
                self.jobCreateDate,
                self.jobUpdateDate)
        self.expertRequired.allowInvalID = False
        self.expertRequired.setNullAllowed(False)
        self.expertRequired.setValue(False)

        self.count.allowInvalID = False
        self.count.setNullAllowed(False)
        self.count.setValue(1)
        self.count.setHasMinimum(True)
        self.count.setMinimum(1)

        self.jobAssignmentID.allowInvalID = False
        self.jobAssignmentID.setNullAllowed(True)
        self.jobAssignmentID.setHasMinimum(True)
        self.jobAssignmentID.setMinimum(0)

        self.jobSkillID.allowInvalID = False
        self.jobSkillID.setNullAllowed(False)
        self.jobSkillID.setHasMinimum(True)
        self.jobSkillID.setMinimum(0)

        self.jobEventID.allowInvalID = False
        self.jobEventID.setNullAllowed(False)
        self.jobEventID.setHasMinimum(True)
        self.jobEventID.setMinimum(0)

        self.optional.allowInvalID = False
        self.optional.setNullAllowed(False)
        self.optional.setValue(False)
        self.myDb = myDb
        if myDb:
            self.fromDb()

    def clone(self, job):
        self.skill = job.skill
        self.setExpertRequired(job.getExpertRequired())
        self.setJobSkillID(job.getJobSkillID())
        self.setJobCreateUser(job.getJobCreateUser())
        self.setJobUpdateUser(job.getJobUpdateUser())
        self.setEventID(job.getEventID())
    
    def isSameState(self, impl):
        result = True
        if not impl or not isinstance(impl, Job):
            result = False
            #print(str(result) + ' Utils.isinstance(ja1,ja2)')
        else:
            result = self.isSameBaseState(impl)
            #print(str(result) + ' isSameBaseState')
        if result:
            ja1 = self.getAssignment()
            ja2 = impl.getAssignment()
            if Utils.isNull(ja1, ja2):
                #print(str(result) + ' Utils.isNull(ja1,ja2)')
                result = Utils.compareNull(ja1,ja2) == 0
                #print(str(result) + ' Utils.compNull(ja1,ja2)')
            if ja1 and result:
                s1 = self.isExpertRequired()
                s2 = impl.isExpertRequired()
                result = s1 == s2
                # print(str(result) + ' isExpertRequired')
            if result:
                s1 = self.getJobID()
                s2 = impl.getJobID()
                result = s1 == s2
                #print(str(result) + ' getJobID')
            if result:
                s1 = self.getJobAssignmentID()
                s2 = impl.getJobAssignmentID()
                result = s1 == s2
                #print(str(result) + ' getJobAssignmentID')
            if result:
                s1 = self.getJobSkillID()
                s2 = impl.getJobSkillID()
                result = s1 == s2
                #print(str(result) + ' getJobSkillID')
            if result:
                s1 = self.getJobEventID()
                s2 = impl.getJobEventID()
                result = s1 == s2
                #print(str(result) + ' getJobEventID')
            if result:
                result = self.getJobCreateDate() == impl.getJobCreateDate()
                #print(str(result) + ' getJobCreateDate')
            if result: 
                result = self.getJobUpdateDate() == impl.getJobUpdateDate()
                #print(str(result) + ' getJobUpdateDate')
            if result:
                s1 = self.getJobCreateUser()
                s2 = impl.getJobCreateUser()
                result = s1 == s2
                #print(str(result) + ' getJobCreateUser')
            if result:
                s1 = self.getJobUpdateUser()
                s2 = impl.getJobUpdateUser()
                result = s1 == s2
                #print(str(result) + ' getJobUpdateUser')
        return result
    
    def getDisplayString(self):
        result = ''
        SPACE  = '                                                        '
        try:
            result = ''
            if self.expertRequired and self.expertRequired.getValue():
                result += "Expert " 
            else:
                result += "       "
            if self.getSkill() and not self.getAssignment():
                skillName = self.getSkill().getSkillName()
                if len(skillName) > Job.SKILL_NAME_SIZE:
                    skillName = skillName[0: Job.SKILL_NAME_SIZE - 1]
                elif len(skillName) < Job.SKILL_NAME_SIZE:
                    skillName += SPACE[0: Job.SKILL_NAME_SIZE - len(skillName)]
                result += skillName
            if self.assignment:
                result += self.assignment.getDisplayString()
            else:
                result += (": unassigned")
            if self.getOptional():
                result += " optional"
            if self.getCount() > 1:
                result += " number "
                result += self.getCount()
        except Exception as e:
            self.log(err=e)
        return result

    def getAssignment(self):
        return self.assignment
    
    def setAssignment(self, newJobAssignment):
        self.assignment = newJobAssignment
        if newJobAssignment:
            oID = self.assignment.getJobAssignmentID()
            self.setJobAssignmentID(oid)
        
    def setSkill(self, newSkill):
        self.skill = newSkill
        oID = 0 
        if newSkill:
            oID = newSkill.getSkillID()
        self.setJobSkillID(oid)

    def getSkill(self):
        return self.skill
    
    def getIndex(self):
        return self.index
    
    def getEventID(self):
        return self.eventID
    
    def setCount(self, count):
        self.count.setValue(count)
    
    def getCount(self):
        return self.count.getValue()
    
    def setEventID(self, eventID):
        self.eventID = eventID
        self.jobEventID.setValue(eventID)

    def isExpertRequired(self):
        return self.expertRequired.getValue()

    def getExpertRequired(self):
        return self.isExpertRequired()
    
    def setExpertRequired(self, expertRequired):
        self.expertRequired.setValue(expertRequired)
    
    def compareTo(self, o):
        result = -1
        if not o:
            result = 1
        elif isinstance(o, Job):
            oKey = o.getJobID()
            key = self.getJobID()
            if key == oKey:
                result = 0
            elif key > oKey:
                result = 1
        else:
            raise ClassCastException("Object " + str(o) + "is not an instance of " + self.__class__.__name__)
        return result
    
    def isAssigned(self):
        return self.assignment != None
    
    def getRequiredAndUnassigned(self):
        return not self.getOptionalBoolean() and not self.isAssigned()

    def getJobID(self):
        return self.jobID.getValue()
    
    def setJobID(self, oid):
        self.jobID.setValue(oid)
    
    def getID(self):
        return self.getJobID()

    def setID(self, d):
        self.setJobID(d)

    def getJobEventID(self):
        return self.jobEventID.getValue()
    
    def setJobEventID(self, d):
        self.jobEventID.setValue(d)
    
    def getJobSkillID(self):
        return self.jobSkillID.getValue()
    
    def setJobSkillID(self, d):
        self.jobSkillID.setValue(d)
    
    def getJobAssignmentID(self):
        return self.jobAssignmentID.getValue()
    
    def setJobAssignmentID(self, jobAssignmentID):
        self.jobAssignmentID.setValue(jobAssignmentID)
        
    def setUpdateUser(self, d):
        self.setJobUpdateUser(d)
    
    def getUpdateDate(self):
        return self.getJobUpdateDate()
    
    def setCreateUser(self, d):
        self.setJobCreateUser(d)
    
    def setCreateDate(self, d):
        self.setJobCreateDate(d)
    
    def setUpdateDate(self, d):
        self.setJobUpdateDate(d)
    
    def getJobCreateDate(self):
        return self.jobCreateDate.getValue()
    
    def setJobCreateDate(self, jobCreateDate):
        self.jobCreateDate.setValue(jobCreateDate)
    
    def getJobUpdateDate(self):
        return self.jobUpdateDate.getValue()
    
    def setJobUpdateDate(self, jobUpdateDate):
        self.jobUpdateDate.setValue(jobUpdateDate)
    
    def getJobCreateUser(self):
        return self.jobCreateUser.getValue()
    
    def setJobCreateUser(self, jobCreateUser):
        self.jobCreateUser.setValue(jobCreateUser)
    
    def getJobUpdateUser(self):
        return self.jobUpdateUser.getValue()
    
    def setJobUpdateUser(self, jobUpdateUser):
        self.jobUpdateUser.setValue(jobUpdateUser)
    
    def setIndex(self, index):
        self.index = index
    
    def getLastUpdateUser(self):
        return self.getJobUpdateUser()
    
    def getCreateUser(self):
        return self.getJobCreateUser()
    
    def getOptional(self):
        return self.optional.getValue()
    
    def setOptional(self, val):
        self.optional.setValue(val)
        
    def toString(self):
        result = ''
        if self.skill:
            result += str(self.skill)
            result += ' '
        else:
            result += ' no skill '
        if self.assignment and self.assignment.volunteer:
            result += str(self.assignment.volunteer)
        else:
            result += ' no assigned volunteer'
        return result
    
    def __str__(self)->str:
        return self.toString()
    
    def toDb(self):
        for name, att in self.__dict__.items():
            a = att
            if isinstance(att, Attribute):
                a = att.value
            self.myDb.__dict__[name] = a
        if self.skill:
            self.myDb.skill = self.skill.myDb
    
    def fromDb(self):
        of = ObjectFactory()
        for name, att in self.myDb.__dict__.items():
            if isinstance(att, bytes):
                att = att.decode()
            myAtt = self.__dict__.get(name)
            if not myAtt: 
                self.__dict__[name] = att
            else:
                if isinstance(myAtt, Attribute):
                    myAtt.value = att
                else:
                    myAtt = att
                self.__dict__[name] = myAtt
        dbID = self.myDb.skill_id
        if dbid:
            self.setSkill(of.getSkill(dbid))
        try:
            jaDbo = self.myDb.assignments.all().first()
            if jaDbo:
                #print('jaDbo = ' + str(self.myDb.assignments.all()))
                self.setAssignment(JobAssignment(jaDbo))
        except:
            pass
    def validate(self):
        result = True
        atts = self.getAttributeList()
        try:
            BusinessObject.validateAttributes(atts)
        except InvalidAttributeValueException as e:
            super().addMessage(e.getMsg())
            result = False
        return result
        
    def save(self):
        self.toDb()
        self.myDb.save()       
        self.fromDb()
  
    def remove(self):
            self.myDb.delete()
              
    def delete(self):
        self.myDb.deleteFlag = True
        self.myDb.save()
    
    def getAttributeList(self): 
        return [
            self.expertRequired,
            self.count,
            self.jobID,
            self.jobAssignmentID,
            self.jobSkillID,
            self.jobEventID,
            self.jobCreateUser,
            self.UpdateUser,
            self.jobCreateDate,
            self.jobUpdateDate,
            self.optional
        ]


class JobAssignment(BusinessObject):
     
    def __init__(self, myDb=None):
        self.jobAssignmentID = IntegerAttribute("jobAssignmentID")
        self.assignmentDate = DateAttribute("assignmentDate")
        self.previousAssignmentDate = DateAttribute("previousAssignmentDate")
        self.accepted = BooleanAttribute("accepted")
        self.jobAssignmentCreateUser = IntegerAttribute("jobAssignmentCreateUser")
        self.jobAssignmentUpdateUser = IntegerAttribute("jobAssignmentUpdateUser")
        self.jobAssignmentCreateDate = DateAttribute("jobAssignmentCreateDate")
        self.jobAssignmentUpdateDate = DateAttribute("jobAssignmentUpdateDate")
        self.volunteer = None
        self.job = None
        super().__init__()
        self.myDb = myDb
        if myDb:
            self.fromDb()   
        super().setIdProperties(self.jobAssignmentID)
        super().setTrackingAttributes(self.jobAssignmentCreateUser,
                self.jobAssignmentUpdateUser,
                self.jobAssignmentCreateDate,
                self.jobAssignmentUpdateUser)
        self.accepted.allowInvalID = False
        self.accepted.setNullAllowed(False)
        self.accepted.setValue(False)

        self.assignmentDate.allowInvalID = False
        self.assignmentDate.setNullAllowed(False)

        self.previousAssignmentDate.allowInvalID = False
        self.previousAssignmentDate.setNullAllowed(True)
    
    def clone(self, source):
        self.setJobAssignmentCreateDate(super().now())
        self.setJobAssignmentUpdateDate(super().now())
        self.setJobAssignmentCreateUser(source.getJobAssignmentCreateUser())
        self.setJobAssignmentUpdateUser(source.getJobAssignmentUpdateUser())
        self.setJobAssignmentVolunteerID(source.getJobAssignmentVolunteerID())
        self.setJobID(source.getJobID())
        self.setAssignmentDate(source.getAssignmentDate())
        self.setPreviousAssignmentDate(source.getPreviousAssignmentDate())
        self.setAccepted(source.isAccepted())
        self.setDeleteFlag(source.getDeleteFlag())
        if source.getVolunteer():
            self.setVolunteer(source.getVolunteer())

    def isSameState(self, impl):
        result = super().isSameBaseState(impl)
        vi1 = self.getVolunteer()
        vi2 = impl.getVolunteer()
        if vi1 != None and vi2 == None:
            result = False
        elif vi1 == None and vi2 != None:
            result = False
        elif vi1 != None and vi2 != None:
            result = vi1.isSameState(vi2)
        if result:
            result = self.getAssignmentDate() == impl.getAssignmentDate()
        if result:
            s1 = self.isAccepted()
            s2 = impl.isAccepted()
            result = s1 == s2
        if result:
            s1 = self.getJobAssignmentID()
            s2 = impl.getJobAssignmentID()
            result = s1 == s2
        if result:
            s1 = self.getJobAssignmentVolunteerID()
            s2 = impl.getJobAssignmentVolunteerID()
            result = s1 == s2
        if result:    
            result = self.getJobAssignmentCreateDate() == impl.getJobAssignmentCreateDate()
        if result:
            result = self.getJobAssignmentUpdateDate() == impl.getJobAssignmentUpdateDate()
        if result:
            s1 = self.getJobAssignmentCreateUser()
            s2 = impl.getJobAssignmentCreateUser()
            result = s1 == s2
        if result:
            s1 = self.getJobAssignmentUpdateUser()
            s2 = impl.getJobAssignmentUpdateUser()
            result = s1 == s2
        return result
    
    def getDisplayString(self):
        sb = '|'
        s = "No Job"
        if self.job:
            s = 'job: ' 
            s += str(self.job)
            s += ' eoj| '
            if not self.job.getSkill():
                s += "no job skill" 
            else:
                s += ' jobskill' 
                s += str(self.job.getSkill())
                s += ' eojobskill'
            sb += s 
            sb += " assigned to "
            if not self.volunteer:
                sb += 'nobody'
            else:
                sb += str(self.volunteer)
                sb += " "
                if self.accepted != None and self.accepted.getValue() != None:
                    if self.accepted.getValue():
                        sb += " accepted "
                    else:
                        sb += ' not accepted'
        else:
            sb += s
        sb += '|'           
        return sb
    
    def __str__(self):
        return self.getDisplayString()

    def getJobAssignmentID(self):
        return self.jobAssignmentID.getValue()
    
    def setJobAssignmentID(self, d):
        self.jobAssignmentID.setValue(d)

    def getID(self):
        return self.getJobAssignmentID()
    
    def setID(self, i):
        self.setJobAssignmentID(i)
        
    def getAssignmentDate(self):
        return self.assignmentDate.getValue()
    
    def setAssignmentDate(self, assignmentDate):
        self.assignmentDate.setValue(assignmentDate)
    
    def getPreviousAssignmentDate(self):
        return self.previousAssignmentDate.getValue()
    
    def setPreviousAssignmentDate(self, previousAssignmentDate):
        self.previousAssignmentDate.setValue(previousAssignmentDate)
    
    def isAccepted(self):
        return self.accepted.getValue()
    
    def getAccepted(self):
        return self.accepted.getValue()

    def setAccepted(self, accepted):
        self.accepted.setValue(accepted)
    
    def getJob(self):
        return self.job
    
    def setJob(self, job):
        self.job = job
        
    def setUpdateUser(self, d):
        self.setJobAssignmentUpdateUser(d)
    
    def getUpdateDate(self):
        return self.getJobAssignmentUpdateDate()
    
    def setCreateUser(self, d):
        self.setJobAssignmentCreateUser(d)
    
    def setCreateDate(self, dat):
        self.setJobAssignmentCreateDate(dat)
    
    def setUpdateDate(self, dat):
        self.setJobAssignmentUpdateDate(dat)
    
    def getJobAssignmentCreateDate(self):
        return self.jobAssignmentCreateDate.getValue()
    
    def setJobAssignmentCreateDate(self, jobAssignmentCreateDate):
        self.jobAssignmentCreateDate.setValue(jobAssignmentCreateDate)
    
    def getJobAssignmentUpdateDate(self):
        return self.jobAssignmentUpdateDate.getValue()
    
    def getJobAssignmentCreateUser(self):
        return self.jobAssignmentCreateUser.getValue()
    
    def setJobAssignmentCreateUser(self, jobAssignmentCreateUser):
        self.jobAssignmentCreateUser.setValue(jobAssignmentCreateUser)
    
    def getJobAssignmentUpdateUser(self):
        return self.jobAssignmentUpdateUser.getValue()
    
    def setJobAssignmentUpdateUser(self, jobAssignmentUpdateUser):
        self.jobAssignmentUpdateUser.setValue(jobAssignmentUpdateUser)
    
    def getVolunteer(self):
        return self.volunteer
    
    def setVolunteer(self, vol):
        self.volunteer = vol
        
    def getLastUpdateUser(self):
        return self.getJobAssignmentUpdateUser()
    
    def getCreateUser(self):
        return self.getJobAssignmentCreateUser()
    
    def toDb(self):
        for name, att in self.__dict__.items():
            a = att
            if isinstance(att, Attribute):
                a = att.value
            self.myDb.__dict__[name] = a
        if self.job:
            self.myDb.job = self.job.myDb
        if self.volunteer:
            self.myDb.volunteer = self.volunteer.myDb
    
    def fromDb(self):
        of = ObjectFactory()
        for name, att in self.myDb.__dict__.items():
            if isinstance(att, bytes):
                att = att.decode()
            myAtt = self.__dict__.get(name)
            if not myAtt: 
                self.__dict__[name] = att
            else:
                if isinstance(myAtt, Attribute):
                    myAtt.value = att
                else:
                    myAtt = att
                self.__dict__[name] = myAtt
        self.job = of.getJob(self.myDb.job_id)
        self.volunteer = of.getVolunteer(self.myDb.volunteer_id)
        self.accepted.value = self.myDb.accepted
            
    def validate(self):
        result = True
        atts = self.getAttributeList()
        try:
            BusinessObject.validateAttributes(atts)
        except InvalidAttributeValueException as e:
            super().addMessage(e.getMsg())
            result = False
        return result
        
    def save(self):
        self.toDb()
        self.myDb.save()       
        self.fromDb()
  
    def remove(self):
            self.myDb.delete()
              
    def delete(self):
        self.myDb.deleteFlag = True
        self.myDb.save()
    
    def getAttributeList(self): 
        return [    
                self.jobAssignmentID,
                self.assignmentDate,
                self.previousAssignmentDate,
                self.accepted,
                self.jobAssignmentCreateUser,
                self.jobAssignmentUpdateUser,
                self.jobAssignmentCreateDate,
                self.jobAssignmentUpdateDate            
            ]


class Relationship(BusinessObject):

    NAME_SIZE = 25

    def __init__(self, myDb=None):
        self.relationshipID = IntegerAttribute("relationshipID")
        self.relationshipCreateUser = IntegerAttribute("relationshipCreateUser")
        self.relationshipUpdateUser = IntegerAttribute("relationshipUpdateUser")
        self.relationshipCreateDate = DateAttribute("relationshipCreateDate")
        self.relationshipUpdateDate = DateAttribute("relationshipUpdateDate")
        self.volunteerOne = None
        self.volunteerTwo = None
        self.relationshipType = None
        super().__init__()
        self.myDb = myDb
        if myDb:
            self.fromDb()
        super().setIdProperties(self.relationshipID)
        super().setTrackingAttributes(self.relationshipCreateUser,
                self.relationshipUpdateUser,
                self.relationshipCreateDate,
                self.relationshipUpdateDate)

    def isSameState(self, impl):
        result = super().isSameBaseState(impl)
        if result:        
            vi1 = self.getVolunteerOne()
            vi2 = self.getVolunteerOne()
            if vi1 != None and vi2 == None:
                result = False
            elif vi1 == None and vi2 != None:
                result = False
            elif vi1 != None and vi2 != None:
                result = vi1.isSameState(vi2)
        if result:    
            vi1 = self.getVolunteerTwo()
            vi2 = impl.getVolunteerTwo()
            if vi1 != None and vi2 == None:
                result = False
            elif vi1 == None and vi2 != None:
                result = False
            elif vi1 != None and vi2 != None:
                result = vi1.isSameState(vi2)
        if result:
            s1 = self.getVolunteerOneID()
            s2 = impl.getVolunteerOneID()
            result = s1 == s2
        if result:
            s1 = self.getVolunteerTwoID()
            s2 = impl.getVolunteerTwoID()
            result = s1 == s2
        if result:
            s1 = self.getRelationshipID()
            s2 = impl.getRelationshipID()
            result = s1 == s2
        if result:
            s1 = self.getRelationshipType()
            s2 = impl.getRelationshipType()
            result = s1 == s2
        if result:
            result = self.getRelationshipCreateDate() == impl.getRelationshipCreateDate()
        if result:
            result = self.getRelationshipUpdateDate() == impl.getRelationshipUpdateDate()
        if result:
            s1 = self.getRelationshipCreateUser()
            s2 = impl.getRelationshipCreateUser()
            result = s1 == s2
        if result:
            s1 = self.getRelationshipUpdateUser()
            s2 = impl.getRelationshipUpdateUser()
            result = s1 == s2
        return result
    
    def getDisplayString(self):
        name1 = 'None'
        if self.getVolunteerOne(): 
            name1 = str(self.getVolunteerOne().getDisplayString())
        name2 = 'None'
        if self.getVolunteerTwo():
            name2 = str(self.getVolunteerTwo())   
        typeStr = ''
        if self.relationshipType: 
            typeStr = str(self.relationshipType)
        if len(name1) < Relationship.NAME_SIZE:
            name1 += VSBase.SPACE[0: Relationship.NAME_SIZE - len(name1)]     
        if len(name2) < Relationship.NAME_SIZE:
            name2 += VSBase.SPACE[0: Relationship.NAME_SIZE - len(name2)]
        return name1 + " and " + name2 + ":   " + typeStr
    
    def getRelationshipType(self):
        return self.relationshipType
    
    def setRelationshipType(self, relationshipType):
        self.relationshipType = relationshipType
        
    def getVolunteerOne(self):
        return self.volunteerOne
    
    def setVolunteerOne(self, newVolunteerOne):
        self.volunteerOne = newVolunteerOne

    def setVolunteerTwo(self, newVolunteerTwo):
        self.volunteerTwo = newVolunteerTwo

    def getVolunteerTwo(self):
        return self.volunteerTwo
    
    def __str__(self):
        return self.getDisplayString()
    
    def compareTo(self, o):
        result = -1
        if isinstance(o,Relationship):
            oKey = o.getID()
            key = self.getID()
            if key == oKey:
                result = 0
            elif key > oKey:
                result = 1
        else:
            raise ClassCastException("Object " + str(o) + "is not an instance of Relationship")
        return result
    
    def getRelationshipID(self):
        return self.relationshipID.getValue()
    
    def setRelationshipID(self, d):
        self.relationshipID.setValue(d)
    
    def getID(self):
        result = None
        if self.getRelationshipID():
            result = self.getRelationshipID()
        return result

    def setID(self, d):
        self.setRelationshipID(d)

    def setDatabaseID(self, d):
        self.setRelationshipID(d)
    
    def setUpdateUser(self, d):
        self.setRelationshipUpdateUser(d)
    
    def getUpdateDate(self):
        return self.getRelationshipUpdateDate()
    
    def setCreateUser(self, d):
        self.setRelationshipCreateUser(d)
    
    def setCreateDate(self, d):
        self.setRelationshipCreateDate(d)
    
    def setUpdateDate(self, d):
        self.setRelationshipUpdateDate(date)
    
    def getRelationshipCreateDate(self):
        return self.relationshipCreateDate.getValue()
    
    def setRelationshipCreateDate(self, relationshipCreateDate):
        self.relationshipCreateDate.setValue(relationshipCreateDate)
    
    def  getRelationshipUpdateDate(self):
        return self.relationshipUpdateDate.getValue()
    
    def setRelationshipUpdateDate(self, relationshipUpdateDate):
        self.relationshipUpdateDate.setValue(relationshipUpdateDate)
    
    def getRelationshipCreateUser(self):
        return self.relationshipCreateUser.getValue()
    
    def setRelationshipCreateUser(self, relationshipCreateUser):
        self.relationshipCreateUser.setValue(relationshipCreateUser)
    
    def getRelationshipUpdateUser(self):
        return self.relationshipUpdateUser.getValue()
    
    def setRelationshipUpdateUser(self, relationshipUpdateUser):
        self.relationshipUpdateUser.setValue(relationshipUpdateUser)
    
    def areTogether(self):
        result = False
        if self.getRelationshipTypeID() == RelationshipType.TOGETHER_PREFERRED_VAL or \
                self.getRelationshipTypeID() == RelationshipType.TOGETHER_REQUIRED_VAL:
            result = True
        return result
    
    def areSeparate(self):
        result = False
        if self.getRelationshipTypeID() == RelationshipType.SEPARATE_PREFERRED_VAL or \
                self.getRelationshipTypeID() == RelationshipType.SEPARATE_REQUIRED_VAL:
            result = True
        return result
    
    def getLastUpdateUser(self):
        return self.getRelationshipUpdateUser()
    
    def getCreateUser(self):
        return self.getRelationshipCreateUser()
        
    def toDb(self):
        for name, att in self.__dict__.items():
            a = att
            if isinstance(att, Attribute):
                a = att.value
            self.myDb.__dict__[name] = a
        if self.volunteerOne:
            self.myDb.volunteeOne = self.volunteerOne.myDb
            self.volunteerOne_ID =  self.volunteerOne.getVolunteerID()
        if self.volunteerTwo:
            self.myDb.volunteeTwo = self.volunteerTwo
            self.volunteerTwo_ID =  self.volunteerTwo.volunteerID
        if self.relationshipType:
            self.myDb.relationshipType = self.relationshipType.myDb
    
    def fromDb(self):
        for name, att in self.myDb.__dict__.items():
            if isinstance(att, bytes):
                att = att.decode()
            myAtt = self.__dict__.get(name)
            if not myAtt: 
                self.__dict__[name] = att
            else:
                if isinstance(myAtt, Attribute):
                    myAtt.value = att
                else:
                    myAtt = att
                self.__dict__[name] = myAtt
        if self.myDb.volunteerOne_id:
            self.VolunteerOne = Volunteer(myDb=self.myDb.volunteerOne)
        if self.myDb.volunteerTwo_id:
            self.VolunteerTwo = self.myDb.volunteerTwo
        if self.getRelationshipID():
            if self.myDb.relationshipType_id:
                self.relationshipType = RelationshipType(self.myDb.relationshipType)

    def validate(self):
        result = True
        atts = self.getAttributeList()
        try:
            BusinessObject.validateAttributes(atts)
        except InvalidAttributeValueException as e:
            super().addMessage(e.getMsg())
            result = False
        return result
        
    def save(self):
        self.toDb()
        self.myDb.save()       
        self.fromDb()
  
    def remove(self):
            self.myDb.delete()
              
    def delete(self):
        self.myDb.deleteFlag = True
        self.myDb.save()
    
    def getAttributeList(self): 
        return [    
                self.relationshipID,
                self.relationshipCreateUser,
                self.relationshipUpdateUser,
                self.relationshipCreateDate,
                self.relationshipUpdateDate
            ]


class Report(BusinessObject):
    
    NAME_SIZE = 255
    URL_SIZE = 255

    def __init__(self, myDb=None):
        self.reportName = StringAttribute("reportName")
        self.reportURL = StringAttribute("reportURL")
        self.reportID = IntegerAttribute("reportID")
        self.reportScheduleID = IntegerAttribute("reportScheduleID")
        self.reportCreateUser = IntegerAttribute("reportCreateUser")
        self.reportUpdateUser = IntegerAttribute("reportUpdateUser")
        self.reportCreateDate = DateAttribute("reportCreateDate")
        self.reportUpdateDate = DateAttribute("reportUpdateDate")
        super().__init__()
        super().setIdProperties(self.reportID)
        super().setTrackingAttributes(self.reportCreateUser,
                self.reportUpdateUser,
                self.reportCreateDate,
                self.reportUpdateDate)

        self.reportName.allowInvalID = False
        self.reportName.setHasMaximumLength(True)
        self.reportName.setAllSpacesAllowed(False)
        self.reportName.setNullStringAllowed(False)
        self.reportName.setNullAllowed(False)

        self.reportURL.allowInvalID = False
        self.reportURL.setHasMaximumLength(True)
        self.reportURL.setAllSpacesAllowed(False)
        self.reportURL.setNullStringAllowed(False)
        self.reportURL.setNullAllowed(False)
        
        self.reportScheduleID.allowInvalID = False
        self.reportScheduleID.setNullAllowed(False)
        self.reportScheduleID.setHasMinimum(True)
        self.reportScheduleID.setMinimum(0)

        self.reportName.setMaximumLength(Report.NAME_SIZE)
        self.reportURL.setMaximumLength(Report.URL_SIZE)
        self.myDb = myDb
        if myDb:
            self.fromDb()

    def isSameState(self, impl):
        result = super().isSameBaseState(impl)
        
        if result:
            s1 = self.getReportName()
            s2 = impl.getReportName()
            result = s1 == s2
        
        if result:
            s1 = self.getReportID()
            s2 = impl.getReportID()
            result = s1 == s2
        
        if result:
            result = self.getReportCreateDate() == impl.getReportCreateDate()
        
        if result:
            result = self.getReportUpdateDate() == impl.getReportUpdateDate()
        
        if result:
            s1 = self.getReportCreateUser()
            s2 = impl.getReportCreateUser()
            result = s1 == s2
        
        if result:
            s1 = self.getReportUpdateUser()
            s2 = impl.getReportUpdateUser()
            result = s1 == s2
        
        return result
    
    def getReportName(self):
        return self.reportName.getValue()
    
    def setReportName(self, newName):
        self.reportName.setValue(newName)
        if newName != None:
            self.setKey(newName)
        
    def getReportURL(self):
        return self.reportURL.getValue()
    
    def setReportURL(self, reportURL):
        self.reportURL.setValue(reportURL)
    
    def getDisplayString(self):
        return self.getReportName()

    def toString(self):
        return self.getDisplayString()
    
    def compareTo(self, o):
        result = -1
        if o == None:
            result = 1
        else:
            okey = o.getReportName()
            key = self.getReportName()
            if key == None and okey != None:
                result = -1
            elif key != None and okey == None:
                result = 1
            elif key == None and okey == None:
                result = 0
            else:
                result = Utils.compareStrings(key, okey)
        return result
    
    def getReportID(self):
        return self.reportID.getValue()
    
    def setReportID(self, reportID):
        self.reportID.setValue(reportID)
    
    def getID(self):
        return self.getReportID()

    def setID(self, oid):
        self.setReportID(oid)

    def getReportScheduleID(self):
        return self.reportScheduleID.getValue()
    
    def setReportScheduleID(self, reportScheduleID):
        self.reportScheduleID.setValue(reportScheduleID)
    
    def setDatabaseID(self, oid):
        self.setReportID(oid)   
        
    def setUpdateUser(self, oid):
        self.setReportUpdateUser(oid)
    
    def getUpdateDate(self):
        return self.getReportUpdateDate()
    
    def setCreateUser(self, oid):
        self.setReportCreateUser(oid)
    
    def setCreateDate(self, d):
        self.setReportCreateDate(d)
    
    def setUpdateDate(self, d):
        self.setReportUpdateDate(d)
    
    def getReportCreateDate(self):
        return self.reportCreateDate.getValue()
    
    def setReportCreateDate(self, reportCreateDate):
        self.reportCreateDate.setValue(reportCreateDate)
  
    def getReportUpdateDate(self):
        return self.reportUpdateDate.getValue()
    
    def setReportUpdateDate(self, reportUpdateDate):
        self.reportUpdateDate.setValue(reportUpdateDate)
    
    def getReportCreateUser(self):
        return self.reportCreateUser.getValue()
    
    def setReportCreateUser(self, reportCreateUser):
        self.reportCreateUser.setValue(reportCreateUser)
   
    def getReportUpdateUser(self):
        return self.reportUpdateUser.getValue()
    
    def setReportUpdateUser(self, reportUpdateUser):
        self.reportUpdateUser.setValue(reportUpdateUser)
    
    def getLastUpdateUser(self):
        return self.getReportUpdateUser()
    
    def getCreateUser(self):
        return self.getReportCreateUser()

    def __str__(self)->str:
        return self.toString()
    
    def toDb(self):
        for name, att in self.__dict__.items():
            a = att
            if isinstance(att, Attribute):
                a = att.value
            self.myDb.__dict__[name] = a
    
    def fromDb(self):
        for name, att in self.myDb.__dict__.items():
            if isinstance(att, bytes):
                att = att.decode()
            myAtt = self.__dict__.get(name)
            if not myAtt: 
                self.__dict__[name] = att
            else:
                if isinstance(myAtt, Attribute):
                    myAtt.value = att
                else:
                    myAtt = att
                self.__dict__[name] = myAtt

    def validate(self):
        result = True
        atts = self.getAttributeList()
        try:
            BusinessObject.validateAttributes(atts)
        except InvalidAttributeValueException as e:
            super().addMessage(e.getMsg())
            result = False
        return result
        
    def save(self):
        self.toDb()
        self.myDb.save()       
        self.fromDb()
  
    def remove(self):
            self.myDb.delete()
              
    def delete(self):
        self.myDb.deleteFlag = True
        self.myDb.save()
    
    def getAttributeList(self): 
        return [
            self.reportName,
            self.reportURL,
            self.reportID,
            self.reportScheduleID,
            self.reportCreateUser,
            self.reportUpdateUser,
            self.reportCreateDate,
            self.reportUpdateDate
        ]


class ScheduleEvent(BusinessObject):
    EVENT_NAME_SIZE = 60
    
    def __init__(self, myDb=None, org=None):
        self.eventID = IntegerAttribute("eventID")
        self.eventName = StringAttribute("eventName")
        self.eventDate = DateAttribute("eventDate")
        self.eventStartTime = StringAttribute('eventStartTime')
        self.accepted = BooleanAttribute('accepted')
        self.eventDuration = IntegerAttribute("eventDuration")
        self.eventCreateUser = IntegerAttribute("eventCreateUser")
        self.eventUpdateUser = IntegerAttribute("eventUpdateUser")
        self.eventCreateDate = DateAttribute("eventCreateDate")
        self.eventUpdateDate = DateAttribute("eventUpdateDate")
        self.organization = org
        self.location = None
        self.recurrence = None
        self.resources = []
        self.jobs = []
        self.schedule = None
        super().__init__()
        self.myDb = myDb
        if myDb:
            self.fromDb()
        super().setIdProperties(self.eventID)
        super().setTrackingAttributes(self.eventCreateUser,
                self.eventUpdateUser,
                self.eventCreateDate,
                self.eventUpdateDate)
        self.eventName.allowInvalID = False
        self.eventName.setAllSpacesAllowed(False)
        self.eventName.setNullStringAllowed(False)
        self.eventName.setNullAllowed(False)
        self.eventName.setHasMaximumLength(True)
        self.eventName.setMaximumLength(255)

        self.eventDate.allowInvalID = False
        self.eventDate.setNullAllowed(False)

        self.eventStartTime.allowInvalID = False
        self.eventStartTime.setAllSpacesAllowed(False)
        self.eventStartTime.setNullStringAllowed(False)
        self.eventStartTime.setNullAllowed(False)
        self.eventStartTime.setHasMaximumLength(True)
        self.eventStartTime.setMaximumLength(8)

        self.eventDuration.allowInvalID = False
        self.eventDuration.setNullAllowed(True)

    def clone(self, event):
        self.setEventName(event.getEventName())
        self.setEventDate(event.getEventDate())
        self.setEventStartTime(event.getEventStartTime())
        self.setEventDuration(event.getEventDuration())
        self.setLocation(event.getLocation())
        self.setAccepted(event.isAccepted())
        self.setOrganization(event.getOrganization())
        self.setEventCreateUser(event.getEventCreateUser())
        self.setEventUpdateUser(event.getEventUpdateUser())
        
    def setAccepted(self, val):
        self.accepted.setValue(val)
        
    def isAccepted(self):
        return self.accepted.getValue()
        
    def isSameState(self, impl):
        result = super().isSameBaseState(impl)
        if result:
            s1 = self.getEventName()
            s2 = impl.getEventName()
            result = s1 == s2
        if result:
            result = self.getEventDate() == impl.getEventDate()
        if result:
            s1 = self.getEventStartTime()
            s2 = impl.getEventStartTime()
            result = s1 == s2
        if result:
            s1 = self.getEventDuration()
            s2 = impl.getEventDuration()
            result = s1 == s2
        if result:
            result = self.getEventCreateDate() == impl.getEventCreateDate()
        if result:
            result = self.getEventUpdateDate() == impl.getEventUpdateDate()
        if result:
            s1 = self.getEventCreateUser()
            s2 = impl.getEventCreateUser()
            result = s1 == s2
        if result:
            s1 = self.getEventUpdateUser()
            s2 = impl.getEventUpdateUser()
            result = s1 == s2
        if result:
            li1 = self.getLocation()
            li2 = impl.getLocation()
            if li1 != None and li2 == None:
                result = False
            elif li1 == None and li2 != None:
                result = False
            elif li1 != None and li2 != None:
                result = li1.isSameState(li2)
        if result:
            er1 = self.getRecurrence()
            er2 = impl.getRecurrence()
            if er1 != None and er2 == None:
                result = False
            elif er1 == None and er2 != None:
                result = False
            elif er1 != None and er2 != None:
                result = er1.isSameState(er2)
        if result:
            result = Utils.compareCollections(self.getJobs(), impl.getJobs(), False)
        if result:
            oi1 = self.getOrganization(True)
            oi2 = impl.getOrganization(True)
            if oi1 != None and oi2 == None:
                result = False
            elif oi1 == None and oi2 != None:
                result = False
            elif oi1 != None and oi2 != None:
                result = oi1.isSameState(oi2)
        return result
    
    def getDisplayString(self):
        sb = 'EventID ' + str(self.getEventID()) + ' '
        nm = self.getEventName()
        if nm != None and len(nm) < ScheduleEvent.EVENT_NAME_SIZE:
            nm += VSBase.SPACE[0: ScheduleEvent.EVENT_NAME_SIZE - len(nm)]
        sb += str(nm)
        if self.getEventDate():
            sb += " "
            sb += self.getEventDate().strftime(VSBase.DATE_FMT)
        if self.getEventStartTime():
            sb += " at "
            sb += str(self.eventStartTime.getValue())
        if self.location:
            sb += " at location "
            sb += str(self.location.getName())
        return sb
    
    def getEventName(self):
        return self.eventName.getValue()
    
    def setEventName(self, newName):
        self.eventName.setValue(newName)
        
    def setEventDate(self, newDate):
        self.eventDate.setValue(newDate)
    
    def getEventDate(self):
        return self.eventDate.getValue()
     
    def setEventDuration(self, newDuration):
        self.eventDuration.setValue(newDuration)
    
    def getEventDuration(self):
        return self.eventDuration.getValue()
    
    def getJobs(self):
        return self.jobs
    
    def addJob(self, job):
        if job != None and isinstance(job, Job):
            self.jobs.append(job) 
        
    def removeJob(self, job):
        if job != None and isinstance(job, Job):
            try:
                self.jobs.remove(job)
            except ValueError:
                pass        
    
    def setOrganization(self, newOrganization):
        self.organization = newOrganization    
        
    def getOrganization(self, allowNone=False):
        if allowNone == False and self.organization == None:
            self.setOrganization(Organization())
        return self.organization
    
    def getEventID(self):
        return self.eventID.getValue()
    
    def setEventID(self, d):
        self.eventID.setValue(d)
    
    def getID(self):
        return self.getEventID()
    
    def setID(self, i):
        self.setEventID(i)
        
    def getEventCreateUser(self):
        return self.eventCreateUser.getValue()
    
    def setEventCreateUser(self, d):
        self.eventCreateUser.setValue(d)
    
    def getEventUpdateUser(self):
        return self.eventUpdateUser.getValue()
    
    def setEventUpdateUser(self, d):
        self.eventUpdateUser.setValue(d)
    
    def getEventCreateDate(self):
        return self.eventCreateDate.getValue()
    
    def setEventCreateDate(self, eventCreateDate):
        self.eventCreateDate.setValue(eventCreateDate)
    
    def getEventUpdateDate(self):
        return self.eventUpdateDate.getValue()
    
    def setEventUpdateDate(self, eventUpdateDate):
        self.eventUpdateDate.setValue(eventUpdateDate)
    
    def setUpdateUser(self, d):
        self.setEventUpdateUser(d)
    
    def getUpdateDate(self):
        return self.getEventUpdateDate()
    
    def setCreateUser(self, d):
        self.setEventCreateUser(d)
    
    def setCreateDate(self, dte):
        self.setEventCreateDate(dte)
    
    def setUpdateDate(self, dte):
        self.setEventUpdateDate(dte)

    def getLocation(self):
        return self.location
    
    def setLocation(self, loc):
        self.location = loc
        
    def getRecurrence(self):
        return self.recurrence
    
    def setRecurrence(self, recurrence):
        self.recurrence = recurrence
        
    def setResources(self, resources):
        self.resources = resources
        
    def getResources(self):
        return self.resources
    
    def addResource(self, resource):
        if resource:
            self.resources.append(resource)
        
    def removeResource(self, resource):
        if resource and self.resources.contains(resource):
            self.resources.remove(resource)
                 
    def getUnassignedJobs(self):
        result = []
        if self.getJobs():
            for job in self.getJobs():
                if not job.isAssigned():
                    result.append(job)
        return result
    
    def hasRequiredAndUnassigned(self):
        result = False
        for j in self.getUnassignedJobs():
            if j.getRequiredAndUnassigned():
                result = True
                break
        return result
    
    def addJobs(self, coll):
        if coll:
            self.jobs.extend(coll)
            
    def getEventStartTime(self):
        return self.eventStartTime.getValue()

    def setEventStartTime(self, time):
        if time and len(time) == 5:
            time += ":00"
        self.eventStartTime.setValue(time)
        
    def setJobs(self, coll):
        self.jobs = coll
        
    def getLastUpdateUser(self):
        return self.getEventUpdateUser()
    
    def getCreateUser(self):
        return self.getEventCreateUser()

    def __str__(self)->str:
        return self.getDisplayString()
    
    def toDb(self):
        for name, att in self.__dict__.items():
            a = att
            if isinstance(att, Attribute):
                a = att.value
            self.myDb.__dict__[name] = a
        if self.organization:
            self.myDb.organization = self.organization.myDb
            self.myDb.organization_ID = self.organization.myDb.organizationID
        if self.location:
            self.myDb.location = self.location.myDb
            self.myDb.location_ID = self.location.myDb.locationID
        if self.recurrence:
            self.myDb.recurrence = self.recurrence.myDb
            self.myDb.recurrence_ID = self.recurrence.myDb.recurrenceID
        if self.schedule:
            self.myDb.schedule = self.schedule.myDb
            self.myDb.schedule_ID = self.schedule.myDb.scheduleID
        if self.eventID.value:
            self.myDb.resources.clear()
            if self.resources:
                for r in self.resources:
                    self.myDb.resources.add(r.myDb)
            
    def fromDb(self):
        for name, att in self.myDb.__dict__.items():
            if isinstance(att, bytes):
                att = att.decode()
            myAtt = self.__dict__.get(name)
            if not myAtt: 
                self.__dict__[name] = att
            else:
                if isinstance(myAtt, Attribute):
                    myAtt.value = att
                else:
                    myAtt = att
                self.__dict__[name] = myAtt
        if self.myDb.organization_id:
            self.organization = Organization(self.myDb.organization)
        if self.myDb.location_id:
            self.location = Location(self.myDb.location)
        if self.myDb.recurrence_id:
            self.recurrence = EventRecurrence(self.myDb.recurrence)
        if self.myDb.schedule:
            self.schedule = Schedule(self.schedule)
        self.resources.clear()
        if self.myDb.eventID:
            if self.myDb.resources.all().first():
                for r in self.myDb.resources.all():
                    self.resources.append(Resource(r))

    def validate(self):
        try:
            super.validate()
            from vscode.calc.calc import EventValidator
            EventValidator().validate(self)
            result = True
            atts = self.getAttributeList()
            BusinessObject.validateAttributes(atts)
        except Exception as e:
            super().addMessage(e.getMsg())
            result = False
        return result
        
    def save(self):
        self.toDb()
        self.myDb.save()       
        self.fromDb()
  
    def remove(self):
            self.myDb.delete()
              
    def delete(self):
        self.myDb.deleteFlag = True
        self.myDb.save()
    
    def getAttributeList(self): 
        return [        
            self.eventID,
            self.eventName,
            self.eventDate,
            self.eventStartTime,
            self.eventDuration,
            self.eventCreateUser,
            self.eventUpdateUser,
            self.eventCreateDate,
            self.eventUpdateDate
        ]


class Schedule(BusinessObject):

    def __init__(self, org=None, myDb=None): 
        self.scheduleID = IntegerAttribute("scheduleID")
        self.scheduleStartDate = DateAttribute("scheduleStartDate")
        self.scheduleEndDate = DateAttribute("scheduleEndDate")
        self.scheduleCreateUser = IntegerAttribute("scheduleCreateUser")
        self.scheduleUpdateUser = IntegerAttribute("scheduleUpdateUser")
        self.scheduleCreateDate = DateAttribute("scheduleCreateDate")
        self.scheduleUpdateDate = DateAttribute("scheduleUpdateDate")
        self.accepted = BooleanAttribute('accepted')
        self.deleteFlag = BooleanAttribute('deleteFlag')
        self.buildResult = None
        self.scheduleStatus = None
        self.organization = None
        self.events = []
        super().__init__()
        if myDb:
            self.myDb = myDb
            self.fromDb()
        else:
            self.myDb = DbSchedule()
            self.toDb()
        self.organization = org
        self.accepted.value = False
        super().setIdProperties(self.scheduleID)
        super().setTrackingAttributes(self.scheduleCreateUser,
                self.scheduleUpdateUser,
                self.scheduleCreateDate,
                self.scheduleUpdateDate)

        self.scheduleStartDate.allowInvalID = False
        self.scheduleStartDate.setNullAllowed(False)

        self.scheduleEndDate.allowInvalID = False
        self.scheduleEndDate.setNullAllowed(False)
        self.setScheduleCreateDate(super().now())
        self.setScheduleUpdateDate(super().now())
        
    def getScheduleID(self):
        return self.scheduleID.getValue()
    
    def setScheduleID(self, oid):
        self.scheduleID.setValue(oid)
    
    def isSameState(self, impl):
        result = super().isSameBaseState(impl)
        
        if result:
            s1 = self.getScheduleID()
            s2 = impl.getScheduleID()
            result = s1 == s2
        
        if result:
            result = self.getScheduleStartDate() == impl.getScheduleStartDate()
        
        if result:
            result = self.getScheduleEndDate() == impl.getScheduleEndDate()
        
        if result:
            result = self.getScheduleCreateDate() == impl.getScheduleCreateDate()
        
        if result:
            result = self.getScheduleUpdateDate() == impl.getScheduleUpdateDate()
        
        if result:
            s1 = self.getScheduleCreateUser()
            s2 = impl.getScheduleCreateUser()
            result = s1 == s2
        
        if result:
            s1 = self.getScheduleUpdateUser()
            s2 = impl.getScheduleUpdateUser()
            result = s1 == s2
        
        if result:
            result = Utils.compareCollections(self.getEvents(), impl.getEvents())
        
        if result:
            oi1 = self.getOrganization(True)
            oi2 = impl.getOrganization(True)
            if oi1 != None and oi2 == None:
                result = False
            elif oi1 == None and oi2 != None:
                result = False
            elif oi1 != None and oi2 != None:
                result = oi1.isSameState(oi2)
        return result
    
    def isAfter(self, other):
        result = False
        if other:
            result = other.getScheduleEndDate() < self.getScheduleStartDate()
        return result
    
    def isBefore(self, other):
        result = False
        if other:
            result = self.getScheduleEndDate() < other.getScheduleStartDate()
        return result
    
    def overlaps(self, other):
        result = True
        if other:
            if other.getScheduleEndDate() < self.getScheduleStartDate():
                result = False
            elif other.getScheduleStartDate() > self.getScheduleEndDate():
                result = False
            elif self.getScheduleEndDate() < other.getScheduleStartDate():
                result = False
            elif self.getScheduleStartDate() > other.getScheduleEndDate():
                result = False
        else:
            result = False
        return result
    
    def getDisplayString(self):
        fmt = "%b %d, %Y"
        result = ''
        if self.getScheduleStartDate():
            result += "from "
            result += self.getScheduleStartDate().strftime(fmt)
        
        if self.getScheduleEndDate():
            result += " to " 
            result += self.getScheduleEndDate().strftime(fmt)
        if self.organization:
            result += '\n'            
            result += str(self.organization)
        return result
    
    def __str__(self):
        return self.getDisplayString()
    
    def accept(self, uid):
        self.accepted.value = True
        self.scheduleUpdateUser.value = uid
        self.scheduleUpdateDate.value = DT.now()
        
    def isAccepted(self):
        return self.accepted.value
        
    def setOrganization(self, newOrganization):
        self.organization = newOrganization
    
    def getOrganization(self, allowNone=False):
        if allowNone == False and not self.organization:
            dbo = DbOrganization()
            self.setOrganization(Organization(dbo))
        return self.organization
    
    def getScheduleStartDate(self):
        return  self.scheduleStartDate.getValue()

    def setScheduleStartDate(self, newStartDate):
        self.scheduleStartDate.setValue(newStartDate)

    def setScheduleEndDate(self, newEndDate):
        self.scheduleEndDate.setValue(newEndDate)
    
    def getScheduleEndDate(self):
        return self.scheduleEndDate.getValue()
        
    def getEvents(self):
        return self.events
    
    def setEvents(self, coll):
        self.events = coll
    
    def addEvent(self, evt):
        if evt and isinstance(evt, ScheduleEvent):
            if not self.events.contains(evt):
                self.events.append(evt)
            
    def removeEvent(self, evt):
        result = True
        if not self.events.contains(evt):
            result = False
        else:
            self.events.remove(evt)
        return result
    
    def getScheduleID(self):
        return self.scheduleID.getValue()
    
    def setScheduleID(self, d):
        self.scheduleID.setValue(d)
    
    def getID(self):
        return self.getScheduleID()
    
    def setID(self, d):
        self.setScheduleID(d)

    def setDatabaseID(self, d):
        self.setScheduleID(d)

    def setUpdateUser(self, d):
        self.setScheduleUpdateUser(d)
    
    def getUpdateDate(self):
        return self.getScheduleUpdateDate()
    
    def setCreateUser(self, d):
        self.setScheduleCreateUser(d)
    
    def setCreateDate(self, d):
        self.setScheduleCreateDate(d)
    
    def setUpdateDate(self, d):
        self.setScheduleUpdateDate(d)
    
    def getScheduleCreateDate(self):
        return self.scheduleCreateDate.getValue()
    
    def setScheduleCreateDate(self, scheduleCreateDate):
        self.scheduleCreateDate.setValue(scheduleCreateDate)
    
    def getScheduleUpdateDate(self):
        return self.scheduleUpdateDate.getValue()
    
    def setScheduleUpdateDate(self, scheduleUpdateDate):
        self.scheduleUpdateDate.setValue(scheduleUpdateDate)
    
    def getScheduleCreateUser(self):
        return self.scheduleCreateUser.getValue()
    
    def setScheduleCreateUser(self, scheduleCreateUser):
        self.scheduleCreateUser.setValue(scheduleCreateUser)
    
    def getScheduleUpdateUser(self):
        return self.scheduleUpdateUser.getValue()
      
    def setScheduleUpdateUser(self, scheduleUpdateUser):
        self.scheduleUpdateUser.setValue(scheduleUpdateUser)
    
    def isBuildValid(self):
        result = False
        if not self.buildResult:
            result = True 
        else: 
            result = self.buildResult.isValid()
        return result

    def getBuildResult(self):
        return self.buildResult
    
    def setBuildResult(self, buildResult):
        self.buildResult = buildResult
    
    def getLastUpdateUser(self):
        return self.getScheduleUpdateUser()
    
    def getCreateUser(self):
        return self.getScheduleCreateUser()
    
    def getScheduleStatus(self):
        return self.scheduleStatus

    def setScheduleStatus(self, ss):
        self.scheduleStatus = ss
        
    def canAcceptOrReject(self):
        stat = self.scheduleStatus.getScheduleStatusKey()
        return stat != ScheduleStatus.ACCEPTED \
            and stat != ScheduleStatus.REJECTED
    
    def validateAccept(self):
        if not self.canAcceptOrReject():
            raise PersistenceException()
        
    def validateReject(self):
        if not self.canAcceptOrReject():
            raise PersistenceException()
        
    def delete(self):
        from vscode.calc.calc import EventRejecter
        #print('enter delete() ' + self.__class__.__name__)
        loginID = self.getLastUpdateUser()
        #print('after getLastUpdateUser() ' + self.__class__.__name__)
        EventRejecter(self, loginId).rejectEvents()
        #print('after EventRejecter() ' + self.__class__.__name__)
        self.flagDeleted()
        #print('after flagDeleted() ' + self.__class__.__name__)
        '''key = self.getScheduleStatus().getScheduleStatisKey()
        if key == ScheduleStatus.ACCEPTED:
            for sei in self.events:
                sei.setEventUpdateUser(loginId)
                sei.delete()
        why?
        '''
    def toDb(self):
        for name, att in self.__dict__.items():
            a = att
            if isinstance(att, Attribute):
                a = att.value
            self.myDb.__dict__[name] = a
        if self.organization:
            if isinstance(self.organization, Organization):
                self.myDb.organization = self.organization.myDb
        if self.scheduleStatus:
            self.myDb.scheduleStatus = self.scheduleStatus.myDb
        if self.events and len(self.events) > 0:
            self.myDb.events.clear()
            for evt in self.events:
                self.myDb.events.add(evt.myDb);
    
    def fromDb(self):
        for name, att in self.myDb.__dict__.items():
            if isinstance(att, bytes):
                att = att.decode()
            myAtt = self.__dict__.get(name)
            if not myAtt: 
                self.__dict__[name] = att
            else:
                if isinstance(myAtt, Attribute):
                    myAtt.value = att
                else:
                    myAtt = att
                self.__dict__[name] = myAtt
            if self.myDb.organization:
                self.organization = Organization(self.myDb.organization)
            if self.myDb.scheduleStatus:
                self.scheduleStatus = ScheduleStatus(self.myDb.scheduleStatus)
            self.events.clear()
            if self.myDb.events and self.myDb.events.exists() > 0:
                for evt in self.myDb.events.all():
                    self.events.append(ScheduleEvent(evt))

    def validate(self):
        result = True
        atts = self.getAttributeList()
        try:
            BusinessObject.validateAttributes(atts)
        except InvalidAttributeValueException as e:
            super().addMessage(e.getMsg())
            result = False
        
        if self.scheduleEndDate.endsBefore(self.scheduleStartDate):
            super().addMessage(VSMessageFactory.getDateSequenceError(
                    MessageSeverity.WARNING,
                    self.getScheduleStartDate(),
                    self.getScheduleEndDate()))
            result = False
        return result
        
    def save(self):
        self.toDb()
        #print('after toDb() ' + self.__class__.__name__)
        #print('self: ' + str(self) + ':')
        #print('myDb ' + str(self.myDb))
        self.myDb.save() 
        #print('after save() ' + self.__class__.__name__)      
        self.fromDb()
        #print('after fromDb() ' + self.__class__.__name__)
  
    def remove(self):
            self.myDb.delete()
              
    def flagDeleted(self):
        #print('enter flagDeleted() ' + self.__class__.__name__)
        self.deleteFlag.value = True
        if self.organization:
            #print('org: ' + str(self.organization))
            self.organization.save()
        self.save()
    
    def getAttributeList(self): 
        return [    
                self.scheduleID,
                self.scheduleStartDate,
                self.scheduleEndDate,
                self.scheduleCreateUser,
                self.scheduleUpdateUser,
                self.scheduleCreateDate,
                self.scheduleUpdateDate         
        ]


class VolunteerSkill(BusinessObject):

    def __init__(self, myDb=None, volunteer=None, skill=None):
        self.volunteerSkillID = IntegerAttribute("volunteerSkillID")
        self.vsExpert = BooleanAttribute("vsExpert")
        self.vsLastAssignment = DateAttribute("vsLastAssignment")
        self.vsPreviousAssignment = DateAttribute("vsPreviousAssignment")
        self.vsCreateUser = IntegerAttribute("vsCreateUser")
        self.vsUpdateUser = IntegerAttribute("vsUpdateUser")
        self.vsCreateDate = DateAttribute("vsCreateDate")
        self.vsUpdateDate = DateAttribute("vsUpdateDate")
        self.volunteer = volunteer
        self.skill = skill
        self.myDb = myDb
        if myDb:
            self.fromDb()
        super().__init__()
        super().setIdProperties(self.volunteerSkillID)
        super().setTrackingAttributes(self.vsCreateUser,
                self.vsUpdateUser,
                self.vsCreateDate,
                self.vsUpdateDate)

        self.vsExpert.allowInvalID = False
        self.vsExpert.setNullAllowed(False)
        self.vsExpert.setValue(False)
        
        self.vsLastAssignment.allowInvalID = False
        self.vsLastAssignment.setNullAllowed(True)

        self.vsPreviousAssignment.allowInvalID = False
        self.vsPreviousAssignment.setNullAllowed(True)
    
    def isSameState(self, impl):
        result = super().isSameBaseState(impl)
        
        vi1 = self.getVolunteer()
        vi2 = impl.getVolunteer()
        if vi1 != None and vi2 == None:
            result = False
        elif vi1 == None and vi2 != None:
            result = False
        elif vi1 != None and vi2 != None:
            result = vi1.isSameState(vi2)
        
        si1 = self.getSkill()
        si2 = impl.getSkill()
        if si1 != None and si2 == None:
            result = False
        elif si1 == None and si2 != None:
            result = False
        elif si1 != None and si2 != None:
            result = si1.isSameState(si2)
        if result:
            s1 = self.getVolunteerSkillID()
            s2 = impl.getVolunteerSkillID()
            result = s1 == s2
        if result:
            s1 = self.isExpert()
            s2 = impl.isExpert()
            result = s1 == s2
        if result:
            result = self.getLastAssignment() == impl.getLastAssignment()
        if result:
            result = self.getPreviousAssignment() == impl.getPreviousAssignment()
        if result:
            result = self.getVsCreateDate() == impl.getVsCreateDate()
        if result:
            result = self.getVsUpdateDate() == impl.getVsUpdateDate()
        if result:
            s1 = self.getVsCreateUser()
            s2 = impl.getVsCreateUser()
            result = s1 == s2
        if result:
            s1 = self.getVsUpdateUser()
            s2 = impl.getVsUpdateUser()
            result = s1 == s2
        return result
    
    def getDisplayString(self):
        result = "id: " + str(self.getVolunteerSkillID()) + ' '
        if self.volunteer:
            result += str(self.volunteer)
            result += " "
        if self.skill:
            if self.vsExpert.value:       
                result += "expert " 
            else:
                result += "       "
            result += self.skill.getDisplayString()
            result += " "
        return result
    
    def __str__(self):
        return self.getDisplayString()

    def getSkill(self):
        return self.skill
    
    def setSkill(self, skill):
        self.skill = skill

    def getVolunteer(self):
        return self.volunteer
    
    def setVolunteer(self, volunteer):
        self.volunteer = volunteer

    def isExpert(self):
        return self.vsExpert.getValue()
    
    def getVsExpert(self):
        return self.vsExpert.getValue()
    
    def setVsExpert(self, vsExpert):
        self.vsExpert.setValue(vsExpert)
    
    def compareTo(self, o):
        result = -1
        if not o:
            result = 1
        elif isinstance(o, VolunteerSkill):
            result = super().compareString(self.getSkill().getSkillName(), o.getSkill().getSkillName())
        else:
            raise ClassCastException("Object " + str(o) + " is not an instance of VolunteerSkill")
        return result
    
    def setVsLastAssignment(self, dat):
        self.vsLastAssignment.setValue(dat)
  
    def getVsLastAssignment(self):
        return self.vsLastAssignment.getValue()
   
    def getLastAssignment(self):
        return self.getVsLastAssignment()
    
    def setLastAssignment(self, dat):
        self.setVsLastAssignment(dat)
    
    def setVsPreviousAssignment(self, dat):
        self.vsPreviousAssignment.setValue(dat)
            
    def getVsPreviousAssignment(self):
        return self.vsPreviousAssignment.getValue()
    
    def getPreviousAssignment(self):
        return self.getVsPreviousAssignment()
    
    def setPreviousAssignment(self, dat):
        self.setVsPreviousAssignment(dat)
    
    def setExpert(self, expert):
        self.setVsExpert(expert)
    
    def getVolunteerSkillID(self):
        return self.volunteerSkillID.getValue()
   
    def setVolunteerSkillID(self, d):
        self.volunteerSkillID.setValue(d)
    
    def getID(self):
        return self.getVolunteerSkillID()

    def setID(self, d):
        self.setVolunteerSkillID(d)

    def getLastAssigmentString(self):
        result = ''
        dte = self.getVsLastAssignment()
        if dte:
            result = dte.strftime(VSBase.DATE_FMT_SLASH)
        return result
    
    def getPreviousAssigmentString(self):
        result = ''
        dte = self.getVsPreviousAssignment()
        if dte:
            result = dte.strftime(VSBase.DATE_FMT_SLASH)
        return result
    
    def setUpdateUser(self, d):
        self.setVsUpdateUser(d)
    
    def getUpdateDate(self):
        return self.getVsUpdateDate()
    
    def setCreateUser(self, d):
        self.setVsCreateUser(d)
    
    def setCreateDate(self, date):
        self.setVsCreateDate(date)
    
    def setUpdateDate(self, dte):
        self.setVsUpdateDate(dte)
    
    def getVsCreateDate(self):
        return self.vsCreateDate.getValue()
    
    def setVsCreateDate(self, vsCreateDate):
        self.vsCreateDate.setValue(vsCreateDate)
    
    def getVsUpdateDate(self):
        return self.vsUpdateDate.getValue()
    
    def setVsUpdateDate(self, vsUpdateDate):
        self.vsUpdateDate.setValue(vsUpdateDate)
    
    def getVsCreateUser(self):
        return self.vsCreateUser.getValue()
    
    def setVsCreateUser(self, vsCreateUser):
        self.vsCreateUser.setValue(vsCreateUser)
    
    def getVsUpdateUser(self):
        return self.vsUpdateUser.getValue()
    
    def setVsUpdateUser(self, vsUpdateUser):
        self.vsUpdateUser.setValue(vsUpdateUser)
    
    def getLastUpdateUser(self):
        return self.getVsUpdateUser()
    
    def getCreateUser(self):
        return self.getVsCreateUser()
    
    def toDb(self):
        for name, att in self.__dict__.items():
            a = att
            if isinstance(att, Attribute):
                a = att.value
            self.myDb.__dict__[name] = a
        if self.volunteer:
            self.myDb.volunteer = self.volunteer.myDb
        if self.skill:
            self.myDb.skill = self.skill.myDb
        
    def fromDb(self):
        of = ObjectFactory()
        for name, att in self.myDb.__dict__.items():
            if isinstance(att, bytes):
                att = att.decode()
            myAtt = self.__dict__.get(name)
            if not myAtt: 
                self.__dict__[name] = att
            else:
                if isinstance(myAtt, Attribute):
                    myAtt.value = att
                else:
                    myAtt = att
                self.__dict__[name] = myAtt
        if self.myDb.volunteer:
            #print('got vol ' + str(self.myDb.volunteer))
            self.volunteer = Volunteer(self.myDb.volunteer)
            if not self.volunteer.myDb:
                self.volunteer.myDb = self.myDb.volunteer
        elif self.myDb.volunteer_id:
            #print('got volunteer_id')
            self.volunteer = of.getVolunteer(self.myDb.volunteer_id)
        #print(self.volunteer.myDb)
        if self.myDb.skill:
            self.skill = Skill(self.myDb.skill)

    def validate(self):
        result = True
        atts = self.getAttributeList()
        try:
            BusinessObject.validateAttributes(atts)
        except InvalidAttributeValueException as e:
            super().addMessage(e.getMsg())
            result = False
        return result
        
    def save(self):
        self.toDb()
        self.myDb.save()       
        self.fromDb()
  
    def remove(self):
            self.myDb.delete()
              
    def delete(self):
        self.myDb.deleteFlag = True
        self.myDb.save()
    
    def getAttributeList(self): 
        return [    
            self.volunteerSkillID,
            self.vsExpert,
            self.vsLastAssignment,
            self.vsPreviousAssignment,
            self.vsCreateUser,
            self.vsUpdateUser,
            self.vsCreateDate,
            self.vsUpdateDate
            ]
        

class VolunteerSkillAssignment(BusinessObject):
    
    def __init__(self, myDb=None):
        
        self.volunteerSkillAssignmentID = IntegerAttribute("volunteerSkillAssignmentID")
        self.assignmentDate = DateAttribute("assignmentDate")
        self.vsaCreateUser = IntegerAttribute("vsaCreateUser")
        self.vsaUpdateUser = IntegerAttribute("vsaUpdateUser")
        self.vsaCreateDate = DateAttribute("vsaCreateDate")
        self.vsaUpdateDate = DateAttribute("vsaUpdateDate")
        self.description = None
        super().__init__()
        self.myDb = myDb
        if myDb:
            self.fromDb()
        super().setIdProperties(self.volunteerSkillAssignmentID)
        super().setTrackingAttributes(self.vsaCreateUser,
                self.vsaUpdateUser,
                self.vsaCreateDate,
                self.vsaUpdateDate)

        self.assignmentDate.allowInvalID = False
        self.assignmentDate.setNullAllowed(True)
    
    def isSameState(self, impl):
        result = super().isSameBaseState(self, impl)
        if result:
            result = self.getAssignmentDate() == impl.getAssignmentDate()
        if result:
            s1 = self.getVolunteerSkillAssignmentID()
            s2 = impl.getVolunteerSkillAssignmentID()
            result = s1 == s2
        if result:
            result = self.getVsaCreateDate() == impl.getVsaCreateDate()
        if result:
            result = self.getVsaUpdateDate() == impl.getVsaUpdateDate()
        if result:
            s1 = self.getVsaCreateUser()
            s2 = impl.getVsaCreateUser()
            result = s1 == s2
        if result:
            s1 = self.getVsaUpdateUser()
            s2 = impl.getVsaUpdateUser()
            result = s1 == s2
        return result
    
    def setDatabaseID(self, i):
        self.setVolunteerSkillAssignmentID(i)
    
    def getDisplayString(self):
        return "VolunteerSkillAssignment{" + \
                "volunteerSkillAssignmentID=" + \
                str(self.volunteerSkillAssignmentID.value) + \
                     ", assignmentDate=" + \
               self.assignmentDate.value.strfmt('%m/%d/%Y') 
    
    def getVolunteerSkillAssignmentID(self):
        return self.volunteerSkillAssignmentID.value
    
    def setVolunteerSkillAssignmentID(self, i):
        self.volunteerSkillAssignmentID.setValue(i)
    
    def getID(self):
        return self.getVolunteerSkillAssignmentID()
    
    def setID(self, d):
        self.setVolunteerSkillAssignmentID(d)
        
    def getAssignmentDate(self):
        return self.assignmentDate
    
    def setAssignmentDate(self, assignmentDate):
        self.assignmentDate.setValue(assignmentDate)
    
    def setUpdateUser(self, d):
        self.setVsaUpdateUser(d)
    
    def getUpdateDate(self):
        return self.getVsaUpdateDate()
    
    def setCreateUser(self, d):
        self.setVsaCreateUser(d)
    
    def setCreateDate(self, d):
        self.setVsaCreateDate(d)
    
    def setUpdateDate(self, d):
        self.setVsaUpdateDate(d)
    
    def getVsaCreateDate(self):
        return self.vsaCreateDate.getValue()
    
    def setVsaCreateDate(self, vsaCreateDate):
        self.vsaCreateDate.setValue(vsaCreateDate)
    
    def getVsaUpdateDate(self):
        return self.vsaUpdateDate.getValue()
    
    def getVsaCreateUser(self):
        return self.vsaCreateUser.getValue()
    
    def getVsaUpdateUser(self):
        return self.vsaUpdateUser.getValue()
    
    def setVsaUpdateUser(self, vsaUpdateUser):
        self.vsaUpdateUser.setValue(vsaUpdateUser)
    
    def getLastUpdateUser(self):
        return self.getVsaUpdateUser()

    def getCreateUser(self):
        return self.getVsaCreateUser()
        
    def toString(self):
        return self.getDisplayString()
        
    def __str__(self):
        return self.toString()
    
    def toDb(self):
        for name, att in self.__dict__.items():
            a = att
            if isinstance(att, Attribute):
                a = att.value
            self.myDb.__dict__[name] = a
    
    def fromDb(self):
        for name, att in self.myDb.__dict__.items():
            if isinstance(att, bytes):
                att = att.decode()
            myAtt = self.__dict__.get(name)
            if not myAtt: 
                self.__dict__[name] = att
            else:
                if isinstance(myAtt, Attribute):
                    myAtt.value = att
                else:
                    myAtt = att
                self.__dict__[name] = myAtt

    def validate(self):
        result = True
        atts = self.getAttributeList()
        try:
            BusinessObject.validateAttributes(atts)
        except InvalidAttributeValueException as e:
            super().addMessage(e.getMsg())
            result = False
        return result
        
    def save(self):
        self.toDb()
        self.myDb.save()       
        self.fromDb()
  
    def remove(self):
            self.myDb.delete()
              
    def delete(self):
        self.myDb.deleteFlag = True
        self.myDb.save()
    
    def getAttributeList(self): 
        return [    
                self.volunteerSkillAssignmentID,
                self.vsaVolunteerSkillID,
                self.vsaEventID,
                self.assignmentDate,
                self.vsaCreateUser,
                self.vsaUpdateUser,
                self.vsaCreateDate,
                self.vsaUpdateDate,
                self.resourceUpdateDate
        ]


class EventPreference(BusinessObject):

    def __init__(self, myDb=None):
        self.preferenceID = IntegerAttribute("preferenceID")
        self.required = BooleanAttribute("required")
        self.preferenceCreateUser = IntegerAttribute("preferenceCreateUser")
        self.preferenceUpdateUser = IntegerAttribute("preferenceUpdateUser")
        self.preferenceCreateDate = DateAttribute("preferenceCreateDate")
        self.preferenceUpdateDate = DateAttribute("preferenceUpdateDate")
        self.volunteer = None
        self.event = None
        self.myDb = myDb
        if myDb:
            self.fromDb()
        super().__init__()
        super().setIdProperties(self.preferenceID)
        super().setTrackingAttributes(self.preferenceCreateUser,
                self.preferenceUpdateUser,
                self.preferenceCreateDate,
                self.preferenceUpdateDate)


        self.required.allowInvalID = False
        self.required.setNullAllowed(False)
        self.required.setValue(False)
    
    def isSameState(self, impl):
        result = isinstance(impl, EventPreference) and super().isSameBaseState(impl)
        if result:
            s1 = self.getPreferenceVolunteerID()
            s2 = impl.getPreferenceVolunteerID()
            result = s1 == s2
        if result:
            s1 = self.getPreferenceEventID()
            s2 = impl.getPreferenceEventID()
            result = s1 == s2
        if result:
            s1 = self.getPreferenceVolunteerID()
            s2 = impl.getPreferenceVolunteerID()
            result = s1 == s2
        if result:
            result = self.getPreferenceCreateDate() == impl.getPreferenceCreateDate()
        if result:
            result = self.getPreferenceUpdateDate() == impl.getPreferenceUpdateDate()
        if result:
            s1 = self.getPreferenceCreateUser()
            s2 = impl.getPreferenceCreateUser()
            result = s1 == s2
        if result:
            s1 = self.getPreferenceUpdateUser()
            s2 = impl.getPreferenceUpdateUser()
            result = s1 == s2
        return result
    
    def getDisplayString(self):
        sb = ''
        if self.volunteer:
            if self.volunteer.getVolunteerFirstName():
                sb += self.volunteer.getVolunteerFirstName()
                sb += " "
            
            if self.volunteer.getVolunteerLastName():
                sb += self.volunteer.getVolunteerLastName()
                sb += " "        
        if  self.event:
            if self.event.getEventName():
                sb += self.event.getEventName()
        return sb

    def setDatabaseID(self, d):
        self.setPreferenceID(d)
        
    def getPreferenceID(self):
        return self.preferenceID.getValue()
    
    def setPreferenceID(self, preferenceID):
        self.preferenceID.setValue(preferenceID)
    
    def setID(self, d):
        self.setPreferenceID(d)
        
    def getID(self):
        return self.getPreferenceID()
    
    def setUpdateUser(self, d):
        self.setPreferenceUpdateUser(d)
    
    def getUpdateDate(self):
        return self.getPreferenceUpdateDate()
    
    def setCreateUser(self, d):
        self.setPreferenceCreateUser(d)
    
    def setCreateDate(self, d):
        self.setPreferenceCreateDate(d)
    
    def setUpdateDate(self, d):
        self.setPreferenceUpdateDate(d)
    
    def getPreferenceCreateDate(self):
        return self.preferenceCreateDate.getValue()
    
    def setPreferenceCreateDate(self, preferenceCreateDate):
        self.preferenceCreateDate.setValue(preferenceCreateDate)
    
    def getPreferenceUpdateDate(self):
        return self.preferenceUpdateDate.getValue()
    
    def setPreferenceUpdateDate(self, preferenceUpdateDate):
        self.preferenceUpdateDate.setValue(preferenceUpdateDate)
    
    def getPreferenceCreateUser(self):
        return self.preferenceCreateUser.getValue()
    
    def setPreferenceCreateUser(self, preferenceCreateUser):
        self.preferenceCreateUser.setValue(preferenceCreateUser)
    
    def getPreferenceUpdateUser(self):
        return self.preferenceUpdateUser.getValue()
    
    def setPreferenceUpdateUser(self, preferenceUpdateUser):
        self.preferenceUpdateUser.setValue(preferenceUpdateUser)
    
    def getVolunteer(self):
        return self.volunteer
    
    def setVolunteer(self, vol):
        self.volunteer = vol
        
    def getEvent(self):
        return self.event
    
    def setEvent(self, event):
        self.event = event
        
    def getRequired(self):
        return self.isRequired()
    
    def isRequired(self):
        return self.required.getValue()
    
    def setRequired(self, required):
        required.setValue(required)
         
    def getLastUpdateUser(self):
        return self.getPreferenceUpdateUser()
    
    def getCreateUser(self):
        return self.getPreferenceCreateUse9r()
    
    def toString(self):
        return self.getDisplayString()
    
    def __str__(self)->str:
        return self.toString()
    
    def toDb(self):
        for name, att in self.__dict__.items():
            a = att
            if isinstance(att, Attribute):
                a = att.value
            self.myDb.__dict__[name] = a
    
        if self.volunteer:
            self.myDb.volunteer = self.volunteer.myDb
        if self.event:
            self.myDb.event = self.event.myDb
            
    def fromDb(self):
        for name, att in self.myDb.__dict__.items():
            if isinstance(att, bytes):
                att = att.decode()
            myAtt = self.__dict__.get(name)
            if not myAtt: 
                self.__dict__[name] = att
            else:
                if isinstance(myAtt, Attribute):
                    myAtt.value = att
                else:
                    myAtt = att
                self.__dict__[name] = myAtt
        if self.myDb.volunteer_id:
            self.setVolunteer(Volunteer(self.myDb.volunteer))
        if self.myDb.event_id:
            self.setEvent(ScheduleEvent(self.myDb.event))

    def validate(self):
        result = True
        atts = self.getAttributeList()
        try:
            BusinessObject.validateAttributes(atts)
        except InvalidAttributeValueException as e:
            super().addMessage(e.getMsg())
            result = False
        return result
        
    def save(self):
        self.toDb()
        self.myDb.save()       
        self.fromDb()
  
    def remove(self):
            self.myDb.delete()
              
    def delete(self):
        self.myDb.deleteFlag = True
        self.myDb.save()
    
    def getAttributeList(self): 
        return [    
                 self.preferenceID,
                self.required,
                self.preferenceCreateUser,
                self.preferenceUpdateUser,
                self.preferenceCreateDate,
                self.preferenceUpdateDate
        ]


class EventRecurrence(BusinessObject):
    

    INTERVAL_MINIMUM = 1

    def __init__(self, myDb=None):    
        self.endDate = DateAttribute("endDate")
        self.startDate = DateAttribute("startDate")
        self.recurrenceID = IntegerAttribute("recurrenceID")
        self.intervalAmount = IntegerAttribute("intervalAmount")
        self.recurrenceCreateUser = IntegerAttribute("recurrenceCreateUser")
        self.recurrenceUpdateUser = IntegerAttribute("recurrenceUpdateUser")
        self.recurrenceCreateDate = DateAttribute("recurrenceCreateDate")
        self.recurrenceUpdateDate = DateAttribute("recurrenceUpdateDate")
        self.completelyBuilt = BooleanAttribute("completelyBuilt")
        self.recurrenceType = None
        super().__init__()
        self.myDb = myDb
        if myDb:
            self.fromDb()
        super().setIdProperties(self.recurrenceID)
        super().setTrackingAttributes(self.recurrenceCreateUser,
                self.recurrenceUpdateUser,
                self.recurrenceCreateDate,
                self.recurrenceUpdateDate)

        self.endDate.allowInvalID = False
        self.endDate.setNullAllowed(True)

        self.startDate.allowInvalID = False
        self.startDate.setNullAllowed(False)

        self.intervalAmount.allowInvalID = False
        self.intervalAmount.setNullAllowed(False)
        self.intervalAmount.setHasMinimum(True)
        self.intervalAmount.setMinimum(EventRecurrence.INTERVAL_MINIMUM)
        
    def isSameState(self, impl):
        result = super().isSameBaseState(impl)
        if result:
            result = self.getStartDate() == impl.getStartDate()
        if result:
            result = self.getEndDate() == impl.getEndDate()
        if result:
            s1 = self.isCompletelyBuilt()
            s2 = impl.isCompletelyBuilt()
            result = s1 == s2
        if result:
            s1 = self.getIntervalAmount()
            s2 = impl.getIntervalAmount()
            result = s1 == s2
        if result:
            s1 = self.getRecurrenceID()
            s2 = impl.getRecurrenceID()
            result = s1 == s2
        if result:
            s1 = self.getTypeID()
            s2 = impl.getTypeID()
            result = s1 == s2
        if result:
            result = self.getRecurrenceCreateDate() == impl.getRecurrenceCreateDate()
        if result:
            result = self.getRecurrenceUpdateDate() == impl.getRecurrenceUpdateDate()
        if result:
            s1 = self.getRecurrenceCreateUser()
            s2 = impl.getRecurrenceCreateUser()
            result = s1 == s2
        if result:
            s1 = self.getRecurrenceUpdateUser()
            s2 = impl.getRecurrenceUpdateUser()
            result = s1 == s2
        return result
    
    def getDisplayString(self):
        sb = str(RecurrenceType.getRecurrenceTypeNameForId(self.getTypeID()))
        if self.startDate != None and self.startDate.getValue() != None:
            sb += " from "
            sb += self.startDate.getValue().strftime(VSBase.DATE_FMT)
        
        if self.endDate != None and self.endDate.getValue() != None:
            sb += " to "
            sb += self.endDate.getValue().strftime(VSBase.DATE_FMT)
        sb += ' id: '
        sb += str(self.recurrenceID)
        return sb

    def getRecurrenceID(self):
        return self.recurrenceID.value
    
    def setRecurrenceID(self, recurrenceID):
        self.recurrenceID.setValue(recurrenceID)
    
    def setID(self, d):
        self.setRecurrenceID(d)

    def getID(self):
        return self.getRecurrenceID()

    def getIntervalAmount(self):
        return self.intervalAmount.getValue()
    
    def setIntervalAmount(self, amt):
        self.intervalAmount.setValue(amt)
    
    def getStartDate(self):
        return self.startDate.value
    
    def setStartDate(self, startDate):
        self.startDate.setValue(startDate)
    
    def setStart(self, recurrenceCreateDate):
        self.startDate.setValue(recurrenceCreateDate)
    
    def getEndDate(self):
        return self.endDate.getValue()

    def setEndDate(self, endDate):
        self.endDate.setValue(endDate)
    
    def setEnd(self, endDate):
        self.endDate.setValue(endDate)
    
    def setUpdateUser(self, d):
        self.setRecurrenceUpdateUser(d)
    
    def getUpdateDate(self):
        return self.getRecurrenceUpdateDate()
    
    def setCreateUser(self, d):
        self.setRecurrenceCreateUser(d)
    
    def setCreateDate(self, d):
        self.setRecurrenceCreateDate(d)
    
    def setUpdateDate(self, d):
        self.setRecurrenceUpdateDate(d)
    
    def getRecurrenceCreateDate(self):
        return self.recurrenceCreateDate.getValue()
    
    def setRecurrenceCreateDate(self, recurrenceCreateDate):
        self.recurrenceCreateDate.setValue(recurrenceCreateDate)
    
    def getRecurrenceUpdateDate(self):
        return self.recurrenceUpdateDate.getValue()
    
    def setRecurrenceUpdateDate(self, recurrenceUpdateDate):
        self.recurrenceUpdateDate.setValue(recurrenceUpdateDate)
  
    def getRecurrenceCreateUser(self):
        return self.recurrenceCreateUser.getValue()
    
    def setRecurrenceCreateUser(self, recurrenceCreateUser):
        self.recurrenceCreateUser.setValue(recurrenceCreateUser)
    
    def getRecurrenceUpdateUser(self):
        return self.recurrenceUpdateUser.getValue()
    
    def setRecurrenceUpdateUser(self, recurrenceUpdateUser):
        self.recurrenceUpdateUser.setValue(recurrenceUpdateUser)
    
    def getCompletelyBuilt(self):
        return self.completelyBuilt.getValue()

    def  setCompletelyBuilt(self, completelyBuilt):
        self.completelyBuilt.setValue(completelyBuilt)
    
    def isCompletelyBuilt(self):
        return self.completelyBuilt.getValue()
     
    def getLastUpdateUser(self):
        return self.getRecurrenceUpdateUser()

    def getCreateUser(self):
        return self.getRecurrenceCreateUser()
    
    def getRecurrenceType(self):
        return self.recurrenceType
    
    def setRecurrenceType(self, obj):
        self.recurrenceType = obj
    
    def __str__(self)->str:
        return self.getDisplayString()
    
    def toDb(self):
        for name, att in self.__dict__.items():
            a = att
            if isinstance(att, Attribute):
                a = att.value
            self.myDb.__dict__[name] = a
        if self.recurrenceType:
            self.myDb.recurrenceType_ID = self.recurrenceType.getRecurrenceTypeID()
            
    def fromDb(self):
        for name, att in self.myDb.__dict__.items():
            if isinstance(att, bytes):
                att = att.decode()
            myAtt = self.__dict__.get(name)
            if not myAtt: 
                self.__dict__[name] = att
            else:
                if isinstance(myAtt, Attribute):
                    myAtt.value = att
                else:
                    myAtt = att
                self.__dict__[name] = myAtt
            if self.recurrenceID.value and self.myDb.recurrenceType_id:
                self.recurrenceType = RecurrenceType(self.myDb.recurrenceType)
                 
    def validate(self):
        result = True
        atts = self.getAttributeList()
        try:
            BusinessObject.validateAttributes(atts)
        except InvalidAttributeValueException as e:
            super().addMessage(e.getMsg())
            result = False
        return result
        
    def save(self):
        self.toDb()
        self.myDb.save()       
        self.fromDb()
  
    def remove(self):
            self.myDb.delete()
              
    def delete(self):
        self.myDb.deleteFlag = True
        self.myDb.save()
    
    def getAttributeList(self): 
        return [    
                self.endDate,
                self.startDate,
                self.recurrenceID,
                self.intervalAmount,
                self.recurrenceCreateUser,
                self.recurrenceUpdateUser,
                self.recurrenceCreateDate,
                self.recurrenceUpdateDate,
                self.completelyBuilt
        ]
        
            
class ObjectFactory(VSBase):

    _instance = None
    _scheduleStatusAccepted = None
    _scheduleStatusRejected = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            # Create the instance only if it does not exist yet
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self._scheduleStatusAccepted = ValueTableManager().getValue(table='ScheduleStatus', key=ScheduleStatus.ACCEPTED)
        self._scheduleStatusNotSet = ValueTableManager().getValue(table='ScheduleStatus', key=ScheduleStatus.NOT_SET)
        self._configurableProps = None

    def getConfigurableProps(self):
        if not self._configurableProps:
            self._configurableProps = {}
            try:
                lst = DbConfigurableProperty.objects.all()
                if lst:
                    for dbo in lst:
                        cp = ConfigurableProperty(dbo)
                        self._configurableProps[cp.getPropertyName()] = cp 
            except Exception as e:
                super().handleException(e)
        result = {}
        result |= self._configurableProps
        return result
                     
    
    def changePassword(self, login, password, loginId):
        login.setPassword(password)  # throw an InvalidPasswordValueException if the format of the password is invalid. 
        login.succeed()
        login.setLastChange(DT.now())
        login.setLoginUpdateUser(loginId)
        login.save()
    
    def createOrganization(self, name, uid):
        dbo = DbOrganization() 
        result = Organization(dbo)
        result.setName(name)
        result.setCreateUser(uid)
        result.setUpdateUser(uid)
        result.save()
        deflt = self.getOrganization(name="System")
        for cs in self.getConfigurationSets(deflt): 
            if deflt.getOrganizationID() == cs.getConfigurationSetOrganizationID(): 
                csn = self.getNewConfigurationSet(cs.getConfigurationSetName(),uid)
                csn.setConfigurationSetOrganizationID(result.getOrganizationID())
                csn.setCreateDate(DT.now())
                csn.setUpdateDate(DT.now())
                csn.save()

                for cp in self.getConfigurableProperties(): 
                    if cp.getPropertyConfigurationSetID() == cs.getConfigurationSetID(): 
                        dbo = DbConfigurableProperty()
                        cpn = ConfigurableProperty(dbo).clone(cp)
                        cpn.setPropertyName(cp.getPropertyName())
                        cpn.setPropertyConfigurationSetID(csn.getConfigurationSetID())
                        cpn.setCreateUser(uid)
                        cpn.setUpdateUser(uid)
                        cpn.setCreateDate(DT.now())
                        cpn.setUpdateDate(DT.now())
                        cpn.save()
                        csn.addProperty(cpn)                  
                    csn.save()                            
            
            for li in self.getLogins(deflt): 
                dbo = DbLogin()
                lin = Login(dbo).clone(li)
                lin.setOrganization(result)
                lin.setCreateUser(uid)
                lin.setUpdateUser(uid)
                lin.setCreateDate(self.now())
                lin.setUpdateDate(self.now())
                lin.save()
            sgs = self.getSecurityGroups(org=deflt)
            for sg in sgs:
                if not sg.getSecurityGroupDescription() or not sg.getSecurityGroupName():
                    #print(sg.securityGroupID)
                    continue
                dbo = DbSecurityGroup() 
                nsg = SecurityGroup(dbo)
                nsg.setOrganization(result)
                nsg.setSecurityGroupCreateDate(self.now())
                nsg.setSecurityGroupCreateUser(uid)
                nsg.setSecurityGroupUpdateDate(self.now())
                nsg.setSecurityGroupUpdateUser(uid)
                if not sg.getSecurityGroupName():
                    continue
                nsg.setSecurityGroupName(sg.getSecurityGroupName())
                if not sg.getSecurityGroupDescription():
                    continue
                nsg.setSecurityGroupDescription(sg.getSecurityGroupDescription())
                nsg.save()
                nsg = None
        result.setName(name)    
        return result
    
    def createLogin(self, log, name, org, user, household=False, volunteer=False):
        exists = DbLogin.objects.filter(loginName=log).exists()
        if exists:
            raise DuplicateLoginException(log)
        dbl = DbLogin()
        li = Login(dbl) 
        li.setLogin(log)
        li.setLoginName(name)
        li.setSecret("Secret1$$")
        li.setCreateDate(self.now())
        li.setCreateUser(user)
        li.setLastChange(self.now())
        li.setUpdateDate(self.now())
        li.setUpdateUser(user)
        li.save()
        li.setLoginStatus(ValueTableManager().getValue('LoginStatus',LoginStatus.STATUS_RESET))
        li.setPassword("Password1")
        li.setOrganization(org)
        li.save()
        h = None
        names = name.split()
        if len(names) < 2:
            raise InvalidArgumentException("Can\'t create Volunteer from \'") + str(name) +'\''
        lastName = names[1]
        idx = 2
        while idx < len(names):
            lastName += ' '
            lastName += names[idx]
            idx+=1
        if household is True:
            hdbo = DbHousehold()
            hdbo.householdFirstName = names[0]
            hdbo.householdLastName = lastName
            hdbo.householdCreateUser = user
            hdbo.householdUpdateUser = user
            hdbo.save()
            h = Household(hdbo)
            h.setOrganization(org)
            hdbo.organization = org.myDb
            hdbo.save()
        elif isinstance(household,Household):
            h = household
        if h and volunteer:
            vol = Volunteer(myDb=DbVolunteer())
            vol.setHousehold(h)
            vol.setVolunteerFirstName(names[0])
            vol.setVolunteerLastName(lastName)
            vol.setCreateUser(user)
            vol.setUpdateUser(user)
            vol.setOrganization(org)
            vol.save()
            vol.setLogin(li)
            vol.myDb.save()
        return li
    
    def getNewProject(self,name,uid,org,parent=None):
        if isinstance(org,DbOrganization):
            org = DbOrganization(org)
        dbo = DbProject.objects.create( 
                                projectName=name,
                                projectCreateUser=uid,
                                projectUpdateUser=uid,
                                organization_ID = org.getOrganizationID(),
                                projectStatus_id=1)
        if parent:
            if isinstance(parent, Project):
                dbo.parent_ID = parent.getProjectID()
            else:
                dbo.parent_ID = parent.projectID
            dbo.save()
        return Project(dbo)
    
    def getProjects(self,org=None,team=None,parent=None):
        result = []
        if org:
            for dbo in DbProject.objects.exclude(deleteFlag=True).filter(organization__organizationID=org.getOrganizationID()).order_by('projectName'):
                result.append(Project(dbo))
        elif team:
            for dbo in DbProject.objects.exclude(deleteFlag=True).filter(teams__teamID=team.getTeamID()).order_by('projectName'):
                result.append(Project(dbo))
        elif parent:
            for dbo in DbProject.objects.exclude(deleteFlag=True).filter(parent__projectID=parent.getProjectID()).order_by('projectName'):
                result.append(Project(dbo))
        else:
            for dbo in DbProject.objects.exclude(deleteFlag=True).order_by('projectName'):
                result.append(Project(dbo))
        return result
    
    def getDeletedTeams(self, org):
        result = []
        if org and isinstance(org, Organization):
            objs = DbTeam.objects.filter(deleteFlag=True).filter(organization_id=+org.getOrganizationID())
            for obj in objs:
                result.append(Team(obj))
        return result
         
    def getDeletedOrganizationProjects(self, org): 
        result = []
        if org and isinstance(org, Organization):
            objs = DbProject.objects.filter(deleteFlag=True).filter(organization_id=org.getOrganizationID())
            for obj in objs:
                result.append(Project(obj))
        return result
    
    def getSecurityGroups(self, org=None):
        result = []
        if org:
            dbos = DbSecurityGroup.objects.exclude(deleteFlag=True).filter(organization__organizationID=org.organizationID.value)
        else:    
            dbos = DbSecurityGroup.objects.exclude(deleteFlag=True)
        for dbo in dbos:
            sg = SecurityGroup(dbo)
            #print (str(sg))
            result.append(sg)
        return result
    
    def getLogins(self, org=None):
        result = []
        dbos = DbLogin.objects.all().exclude(deleteFlag=True)
        for dbo in dbos:
            if dbo.organization and dbo.organization.organizationID and org and org.organizationID.value:
                if dbo.organization.organizationID != org.organizationID.value:
                    continue
            result.append(Login(dbo))
        return result
    
    @staticmethod
    def resetSingleton(): 
        _instance = None

    def getTableNames(self):
        result = []
        cnx = None
        try:
            cnx = mysql.connector.connect(user='root', password='root', \
                              host='127.0.0.1', \
                              database='VolunteerScheduler')
            with cnx.cursor() as cursor: 
                result = cursor.execute("SHOW TABLES")
                result = [row[0] for row in cursor.fetchall()]
            cnx.close()
            cnx = None
        except Exception as e:
            super().handleException(e)
        if cnx:
            cnx.close()
        return result

    def getTableSize(self, name):
        if isinstance(name, str):
            tableName = 'vs_db' + name.lower()
        elif isinstance(name,type):
            tableName = 'vs_db' + name.__name__.lower()
        else:
            raise InvalidArgumentException() 
        result = 0
        cnx = None
        try:
            cnx = mysql.connector.connect(user='root', password='root', \
                              host='127.0.0.1', \
                              database='VolunteerScheduler')
            with cnx.cursor() as cursor: 
                result = cursor.execute("SELECT COUNT(*) FROM " + tableName)
                result = [row[0] for row in cursor.fetchall()]
                result = result[0]
            cnx.close()
            cnx = None
        except Exception as e:
            super().handleException(e)
        if cnx:
            cnx.close()
        return result
    
    def executeSqlUpdate(self, sql):
        result = None
        cnx = None
        try:
            cnx = mysql.connector.connect(user='root', password='root', \
                              host='127.0.0.1', \
                              database='VolunteerScheduler')
            with cnx.cursor() as cursor: 
                result = cursor.execute(sql)
                result = [row[0] for row in cursor.fetchall()]
            cnx.close()
            cnx = None
        except Exception as e:
            super().handleException(e)
        if cnx:
            cnx.close()
        return result

    def refresh(self, vsp):
        vsp.fromDb()

    def save(self, p):
        p.myDb.save()

    def delete(self, p):
        p.setDeleteFlag(True)
        p.save(p)

    def remove(self, p):
        pdb = p.myDb
        if pdb:
            pdb.delete()
            
    def getConfigurableProperties(self):
        result = []
        for dbo in DbConfigurableProperty.objects.exclude(deleteFlag=True):
            result.append(ConfigurableProperty(dbo))
        if len(result) > 1:
            Collections.sort(result, ConfigurablePropertyComparator())
        return result

    def getJobsRequiringSkill(self, skill):
        result = []
        skillID = skill.getSkillID()
        if skillID:
            for j in DbJob.objects.exclude(deleteFlag=True).filter(skill_id=skillID): 
                result.append(Job(j))
        if len(result) > 1:
            Collections.sort(result, ComparatorFactory.getComparator(result[0]))    
        return result
    
    def getEventResourceAssignments(self, sei, resources):
        result = []
        if sei and isinstance(sei, ScheduleEvent):
            for obj in sei.resources:
                if obj in resources:
                    result.append(obj)
        return result
    
    def getEventResources(self, sei=None):
        result = []
        if sei:
            result.extend(sei.getResources())
        else:
            for obj in DbResource.objects.exclude(deleteFlag=True):
                result.append(Resource(obj))
        return result
    
    def getOtherEvents(self, evtid,org):
        result = []
        evt = DbScheduleEvent.objects.filter(pk=evtid).first()
        dbos = DbScheduleEvent.objects.exclude(deleteFlag=True)\
        .filter(organization_id=org.getOrganizationID())\
        .filter(eventDate=evt.eventDate)\
        .filter(location_id=evt.location_id)\
        .exclude(eventID=evt.eventID)
        for dbo in dbos:
            result.append(ScheduleEvent(dbo))
        return result
    
    def getOtherFamilyVolunteers(self, hid, vid):
        result = []# kluge don't trust deducting 1 from vid
        dbos = DbVolunteer.objects.exclude(deleteFlag=True)\
        .exclude(volunteerID=(vid-1)).filter(household_id=hid)
        #print('hID ' + str(hid) +' vID ' + str(vid))
        for dbo in dbos:
            #print(str(dbo.volunteerID) + ' ' + str(dbo.volunteerFirstName))
            if dbo.volunteerID == vid:
                continue
            result.append(Volunteer(dbo))
        return result
                 
    def getNewHousehold(self, first, last, uid, org):
        add = DbAddress.objects.create(
                        addressCreateUser=uid,
                        addressUpdateUser=uid)
        dbo = DbHousehold.objects.create(
                        householdCreateUser=uid,
                        householdUpdateUser=uid,
                        householdFirstName=first,
                        householdLastName=last,
                        address_id=add.addressID,
                        organization_id=org.getOrganizationID())
        return Household(dbo)
    
    def getLocation(self, oid=None, name=None, org=None):
        result = None
        #print('\nname ' + str(name) + ' org ' + str(org))
        if name and org:
            #print('name ' + str(name) + ' org ' + str(org) + ' ID ' + str(org.getOrganizationID())) 
            dbo = DbLocation.objects.exclude(deleteFlag=True).filter(locationName=name)\
            .filter(organization_id=org.getOrganizationID()).first()
            #print('\ndbo = "' + str(dbo) + '"') 
            if dbo:
                result = Location(dbo)
        elif oid:
            dbo = DbLocation.objects.exclude(deleteFlag=True).filter(pk=oid).first()
            if dbo:
                result = Location(dbo)
        return result
    
    def getNewLocation(self, name, uid, org):
        dbo = DbLocation.objects.create(
                        locationName=name,
                        locationCreateUser=uid,
                        locationUpdateUser=uid,
                        organization_id=org.getOrganizationID())
        return Location(dbo)
    
    def getLocations(self, org=None):
        result = []
        if org:
            dbos = DbLocation.objects.exclude(deleteFlag=True).filter(organization_id=org.organizationID.value)
        else:
            dbos = DbLocation.objects.exclude(deleteFlag=True)
        for dbo in dbos:
            result.append(Location(dbo))
        return result
    

    def getPrivilege(self, pid):
        result = None
        try: 
            dbo = DbPrivilege.objects.exclude(deleteFlag=True).get(pk=pid)
            result = Privilege(dbo)
        except:
            pass
        return result
    
    def getPrivileges(self):
        result = []
        for dbo in DbPrivilege.objects.exclude(deleteFlag=True):
            result.append(Privilege(dbo))
        if len(result) > 1:
            Collections.sort(result)
        return result
    
    def getDeletedLogins(self):
        result = []
        for dbo in DbLogin.objects.filter(deleteFlag=True):
            result.append(Login(dbo))
        if len(result) > 1:
            Collections.sort(result)
        return result
    
    def getDeletedSkills(self):
        result = []
        for dbo in DbSkill.objects.filter(deleteFlag=True):
            result.append(Skill(dbo))
        if len(result) > 1:
            Collections.sort(result)
        return result        
    
    def getDeletedTasks(self):
        result = []
        for dbt in DbTask.objects.filter(deleteFlag=True):
            result.append(Task(dbt));
        return result
    
    def getResourceAvailabilities(self, sei):
        result = []
        myMap = {}
        resources = self.getResources(sei.getOrganization())
        for r in resources: 
            ra = ResourceAvailability(r, r.getCount())
            myMap[ra.getKey()] = ra
        
        ejrs = self.getEventJoinToResources()
        for ejr in ejrs: 
            if ejr.getEventID() == sei.getEventID():
                ra = None
                try: 
                    ra = myMap[ejr.getResourceID()]
                except:
                    pass
                if ra: 
                    ra.setCount(ra.getCount() - ejr.getCount())
            else: 
                sei2 = self.getEvent(ejr.getEventID())
                if sei2 and Utils.isOverlap(sei, sei2): 
                    ra = myMap.get(ejr.getResourceID())
                    if ra: 
                        available = ra.getCount() - ejr.getCount()
                        if available <= 0:
                            try: 
                                del myMap[ra.getResource().getKey()]
                            except:
                                pass
                        else: 
                            ra.setCount(available)
        list1 = myMap.values()
        for i in list1:
            result.append(i)
        return result

    def getResourceUsage(self, sei, res):
        result = 0
        for dbo in DbEventJoinToResource.objects.filter(resource_id=res.getResourceID())\
        .filter(event_id=sei.getEventID()): 
                result += dbo.count
        return result
    
    def getDeletedResources(self, org=None):
        result = []
        if org:
            dbos = DbResource.objects.filter(deleteFlag=True).filter(organization__organizationID=ord.organizationID)
        else:
            dbos = DbResource.objects.filter(deleteFlag=True) 
        for dbo in dbos:
            result.append(Resource(dbo))
        return result
    
    def getDeletedLocations(self, org=None):
        result = []
        if org:
            dbos = DbLocation.objects.filter(deleteFlag=True).filter(organization__organizationID=ord.organizationID)
        else:
            dbos = DbLocation.objects.filter(deleteFlag=True) 
        for dbo in dbos:
            result.append(Location(dbo))
        return result
    
    def getRecurringEvents(self, org):
        result = []
        evts = DbScheduleEvent.objects.exclude(deleteFlag=True)\
        .filter(organization_id=org.getOrganizationID())
        #print(evts)
        for evt in evts:
            #print(str(evt.recurrence_id))
            if evt.recurrence_id:
                er = evt.recurrence
                #print(str(er))
                if er and not er.completelyBuilt:
                    result.append(ScheduleEvent(evt))
        return result;    

    def getDeletedSecurityGroups(self, org=None):
        result = []
        if org:
            dbos = DbSecurityGroup.objects.filter(deleteFlag=True).filter(organization__organizationID=ord.organizationID)
        else:
            dbos = DbSecurityGroup.objects.filter(deleteFlag=True) 
        for dbo in dbos:
            result.append(SecurityGroup(dbo))
        return result
    
    def getDeletedVolunteerSkills(self, vol=None):
        result = []
        if vol:
            dbos = DbVolunteerSkill.objects.filter(deleteFlag=True).filter(volunteer__volunteerID=vol.volunteerID)
        else:
            dbos = DbVolunteerSkill.objects.filter(deleteFlag=True)
        for dbo in dbos:
            result.append(VolunteerSkill(dbo))
        return result
    
    def getDeletedVolunteerSkillAssignments(self):
        result = []
        for dbo in DbVolunteerSkillAssignment.objects.filter(deleteFlag=True):
            result.append(VolunteerSkillAssignment(dbo))
        return result
    
    def getNewPassword(self, pwd, uid, login=None): 
        dbo = DbPassword(password=pwd,
                         passwordCreateUser=uid,
                         passwordUpdateUser=uid)
        result = Password(dbo)
        if login:
            result.login = login
        result.setPasswordCreateDate(DT.now())   
        result.setPasswordUpdateDate(DT.now()) 
        result.save()
        return result
    
    def getPassword(self, oid):
        result = None
        dbo = None
        try:
            #print('oid=' + str(oid))
            dbo = DbPassword.objects.exclude(deleteFlag=True).filter(pk=oid).first()
        except:
            pass
        if dbo:
            result = Password(dbo)
        #print(str(oid) + ' was ' + str(result))
        return result
    
    def getPasswords(self,login=None):
        result = []
        if login:
            for dbo in DbPassword.objects.all().exclude(deleteFlag=True).filter(login__loginID=login.loginID.value):
                result.append(Password(dbo))
        else:
            for dbo in DbPassword.objects.all():
                result.append(Password(dbo))
        return result
    
    def getRecentPasswords(self, li, months):
        result = []
        if li and months and isinstance(li, Login) and isinstance(months, int):
            pwds = self.getPasswords(login=li)
            now = DT.now()
            tgt = now - relativedelta(months=months)
            tgt = tgt.date()
            # print(tgt)
            for pwd in pwds:
                # print(pwd)                
                if months > 0: 
                    cd = pwd.getPasswordCreateDate()
                    # print(cd)
                    if cd < tgt: 
                        continue                    
                    result.append(pwd)      
        return result
    
    def getRecurrenceTypes(self):
        result = []
        for dbo in DbRecurrenceType.objects.all().order_by('recurrenceTypeKey'):
            result.append(RecurrenceType(dbo))
        return result

    def getLoginStatuses(self):
        result = []
        for dbo in DbLoginStatus.objects.all().order_by('loginStatusType'):
            result.append(LoginStatus(dbo))
        return result

    def getScheduleStatuses(self):
        result = []
        for dbo in DbScheduleStatus.objects.all().order_by('scheduleStatusKey'):
            result.append(ScheduleStatus(dbo))
        return result
    
    def getStateCodes(self):
        result = []
        for dbo in DbStateCode.objects.all().order_by('sc_code'):
            result.append(StateCode(dbo))
        return result
    
    def getNewWorkAddress(self,add,uid):
        dbo = DbWorkAddress.objects.create(
                                    address_id=add.getAddressID(),
                                    waCreateUser=uid,
                                    waUpdateUser=uid)
        return WorkAddress(dbo)

    def getWorkAddress(self, oid):
        result = None
        try:
            dbo = DbWorkAddress.objects.get(pk=oid)
            if dbo:
                result = WorkAddress(dbo)
        except:
            pass
        return result

    def getWorkAddresses(self):
        result = []
        for dbo in DbWorkAddress.objects.exclude(deleteFlag=True).order_by('workAddressID'):
            result.append(WorkAddress(dbo))
        return result
    
    def getAddresses(self):
        result = []
        for dbo in DbAddress.objects.exclude(deleteFlag=True).order_by('addressID'):
            result.append(Address(dbo))
        return result
    
    def getAddress(self, oid):
        result = None
        dbo = DbAddress.objects.exclude(deleteFlag=True).filter(pk=oid).first()
        if dbo:
            result = Address(dbo)
        return result

    def getActivity(self, oid):
        result = None
        dbo = DbActivity.objects.exclude(deleteFlag=True).filter(pk=oid).first()
        if dbo:
            result = Activity(dbo)
        return result
    
    def getProject(self, uid):
        result = None 
        try:
            qr = DbProject.objects.exclude(deleteFlag=True).filter(pk=uid).first()
            if qr:
                result = Project(qr)
        except Exception as e:
            self.handleException(e)
        return result

    def getOrganizations(self,dbo=False):
        result = [] 
        try:
            qr = DbOrganization.objects.exclude(deleteFlag=True)
            for db in qr:
                if dbo:
                    result.append(db)
                else:
                    org = Organization(db)
            #        print(org)
                    result.append(org)
        except Exception as e:
            self.handleException(e)
        #print(result)
        return result

    def getOrganization(self, uid=None, name=None):
        result = None 
        if not name:
            try:
                qr = DbOrganization.objects.exclude(deleteFlag=True).filter(pk=uid).first()
                if qr:
                    result = Organization(qr)
            except Exception as e:
                self.handleException(e)
        else:   
            try:         
                qr = DbOrganization.objects.exclude(deleteFlag=True).filter(organizationName=name).first()
                if qr:
                    result = Organization(qr)
            except Exception as e:
                self.handleException(e)
        return result
    
    def getNewTask(self,name, uid, org):
        dbo = DbTask.objects.create(
                                taskCreateUser=uid,
                                taskUpdateUser=uid,
                                taskName=name,
                                organization_id=org.getOrganizationID())
        return Task(dbo)

    def getTask(self, uid):
        result = None 
        try:
            qr = DbTask.objects.exclude(deleteFlag=True).filter(pk=uid).first()
            if qr:
                result = Task(qr)
        except Exception as e:
            self.handleException(e)
        return result
    
    def getNewTeam(self,name,uid,org):
        dbo = DbTeam.objects.create(
                                teamCreateUser=uid,
                                teamUpdateUser=uid,
                                teamName=name,
                                organization_id=org.getOrganizationID())
        return Team(dbo)
    
    def getTeam(self, uid):
        result = None 
        try:
            dbo = DbTeam.objects.exclude(deleteFlag=True).filter(pk=uid).first()
            if dbo:
                result = Team(dbo)
        except Exception as e:
            self.handleException(e)
        return result
    
    def getNewAddress(self,uid):
        dbo = DbAddress.objects.create(
                    addressCreateUser=uid,
                    addressUpdateUser=uid)
        return Address(dbo)
        
    def getVolunteersFromTask(self, tsk):
        result = []
        if tsk:
            dbt = tsk.myDb
            vols = dbt.volunteers.all()
            for v in vols:
                vol = Volunteer(v)
                result.append(vol)
        return result
        
    def getNewPrivilege(self, name, uid):
        dbo = DbPrivilege.objects.create( 
                    privilegeName=name,
                    privilegeCreateUser=uid,
                    privilegeUpdateUser=uid)
        return Privilege(dbo)
    
    def getSecurityGroup(self, oid):
        result = None
        dbo = DbSecurityGroup.objects.exclude(deleteFlag=True).filter(pk=oid).first()
        if dbo:
            result = SecurityGroup(dbo)
        return result   

    def addDefaultAuthorizations(self, org, loginId): 
        if not org.getOrganizationID(): 
            org.save()
        
        defOrg = self.getOrganization(name=Constants.DEFAULT_ORGANIZATION)
        groups = self.getSecurityGroups(defOrg)
        for sg in groups:
            #print(str(sg)) 
            sg2 = SecurityGroup(sg=sg)
            sg2.setOrganization(org)
            sg2.setCreateUser(loginId)
            sg2.setUpdateUser(loginId)
 

    def getNewSecurityGroup(self, name, desc, level, uid, org):
        dbo = DbSecurityGroup.objects.create(securityGroupName=name,
                                               level=level,
                                               securityGroupCreateUser = uid,
                                               securityGroupUpdateUser = uid,
                                               securityGroupDescription = desc,
                                               organization_ID = org.getOrganizationID())
                                               
        return SecurityGroup(dbo)
    

    def getReport(self, oid=None,schedule=None):
        result = None
        try:
            if oid:
                dbo = DbReport.objects.exclude(deleteFlag=True).filter(pk=oid).first()
            elif schedule:
                dbo =  DbReport.objects.exclude(deleteFlag=True)\
                .filter(schedule_id=schedule.getScheduleID())
            if dbo:
                result = Report(dbo)
        except DbReport.DoesNotExist:
            pass
        return result
    
    def getReports(self):
        result = []
        for dbo in DbReport.objects.exclude(deleteFlag=True):
            result.append(Report(dbo))
        return result
    
    def getNewReport(self, name,uid,url=None):
        dbo = DbReport.objects.create(
                            reportName = name,
                            reportCreateUser = uid,
                            reportUpdateUser = uid)
        if url:
            dbo.reportURL = url
            dbo.save()
        return Report(dbo)
    
    def getEventRecurrence(self, oid):
        result = None
        try:
            dbo = DbEventRecurrence.objects.exclude(deleteFlag=True).filter(pk=oid).first()
            result = EventRecurrence(dbo)
        except DbEventRecurrence.DoesNotExist:
            pass
        return result
    
    def getNewEventRecurrence(self, uid, typeID=None, interval=1):
        dbo = DbEventRecurrence.objects.create(recurrenceCreateUser=uid,
                                               recurrenceUpdateUser=uid,
                                               intervalAmount=interval)
        result = EventRecurrence(dbo)
        if typeID:
            t = self.getRecurrenceType(typeID)
            if t:
                result.setRecurrenceType(t)
                dbo.recurrenceType_ID = typeID
                dbo.save()
        return result
    
    def getEventPreference(self, vol=None, oid=None):
        result = None
        if vol:
            dbo = DbEventPreference.objects.exclude(deleteFlag=True).filter(volunteer_id=vol.volunteerID).first()
        elif oid:
            dbo = DbEventPreference.objects.exclude(deleteFlag=True).filter(pk=oid).first()
        if dbo:            
            result = EventPreference(dbo)
        return result

    def getEventPreferences(self):
        result = []
        dbos = DbEventPreference.objects.exclude(deleteFlag=True)
        for dbo in dbos:
            result.append(EventPreference(dbo))
        return result
    
    def getNewEventPreference(self, vol,evt,uid):
        dbo = DbEventPreference.objects.create(
                                                volunteer_id=vol.getVolunteerID(),
                                                event_id=evt.getEventID(),
                                                preferenceCreateUser=uid,
                                                preferenceUpdateUser=uid)
        return EventPreference(dbo)
    
    def getNewEventJoinToResource(self,evt,res,uid,count=0):
        dbo = DbEventJoinToResource.objects.create(
                                            event_id=evt.getEventID(),
                                            resource_id=res.getResourceID(),
                                            createUser=uid,
                                            updateUser=uid,
                                            count=count)
        return EventJoinToResource(dbo)
    
    def getNewResource(self, name,uid,org):
        dbo = DbResource.objects.create(name=name,
                                        resourceCreateUser=uid,
                                        resourceUpdateUser=uid,
                                        organization_id=org.getOrganizationID()) 
        return Resource(dbo)
    
    def getResource(self, oid=None,name=None,org=None):
        result = None
        dbo = None
        if oid:
            try:
                dbo = DbResource.objects.exclude(deleteFlag=True).filter(pk=oid).first()
            except:
                pass
        elif name and org:
            try:
                dbo = DbResource.objects.exclude(deleteFlag=True).\
                filter(organization__organizationID=org.getOrganizationID()).\
                filter(name=name).first()
            except:
                pass
        if dbo:
            result = Resource(dbo)    
        return result

    def getResources(self, org):
        result = []
        if org:
            dbos = DbResource.objects.exclude(deleteFlag=True)\
            .filter(organization_id=org.getOrganizationID())
        else:
            dbos = DbResource.objects.exclude(deleteFlag=True)
        for dbo in dbos:
            result.append(Resource(dbo))
        return result
    

    def getHousehold(self, oid):
        result = None
        try:
            dbo = DbHousehold.objects.exclude(deleteFlag=True).filter(pk=oid).first()
            if dbo:
                result = Household(dbo)
        except:
            pass
        return result
    
    def getHouseholds(self, lastName=None,org=None):
        result = []
        dbos = []
        if lastName:
            if not org:
                raise InvalidArgumentException('If you specify name you must aalso specify org ')
            dbos = DbHousehold.objects.exclude(deleteFlag=True)\
            .filter(householdLastName=lastName).\
            filter(organization_id=org.organizationID)
        elif org: 
            dbos = dbos = DbHousehold.objects.exclude(deleteFlag=True).\
            filter(organization_id=org.organizationID)
        else:
            dbos = DbHousehold.objects.exclude(deleteFlag=True)
        for dbo in dbos:
            result.append(Household(dbo))
        return result

    def getAvailability(self, oid=None,vol=None):
        result = []
        dbo = None
        if oid:
            try:
                dbo = DbAvailability.objects.exclude(deleteFlag=True).filter(pk=oid).first()
                result.append(Availability(dbo))
            except:
                pass
        elif vol:
            try:
                dbos = DbAvailability.objects.exclude(deleteFlag=True).filter(volunteer__volunyeerID=vol.volunyeerID.value)
                for dbo in dbos:
                    result.append(Availability(dbo))
            except:
                pass
        else:
            raise MissingArgumentException("You mudt specify eithetman ID oa an organization")
        return result
    
    def getAvailabilities(self):
        result = []
        for dbo in DbAvailability.objects.exclude(deleteFlag=True):
            result.append(Availability(dbo))
        return result

    def getActivities(self):
        result = []
        for dbo in DbActivity.objects.exclude(deleteFlag=True):
            result.append(Activity(dbo))
        return result
    
    def getProjectResource(self, oid):
        result = None
        try:
            dbo = DbProjectResource.objects.exclude(deleteFlag=True).filter(pk=oid).first()
            result = ProjectResource(dbo)
        except:
            pass
        return result
    
    def getProjectResources(self, org):
        result = []
        try:
            dbos = DbProjectResource.objects.exclude(deleteFlag=True)\
            .filter(organization_id=org.organizationID.value)
            for dbo in dbos:
                result.append(ProjectResource(dbo))
        except:
            pass
        return result
    
    def getTeams(self):
        result = []
        for dbo in DbTeam.objects.exclude(deleteFlag=True):
            result.append(Team(dbo))
        return result
    
    def getTasks(self):
        result = []
        for dbo in DbTask.objects.exclude(deleteFlag=True):
            result.append(Task(dbo))
        return result
    
    def getNewVolunteer(self,  h, uid, org, fName=None, lName=None):
        dbo = DbVolunteer.objects.create(
            volunteerCreateUser=uid,
            volunteerUpdateUser=uid,
            household_id=h.getHouseholdID(),
            organization_id=org.getOrganizationID())
        if fName:
            dbo.volunteerFirstName = fName
        if lName:
            dbo.volunteerLastName = lName
        if org or fName or lName:
            dbo.save()
        #print(dbo)
        result = Volunteer(myDb=dbo)
        #print(result)
        return result

    def getVolunteers(self,org=None,household=None,skill=None):
        result = []
        dbos = None
        if skill and org:
            dbos = DbVolunteer.objects.exclude(deleteFlag=True).\
            filter(organization_id=org.getOrganizationID()).\
            filter(skill_id=skill.getSkillID())
        elif org:
            dbos = DbVolunteer.objects.exclude(deleteFlag=True)\
            .filter(organization_id=org.getOrganizationID())
        elif household:
            dbos = DbVolunteer.objects.exclude(deleteFlag=True)\
            .filter(household_id=household.getHouseholdID())
        elif skill and not org:
            raise MissingArgumentException('if you specify skill, you must also specify org')
        elif not org and not household and not skill:
            raise MissingArgumentException('No request parameter')
        if dbos:
            for dbo in dbos:
                result.append(Volunteer(dbo))
        return result
    
    def getVolunteersNamed(self, last, org, first=None):
        result = []
        try:
            dbos = None
            if first:
                dbos = DbVolunteer.objects.exclude(deleteFlag=True)\
                .filter(organization_id=org.getOrganizationID())\
                .filter(volunteerFirstName=first).filter(volunteerLastName=last)
            else:                
                dbos = DbVolunteer.objects.exclude(deleteFlag=True)\
                .filter(organization_id=org.getOrganizationID())\
                .filter(volunteerLastName=last)
            if dbos:
                for dbo in dbos:
                    result.append(Volunteer(dbo))
        except:
            pass
        return result

    def getNewVolunteerSkill(self, vol,skill,uid):
        #print(vol.myDb)
        dbo = DbVolunteerSkill.objects.create(
                                        vsCreateUser=uid, 
                                        vsUpdateUser=uid,
                                        volunteer_id=vol.getVolunteerID(),
                                        skill_id=skill.getSkillID())
        #print(vol.myDb)
        vs = VolunteerSkill(dbo, vol, skill)
        #print(vol.myDb)
        #print(skill.myDb)
        #vs.setVolunteer(vol)
        #vs.setSkill(skill)
        return vs 
    
    def getVolunteerSkill(self, oid):
        result = None
        dbo = None
        if oid:
            try:
                dbo = DbVolunteerSkill.objects.exclude(deleteFlag=True).filter(pk=oid).first()
            except:
                pass
        if dbo:
            result = VolunteerSkill(dbo)
        return result
    
    def getVolunteerSkills(self, org=None, vol=None, skill=None, expert=False):
        result = []
        dbos = None
        if skill:
            try:
                if expert:
                    dbos = DbVolunteerSkill.objects.exclude(deleteFlag=True)\
                    .filter(skill_id=skill.getSkillID()).filter(expert=True)
                else:
                    dbos = DbVolunteerSkill.objects.exclude(deleteFlag=True)\
                    .filter(skill_id=skill.getSkillID())
            except:
                pass
        elif vol:
            #print(vol.myDb.volunteerID)
            #for x in DbVolunteerSkill.objects.all():
            #    print(x)
            dbos = DbVolunteerSkill.objects.exclude(deleteFlag=True)\
            .filter(volunteer_id=vol.myDb.volunteerID)
            #print(dbos)
        else:
            dbos = DbVolunteerSkill.objects.exclude(deleteFlag=True)
        if dbos:
            for dbo in dbos:
                result.append(VolunteerSkill(dbo))
        return result

    def getNewVolunteerSkillAssignment(self,volSkill,evt, uid):
        dbo = DbVolunteerSkillAssignment.objects.create(
                                        vsaCreateUser=uid,
                                        vsaUpdateUser=uid,
                                        volunteerSkill_id=volSkill.getVolunteerSkillID(),
                                        event_id=evt.getEventID())
        return VolunteerSkillAssignment(dbo)
    
    def getVolunteerSkillAssignment(self, oid):
        result = None
        try:
            dbo = DbVolunteerSkillAssignment.objects.\
            exclude(deleteFlag=True).filter(pk=oid).first
            if dbo:
                result = VolunteerSkillAssignment(dbo)
        except Exception as e:
            self.handleException(e)
        return result
    

    def getVolunteerSkillAssignments(self,start=None,end=None):
        result = []
        dbos = None
        if start and end:
            dbos = DbVolunteerSkillAssignment.objects.exclude(deleteFlag=True).filter(assignmentDate_gte=start).filter(assignmentDate_lte=end)
        elif start and not end:
            dbos = DbVolunteerSkillAssignment.objects.exclude(deleteFlag=True).filter(assignmentDate_gte=start)
        elif end and not start:
            dbos = DbVolunteerSkillAssignment.objects.exclude(deleteFlag=True).filter(assignmentDate_lte=end) 
        else:
            dbos = DbVolunteerSkillAssignment.objects.exclude(deleteFlag=True)
        if dbos:
            for dbo in dbos:
                result.append(VolunteerSkillAssignment(dbo))
        if len(result) > 1: 
            Collections.sort(result)        
        return result
    
    def getNewEvent(self,name=None, uid=None, org=None, sei=None, dbo=False):
        dbo1 = DbScheduleEvent.objects.create(
                            eventDate=DT.now(),
                            eventDuration=1,
                            eventStartTime='00:00',
                            eventName=name,
                            eventCreateUser=uid,
                            eventUpdateUser=uid)
        if org:
            dbo1.organization_ID = org.getOrganizationID()
            dbo1.save()
        
        result = ScheduleEvent(dbo1)
        if sei:
            result.clone(sei)
            result.save()
        if dbo:
            result = dbo1 
        return result
    
    def getEvent(self, oid):
        result = None
        try:
            dbo = DbScheduleEvent.objects.exclude(deleteFlag=True).filter(pk=oid).first()
            result = ScheduleEvent(dbo)
        except:
            pass
        return result
    
    def getEvents(self, org=None,start=None,end=None,schedule=None, dbo=False):
        dbos = None
        result = []
        if schedule:
            dbos = DbScheduleEvent.objects.exclude(deleteFlag=True).filter(schedule_id=schedule.getScheduleID())
        elif org and not start and not end:
            dbos = DbScheduleEvent.objects.exclude(deleteFlag=True).filter(organization_id=org.getOrganizationID())
        elif not org and not start and not end:
            dbos = DbScheduleEvent.objects.exclude(deleteFlag=True)
        elif org and start and end:
            dbos = DbScheduleEvent.objects.exclude(deleteFlag=True).filter(organization_id=org.getOrganizationID()) \
            .filter(eventDate_gte=start).filter(eventDate_lte=end)
        else:
            raise InvalidRequestError('if either start or end are provided, both must be provided \nstart: "' +str(start) + '" end: "' \
                                      + str(end) + '"\n')
        for db in dbos:
            if dbo:
                result.append(db)
            else:
                result.append(ScheduleEvent(db))
        return result
    
    def acceptSchedule(self, schedule, uid):
        if schedule.canAcceptOrReject(): 
            schedule.validateAccept()
            schedule.accept(uid)
            for evt in schedule.getEvents():
                self.acceptEvent(evt,uid)
            schedule.setScheduleStatus(self._getScheduleStatusAccepted())
            schedule.setScheduleUpdateUser(uid)
            schedule.save()
        return schedule
                
    def rejectSchedule(self, schedule, uid):
        schedule.validateReject()
        from vscode.calc.calc import EventRejecter
        EventRejecter(schedule, uid).rejectEvents()
        rpt = self.getReport(schedule=schedule)
        if rpt:
            self.deleteReport(rpt, uid)
        schedule.setScheduleStatus(self._getScheduleStatusRejected())
        schedule.save()
        schedule.delete()
        return schedule
        
    def acceptEvent(self, evt, uid):
        #print(evt)
        evt.setAccepted(True)
        for dbjob in DbJob.objects.exclude(deleteFlag=True).filter(event_id=evt.getEventID()):
        #    print('dbjob: ' + str(dbjob))
            dbja = DbJobAssignment.objects.exclude(deleteFlag=True).filter(job_id=dbjob.jobID).first()
            #print('ja1 ' + str(dbja))
            if dbja:
                dbja.accepted = True
                dbja.jobAssignmentUpdateUser = uid
                if not dbja.jobAssignmentCreateUser:
                    dbja.jobAssignmentCreateUser = uid
            #        print('ja2 ' + str(dbja))
                dbja.save()
            #    print('ja3 ' + str(dbja))
        evt.save()
        return evt
    
    def getEventRecurrences(self, start=None, end=None):
        result = []
        dbos = DbEventRecurrence.objects.exclude(deleteFlag=True)
        for dbo in  dbos:
            if start:
                if start > dbo.endDate:
                        continue
            if end:
                if end < dbo.startDate: 
                    continue
            result.append(EventRecurrence(dbo))
        return result;
    
    def getNewSkill(self, name, uid, org):
        dbo = DbSkill.objects.create(
                        skillName=name,
                        skillCreateUser=uid,
                        skillUpdateUser=uid,
                        organization_id=org.getOrganizationID())
        return Skill(dbo)
    
    def getNewDbSkill(self, name, uid, org):
        dbo = DbSkill.objects.create(skillName=name,
                                      skillCreateUser=uid,
                                      skillUpdateUser=uid,
                                      organization_id=org.getOrganizationID())
        return dbo
    
    def getVolunteer(self,oid=None,first=None,last=None,org=None,login=None):
        result = None
        if oid:
            try:
                dbo = DbVolunteer.objects.exclude(deleteFlag=True).filter(pk=oid).first()
                result = Volunteer(dbo) 
            except:
                pass
        elif login:
            result = Volunteer(login.myDb.volunteer)
        elif first and last and org:
            dbo = DbVolunteer.objects.exclude(deleteFlag=True)\
            .filter(volunteerFirstName=first).filter(volunteerlarstName=last)\
            .filter(organization__organizationID=org.organizationID).first()
            result = Volunteer(dbo)
        else:
            raise MissingArgumentException('you must specify either oID or login, or first,lsst, and org ') 
        return result
    
    def getDeletedVolunteer(self,first=None,last=None,org=None,oid=None):
        result = None
        if oid:
            try:
                dbo = DbVolunteer.objects.filter(deleteFlag=True).filter(pk=oid).first()
                result = Volunteer(dbo) 
            except:
                pass
        elif first and last and org:
            dbo = DbVolunteer.objects.filter(deleteFlag=True)\
            .filter(volunteerFirstName=first).filter(volunteerlarstName=last)\
            .filter(organization__organizationID=org.organizationID).first()
            result = Volunteer(dbo)
        else:
            raise MissingArgumentException('you must specify either oID or login, or first,lsst, and org ') 
        return result
    
    def getLogin(self, first=None, last=None, login=None, org=None, oid=None):
        result = None
        if oid:
            try:
                dbo = DbLogin.objects.exclude(deleteFlag=True).filter(pk=oid).first()
                if dbo:
                    result = Login(dbo)
            except:
                pass
        elif login and org:
            dbo = DbLogin.objects.exclude(deleteFlag=True)\
            .filter(organization_id=org.getOrganizationID())\
            .filter(login=login).first()
            if dbo:
                result = Login(dbo)
        elif first and last and org:
            try:
                name = first + " " + last
                dbo = DbLogin.objects.exclude(deleteFlag=True).filter(organization__organizationID=org.organizationID)\
                .filter(loginName=name).first()
                if dbo:
                    result = Login(dbo)
            except:
                pass 
        else:
            raise InvalidArgumentException('you must specify either oID or first,last and org')
        return result
    
    def getSkill(self, oid=None, name=None, org=None ):
        result = None 
        if oid:
            dbs = DbSkill.objects.filter(pk=oid).first()
            if dbs:
                result = Skill(dbs)
        elif name and org:
            dbos = DbSkill.objects.exclude(deleteFlag=True)\
            .filter(organization__organizationID=org.organizationID)\
            .filter(skillName=name)
            cnt = dbos.count()
            if cnt > 1:
                raise NotUniqueException('received ' + str(cnt) + ' Skill objects from the database')
            if cnt == 1:
                result = Skill(dbos.first())
        else:
            raise MissingArgumentException('you must specify oID or name and org')    
        return result
    
    def getSkills(self, org):
        result = []
        dbos = DbSkill.objects.exclude(deleteFlag=True)\
        .filter(organization_id=org.getOrganizationID())
        for dbo in dbos:
            result.append(Skill(dbo))
        return result
    
    def getNewSkillRelationship(self, s1, s2, uid,typ=None):
        dbo = DbSkillRelationship.objects.create(skillOne_id=s1.getSkillID(),
                                                 skillTwo_id=s2.getSkillID(),
                                                 skillRelationshipCreateUser=uid,
                                                 skillRelationshipUpdateUser=uid)
        if typ:
            dbo.skillRelationshipType_ID = typ.getSkillRelationshipTypeID()
        dbo.save()
        return SkillRelationship(dbo)
    
    def getSkillRelationship(self, oid):
        result = None
        dbo = DbSkillRelationship.objects.exclude(deleteFlag=True).filter(pk=oid).first()
        if dbo:
            result = SkillRelationship(dbo)
        return result

    def getSkillRelationships(self, skill=None):
        result = []
        dbos = None
        if skill:
            dbos = DbSkillRelationship.objects.exclude(deleteFlag=True)\
            .filter(Q(skillOne__skillID=skill.skillID) | Q(skillTwo__skillID=skill.skillID))
        else:
            dbos = DbSkillRelationship.objects.exclude(deleteFlag=True)
        for dbo in dbos:
            result.append(SkillRelationship(dbo))
        return result
    
    def getNewJobAssignment(self, job=None, vol=None, uid=None):
        dbo=DbJobAssignment.objects.create(
                                    job_id=job.getJobID(),
                                    volunteer_id=vol.getVolunteerID(),
                                    jobAssignmentCreateUser=uid,
                                    jobAssignmentUpdateUser=uid)
        return JobAssignment(dbo)
    
    def getJobAssignment(self, oid,dbonly=False):
        result = None
        dbo = DbJobAssignment.objects.exclude(deleteFlag=True).filter(pk=oid).first()
        if dbo:
            if dbonly:
                result = dbo
            else:
                result = JobAssignment(dbo)
        return result

    def getJobAssignments(self, login=None,vol=None,household=None,job=None):
        result = []
        if login:
            dbos = DbJobAssignment.objects.exclude(deleteFlag=True)\
            .filter(volunteer__login__loginID=login.loginID)
        elif vol:
            dbos = DbJobAssignment.objects.exclude(deleteFlag=True)\
            .filter(volunteer__volunteerID=vol.volunteerID)
        elif household:
            dbos = DbJobAssignment.objects.exclude(deleteFlag=True)\
            .filter(volunteer__household__householdID=household.householdID)
        elif job:
            dbos = DbJobAssignment.objects.exclude(deleteFlag=True)\
            .filter(job__jobID=job.jobID)
        else:
            dbos = DbJobAssignment.objects.exclude(deleteFlag=True)
        for dbo in dbos:
            result.append(JobAssignment(dbo))
        return result
    
    def getDeletedObject(self, cls, oid):
        result = None
        name = None
        if isinstance(cls, str):
            name = cls
        else:
            name = cls.__name__
        dbName = 'Db' + name
        module_name = "vs.models"
        import importlib
        module = importlib.import_module(module_name)
        srcClass = getattr(module, dbName)
        try:
            dbo = srcClass.objects.filter(pk=oid).filter(deleteFlag=True)
            if dbo:
                result = srcClass(dbo)
        except Exception as err:
            super().handleException(err)
        return result

    def getDeletedObjects(self, cls):
        result = []
        name = None
        if isinstance(cls, str):
            name = cls
        else:
            name = cls.__name__
        dbName = 'Db' + name
        module_name = "vs.models"
        import importlib
        module = importlib.import_module(module_name)
        srcClass = getattr(module, dbName)
        try:
            dbos = srcClass.objects.filter(deleteFlag=True)
            if dbos:
                for dbo in dbos:
                    result.append(srcClass(dbo))
        except Exception as err:
            super().handleException(err)
        return result
    
    def getObjects(self, cls):
        result = []
        name = None
        if isinstance(cls, str):
            name = cls
        else:
            name = cls.__name__
        dbName = 'Db' + name
        module_name = "vs.models"
        import importlib
        module = importlib.import_module(module_name)
        srcClass = getattr(module, dbName)
        try:
            dbos = srcClass.objects.exclude(deleteFlag=True)
            if dbos:
                for dbo in dbos:
                    result.append(srcClass(dbo))
        except Exception as err:
            super().handleException(err)
        return result
        
    def getObject(self, cls, oid):
        result = None
        name = None
        if isinstance(cls, str):
            name = cls
        else:
            name = cls.__name__
        dbName = 'Db' + name
        module_name = "vs.models"
        import importlib
        module = importlib.import_module(module_name)
        srcClass = getattr(module, dbName)
        try:
            dbo = srcClass.objects.filter(pk=oid).exclude(deleteFlag=True)
            if dbo:
                result = srcClass(dbo)
        except Exception as err:
            super().handleException(err)
        return result
        
    def getDeletedJobAssignments(self):
        result = []
        dbos = DbJobAssignment.objects.filter(deleteFlag=True)
        for dbo in dbos:
            result.append(JobAssignment(dbo))
        return result
    
    def getNewJob(self,  skill, uid, event, dbo=False):
        if dbo:
            eID = event.eventID
        else:
            eID =  event.getEventID()
        dbo = DbJob.objects.create(
            jobCreateUser=uid,
            jobUpdateUser=uid,
            skill_id=skill.getSkillID(),
            event_id=eid)
        return Job(dbo)

    def getJobs(self, event=None,dbo=False):
        result = []
        if event:
            if dbo:
                for db in DbJob.objects.exclude(deleteFlag=True)\
                .filter(event_id=event.eventID):
                    result.append(Job(db))
            else:
                for db in DbJob.objects.exclude(deleteFlag=True)\
                .filter(event_id=event.getEventID()):
                    result.append(Job(db))
        else:
            for db in DbJob.objects.exclude(deleteFlag=True):
                result.append(Job(db))
        return result
    
    def getJobsOverlapping(self, se1, dbo=False):
        result = []
        if dbo:
            eID = se1.eventID
            org = Organization(se1.organization)
        else:
            eID = se1.getEventID()
            org = se1.getOrganization()
        #print(se1)
        #result.extend(self.getJobs(se1))
        evts = self.getEvents(org,dbo=True)
        #print(str(len(evts)) + ' ' + str(evts))
        for se2 in evts:
            #print(str(se1.getEventID()) + ' ' + str(se2.eventID))
            if eID == se2.eventID:
                #print('Skipping ' + str(se2))
                continue
            #print('got ' + str(se2))
            if Utils.eventsOverlap(se1, se2, dbo=True):
                #print(se2.eventID) 
                result.extend(self.getJobs(se2, dbo=True))               
        return result
    
    def getNewSchedule(self, start, end, uid, org):
        dbo = DbSchedule.objects.create(scheduleStartDate=start,
                                        scheduleEndDate=end,
                                        scheduleCreateUser=uid,
                                        scheduleUpdateUser=uid,
                                        scheduleStatus_id=1,
                                        organization_id=org.getOrganizationID())
        result = Schedule(myDb=dbo)
        #print(result.__class__.__name__ + ' ' + str(isinstance(result, DbSchedule)))
        #print('getNewSchedule ' + str(org))
        result.setOrganization(org)
        return result 

    def getSchedule(self, oid=None,evt=None):
        result = None
        dbo = None
        if oid:
            dbo = DbSchedule.objects.exclude(deleteFlag=True).filter(pk=oid)
        elif evt:
            dboEvt = DbScheduleEvent.objects.exclude(deleteFlag=True)\
            .filter(pk=evt.eventID).first()
            if dboEvt:
                dbo = dboEvt.schedule
        else:
            raise MissingArgumentException('you must specify either oID or evt')
        if dbo:
            result = Schedule(dbo)
        return result
    
    def getSchedules(self, org=None,start=None,end=None):
        result = []
        dbos = None
        if start and end and org:
            dbos = DbSchedule.objects.exclude(deleteFlag=True)\
            .filter(organization_id=org.organizationID.value)\
            .filter(scheduleStartDate__lte=start).filter(scheduleEndDate__gte=end)  
        elif start and org:
            dbos = DbSchedule.objects.exclude(deleteFlag=True)\
            .filter(organization_id=org.organizationID.value)\
            .filter(scheduleStartDate__lte=start) 
        elif end and org:
            dbos = DbSchedule.objects.exclude(deleteFlag=True)\
            .filter(organization_id=org.organizationID.value)\
            .filter(scheduleEndDate__gte=end) 
        elif org:
            dbos = DbSchedule.objects.exclude(deleteFlag=True)\
            .filter(organization_id=org.organizationID.value)
        else:
            raise MissingArgumentException('you must specify org and, optionally, start and/or end')
        if dbos:
            for dbo in dbos:
                result.append(Schedule(dbo))
        return result

    def getRelationship(self, oid):
        result = None
        try:
            dbo = DbRelationship.objects.exclude(deleteFlag=True).filter(pk=oid).first()
            result = Relationship(dbo)
        except:
            pass
        return result
    
    def getNewRelationship(self, vol1,vol2, uid,org,typ=None):
        dbo = DbRelationship.objects.create(
                            relationshipCreateUser=uid,
                            relationshipUpdateUser=uid,
                            volunteerOne_id=vol1.getVolunteerID(),
                            volunteerTwo_id=vol2.getVolunteerID(),
                            organization_id=org.getOrganizationID())
        result = Relationship(dbo)
        if typ:
            result.setRelationshipType(typ)
            result.save()
        return result
    
    def getRelationships(self,org=None,vol=None):
        result = []
        #print(DbRelationship.objects.all())
        if org:
            for dbo in DbRelationship.objects.exclude(deleteFlag=True)\
            .filter(organization_id=org.getOrganizationID()):
                result.append(Relationship(dbo))
        elif vol:
            for dbo in DbRelationship.objects.exclude(deleteFlag=True)\
            .filter(Q(volunteerOne_id=vol.volunteerID) | \
                    Q(volunteerTwo_id=vol.volunteerID)):
                result.append(Relationship(dbo))
        else:
            raise MissingArgumentException('you must specify either org or vol')
        return result

    def getRelationshipTypes(self):
        result = []
        for dbo in DbRelationshipType.objects.all().order_by('relationshipTypeName'):
            result.append(RelationshipType(dbo))
        return result

    def getSkillRelationshipTypes(self):
        result = []
        for dbo in DbSkillRelationshipType.objects.all():
            result.append(SkillRelationshipType(dbo))
        return result
    
    def getConfigurationSet(self, uid):
        result = None
        if uid:
            dbo = DbConfigurationSet.objects.exclude(deleteFlag=True).filter(pk=uid).first()
            if dbo:
                result = ConfigurationSet(dbo)
        return result

    def getConfigurationSets(self, org=None):
        result =  []
        if org:
            dbos = DbConfigurationSet.objects.exclude(deleteFlag=True)\
            .filter(organization_id=org.organizationID.value) 
        else:
            dbos = DbConfigurationSet.objects.exclude(deleteFlag=True)
        for dbo in dbos:
            result.append(ConfigurationSet(dbo))
        if len(result) > 1:
            Collections.sort(result)
        return result  

    def getConfigurableProperty(self, oid):
        result = None
        if oid:
            dbo = DbConfigurableProperty.objects.exclude(deleteFlag=True).filter(pk=oid).first()
            if dbo:
                result = ConfigurableProperty(dbo)
        return result

    def getNewConfigurableProperty(self, name,uid,typ,value=None,desc=None):
        dbo = DbConfigurableProperty.objects.create(
                                propertyName=name,
                                propertyType=typ,
                                propertyCreateUser=uid,
                                propertyUpdateUser=uid)
        result = ConfigurableProperty(dbo)
        if value:
            result.setPropertyValue(value)
        if desc:
            result.setPropertyDescription(desc)
        if value or desc:
            result.save()
        return result 
    
    def getNewConfigurationSet(self,name, uid):
        result = ConfigurationSet(DbConfigurationSet(
            configurationSetName=name,
            configurationSetCreateUser=uid,
            configurationSetUpdateUser=uid))
        return result
    
    def getOpenDatesBefore(self, start, org):
        result = []
        dbos = DbScheduleEvent.objects.exclude(deleteFlag=True)\
        .filter(organization_id=org.getOrganizationID())\
        .filter(eventDate__lte=start)
        for dbo in dbos:
            if dbo.schedule_id:
                continue
            result.append(ScheduleEvent(dbo))
        return result  
      
    def deleteReport(self, rpt, uid):
        if rpt: 
            rpt.setReportUpdateUser(uid)
            fileName = self._getReportFileName(rpt)
            path = Path(fileName)
            if path.exists() and path.is_file(): 
                path.unlink(missing_ok=True)
            rpt.remove()
        
    def _getReportFileName(self, report): 
        result = VSSystemOption().get(Constants.PROPERTY_PDF_LOCATION)\
            + str(report.getReportURL())
        return result
     
    def _getScheduleStatusAccepted(self):
        if not ObjectFactory._scheduleStatusAccepted:
            for ss in self.getScheduleStatuses(): 
                if "Accepted".casefold() == ss.getScheduleStatusName().casefold(): 
                    ObjectFactory._scheduleStatusAccepted = ss
                    break
        return ObjectFactory._scheduleStatusAccepted
     
    def _getScheduleStatusRejected(self):
        if not ObjectFactory._scheduleStatusRejected:
            for ss in self.getScheduleStatuses(): 
                if "Rejected".casefold() == ss.getScheduleStatusName().casefold(): 
                    ObjectFactory._scheduleStatusRejected = ss
                    break
        return ObjectFactory._scheduleStatusAccepted
    
    def _getScheduleStatusNotSet(self):
        if not ObjectFactory._scheduleStatusNotSet: 
            for ss in self.getScheduleStatuses(): 
                if "Not set".casefold() == ss.getScheduleStatusName().casefold():
                    ObjectFactory._scheduleStatusNotSet = ss
                    break
        return ObjectFactory._scheduleStatusAccepted
    
    def getNewProjectStatus(self, desc=None, key=None):
        result = ProjectStatus(DbProjectStatus())
        if desc:
            result.setProjectStatusDescription(desc)
        if key:
            result.setProjectStatusType(key)
        result.save()
        return result

    def getProjectStatus(self, oid):
        result = None
        dbo = DbProjectStatus.objects.exclude(deleteFlag=True).filter(pk=oid).first()
        if dbo:
            result = ProjectStatus(dbo)
        return result

    def getDeletedProjectStatus(self, oid):
        result = None
        dbo = DbProjectStatus.objects.filter(deleteFlag=True).filter(pk=oid).first()
        if dbo:
            result = ProjectStatus(dbo)
        return result
    
    def getNewStateCode(self, code, name):
        dbo = DbStateCode.objects.create(sc_code=code,sc_name=name)
        return StateCode(dbo)

    def getStateCode(self, oid):
        result = None
        dbo = DbStateCode.objects.exclude(deleteFlag=True).filter(pk=oid).first()
        if dbo:
            result = StateCode(dbo)
        return result

    def getDeletedStateCode(self, oid):
        result = None
        dbo = DbStateCode.objects.filter(deleteFlag=True).filter(pk=oid).first()
        if dbo:
            result = StateCode(dbo)
        return result

    def getNewRecurrenceType(self, name=None, key=None):
        result = RecurrenceType(DbRecurrenceType())
        if name:
            result.recurrenceTypeName.value = name
        if key:
            result.recurrenceTypeKey.value = key
        result.save()
        return result

    def getRecurrenceType(self, oid):
        result = None
        dbo = DbRecurrenceType.objects.exclude(deleteFlag=True).filter(pk=oid).first()
        if dbo:
            result = RecurrenceType(dbo)
        return result

    def getDeletedRecurrenceType(self, oid):
        result = None
        dbo = DbRecurrenceType.objects.filter(deleteFlag=True).filter(pk=oid).first()
        if dbo:
            result = RecurrenceType(dbo)
        return result

    def getDeletedAddress(self, oid):
        result = None
        dbo = DbAddress.objects.filter(deleteFlag=True).filter(pk=oid).first()
        if dbo:
            result = Address(dbo)
        return result

    def getDeletedPrivilege(self, oid):
        result = None
        dbo = DbPrivilege.objects.filter(deleteFlag=True).filter(pk=oid).first()
        if dbo:
            result = Privilege(dbo)
        return result

    def getNewOrganization(self,name=None,uid=None):
        result = Organization(DbOrganization())
        if name:
            result.setOrganizationName(name)
        if uid:
            result.setOrganizationCreateUser(uid)
            result.setOrganizationUpdateUser(uid)
        return result

    def getDeletedOrganization(self, oid):
        result = None
        dbo = DbOrganization.objects.filter(deleteFlag=True).filter(pk=oid).first()
        if dbo:
            result = Organization(dbo)
        return result

    def getDeletedSecurityGroup(self, oid):
        result = None
        dbo = DbSecurityGroup.objects.filter(deleteFlag=True).filter(pk=oid).first()
        if dbo:
            result = SecurityGroup(dbo)
        return result

    def getNewLoginStatus(self, desc, typ):
        dbo = DbLoginStatus.objects.create(loginStatusDescription=desc,loginStatusType=typ)
        return LoginStatus(dbo)

    def getLoginStatus(self, oid):
        result = None
        dbo = DbLoginStatus.objects.exclude(deleteFlag=True).filter(pk=oid).first()
        if dbo:
            result = LoginStatus(dbo)
        return result

    def getDeletedLoginStatus(self, oid):
        result = None
        dbo = DbLoginStatus.objects.filter(deleteFlag=True).filter(pk=oid).first()
        if dbo:
            result = LoginStatus(dbo)
        return result

    def getNewLogin(self,login,uid,org):
        dbo = DbLogin.objects.create(
                                login=login,
                                loginCreateUser=uid,
                                loginUpdateUser=uid,
                                organization_id=org.getOrganizationID())
        return Login(dbo)

    def getDeletedLogin(self, oid):
        result = None
        dbo = DbLogin.objects.filter(deleteFlag=True).filter(pk=oid).first()
        if dbo:
            result = Login(dbo)
        return result

    def getNewAvailability(self, uid):
        dbo = DbAvailability.objects.create(availabilityCreateUser=uid,
                                            availabilityUpdateUser=uid)
        return Availability(dbo)

    def getDeletedAvailability(self, oid):
        result = None
        dbo = DbAvailability.objects.filter(deleteFlag=True).filter(pk=oid).first()
        if dbo:
            result = Availability(dbo)
        return result

    def getDeletedHousehold(self, oid):
        result = None
        dbo = DbHousehold.objects.filter(deleteFlag=True).filter(pk=oid).first()
        if dbo:
            result = Household(dbo)
        return result

    def getDeletedWorkAddress(self, oid):
        result = None
        #print('\nwa: oID ' + str(oid) + ' ' + str(DbWorkAddress.objects.all().first()))
        dbo = DbWorkAddress.objects.filter(deleteFlag=True).filter(pk=oid).first()
        if dbo:
            result = WorkAddress(dbo)
        return result

    def getNewSkillRelationshipType(self, name, key):
        dbo = DbSkillRelationshipType.objects.create(
                                        skillRelationshipTypeName=name,
                                        skillRelationshipTypeKey=key)
        return SkillRelationshipType(dbo)

    def getSkillRelationshipType(self,oid):
        result = None
        dbo = DbSkillRelationshipType.objects.exclude(deleteFlag=True).filter(pk=oid).first()
        if dbo:
            result = SkillRelationshipType(dbo)
        return result

    def getDeletedSkillRelationshipType(self,oid):
        result = None
        dbo = DbSkillRelationshipType.objects.filter(deleteFlag=True).filter(pk=oid).first()
        if dbo:
            result = SkillRelationshipType(dbo)
        return result

    def getDeletedSkill(self,oid):
        result = None
        dbo = DbSkill.objects.filter(deleteFlag=True).filter(pk=oid).first()
        if dbo:
            result = Skill(dbo)
        return result

    def getDeletedSkillRelationship(self,oid):
        result = None
        dbo = DbSkillRelationship.objects.filter(deleteFlag=True).filter(pk=oid).first()
        #print(DbSkillRelationship.objects.all())
        if dbo:
            result = SkillRelationship(dbo)
        return result
    
    def getNewActivity(self, name, uid, hours, description):
        dbo = DbActivity.objects.create(
                                    activityCreateUser=uid,
                                    activityUpdateUser=uid,
                                    name=name,
                                    hoursWorked=hours,
                                    description=description)
        return Activity(dbo)

    def getDeletedActivity(self, oid):
        result = None
        dbo = DbActivity.objects.filter(deleteFlag=True).filter(pk=oid).first()
        if dbo:
            result = Activity(dbo)
        return result

    def getDeletedTeam(self, oid):
        result = None
        dbo = DbTeam.objects.filter(deleteFlag=True).filter(pk=oid).first()
        if dbo:
            result = Team(dbo)
        return result

    def getNewTaskStatus(self, desc, typ):
        dbo = DbTaskStatus.objects.create(
                            taskStatusDescription=desc,
                            taskStatusType=typ)
        return TaskStatus(dbo)

    def getTaskStatus(self, oid):
        result = None
        dbo = DbTaskStatus.objects.exclude(deleteFlag=True).filter(pk=oid).first()
        if dbo:
            result = TaskStatus(dbo)
        return result

    def getDeletedTaskStatus(self, oid):
        result = None
        dbo = DbTaskStatus.objects.filter(deleteFlag=True).filter(pk=oid).first()
        if dbo:
            result = TaskStatus(dbo)
        return result

    def getNewProjectResource(self, name, uid, org, count=None, cost=None, reusable=None):
        dbo = DbProjectResource.objects.create(
                                name = name,
                                resourceCreateUser = uid,
                                resourceUpdateUser = uid,
                                organization_id=org.getOrganizationID())
        result = ProjectResource(dbo)
        if count:
            result.setCount(count)
        if cost:
            result.setCost(cost)
        if reusable:
            result.setReusable(reusable)
        if count is not None or cost is not None or reusable is not None:
            result.save()
        return result

    def getDeletedProjectResource(self, oid):
        result = None
        dbo = DbProjectResource.objects.filter(deleteFlag=True).filter(pk=oid).first()
        if dbo:
            result = ProjectResource(dbo)
        return result
    
    def getDeletedVolunteerSkill(self, oid):
        result = None
        dbo = DbVolunteerSkill.objects.filter(deleteFlag=True).filter(pk=oid).first()
        if dbo:
            result = VolunteerSkill(dbo)
        return result

    def getNewRelationshipType(self, name=None, key=None):
        result = RelationshipType(DbRelationshipType())
        if name:
            result.setRelationshipTypeName(name)
        if key:
            result.setRelationshipTypeKey(key)            
        return result

    def getRelationshipType(self, oid):
        result = None
        dbo = DbRelationshipType.objects.exclude(deleteFlag=True).filter(pk=oid).first()
        if dbo:
            result = RelationshipType(dbo)
        return result

    def getDeletedRelationshipType(self, oid):
        result = None
        dbo = DbRelationshipType.objects.filter(deleteFlag=True).filter(pk=oid).first()
        if dbo:
            result = RelationshipType(dbo)
        return result

    def getJob(self, oid):
        result = None
        dbo = DbJob.objects.exclude(deleteFlag=True).filter(pk=oid).first()
        if dbo:
            result = Job(dbo)
        return result

    def getDeletedJob(self, oid):
        result = None
        dbo = DbJob.objects.filter(deleteFlag=True).filter(pk=oid).first()
        if dbo:
            result = Job(dbo)
        return result

    def getDeletedProject(self, oid):
        result = None
        dbo = DbProject.objects.filter(deleteFlag=True).filter(pk=oid).first()
        if dbo:
            result = Project(dbo)
        return result

    def getDeletedTask(self, oid):
        result = None
        dbo = DbTask.objects.filter(deleteFlag=True).filter(pk=oid).first()
        if dbo:
            result = Task(dbo)
        return result

    def getDeletedResource(self, oid):
        result = None
        dbo = DbResource.objects.filter(deleteFlag=True).filter(pk=oid).first()
        if dbo:
            result = Resource(dbo)
        return result

    def getDeletedLocation(self, oid):
        result = None
        dbo = DbLocation.objects.filter(deleteFlag=True).filter(pk=oid).first()
        if dbo:
            result = Location(dbo)
        return result

    def getDeletedEventRecurrence(self, oid):
        result = None
        dbo = DbEventRecurrence.objects.filter(deleteFlag=True).filter(pk=oid).first()
        if dbo:
            result = EventRecurrence(dbo)
        return result
    
    def getNewScheduleEvent(self, name=None, uid=None, org=None):
        result = ScheduleEvent(DbScheduleEvent())
        if name:
            result.setEventName(name)
        if uid:
            result.setEventCreateUser(uid)
            result.setEventUpdateUser(uid)
        if org:
            result.setOrganization(org)
        return result

    def getScheduleEvent(self, oid):
        result = None
        dbo = DbScheduleEvent.objects.exclude(deleteFlag=True).filter(pk=oid).first()
        if dbo:
            result = ScheduleEvent(dbo)
        return result

    def getDeletedScheduleEvent(self, oid):
        result = None
        dbo = DbScheduleEvent.objects.filter(deleteFlag=True).filter(pk=oid).first()
        if dbo:
            result = ScheduleEvent(dbo)
        return result

    def getDeletedRelationship(self, oid):
        result = None
        dbo = DbRelationship.objects.filter(deleteFlag=True).filter(pk=oid).first()
        if dbo:
            result = Relationship(dbo)
        return result

    def getDeletedJobAssignment(self, oid):
        result = None
        dbo = DbJobAssignment.objects.filter(deleteFlag=True).filter(pk=oid).first()
        if dbo:
            result = JobAssignment(dbo)
        return result

    def getDeletedEventPreference(self, oid):
        result = None
        dbo = DbEventPreference.objects.filter(deleteFlag=True).filter(pk=oid).first()
        if dbo:
            result = EventPreference(dbo)
        return result


    def getDeletedConfigurableProperty(self, oid):
        result = None
        dbo = DbConfigurableProperty.objects.filter(deleteFlag=True).filter(pk=oid).first()
        if dbo:
            result = ConfigurableProperty(dbo)
        return result

    def getDeletedConfigurationSet(self, oid):
        result = None
        dbo = DbConfigurationSet.objects.filter(deleteFlag=True).filter(pk=oid).first()
        if dbo:
            result = ConfigurationSet(dbo)
        return result

    def getNewScheduleStatus(self, name, key):
        dbo = DbScheduleStatus.objects.create(scheduleStatusName=name,
                                              scheduleStatusKey=key)
        result = ScheduleStatus(dbo)
        return result

    def getScheduleStatus(self, oid):
        result = None
        dbo = DbScheduleStatus.objects.exclude(deleteFlag=True).filter(pk=oid).first()
        if dbo:
            result = ScheduleStatus(dbo)
        return result

    def getDeletedScheduleStatus(self, oid):
        result = None
        dbo = DbScheduleStatus.objects.filter(deleteFlag=True).filter(pk=oid).first()
        if dbo:
            result = ScheduleStatus(dbo)
        return result
    
    def getDeletedSchedule(self, oid):
        result = None
        dbo = DbSchedule.objects.filter(deleteFlag=True).filter(pk=oid).first()
        if dbo:
            result = Schedule(dbo)
        return result

    def getDeletedVolunteerSkillAssignment(self, oid):
        result = None
        dbo = DbVolunteerSkillAssignment.objects.filter(deleteFlag=True).filter(pk=oid).first()
        if dbo:
            result = VolunteerSkillAssignment(dbo)
        return result

    def getDeletedReport(self, oid):
        result = None
        dbo = DbReport.objects.filter(deleteFlag=True).filter(pk=oid).first()
        if dbo:
            result = Report(dbo)
        return result

    def getDeletedPassword(self, oid):
        result = None
        dbo = DbPassword.objects.filter(deleteFlag=True).filter(pk=oid).first()
        if dbo:
            result = Password(dbo)
        return result

    def getScheduleEvents(self):
        result = []
        for dbo in DbScheduleEvent.objects.exclude(deleteFlag=True):
            result.append(ScheduleEvent(dbo))
        return result

    def getProjectStatuses(self):
        result = []
        for dbo in DbProjectStatus.objects.exclude(deleteFlag=True):
            result.append(ProjectStatus(dbo))
        return result
    
    def getDeletedProjectStatuses(self):
        result = []
        for dbo in DbProjectStatus.objects.filter(deleteFlag=True):
            result.append(ProjectStatus(dbo))
        return result

    def getDeletedStateCodes(self):
        result = []
        for dbo in DbStateCode.objects.filter(deleteFlag=True):
            result.append(StateCode(dbo))
        return result

    def getDeletedRecurrenceTypes(self):
        result = []
        for dbo in DbRecurrenceType.objects.filter(deleteFlag=True):
            result.append(RecurrenceType(dbo))
        return result
    
    def getDeletedAddresses(self):
        result = []
        for dbo in DbAddress.objects.filter(deleteFlag=True):
            result.append(Address(dbo))
        return result
    
    def getDeletedPrivileges(self):
        result = []
        for dbo in DbPrivilege.objects.filter(deleteFlag=True):
            result.append(Privilege(dbo))
        return result

    def getDeletedOrganizations(self):
        result = []
        for dbo in DbOrganization.objects.filter(deleteFlag=True):
            result.append(Organization(dbo))
        return result

    def getDeletedLoginStatuses(self):
        result = []
        for dbo in DbLoginStatus.objects.filter(deleteFlag=True):
            result.append(LoginStatus(dbo))
        return result

    def getDeletedAvailabilities(self):
        result = []
        for dbo in DbAvailability.objects.filter(deleteFlag=True):
            result.append(Availability(dbo))
        return result

    def getDeletedHouseholds(self):
        result = []
        for dbo in DbHousehold.objects.filter(deleteFlag=True):
            result.append(Household(dbo))
        return result

    def getDeletedWorkAddresses(self):
        result = []
        for dbo in DbWorkAddress.objects.filter(deleteFlag=True):
            result.append(WorkAddress(dbo))
        return result

    def getDeletedSkillRelationshipTypes(self):
        result = []
        for dbo in DbSkillRelationshipType.objects.filter(deleteFlag=True):
            result.append(SkillRelationshipType(dbo))
        return result

    def getDeletedSkillRelationships(self):
        result = []
        for dbo in DbSkillRelationship.objects.filter(deleteFlag=True):
            result.append(SkillRelationship(dbo))
        return result

    def getDeletedActivities(self):
        result = []
        for dbo in DbActivity.objects.filter(deleteFlag=True):
            result.append(Activity(dbo))
        return result

    def getDeletedVolunteers(self):
        result = []
        for dbo in DbVolunteer.objects.filter(deleteFlag=True):
            result.append(Volunteer(dbo))
        return result

    def getTaskStatuses(self):
        result = []
        for dbo in DbTaskStatus.objects.exclude(deleteFlag=True):
            result.append(TaskStatus(dbo))
        return result

    def getDeletedTaskStatuses(self):
        result = []
        for dbo in DbTaskStatus.objects.filter(deleteFlag=True):
            result.append(TaskStatus(dbo))
        return result

    def getDeletedProjectResources(self):
        result = []
        for dbo in DbProjectResource.objects.filter(deleteFlag=True):
            result.append(ProjectResource(dbo))
        return result

    def getDeletedRelationshipTypes(self):
        result = []
        for dbo in DbRelationshipType.objects.filter(deleteFlag=True):
            result.append(RelationshipType(dbo))
        return result

    def getDeletedJobs(self):
        result = []
        for dbo in DbJob.objects.filter(deleteFlag=True):
            result.append(Job(dbo))
        return result

    def getDeletedProjects(self):
        result = []
        for dbo in DbProject.objects.filter(deleteFlag=True):
            result.append(Project(dbo))
        return result

    def getDeletedEventRecurrences(self):
        result = []
        for dbo in DbEventRecurrence.objects.filter(deleteFlag=True):
            result.append(EventRecurrence(dbo))
        return result

    def getDeletedScheduleEvents(self):
        result = []
        for dbo in DbScheduleEvent.objects.filter(deleteFlag=True):
            result.append(ScheduleEvent(dbo))
        return result
    
    def getEventJoinToResource(self, evt, res):
        dbo = DbEventJoinToResource.objects.exclude(deleteFlag=True)\
        .filter(event_id=evt.getEventID()).filter(resource_id=res.getResourceID())
        return EventJoinToResource(dbo)

    def getEventJoinToResources(self,evt=None):
        result = []
        dbos = None
        if evt:
            dbos = DbEventJoinToResource.objects.filter(event_id=evt.getEventID())
        else:
            dbos = DbEventJoinToResource.objects.all()
        for dbo in dbos:
            result.append(EventJoinToResource(dbo))
        return result

    def getDeletedRelationships(self):
        result = []
        for dbo in DbRelationship.objects.filter(deleteFlag=True):
            result.append(Relationship(dbo))
        return result

    def getDeletedEventPreferences(self):
        result = []
        for dbo in DbEventPreference.objects.filter(deleteFlag=True):
            result.append(EventPreference(dbo))
        return result

    def getDeletedConfigurableProperties(self):
        result = []
        for dbo in DbConfigurableProperty.objects.filter(deleteFlag=True):
            result.append(ConfigurableProperty(dbo))
        return result

    def getDeletedConfigurationSets(self):
        result = []
        for dbo in DbConfigurationSet.objects.filter(deleteFlag=True):
            result.append(ConfigurationSet(dbo))
        return result

    def getDeletedScheduleStatuses(self):
        result = []
        for dbo in DbScheduleStatus.objects.filter(deleteFlag=True):
            result.append(ScheduleStatus(dbo))
        return result

    def getDeletedSchedules(self):
        result = []
        for dbo in DbSchedule.objects.filter(deleteFlag=True):
            result.append(Schedule(dbo))
        return result
    
    def getDeletedReports(self):
        result = []
        for dbo in DbReport.objects.filter(deleteFlag=True):
            result.append(Report(dbo))
        return result

    def getDeletedPasswords(self):
        result = []
        for dbo in DbPassword.objects.filter(deleteFlag=True):
            result.append(Report(dbo))
        return result


class OrganizationHolder(ABC):
    
    SYSTEM_DEFAULT_ORGANIZATION_NAME = "$$default$$"

    _organization = None

    @staticmethod
    def getOrganization():
        if not OrganizationHolder._organization:
            orgs = ObjectFactory().getOrganizations()
            if len(orgs) == 2:
                for org in orgs:
                    if org.getName() == OrganizationHolder.SYSTEM_DEFAULT_ORGANIZATION_NAME:
                        continue                           
                    OrganizationHolder._organization = org
                    break
        return OrganizationHolder._organization
    
    @staticmethod
    def setOrganization(org):
        OrganizationHolder._organization = org
    