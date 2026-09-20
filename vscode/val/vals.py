from abc import abstractmethod,ABC
from vs.models import DbProjectStatus,DbTaskStatus,DbLoginStatus,\
DbRelationshipType,DbRecurrenceType,DbSkillRelationshipType,DbStateCode,\
DbScheduleStatus
from vscode.att.attribute import Attribute,StringAttribute,IntegerAttribute,BooleanAttribute
from vscode.base.base import BusinessObjectBase
from vscode.utils.exceptions import InvalidArgumentException 


class ValueTableManager(ABC):
    _instance = None
    tables  = {}

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            # Create the instance if it doesnt exist yet
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        pass

    def getValues(self, name):
        result = []
        mp = self._getMap(name)
        if mp:
            for vte in mp.values():
                result.append(vte.getValue())
        return result

    def getValueEntries(self, name):
        result = []
        mp = self._getMap(name)
        if mp:
            for vte in mp.values():
                result.append(vte)
        return result

    def getValue(self, table='String', key=0):
        result = None
        #print(str(type(table)) +   + str(type(key)))
        if not table:
            raise InvalidArgumentException("getValue(table, key) " +
                    "table was null")
        elif not isinstance(table, str):
            raise InvalidArgumentException("getValue(table, key) " +
                    "table must be a String not " + table.__class__.__name__ )
        mp = self._getMap(table)
        #print(mp)
        if mp:
            result = mp.get(key)
            #print(table +   +str(len(mp)))
        #result = ValueTableManager.tables[table][key]
        #print(ValueTableManager()._getMap(LoginStatus))
        return result

    def _getMap(self, name):
        if not name or not isinstance(name, str):
            raise InvalidArgumentException(str(name) +  + str(type(name)))
        mp = ValueTableManager.tables.get(name)
        lmp = None
        if not mp:
            #if name is LoginStatus:
            #   print(loading LS)
            vtClass = globals().get(name)
            if vtClass:
                mp = vtClass()
                lmp = mp.load()
                ValueTableManager.tables[name] = lmp
                #print(lmp)
        else:
            lmp = mp
            #print(lmp)
        return lmp

class ValueTable(BusinessObjectBase):
    
    def __init__(self):
        super().__init__()

    @abstractmethod
    def getValue(self):
        pass

class ProjectStatus(ValueTable):
    DEFINED = 1
    ON_HOLD = 2
    UNDERWAY = 3
    COMPLETE = 4
    CANCELED = 5
    MINIMUM_TYPE = DEFINED
    MAXIMUM_TYPE = CANCELED


    def __init__(self, myDb=None):
        super().__init__()
        self.myDb = myDb
        self.projectStatusID = IntegerAttribute("projectStatusID")
        self.projectStatusType = IntegerAttribute("projectStatusType")
        self.projectStatusDescription = StringAttribute("projectStatusDescription")
        self.deleteFlag = BooleanAttribute('deleteFlag')

        self.projectStatusID.setHasMaximum(False)
        self.projectStatusID.setHasMinimum(True)
        self.projectStatusID.setMinimum(1)

        self.projectStatusType.setHasMaximum(True)
        self.projectStatusType.setHasMinimum(True)
        self.projectStatusType.setMinimum(ProjectStatus.MINIMUM_TYPE)
        self.projectStatusType.setMaximum(ProjectStatus.MAXIMUM_TYPE)

        self.projectStatusDescription.setAllSpacesAllowed(False)
        self.projectStatusDescription.setHasMaximumLength(True)
        self.projectStatusDescription.setHasMinimumLength(True)
        self.projectStatusDescription.setMixedCase(True)
        self.projectStatusDescription.setNullStringAllowed(False)
        self.projectStatusDescription.setMaximumLength(100)
        self.projectStatusDescription.setMinimumLength(1)
        
        self.deleteFlag.value = False
        if myDb:
            self.fromDb()
        
    def getProjectStatusDescription(self):
        return self.projectStatusDescription.getValue()

    def setProjectStatusDescription(self, projectStatusDescription):
        self.projectStatusDescription.setValue(projectStatusDescription)
        
    def getValue(self):
        return self.getProjectStatusDescription()
    
    def load(self):
        result = {}
        for dbps in DbProjectStatus.objects.all():
            ps = ProjectStatus(dbps)
            ps.fromDb()
            #print(ps)
            result[dbps.projectStatusType] = ps
        #print(result)        
        return result
    
    def getDisplayString(self):
        result = 'ProjectStatus{projectStatusID: '
        if not self.projectStatusID:
            result += None
        else:
            result += str(self.projectStatusID.value)
            
        result += ', projectStatusType:'    
        if not self.projectStatusType:
            result += None
        else:
            result += str(self.projectStatusType.value)
            
        result += ', projectStatusDescription:' 
        if not self.projectStatusDescription:
            result += None
        else:
            result += str(self.projectStatusType.value)
        return result
        
    def getProjectStatusType(self):
        return self.projectStatusType.getValue()
    
    def setProjectStatusType(self, projectStatusType):
        self.projectStatusType.setValue(projectStatusType)
      
    def getProjectStatusID(self):
        return self.projectStatusID.value
    
    def setProjectStatusID(self, projectStatusID):
        self.projectStatusID.setValue(projectStatusID)
      
    def __str__(self):
        return self.getDisplayString()
    

    def toDb(self):
        for name,att in self.__dict__.items():
            a = att
            if isinstance(att, Attribute):
                a = att.value
            self.myDb.__dict__[name] = a
    
    def fromDb(self):
        for name,att in self.myDb.__dict__.items():
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
        BusinessObjectBase.validateAttributes(atts)
        
    def save(self):
        self.toDb()
        self.myDb.save()       
        self.fromDb()
    
    def delete(self):
            self.deleteFlag.value = True
            self.save()
    
    def remove(self):
            self.myDb.delete()
    
    def getAttributeList(self):  
        return [
        self.projectStatusID,
        self.projectStatusType,
        self.projectStatusDescription
        ]
        
