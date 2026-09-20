from vscode.att.attribute import BooleanAttribute,IntegerAttribute,StringAttribute,NumericStringAttribute,CurrencyAttribute,TimeAttribute,DateAttribute
from django.test import TestCase
from django.utils import timezone
from datetime import datetime as DT,timedelta,time
from vscode.loader.loaders import *
from vscode.base.base import *
from vscode.base.business_objects  import *
from vs.models import *
from vscode.val.vals import ValueTableManager
class VolunteerSchedulerValueTableTests(TestCase):      
    def testLoader(self):
        err = None
        try:
            lm = LoaderManager()
            lm.load()
        except Exception as e:
            err = e
        assert not err,'loader had an exception'
        
    def testValueTableManager(self):
        lm = LoaderManager()
        lm.load()
        vtm = ValueTableManager()
        err = None
        val = None
        try:
            val = vtm.getValues('ProjectStatus')
        except Exception as e:
            err = e
        assert not err, "ValueTableManager.getValues(ProjectStatus) threw an exception: " + str(err)
        assert val , "ValueTableManager.getValues(ProjectStatus failed to find anything"
        assert isinstance(val,list), "ValueTableManager.getValues(ProjectStatus returned " + str(type(val))
        
        err = None
        val = None
        try:
            val = vtm.getValueEntries('TaskStatus')
        except Exception as e:
            err = e
        assert not err, "ValueTableManager.getValueEntries(TaskStatus) threw an exception: " + str(err)
        assert val and isinstance(val,list), "ValueTableManager.getValueEntries(TaskStatus failed to find anything"
        
        err = None
        val = None
        try:
            val = vtm.getValue('LoginStatus', 4)
        except Exception as e:
            err = e
        assert not err, "ValueTableManager.LoginStatus(LoginStatus) threw an exception: " + str(err)
        assert val and isinstance(val,LoginStatus), "ValueTableManager.getValues(LoginStatus failed to find anything"
        
        err = None
        val = None
        try:
            val = vtm.getValue('RecurrenceType', 1)
        except Exception as e:
            err = e
        assert not err, "ValueTableManager.getValues(RecurrenceType) threw an exception: " + str(err)
        assert val and isinstance(val,RecurrenceType), "ValueTableManager.getValues(RecurrenceType failed to find anything"
                
        err = None
        val = None
        try:
            val = vtm.getValue('RelationshipType', 1)
        except Exception as e:
            err = e
        assert not err, "ValueTableManager.getValues(RelationshipType) threw an exception: " + str(err)
        assert val and isinstance(val,RelationshipType), "ValueTableManager.getValues(RelationshipType failed to find anything"
             
        err = None
        val = None
        try:
            val = vtm.getValue('SkillRelationshipType', 1)
        except Exception as e:
            err = e
        assert not err, "ValueTableManager.getValues(SkillRelationshipType) threw an exception: " + str(err)
        assert val and isinstance(val,SkillRelationshipType), "ValueTableManager.getValues(SkillRelationshipType failed to find anything"
             
        err = None
        val = None
        try:
            val = vtm.getValue('StateCode', 'IA')
        except Exception as e:
            err = e
        assert not err, "ValueTableManager.getValues(StateCode) threw an exception: " + str(err)
        assert val and isinstance(val,StateCode), "ValueTableManager.getValues(StateCode failed to find anything"
             
        err = None
        val = None
        try:
            val = vtm.getValue('ScheduleStatus', 1)
        except Exception as e:
            err = e
        assert not err, "ValueTableManager.getValues(ScheduleStatus) threw an exception: " + str(err)
        assert val and isinstance(val,ScheduleStatus), "ValueTableManager.getValues(ScheduleStatus failed to find anything"
     
    def testProjectStatus(self):
        err = None
        try:
            ProjectStatusLoader(True).load()
            #print(DbProjectStatus.objects.all())
            vtm = ValueTableManager()
            entries = vtm.getValueEntries("ProjectStatus")
            #print(entries)
            entry = vtm.getValue('ProjectStatus', 1)
            #print(entry)
            vals = vtm.getValues('ProjectStatus')
            #print(vals)
        except Exception as e:
            err = e
        assert not err, 'testProjectStatus had an exception'

    def testLoginStatus(self):
        err = None
        try:
            LoginStatusLoader(True).load()
            #print(DbProjectStatus.objects.all())
            vtm = ValueTableManager()
            entries = vtm.getValueEntries("LoginStatus")
            #print(entries)
            entry = vtm.getValue("LoginStatus", 1)
            #print(entry)
            vals = vtm.getValues("LoginStatus")
            #print(vals)
        except Exception as e:
            err = e
        assert not err, 'testLoginStatus had an exception'
        
    def testTaskStatus(self):
        err = None
        try:
            TaskStatusLoader(True).load()
            #print(DbProjectStatus.objects.all())
            vtm = ValueTableManager()
            entries = vtm.getValueEntries("TaskStatus")
            #print(entries)
            entry = vtm.getValue("TaskStatus", 1)
            #print(entry)
            vals = vtm.getValues("TaskStatus")
            #print(vals)
        except Exception as e:
            err = e
        assert not err, 'testTaskStatus had an exception'
      
    def testRecurrenceType(self):
        err = None
        try:
            RecurrenceTypeLoader(True).load()
            #print(DbProjectStatus.objects.all())
            vtm = ValueTableManager()
            entries = vtm.getValueEntries("RecurrenceType")
            #print(entries)
            entry = vtm.getValue("RecurrenceType", 1)
            #print(entry)
            vals = vtm.getValues("RecurrenceType")
            #print(vals)  
        except Exception as e:
            err = e
        assert not err, 'testRecurrenceType had an exception'
              
    def testSkillRelationshipType(self):
        err = None
        try:
            SkillRelationshipTypeLoader(True).load()
            #print(DbSkillRelationshipType.objects.all())
            vtm = ValueTableManager()
            entries = vtm.getValueEntries("SkillRelationshipType")
            #print(entries)
            entry = vtm.getValue("SkillRelationshipType", 1)
            #print(entry)
            vals = vtm.getValues("SkillRelationshipType")
            #print(vals)
        except Exception as e:
            err = e
        assert not err, 'testSkillRelationshipType had an exception'
                              
    def testRelationshipType(self):
        err = None
        try:
            RelationshipTypeLoader(True).load()
            #print(DbProjectStatus.objects.all())
            vtm = ValueTableManager()
            entries = vtm.getValueEntries("RelationshipType")
            #print(entries)
            entry = vtm.getValue("RelationshipType", 1)
            #print(entry)
            vals = vtm.getValues("RelationshipType")
            #print(vals)  
        except Exception as e:
            err = e
        assert not err, 'testRelationshipType had an exception'      
                   
    def testStateCode(self):
        err = None
        try:
            StateCodeLoader(True).load()
            #print(DbStateCode.objects.all())
            vtm = ValueTableManager()
            entries = vtm.getValueEntries("StateCode")
            #print(entries)
            entry = vtm.getValue("StateCode", "IA")
            #print(entry)
            vals = vtm.getValues("StateCode")
            #print(vals)
        except Exception as e:
            err = e
        assert not err, 'testStateCode had an exception'      
        
    def testScheduleStatus(self):
        err = None
        try:
            ScheduleStatusLoader(True).load()
            #print(DbScheduleStatus.objects.all())
            vtm = ValueTableManager()
            entries = vtm.getValueEntries("ScheduleStatus")
            #print(entries)
            assert entries, 'getValueEntries("ScheduleStatus")'
            entry = vtm.getValue('ScheduleStatus', 1)
            assert entry, "getValue('ScheduleStatus', 1)"
            #print(entry)
            vals = vtm.getValues('ScheduleStatus')
            assert vals, "getValues('ScheduleStatus')"
            #print(vals)
        except Exception as e:
            err = e
        assert not err, 'testScheduleStatus had an exception'  
        
    def testPrivilege(self):
        err = None
        try:
            self.testLoader()
            dbo = DbPrivilege()
            obj = Privilege(dbo)
            obj.setPrivilegeCreateUser(1)
            obj.setPrivilegeUpdateUser(1)
            obj.privilegeName.value='test'
            obj.save()
            obj2=DbPrivilege.objects.all()
            assert obj2 != None
            #print(obj2)
        except Exception as e:
            err = e
        assert not err, 'testPrivilege had an exception'
        
    def testPassword(self):
        err = None
        try:
            dbo = DbPassword()
            obj = Password(dbo)
            obj.setPasswordCreateDate(DT.now())
            obj.setPasswordUpdateDate(DT.now())
            obj.setPasswordCreateUser(1)
            obj.setPasswordUpdateUser(1)
            obj.setPassword('txt')
            obj.save()
            obj2=DbPassword.objects.all()
            assert obj2 != None
            #print(obj2)
        except Exception as e:
            err = e
        assert not err, 'testPassword had an exception'
      