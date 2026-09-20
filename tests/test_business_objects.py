from datetime import datetime as DT
from django.test import TestCase
from django.utils import timezone
from django.db import transaction
from django.db import models 
from datetime import datetime as DT,timedelta,time
from loguru import logger

from vscode.att.attribute import BooleanAttribute,IntegerAttribute,StringAttribute,NumericStringAttribute,CurrencyAttribute,TimeAttribute,DateAttribute
from vscode.loader.loaders import *
from vscode.base.base import *
from vscode.base.business_objects  import *
from vs.models import *
from vscode.val.vals import ValueTableManager

class VSTestBase(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def log(self, msg=None,err=None):
        if msg:
            logger.debug(msg)
        if err:
            logger.opt(exception=True).debug(err)  
            
    def handleException(self, err):
        self.log(err=err)  
        
    def now(self):
        return DT.now()
          
class VolunteerSchedulerBusinessObjectTests(VSTestBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
         
    def testLogin(self):
        LoaderManager().load()
        org = DbOrganization ()
        org.organizationName = 'org'
        org.organizationCreateUser = 1
        org.organizationUpdateUser = 1
        org.save()
        lis = DbLoginStatus()
        lis.loginStatusType = 1
        lis.save()
        dbl = DbLogin()
        obj = Login(dbl)
        obj.setLogin('velda')
        obj.setLoginName('zelda snurtz')
        obj.setFailures(0),
        obj.setLastChange(DT.now().date())
        obj.setSecret('secret12')
        obj.setLoginCreateUser(1)
        obj.setLoginUpdateUser(1)
        obj.setLoginCreateDate(DT.now())
        obj.setLoginUpdateDate(DT.now())
        obj.setDeleteFlag(False)
        obj.setOrganization(org)
        err = None
        try:
            obj.loginStatus = lis
            obj.save()
            obj2=DbLogin.objects.get(pk=obj.getLoginID())
            #print(obj2)
            if not obj2:
                raise Exception("didnt get anything from db")
            obj2.delete()
        except Exception as e:
            err = e
        assert not err, 'delete failed '  + str(err)
        obj.setDeleteFlag(False)
        obj.save
        exp = None
        err = None
        try:
            exp = obj.isExpired()
        except Exception as e:
            err = e
            logger.opt(exception=True).debug(e)
        assert not err, 'isExpired ' + str(err)
        assert not exp, 'got true result from isExpired()'
        obj.lock()
        assert obj.isLocked(), 'lock failed'
        obj.reset()
        assert obj.isReset(),  'reset failed'
               
    def testAddress(self):
        self.of=ObjectFactory()
        dbObj = DbAddress()
        obj = Address(dbObj)
        obj.addressCreateUser=1
        obj.addressUpdateUser=1
        obj.street.value = 'My Address'
        obj.addressOrganizationID.value = 1
        obj.addressLineTwo.value = "addressLineTwo"
        obj.city.value = "city"
        obj.state.value = "mn"
        obj.postalCode.value = "postalCode"
        obj.phone.value = "phone"
        obj.mobilePhone.value = "mobilePhone"
        obj.fax.value = "fax"
        obj.pager.value = "pager"
        obj.email.value = "email"
        obj.toDb()
        assert obj.isSameState(obj) 
        #print(obj)
        #print(dbObj)
        obj.save()
        #print(obj)
        obj.delete()
        
    def testOrganization(self):
        dbo = DbOrganization()
        org = Organization(dbo)
        org.setCreateUser(1)
        org.setUpdateUser(1)
        org.organizationName.value='test'
        org.save()
        org.setStreet('test street')
        org.setOrganizationCreateDate(DT.now())
        org.setOrganizationUpdateDate(DT.now())
        org.save()
        dbo2=DbOrganization.objects.exclude(deleteFlag=True)[0]
        assert dbo2,"didn't get an db org" 
        assert dbo2.address, 'no dbo.address'
        assert dbo2.address.street == 'test street', 'wrong db address :' + str(dbo2.address.street)
        org2 = Organization(dbo2)
        assert org2,"didn't get an org" 
        assert org2.getStreet() == 'test street', 'wrong address: ' + str(org2.getStreet())
        org2.delete()
        
    def testConfigurableProperty(self):
        dbo = DbConfigurableProperty()
        obj = ConfigurableProperty(dbo)
        obj.setCreateUser(1)
        obj.setUpdateUser(1)
        obj.propertyName.value='test property'
        obj.propertyType.value = 1
        obj.propertyValue.value = models.CharField(max_length=255, null=True, blank=True)
        obj.propertyDescription.value = models.CharField(max_length=255, null=True, blank=True)
        obj.save()
        obj2=DbConfigurableProperty.objects.all()[0]
        assert obj2.propertyName == 'test property', 'Wrong error'
        obj2.delete()
        
    def testConfigurationSet(self):
        dbOrg = DbOrganization()
        org = Organization(dbOrg)
        org.setCreateUser(1)
        org.setUpdateUser(1)
        org.setOrganizationCreateDate(DT.now())
        org.setOrganizationUpdateDate(DT.now())
        org.organizationName.value='testConfigurationSet-org'
        org.save()
        org.setStreet('testConfigurationSet org street')
        org.save()
        #print(org)
        dbo = DbConfigurableProperty()
        obj = ConfigurableProperty(dbo)
        obj.setCreateUser(1)
        obj.setUpdateUser(1)
        obj.propertyName.value='testConfigurationSet cp1'
        obj.propertyType.value = 1
        obj.propertyValue.value = 'testConfigurationSet = cp1'
        obj.propertyDescription.value = 'testConfigurationSet = cp1'
        obj.save()
        dbcs = DbConfigurationSet()
        obcs = ConfigurationSet(dbcs)
        obcs.configurationSetName.value = 'testConfigurationSet cs'
        obcs.configurationSetCreateUser.value = 1
        obcs.configurationSetUpdateUser.value = 1
        obcs.save()
        obcs.properties.append(obj)
        obcs.setOrganization(org)
        obcs.save()
        dbo2 = DbConfigurationSet.objects.all()[0]
        obj2 = ConfigurationSet(dbo2)
        assert obj2, 'obj2 was null'
        #print(str(obj2))
        #print(*********************)
        dbOrg.delete()
        
    def testLocation(self):
        dbOrg = DbOrganization()
        org = Organization(dbOrg)
        org.setCreateUser(1)
        org.setUpdateUser(1)
        org.organizationName.value='testLocation -org'
        org.save()
        org.setStreet('testLocationt org street')
        org.setOrganizationCreateDate(DT.now())
        org.setOrganizationUpdateDate(DT.now())
        org.save()
        #print(org)
        dbo = DbLocation()
        obj = Location(dbo)
        obj.setCreateUser(1)
        obj.setUpdateUser(1)
        obj.locationName.value='testLocation'
        obj.setOrganization(org)
        obj.save()
        obj2 = DbLocation.objects.all()[0]
        assert obj2, 'obj2 was null'
        dbOrg.delete()
    
    def testResource(self):
        dbOrg = DbOrganization()
        org = Organization(dbOrg)
        org.setCreateUser(1)
        org.setUpdateUser(1)
        org.organizationName.value='testResource -org'
        org.save()
        org.setStreet('testResource org street')
        org.setOrganizationCreateDate(DT.now())
        org.setOrganizationUpdateDate(DT.now())
        org.save()
        #print(org)
        dbo = DbResource()
        obj = Resource(dbo)
        obj.setCreateUser(1)
        obj.setUpdateUser(1)
        obj.setName('testResource')
        obj.setCount(10)
        obj.setOrganization(org)
        obj.save()
        obj2 = DbResource.objects.all()[0]
        assert obj2, 'nothing from DbResource.objects.all()[0]'
        #print(obj2)
        #print(obj)
        dbOrg.delete()    
   
    def testActivity(self):
        err=None
        dbo = DbActivity()
        obj = Activity(dbo)
        obj.setCreateUser(1)
        obj.setUpdateUser(1)
        obj.setName('test Activity')
        dbo = DbActivity()
        obj = Activity(dbo)
        obj.setCreateUser(1)
        obj.setUpdateUser(1)
        obj.setName('test Activity')
        obj.setHoursWorked(10)
        obj.save()
        obj2 = Activity(DbActivity.objects.all()[0])
        assert obj2, 'no object'
        assert obj2.getName() == 'test Activity', ' wrong activity name'
        #TODO test getCost after volunteer is built 
        
    def testAvailability(self):
        err = None
        now = DT.now()
        dbo = DbAvailability()
        obj = Availability(dbo)
        obj.setCreateUser(1)
        obj.setUpdateUser(1)
        obj.setAvailabilityStartDate(now)
        obj.setAvailabilityEndDate(now)
        obj.save()
        obj2 = DbAvailability.objects.all()[0]
        assert obj2, 'db read failed'
        id1 = dbo.availabilityID
        assert id1, 'no primary key' 
        try:
            dbo2 = DbAvailability.objects.exclude(deleteFlag=True).get(pk=id1)
        except Exception as e:
            err = e
            self.log(err=err)
        assert not err, 'gat an exception' 
        assert dbo2, 'get by pk failed'
        obj2 = Availability(dbo2)
        obj2.delete()
        dbo2 = DbAvailability.objects.all()[0]
        dbo3 = DbAvailability.objects.exclude(deleteFlag=True).filter(pk=id1).first()
        assert dbo2, "didn't get deleted availability"
        assert not dbo3, 'got a deleted item' 
        obj2.remove() 
        dbo3 = DbAvailability.objects.filter(pk=id1).first()
        assert not dbo3, 'availability not removed'
        
    def testJob(self):
        err = None
        now = DT.now()
        dbo = DbJob()
        obj = Job(dbo)
        obj.setCreateUser(1)
        obj.setUpdateUser(1)
        obj.setJobCreateDate(now)
        obj.setJobUpdateDate(now)
        obj.setCount(1)
        obj.save()
        obj2 = DbJob.objects.all()[0]
        assert obj2, 'db read failed'
        id1 = dbo.jobID
        assert id1, 'no primary key' 
        try:
            dbo2 = DbJob.objects.exclude(deleteFlag=True).get(pk=id1)
        except Exception as e:
            err = e
            self.log(err=err)
        assert not err, 'gat an exception' 
        assert dbo2, 'get by pk failed'
        obj2 = Job(dbo2)
        obj2.delete()
        dbo2 = DbJob.objects.all()[0]
        dbo3 = DbJob.objects.exclude(deleteFlag=True).filter(pk=id1).first()
        assert dbo2, "didn't get deleted Job"
        assert not dbo3, 'got a deleted item' 
        assert obj2.isSameState(obj2), 'equal failed'
        obj2.remove() 
        dbo3 = DbJob.objects.filter(pk=id1).first()
        assert not dbo3, 'job not removed'
        
    def testReport(self):
        err = None
        now = DT.now()
        dbo = DbReport()
        obj = Report(dbo)
        obj.setCreateUser(1)
        obj.setUpdateUser(1)
        obj.setReportCreateDate(now)
        obj.setReportUpdateDate(now)
        obj.save()
        obj2 = DbReport.objects.all()[0]
        assert obj2, 'db read failed'
        id1 = dbo.reportID
        assert id1, 'no primary key' 
        try:
            dbo2 = DbReport.objects.exclude(deleteFlag=True).get(pk=id1)
        except Exception as e:
            err = e
            self.log(err=err)
        assert not err, 'gat an exception' 
        assert dbo2, 'get by pk failed'
        obj2 = Report(dbo2)
        obj2.delete()
        dbo2 = DbReport.objects.all()[0]
        dbo3 = DbReport.objects.exclude(deleteFlag=True).filter(pk=id1).first()
        assert dbo2, "didn't get deleted Report"
        assert not dbo3, 'got a deleted item' 
        assert obj2.isSameState(obj2), 'equal failed'
        obj2.remove() 
        dbo3 = DbReport.objects.filter(pk=id1).first()
        assert not dbo3, 'Report not removed'
    
    def testProjectResource(self):
        err = None
        now = DT.now()
        dboo = DbOrganization()
        org = Organization(dboo)
        org.setCreateUser(1)
        org.setUpdateUser(1)
        org.organizationName.value='testProjectResource -org'
        org.save()
        org.setStreet('testProjectResource org street')
        org.setOrganizationCreateDate(DT.now())
        org.setOrganizationUpdateDate(DT.now())
        org.save()
        dbo = DbProjectResource()
        obj = ProjectResource(dbo)
        obj.setOrganization(org)
        obj.setName('testProjectResource')
        obj.setCreateUser(1)
        obj.setUpdateUser(1)
        obj.setResourceCreateDate(now)
        obj.setResourceUpdateDate(now)
        obj.setReusable(False)
        obj.setCost(100.10)
        obj.setCount(5)
        obj.save()
        obj2 = DbProjectResource.objects.all()[0]
        assert obj2, 'db read failed'
        id1 = dbo.resourceID
        assert id1, 'no primary key' 
        try:
            dbo2 = DbProjectResource.objects.exclude(deleteFlag=True).get(pk=id1)
        except Exception as e:
            err = e
            self.log(err=err)
        assert not err, 'gat an exception' 
        assert dbo2, 'get by pk failed'
        obj2 = Report(dbo2)
        obj2.delete()
        dbo2 = DbProjectResource.objects.all()[0]
        dbo3 = DbProjectResource.objects.exclude(deleteFlag=True).filter(pk=id1).first()
        assert dbo2, "didn't get deleted ProjectResource"
        assert not dbo3, 'got a deleted item' 
        assert obj2.isSameState(obj2), 'equal failed'
        obj2.remove() 
        dbo3 = DbProjectResource.objects.filter(pk=id1).first()
        assert not dbo3, 'ProjectResource not removed'
      
    def testHousehold(self):
        err = None
        now = DT.now()
        LoaderManager().load()
        dboo = DbOrganization()
        org = Organization(dboo)
        org.setCreateUser(1)
        org.setUpdateUser(1)
        org.organizationName.value='testHousehold -org'
        org.save()
        org.setStreet('testHousehold org street')
        org.setOrganizationCreateDate(DT.now())
        org.setOrganizationUpdateDate(DT.now())
        org.save()
        dbo = DbHousehold()
        obj = Household(myDb=dbo)
        obj.setOrganization(org)
        obj.setHouseholdFirstName('1st')
        obj.setHouseholdLastName('testHousehold')
        obj.setCreateUser(1)
        obj.setUpdateUser(1)
        obj.setHouseholdCreateDate(now)
        obj.setHouseholdUpdateDate(now)
        obj.save()
        obj2 = DbHousehold.objects.all()[0]
        assert obj2, 'db read failed'
        id1 = dbo.householdID
        assert id1, 'no primary key' 
        try:
            dbo2 = DbHousehold.objects.exclude(deleteFlag=True).get(pk=id1)
        except Exception as e:
            err = e
            self.log(err=err)
        assert not err, 'gat an exception' 
        assert dbo2, 'get by pk failed'
        obj2 = Household(myDb=dbo2)
        obj2.delete()
        dbo2 = DbHousehold.objects.all()[0]
        dbo3 = DbHousehold.objects.exclude(deleteFlag=True).filter(pk=id1).first()
        assert dbo2, "didn't get deleted Household"
        assert not dbo3, 'got a deleted item' 
        assert obj2.isSameState(obj2), 'equal failed'
        obj2.remove() 
        dbo3 = DbHousehold.objects.filter(pk=id1).first()
        assert not dbo3, 'Household not removed'
   
 