class TaskStatus(ValueTable):
    NOT_STARTED = 1
    ON_HOLD = 2
    ASSIGNED = 3
    ACTIVE = 4
    COMPLETE = 5
    CANCELED = 6
    MINIMUM_TYPE = NOT_STARTED
    MAXIMUM_TYPE = CANCELED

    def __init__(self, myDb=None):
        self.myDb = myDb
        self.taskStatusID = IntegerAttribute("taskStatusID")
        self.taskStatusType = IntegerAttribute("taskStatusType")
        self.taskStatusDescription = StringAttribute("taskStatusDescription")
        self.deleteFlag = BooleanAttribute('deleteFlag')
        super().__init__()
        if myDb:
            self.fromDb()

        self.taskStatusID.setHasMaximum(False)
        self.taskStatusID.setHasMinimum(True)
        self.taskStatusID.setMinimum(1)

        self.taskStatusType.setHasMaximum(True)
        self.taskStatusType.setHasMinimum(True)
        self.taskStatusType.setMaximum(TaskStatus.MAXIMUM_TYPE)
        self.taskStatusID.setMinimum(TaskStatus.MINIMUM_TYPE)

        self.taskStatusDescription.setAllSpacesAllowed(False)
        self.taskStatusDescription.setHasMaximumLength(True)
        self.taskStatusDescription.setHasMinimumLength(True)
        self.taskStatusDescription.setMixedCase(True)
        self.taskStatusDescription.setNullStringAllowed(False)
        self.taskStatusDescription.setMaximumLength(100)
        self.taskStatusDescription.setMinimumLength(1)
        
        self.deleteFlag.value = False

    def getTaskStatusDescription(self):
        return self.taskStatusDescription.getValue()

    def setTaskStatusDescription(self, taskStatusDescription):
        self.taskStatusDescription.setValue(taskStatusDescription)
        
    def getValue(self):
        return self.getTaskStatusDescription()
        
    def load(self):
        result = {}
        for dbps in DbTaskStatus.objects.all():
            ps = TaskStatus(dbps)
            ps.fromDb()
            #print(ps)
            result[dbps.taskStatusType] = ps
        #print(result)        
        return result
    
    def getDisplayString(self):
        result = 'TaskStatus{TaskStatusID='
        if not self.taskStatusID:
            result += None
        else:
            result += str(self.taskStatusID.value)
            
        result += ', taskStatusType='    
        if not self.taskStatusType:
            result += None
        else:
            result += str(self.taskStatusType.value)
            
        result += ', taskStatusDescription=' 
        if not self.taskStatusDescription:
            result += None
        else:
            result += str(self.taskStatusDescription.value)
        return result    

    def getTaskStatusType(self):
        return self.taskStatusType.getValue()

    def setTaskStatusType(self, uid):
        self.taskStatusType.setValue(uid)
        
    def getTaskStatusID(self):
        return self.taskStatusID.getValue()

    def __str__(self):
        return self.getDisplayString()
    
    def toDb(self):
        for name,att in self.__dict__.items():
            a = att
            if isinstance(att, Attribute):
                a = att.value
            self.myDb.__dict__[name] = a
    
    def fromDb(self):
        for name,att in self.myDb.__dict__.items():
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
        BusinessObjectBase.validateAttributes(atts)
        
    def save(self):
        self.toDb()
        self.myDb.save()       
        self.fromDb()
    
    def delete(self):
            self.deleteFlag.value = True
            self.save()
    
    def remove(self):
            self.myDb.delete()
    
    def getAttributeList(self):  
        return [
        self.taskStatusID,
        self.taskStatusType,
        self.taskStatusDescription
        ]
        
class LoginStatus(ValueTable): 

    STATUS_READY = 1
    STATUS_LOCKED = 2
    STATUS_RESET = 3
    STATUS_EXPIRED = 4
    READY = "Ready"
    LOCKED = "Locked"
    RESET = "Reset"
    EXPIRED = "Expired"
    MINIMUM_STATUS = STATUS_READY
    MAXIMUM_STATUS = STATUS_EXPIRED
    
    
    def __init__(self, myDb=None):
        self.myDb = myDb
        super().__init__()
        self.loginStatusID = IntegerAttribute("loginStatusID")
        self.loginStatusType = IntegerAttribute("loginStatusType")
        self.loginStatusDescription = StringAttribute("loginStatusDescription")
        self.deleteFlag = BooleanAttribute('deleteFlag')

        self.loginStatusID.setHasMaximum(False)
        self.loginStatusID.setHasMinimum(True)
        self.loginStatusID.setMinimum(1)

        self.loginStatusType.setHasMaximum(True)
        self.loginStatusType.setHasMinimum(True)
        self.loginStatusType.setMinimum(LoginStatus.MINIMUM_STATUS)
        self.loginStatusType.setMaximum(LoginStatus.MAXIMUM_STATUS)

        self.loginStatusDescription.setAllSpacesAllowed(False)
        self.loginStatusDescription.setHasMaximumLength(True)
        self.loginStatusDescription.setHasMinimumLength(True)
        self.loginStatusDescription.setMixedCase(True)
        self.loginStatusDescription.setNullStringAllowed(False)
        self.loginStatusDescription.setMaximumLength(100)
        self.loginStatusDescription.setMinimumLength(1)
        
        self.deleteFlag.value = False
        
        if myDb:
            self.fromDb()
        
    def load(self):
        result = {}
        for dbps in DbLoginStatus.objects.all():
            ps = LoginStatus(dbps)
            ps.fromDb()
            #print(ps)
            result[dbps.loginStatusID] = ps
        #print(result)        
        return result
    
    def getDisplayString(self):
        result = 'LoginStatus{LoginStatusID='
        if not self.loginStatusID:
            result += None
        else:
            result += str(self.loginStatusID.value)
            
        result += ', LoginStatusType='
        if not self.loginStatusType:
            result += None
        else:
            result += str(self.loginStatusType.value)
            
        result += ', loginStatusDescription=' 
        if not self.loginStatusDescription:
            result += None
        else:
            result += str(self.loginStatusDescription.value)
        result += 'deleteFlag=' + str(self.deleteFlag)
        return result    

    def getLoginStatusID(self):
        return self.loginStatusID.getValue()
    
    def setLoginStatusID(self, loginStatusID):
        self.loginStatusID.setValue(loginStatusID)
        
    def getLoginStatusType(self):
        return self.loginStatusType.getValue()

    def setLoginStatusType(self, loginStatusType):
        self.loginStatusType.setValue(loginStatusType)

    def getLoginStatusDescription(self):
        return self.loginStatusDescription.getValue()
    
    def setLoginStatusDescription(self, value):
        self.loginStatusDescription.setValue(value)
        
    def __str__(self):
        return self.getDisplayString()
    
    def toDb(self):
        for name,att in self.__dict__.items():
            a = att
            if isinstance(att, Attribute):
                a = att.value
            self.myDb.__dict__[name] = a
    
    def fromDb(self):
        for name,att in self.myDb.__dict__.items():
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
        BusinessObjectBase.validateAttributes(atts)
        
    def save(self):
        self.toDb()
        self.myDb.save()       
        self.fromDb()
    
    def delete(self):
            self.deleteFlag.value = True
            self.save()
    
    def remove(self):
            self.myDb.delete()
    
    def getAttributeList(self):  
        return [
        self.loginStatusID,
        self.loginStatusType,
        self.loginStatusDescription
        ]
        
    def getValue(self):
        return self.getLoginStatusDescription()
    
class RecurrenceType(ValueTable):
    DAILY = 1
    WEEKLY = 2
    MONTHLY_DATE = 3
    MONTHLY_DAY = 4
    YEARLY = 5
    MINIMUM = DAILY
    MAXIMUM = YEARLY

    def __init__(self, myDb=None):    
        super().__init__()
        
        self.myDb = myDb

        self.recurrenceTypeID = IntegerAttribute("recurrenceTypeID")
        self.recurrenceTypeKey = IntegerAttribute("recurrenceTypeKey")
        self.recurrenceTypeName = StringAttribute("recurrenceTypeName")
        self.deleteFlag = BooleanAttribute('deleteFlag')

        self.recurrenceTypeID.setHasMaximum(False)
        self.recurrenceTypeID.setHasMinimum(True)
        self.recurrenceTypeID.setMinimum(1)

        self.recurrenceTypeKey.setHasMaximum(False)
        self.recurrenceTypeKey.setHasMinimum(True)
        self.recurrenceTypeKey.setMinimum(1)

        self.recurrenceTypeName.setAllSpacesAllowed(False)
        self.recurrenceTypeName.setHasMaximumLength(True)
        self.recurrenceTypeName.setHasMinimumLength(True)
        self.recurrenceTypeName.setMixedCase(True)
        self.recurrenceTypeName.setNullStringAllowed(False)
        self.recurrenceTypeName.setMaximumLength(100)
        self.recurrenceTypeName.setMinimumLength(1)
        
        self.deleteFlag.value = False    
        
    def load(self):
        result = {}
        for dbps in DbRecurrenceType.objects.all():
            ps = RecurrenceType(dbps)
            ps.fromDb()
            #print(ps)
            result[dbps.recurrenceTypeKey] = ps
        #print(result)        
        return result
    
    def getDisplayString(self):
        result = 'RecurrenceType{recurrenceTypeID='
        if not self.recurrenceTypeID.value:
            result += 'None'
        else:
            result += str(self.recurrenceTypeID.value)
            
        result += ', recurrenceTypeKey='    
        if not self.recurrenceTypeKey.value:
            result += 'None'
        else:
            result += str(self.recurrenceTypeKey.value)
            
        result += ', recurrenceTypeName=' 
        if not self.recurrenceTypeName.value:
            result += 'None'
        else:
            result += str(self.recurrenceTypeName.value)
        return result   
    
    def getRecurrenceTypeKey(self):
        return self.recurrenceTypeKey.getValue()
    
    def setRecurrenceTypeKey(self, recurrenceTypeKey):
        self.recurrenceTypeKey.setValue(recurrenceTypeKey)

    def setRecurrenceTypeName(self, name):
        self.recurrenceTypeName.setValue(name)
    
    def getRecurrenceTypeName(self):
        return self.recurrenceTypeName.getValue()
    
    def getRecurrenceTypeID(self):
        return self.recurrenceTypeID.getValue()
    
    def setRecurrenceTypeID(self, recurrenceTypeID):
        self.recurrenceTypeID.setValue(recurrenceTypeID)

    def __str__(self):   
        return self.getDisplayString()
    
    def toDb(self):
        for name,att in self.__dict__.items():
            a = att
            if isinstance(att, Attribute):
                a = att.value
            self.myDb.__dict__[name] = a
    
    def fromDb(self):
        for name,att in self.myDb.__dict__.items():
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
        BusinessObjectBase.validateAttributes(atts)
        
    def save(self):
        self.toDb()
        self.myDb.save()       
        self.fromDb()
    
    def delete(self):
            self.deleteFlag.value = True
            self.save()
    
    def remove(self):
            self.myDb.delete()
    
    def getAttributeList(self):  
        return [        
            self.recurrenceTypeID,
            self.recurrenceTypeKey,
            self.recurrenceTypeName
        ]
        
    def getValue(self):
        return self.getRecurrenceTypeName()

class RelationshipType(ValueTable):

    TOGETHER_REQUIRED_VAL = 1
    SEPARATE_REQUIRED_VAL = 2
    TOGETHER_PREFERRED_VAL = 3
    SEPARATE_PREFERRED_VAL = 4
    MINIMUM_TYPE = TOGETHER_REQUIRED_VAL
    MAXIMUM_TYPE = SEPARATE_PREFERRED_VAL

    def __init__(self, myDb=None):
        super().__init__()
        self.myDb = myDb
        self.relationshipTypeID = IntegerAttribute("relationshipTypeID")
        self.relationshipTypeKey = IntegerAttribute("relationshipTypeKey")
        self.relationshipTypeName = StringAttribute("relationshipTypeName")
        self.deleteFlag = BooleanAttribute('deleteFlag')

        self.relationshipTypeID.setHasMaximum(False)
        self.relationshipTypeID.setHasMinimum(True)
        self.relationshipTypeID.setMinimum(1)

        self.relationshipTypeKey.setHasMaximum(False)
        self.relationshipTypeKey.setHasMinimum(True)
        self.relationshipTypeKey.setMinimum(1)

        self.relationshipTypeName.setAllSpacesAllowed(False)
        self.relationshipTypeName.setHasMaximumLength(True)
        self.relationshipTypeName.setHasMinimumLength(True)
        self.relationshipTypeName.setMixedCase(True)
        self.relationshipTypeName.setNullStringAllowed(False)
        self.relationshipTypeName.setMaximumLength(100)
        self.relationshipTypeName.setMinimumLength(1)
        
        self.deleteFlag.value = False
        if myDb:
            self.fromDb()

    def load(self):
        result = {}
        for dbps in DbRelationshipType.objects.all():
            ps = RelationshipType(dbps)
            ps.fromDb()
            #print(ps)
            result[dbps.relationshipTypeKey] = ps
        #print(result)        
        return result
    
    def getDisplayString(self):
        result = 'RelationshipType{relationshipTypeID='
        if not self.relationshipTypeID.value:
            result += 'None'
        else:
            result += str(self.relationshipTypeID.value)
            
        result += ', relationshipTypeKey='    
        if not self.relationshipTypeKey.value:
            result += 'None'
        else:
            result += str(self.relationshipTypeKey.value)
            
        result += ', relationshipTypeName=' 
        if not self.relationshipTypeName.value:
            result += 'None'
        else:
            result += str(self.relationshipTypeName.value)
        return result   

    @staticmethod
    def getRelationshipTypeNameForId(tid):
        result = ''
        table = ValueTableManager().getValueEntries(RelationshipType)
        if table:
            for rt in table:
                if rt.getRelationshipTypeID() == id:
                    result = rt.getValue()
                    break
        return result
    
    def getRelationshipTypeKey(self):
        return self.relationshipTypeKey.getValue()
    

    def setRelationshipTypeKey(self, relationshipTypeKey):
        self.relationshipTypeKey.setValue(relationshipTypeKey)
        
    def setRelationshipTypeName(self, name):
        self.relationshipTypeName.setValue(name)
    
    def getRelationshipTypeName(self):
        return self.relationshipTypeName.getValue()
    

    def getRelationshipTypeID(self):
        return self.relationshipTypeID.getValue()

    def setRelationshipTypeID(self, relationshipTypeID):
        self.relationshipTypeID.setValue(relationshipTypeID)
        
    def __str__(self):   
        return self.getDisplayString()
    
    def toDb(self):
        for name,att in self.__dict__.items():
            a = att
            if isinstance(att, Attribute):
                a = att.value
            self.myDb.__dict__[name] = a
    
    def fromDb(self):
        for name,att in self.myDb.__dict__.items():
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
        BusinessObjectBase.validateAttributes(atts)
        
    def save(self):
        self.toDb()
        self.myDb.save()       
        self.fromDb()
    
    def delete(self):
        self.deleteFlag.value=True
        self.save()
            
    def remove(self):
            self.myDb.delete()
    
    def getAttributeList(self):  
        return [ 
        self.relationshipTypeID,
        self.relationshipTypeKey,
        self.relationshipTypeName
        ]
        
    def getValue(self):
        return self.getRelationshipTypeName()
    
    @staticmethod
    def areMutuallyExcluded(type1, type2):
        result = False
        if (type1 == RelationshipType.TOGETHER_REQUIRED_VAL and type2 == RelationshipType.SEPARATE_REQUIRED_VAL):
            result = True
        elif (type2 == RelationshipType.TOGETHER_REQUIRED_VAL and type1 == RelationshipType.SEPARATE_REQUIRED_VAL):
            result = True
        elif (type1 == RelationshipType.TOGETHER_REQUIRED_VAL and type2 == RelationshipType.SEPARATE_PREFERRED_VAL):
            result = True
        elif (type2 == RelationshipType.TOGETHER_REQUIRED_VAL and type1 == RelationshipType.SEPARATE_PREFERRED_VAL):
            result = True
        elif (type1 == RelationshipType.TOGETHER_PREFERRED_VAL and type2 == RelationshipType.SEPARATE_REQUIRED_VAL):
            result = True
        elif (type2 == RelationshipType.TOGETHER_PREFERRED_VAL and type1 == RelationshipType.SEPARATE_REQUIRED_VAL):
            result = True
        elif (type1 == RelationshipType.TOGETHER_PREFERRED_VAL and type2 == RelationshipType.SEPARATE_PREFERRED_VAL):
            result = True
        elif (type2 == RelationshipType.TOGETHER_PREFERRED_VAL and type1 == RelationshipType.SEPARATE_PREFERRED_VAL):
            result = True
        return result
    
class SkillRelationshipType(ValueTable):

    TOGETHER_ALLOWED_VAL = 1
    SEPARATE_REQUIRED_VAL = 2
    MINIMUM_TYPE = TOGETHER_ALLOWED_VAL
    MAXIMUM_TYPE = SEPARATE_REQUIRED_VAL

    def __init__(self, myDb=None):
        super().__init__()
        
        
        self.skillRelationshipTypeID = IntegerAttribute("skillRelationshipTypeID")
        self.skillRelationshipTypeKey = IntegerAttribute("skillRelationshipTypeKey")
        self.skillRelationshipTypeName = StringAttribute("skillRelationshipTypeName")
        self.deleteFlag = BooleanAttribute('deleteFlag')
        
        self.skillRelationshipTypeID.setHasMaximum(False)
        self.skillRelationshipTypeID.setHasMinimum(True)
        self.skillRelationshipTypeID.setMinimum(1)

        self.skillRelationshipTypeKey.setHasMaximum(False)
        self.skillRelationshipTypeKey.setHasMinimum(True)
        self.skillRelationshipTypeKey.setMinimum(1)

        self.skillRelationshipTypeName.setAllSpacesAllowed(False)
        self.skillRelationshipTypeName.setHasMaximumLength(True)
        self.skillRelationshipTypeName.setHasMinimumLength(True)
        self.skillRelationshipTypeName.setMixedCase(True)
        self.skillRelationshipTypeName.setNullStringAllowed(False)
        self.skillRelationshipTypeName.setMaximumLength(100)
        self.skillRelationshipTypeName.setMinimumLength(1)
        
        self.deleteFlag.value = False
        self.myDb=myDb
        if myDb:
            self.fromDb()  

    def load(self):
        result = {}
        for dbps in DbSkillRelationshipType.objects.all():
            ps = SkillRelationshipType(dbps)
            ps.fromDb()
            #print(ps)
            result[dbps.skillRelationshipTypeKey] = ps
        #print(result)        
        return result
    
    def getDisplayString(self):
        result = 'SkillRelationshipType{skillRelationshipTypeKeyID='
        if not self.skillRelationshipTypeID.value:
            result += None
        else:
            result += str(self.skillRelationshipTypeID.value)
            
        result += ', skillRelationshipTypeKey='
        if not self.skillRelationshipTypeKey.value:
            result += None
        else:
            result += str(self.skillRelationshipTypeKey.value)
            
        result += ', skillRelationshipTypeName='
        if not self.skillRelationshipTypeName.value:
            result += None
        else:
            result += str(self.skillRelationshipTypeName.value)
        return result   

    def getRelationshipTypeNameForId(self, key):
        result = ''
        entries = ValueTableManager().getValueEntries(SkillRelationshipType)
        for rt in entries:
            if (rt.getSkillRelationshipTypeID() == key):
                result = rt.getValue()
                break
        return result
    
    def getSkillRelationshipTypeKey(self):
        return self.skillRelationshipTypeKey.getValue()
    
    def setSkillRelationshipTypeKey(self, skillRelationshipTypeKey):
        self.skillRelationshipTypeKey.setValue(skillRelationshipTypeKey)

    def setSkillRelationshipTypeName(self, name):
        self.skillRelationshipTypeName.setValue(name)
    
    def getSkillRelationshipTypeName(self):
        return self.skillRelationshipTypeName.getValue()
    
    def getSkillRelationshipTypeID(self):
        return self.skillRelationshipTypeID.getValue()
    
    def setSkillRelationshipTypeID(self, skillRelationshipTypeID):
        self.skillRelationshipTypeID.setValue(skillRelationshipTypeID)

    def __str__(self):
        return self.getDisplayString()
    
    def toDb(self):
        for name,att in self.__dict__.items():
            a = att
            if isinstance(att, Attribute):
                a = att.value
            self.myDb.__dict__[name] = a
    
    def fromDb(self):
        for name,att in self.myDb.__dict__.items():
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
        BusinessObjectBase.validateAttributes(atts)
        
    def save(self):
        self.toDb()
        self.myDb.save()       
        self.fromDb()
    
    def delete(self):
            self.deleteFlag.value = True
            self.save()
    
    def remove(self):
            self.myDb.delete()
    
    def getAttributeList(self):  
        return [ 
        self.skillRelationshipTypeID,
        self.skillRelationshipTypeKey,
        self.skillRelationshipTypeName
        ]
        
    def getValue(self):
        return self.skillRelationshipTypeName.getValue()

class StateCode(ValueTable):
    
    def __init__(self, myDb=None):
        super().__init__()
        self.myDb = myDb
        self.sc_ID = IntegerAttribute("sc_id")
        self.sc_name = StringAttribute("sc_name")
        self.sc_code = StringAttribute("sc_code")
        self.deleteFlag = BooleanAttribute('deleteFlag')


        self.sc_id.setHasMaximum(False)
        self.sc_id.setHasMinimum(True)
        self.sc_id.setMinimum(1)

        self.sc_name.setAllSpacesAllowed(False)
        self.sc_name.setHasMaximumLength(True)
        self.sc_name.setHasMinimumLength(True)
        self.sc_name.setMixedCase(True)
        self.sc_name.setNullStringAllowed(False)
        self.sc_name.setMaximumLength(100)
        self.sc_name.setMinimumLength(1)
        
        self.sc_code.setAllSpacesAllowed(False)
        self.sc_code.setHasMaximumLength(True)
        self.sc_code.setHasMinimumLength(True)
        self.sc_code.setMixedCase(True)
        self.sc_code.setNullStringAllowed(False)
        self.sc_code.setMaximumLength(2)
        self.sc_code.setMinimumLength(2)
        
        self.deleteFlag.value = False

    def load(self):
        result = {}
        for dbps in DbStateCode.objects.all():
            ps = StateCode(dbps)
            ps.fromDb()
            #print(ps)
            result[dbps.sc_code] = ps
        #print(result)        
        return result
    
    def getDisplayString(self):
        result = 'StateCode{sc_id='
        if not self.sc_id.value:
            result += None
        else:
            result += str(self.sc_id.value)
            
        result += ', sc_code='    
        if not self.sc_code.value:
            result += None
        else:
            result += str(self.sc_code.value)
            
        result += ', sc_name=' 
        if not self.sc_name.value:
            result += None
        else:
            result += str(self.sc_name.value)
        return result   
    
    def getSc_code(self):
        return self.sc_code.getValue()

    def setSc_code(self, value):
        self.sc_code.setValue(value)

    def getSc_id(self):
        return self.sc_id.getValue()
    
    def setSc_id(self, sc_id):
        self.sc_id.setValue(sc_id)
        
    def getSc_name(self):
        return self.sc_name.getValue()

    def setSc_name(self, sc_name):
        self.sc_name.setValue(sc_name)

    def __str__(self):
        return self.getDisplayString()
    
    def toDb(self):
        for name,att in self.__dict__.items():
            a = att
            if isinstance(att, Attribute):
                a = att.value
            self.myDb.__dict__[name] = a
    
    def fromDb(self):
        for name,att in self.myDb.__dict__.items():
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
        BusinessObjectBase.validateAttributes(atts)
        
    def save(self):
        self.toDb()
        self.myDb.save()       
        self.fromDb()
    
    def delete(self):
            self.deleteFlag.value = True
            self.save()
    
    def remove(self):
            self.myDb.delete()
    
    def getAttributeList(self):  
        return [ 
            self.sc_id,
            self.sc_name,
            self.sc_code
        ]
        
    def getValue(self):
        return self.sc_code.getValue()

class ScheduleStatus(ValueTable):

    NOT_SET = 1
    ACCEPTED = 2
    REJECTED = 3
    MINIMUM_TYPE = NOT_SET
    MAXIMUM_TYPE = REJECTED

    def __init__(self, myDb=None):
        super().__init__()
        self.myDb = myDb
        self.scheduleStatusID = IntegerAttribute("scheduleStatusID")
        self.scheduleStatusKey = IntegerAttribute("scheduleStatusKey")
        self.scheduleStatusName = StringAttribute("scheduleStatusName")
        self.deleteFlag = BooleanAttribute('deleteFlag')
        
        self.scheduleStatusID.setHasMaximum(False)
        self.scheduleStatusID.setHasMinimum(True)
        self.scheduleStatusID.setMinimum(1)

        self.scheduleStatusKey.setHasMaximum(False)
        self.scheduleStatusKey.setHasMinimum(True)
        self.scheduleStatusKey.setMinimum(1)

        self.scheduleStatusName.setAllSpacesAllowed(False)
        self.scheduleStatusName.setHasMaximumLength(True)
        self.scheduleStatusName.setHasMinimumLength(True)
        self.scheduleStatusName.setMixedCase(True)
        self.scheduleStatusName.setNullStringAllowed(False)
        self.scheduleStatusName.setMaximumLength(100)
        self.scheduleStatusName.setMinimumLength(1)
        
        self.deleteFlag.value = False

        if myDb:
            self.fromDb()
            
    def load(self):
        result = {}
        for dbps in DbScheduleStatus.objects.all():
            ps = ScheduleStatus(dbps)
            ps.fromDb()
            #print(ps)
            result[dbps.scheduleStatusKey] = ps
        #print(result)        
        return result
    
    def getDisplayString(self):
        result = 'ScheduleStatus{scheduleStatusID='
        if not self.scheduleStatusID.value:
            result += 'None'
        else:
            result += str(self.scheduleStatusID.value)
            
        result += ', scheduleStatusKey='
        if not self.scheduleStatusKey.value:
            result += 'None'
        else:
            result += str(self.scheduleStatusKey.value)
            
        result += ', scheduleStatusName=' 
        if not self.scheduleStatusName.value:
            result += 'None'
        else:
            result += str(self.scheduleStatusName.value)
        return result   
    
    def getScheduleStatusKey(self):
        return self.scheduleStatusKey.getValue()
    
    def setScheduleStatusKey(self, scheduleStatusKey):
        self.scheduleStatusKey.setValue(scheduleStatusKey)

    def setScheduleStatusName(self, name):
        self.scheduleStatusName.setValue(name)
    
    def getScheduleStatusName(self):
        return self.scheduleStatusName.getValue()
    
    def getScheduleStatusID(self):
        return self.scheduleStatusID.getValue()
    
    def setScheduleStatusID(self, val):
        self.scheduleStatusID.setValue(val)

    def __str__(self):
        return self.getDisplayString()
    
    def toDb(self):
        for name,att in self.__dict__.items():
            a = att
            if isinstance(att, Attribute):
                a = att.value
            self.myDb.__dict__[name] = a
    
    def fromDb(self):
        for name,att in self.myDb.__dict__.items():
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
        BusinessObjectBase.validateAttributes(atts)
        
    def save(self):
        self.toDb()
        self.myDb.save()       
        self.fromDb()
    
    def delete(self):
            self.deleteFlag.value = True
            self.save()
    
    def remove(self):
            self.myDb.delete()
    
    def getAttributeList(self):  
        return [ 
        self.scheduleStatusID,
        self.scheduleStatusKey,
        self.scheduleStatusName
        ]
        
    def getValue(self):
        return self.scheduleStatusName.getValue()

