from vscode.att.attribute import BooleanAttribute,IntegerAttribute,StringAttribute,NumericStringAttribute,CurrencyAttribute,TimeAttribute,DateAttribute
from django.test import TestCase
from django.utils import timezone
from .test_business_objects import  VSTestBase
from datetime import datetime as DT,timedelta,time

from vscode.base.base import *
from vscode.base.business_objects import *
from vscode.utils.utils import *
from vscode.loader.loaders import *
from vscode.val.vals import ValueTableManager
from vs.models import *     
             
class ObjectFactoryTests(VSTestBase):
       
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    #    self._getRequiredTests()
        
    def test_getOFCounts(self):
        count = 0
        lines = 0
        with open('D:\\eclipseWorkspace\\volsched\\vscode\\base\\business_objects.py', 'r', encoding="utf-8") as file:
            for l in file:
                lines += 1
                if 'to' + 'do' in str(l).strip().lower():
                    count += 1
        if count:
            print('\nThere are ' + str(count) + ' unfinished OF methods in ' +str(lines)) 
        count = 0
        lines = 0
        with open('D:\\eclipseWorkspace\\volsched\\tests\\test_object_factory.py', 'r', encoding="utf-8") as file:
            for l in file:
                lines += 1
                if str(l).strip().lower().find('to' + 'do') >= 0:
                    count += 1
        if count:
            print('\nThere are ' + str(count) + ' unfinished ObjectFactory tests in ' +str(lines) + ' lines of code')          
                                                 
    def test_createLogin(self):
        LoaderManager().load()
        err = None
        li2 = None
        of = ObjectFactory()
        try:
            dbo = DbOrganization()
            org = Organization(dbo)
            org.setOrganizationName('test_createLogin')
            org.setCreateUser(1)
            org.setUpdateUser(1)
            org.save()
            log1 = 'testuser1'
            log2 = 'testuser2'
            name1 = 'Test User Tne First'
            name2 = 'Test User Tne Second'
            li = of.createLogin(log1, name1, org, 1, household=False, volunteer=False)
            li2 = DbLogin.objects.filter(login=log1)[0]
            li3 = of.createLogin(log2, name2, org, 1, household=True, volunteer=True)
            li4 = DbLogin.objects.filter(login=log2)[0] 
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert li, 'didn\'t get a new login'
        assert li2, 'didn\' fetch new login'
        assert li3, 'didn\' build login & vol'
        assert li4, 'didn\' fetch new login & vol'

    def test_getConfigurableProperties(self):
        LoaderManager().load()
        of = ObjectFactory()
        result = None
        err = None
        try:
            result = of.getConfigurableProperties()
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, 'no output'
 
    def test_getTableNames(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        try:
            rows = of.getTableNames()
            #print(len(rows))
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert rows, 'no result'
        assert len(rows) == 64, 'invalID row count expected 64, but got: ' + str(len(rows))
        
    def test_getTableSize(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        szClass = 0
        szString = 0
        try:
            szClass = of.getTableSize(StateCode)
            #print(szClass)
            szString = of.getTableSize('StateCode')
            #print(szString)
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert szClass == 52, 'wrong count for class argument, expected 52, got: ' + str(szClass)
        assert szString == 52, 'wrong count for string argument  expected 52, got: ' + str(szString)
        
    def test_changePassword(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        result = "to be replaced"
        newVal = 'newtest_changePassword'
        try:
            #print(DbOrganization.objects.all())
            org = of.createOrganization('test_changePassword',1)
            li = of.createLogin('test_changePassword','first test_changePassword',org,1)
            of.changePassword(li,newVal,1)
            pw = li.getPassword().getPassword()
            result = Encrypter().decrypt(pw)
            #print(result)
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
        assert result == newVal, 'wrong result'
 
    def test_createOrganization(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        org = None
        result = "test_createOrganization"
        try:
            org = of.createOrganization(result, 1)
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert org, "no output"
        assert org.getOrganizationName() == result, 'wrong org name: ' + org.getOrganizationName()
 
    def test_executeSqlUpdate(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        result = None
        try:
            result = of.executeSqlUpdate('SELECT count(*) frOM VolunteerScheduler.vs_dbstatecode;')
            #print(result)
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
        assert result[0] == 52, 'Wrong result expected 52, but got ' + str(result[0])
 
    def test_getConfigurableProps(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        result = None
        try:
            result = of.getConfigurableProps()
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"

    def test_getConfigurationSets(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        result = None
        try:
            #print(DbConfigurationSet.objects.all())
            result = of.getConfigurationSets() 
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
        assert len(result) == 4, 'expected 4 got ' + str(len(result))
 
    def test_getConfigurationSetsForOrg(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        result = None
        try:
            dbo = DbOrganization.objects.filter(pk=1).first()
            org = Organization(dbo)
            result = of.getConfigurationSets(org)
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
        assert len(result) == 2, 'expected 2 configuration setsgot ' + str(len(result))
        assert len(result[0].getProperties()) == 9, 'expected 9 configurable properties got ' + str(len(result[0].getProperties()))
 
    def test_getDeletedOrganizationProjects(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = 'test_getDeletedOrganizationProjects'
        result = None
        try:
            ps = ValueTableManager().getValue('ProjectStatus',ProjectStatus.DEFINED)
            org = of.createOrganization(name, 1)
            dbo = DbProject()
            proj = Project(dbo)
            proj.setStatus(ps)
            proj.projectName.value = name
            proj.projectStartDate.value = None
            proj.projectFinishDate = None
            proj.projectCreateUser.value = 1
            proj.projectUpdateUser.value = 1
            proj.projectCreateDate = DT.now()
            proj.projectUpdateDate = DT.now()
            proj.setOrganization(org)
            proj.save()
            proj.delete()
            result = of.getDeletedOrganizationProjects(org)
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
        assert len(result) == 1, 'expected 1 project, got ' + str(len(result))
        assert isinstance(result[0], Project), 'nat a project. got ' + str(type(result[0])) 
        assert result[0].getProjectName() == name, 'wrong name'
        
    def test_getDeletedTeams(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        result = None
        name = 'test_getDeletedTeams'
        try:
            org = of.createOrganization(name, 1)
            dbo = DbTeam()
            t = Team(dbo, org)
            t.setTeamName(name)
            t.save()
            t.delete()
            result = of.getDeletedTeams(org)[0]            
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getEventResourceAssignments(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        result = None
        try:
            name = 'test_getEventResourceAssignments'
            res = []
            org = of.createOrganization(name + 'org', 1)
            dbo = DbScheduleEvent()
            evt = ScheduleEvent(dbo)            
            evt.setEventName(name)
            evt.setEventStartTime('10:00:00')
            evt.setEventDate(super().now())
            evt.setEventCreateUser(1)
            evt.setEventUpdateUser(1)
            evt.setEventDuration(60)
            evt.save()
            evt.setOrganization(org)
            evt.save()
            dbor1 = DbResource()
            r1 = Resource(dbor1)
            r1.setName(name + '1')
            r1.setCreateUser(1)
            r1.setUpdateUser(1)
            r1.save()
            res.append(r1)
            dbor2 = DbResource()
            r2 = Resource(dbor2)
            r2.setName(name + '2')
            r2.setCreateUser(1)
            r2.setUpdateUser(1)
            r2.save()
            dbor3 = DbResource()
            r3 = Resource(dbor3)
            r3.setName(name + '3')
            r3.setCreateUser(1)
            r3.setUpdateUser(1)
            r3.save()
            evt.resources.append(r1)
            evt.resources.append(r2)
            dbo.resources.set([dbor1, dbor2])
            evt.save()
            result = of.getEventResourceAssignments(evt, res)
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
        assert len(result) == 1, 'Wrong count expected 1, got ' + str(len(result))
 
    def test_getEventResourcesNoEvt(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        result = None
        try:
            name = 'test_getEventResourcesNoEvt'
            res = []
            org = of.createOrganization(name + 'org', 1)
            dbo = DbScheduleEvent()
            evt = ScheduleEvent(dbo)            
            evt.setEventName(name)
            evt.setEventStartTime('10:00:00')
            evt.setEventDate(super().now())
            evt.setEventCreateUser(1)
            evt.setEventUpdateUser(1)
            evt.setEventDuration(60)
            evt.save()
            evt.setOrganization(org)
            evt.save()
            dbor1 = DbResource()
            r1 = Resource(dbor1)
            r1.setName(name + '1')
            r1.setCreateUser(1)
            r1.setUpdateUser(1)
            r1.save()
            res.append(r1)
            dbor2 = DbResource()
            r2 = Resource(dbor2)
            r2.setName(name + '2')
            r2.setCreateUser(1)
            r2.setUpdateUser(1)
            r2.save()
            dbor3 = DbResource()
            r3 = Resource(dbor3)
            r3.setName(name + '3')
            r3.setCreateUser(1)
            r3.setUpdateUser(1)
            r3.save()
            evt.resources.append(r1)
            evt.resources.append(r2)
            dbo.resources.set([dbor1, dbor2])
            evt.save()
            result = of.getEventResources()
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
        assert len(result) == 3, 'Wrong count expected 3, got ' + str(len(result))
 
    def test_getEventResourcesForEvt(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        result = None
        try:
            name = 'test_getEventResourcesForEvt'
            res = []
            org = of.createOrganization(name + 'org', 1)
            dbo = DbScheduleEvent()
            evt = ScheduleEvent(dbo)            
            evt.setEventName(name)
            evt.setEventStartTime('10:00:00')
            evt.setEventDate(super().now())
            evt.setEventCreateUser(1)
            evt.setEventUpdateUser(1)
            evt.setEventDuration(60)
            evt.save()
            evt.setOrganization(org)
            evt.save()
            dbor1 = DbResource()
            r1 = Resource(dbor1)
            r1.setName(name + '1')
            r1.setCreateUser(1)
            r1.setUpdateUser(1)
            r1.save()
            res.append(r1)
            dbor2 = DbResource()
            r2 = Resource(dbor2)
            r2.setName(name + '2')
            r2.setCreateUser(1)
            r2.setUpdateUser(1)
            r2.save()
            dbor3 = DbResource()
            r3 = Resource(dbor3)
            r3.setName(name + '3')
            r3.setCreateUser(1)
            r3.setUpdateUser(1)
            r3.save()
            evt.resources.append(r1)
            evt.resources.append(r2)
            dbo.resources.set([dbor1, dbor2])
            evt.save()
            result = of.getEventResources(evt)
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
        assert len(result) == 1, 'Wrong count expected 1, got ' + str(len(result))
    
    def test_getJobsRequiringSkill(self):
        of = ObjectFactory()
        err = None
        result = None
        name = 'test_getJobsRequiringSkill'
        try:
            LoaderManager().load()
            org = of.createOrganization(name + 'org', 1)
            evt = of.getNewEvent(name, 1, org)
            skill = of.getNewSkill(name,1,org)
            job1 = of.getNewJob(skill,1,evt)
            job1.count.value=1
            job1.save()
            result = of.getJobsRequiringSkill(skill)
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
        assert len(result) == 1, 'Wrong count expected 1, got ' + str(len(result))
    
    def test_getLogins(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        result1 = None
        result2 = None
        try:
            org = of.createOrganization('test_getLogins', 1)
            org.save()
            li = of.createLogin('vjfetzer', 'Veeble Fetzer', org,1)
            result1 = of.getLogins()
            result2 = of.getLogins(org)
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert li, 'got no Liogin'
        assert result1, "no output for no org"
        assert len(result1) == 11, "expected 11 logins, got " + str(len(result1))
        assert result2, "no output for org"
        assert len(result2) == 3, "expected 3 logins, got " + str(len(result2))
       
    def test_getCurrentUsersPrivileges(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        result = None
        try:
            org = of.createOrganization('test_getLogins', 1)
            org.save()
            li = of.createLogin('vjfetzer', 'Veeble Fetzer', org,1)
            for sg in of.getSecurityGroups():
                li.addSecurityGroup(sg)
            li.save()
            result = of.getCurrentUsersPrivileges(li)
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert li, 'got no Login'
        assert result, 'got no privilege list'
        assert len(result)  == 24, 'Wrong count expected 24 got ' + str(len(result))
    
    def test_getNewConfigurationSet(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        result = None
        try:
            result = of.getNewConfigurationSet('name',1)
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getNewPassword(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        result = None
        name = 'test_getNewPassword'
        try:
            result = of.getNewPassword(name,1)
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getOrganization(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        result1 = None
        result2 = None
        name = 'test_getOrganization'
        try:
            org = of.createOrganization(name, 1)
            result1 = of.getOrganization(org.getOrganizationID())
            result2 = of.getOrganization(name=name)
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result1, "no output for id"
        assert result2, "no output for name"
 
    def test_getOrganizations(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        result = None
        try:
            result = of.getOrganizations()
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
        assert len(result) == 2, 'wrong count expected 2. Got ' + str(len(result))
 
    def test_getPassword(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        result = None
        name = 'test_getPassword'
        try:
            pwd = of.getNewPassword(name,1)
            pwd.setPassword('Gronk123')
            pwd.save()
            #print('\npwd = ' + str(pwd.getPasswordID()))
            result = of.getPassword(pwd.getPasswordID())
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getPasswords(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = 'test_getPassword'
        result1 = None
        result2 = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            li = of.createLogin('vzebee', 'Veeble Zeebee', org,1)
            li.save()
            pwd = of.getNewPassword(name,1,login=li)
            pwd.setPassword(name)
            pwd.save()
            result1 = of.getPasswords()
            result2 = of.getPasswords(li)
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result1, "no output - no arg"
        assert len(result1) > 0, 'empty list - no org'
        assert result2, "no output - with arg"
        assert len(result2) == 1, 'wrong count expected 1, got ' + str(len(result2))
 
    def test_getProject(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = 'test_getProject'
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            proj = of.getNewProject(name,1,org)
            proj.save()
            result = of.getProject(proj.getProjectID())
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getProjects(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        result1 = None
        result2 = None
        result3 = None
        name ='test_getProjects'
        try:
            org = of.createOrganization(name, 1)
            org.save()
            parent = of.getNewProject(name + '-parent', 1,org)
            parent.save()
            child = of.getNewProject(name, 1, org, parent=parent)
            child.save()
            result1 = of.getProjects()
            result2 = of.getProjects(org=org)
            result3 = of.getProjects(parent=parent)
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result1, "no output"
        assert len(result1) == 2, 'Wrong count. Expected 2 but got ' + str(len(result1))
        assert result2, "no output"
        assert len(result2) == 2, 'Wrong count. Expected 2 but got ' + str(len(result2))
        assert result3, "no output"
        assert len(result3) == 1, 'Wrong count. Expected 1 but got ' + str(len(result3))
        
    def test_getRecentPasswords(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        result = None
        name = 'test_getRecentPasswords'
        try:
            org = of.createOrganization(name, 1)
            org.save()
            li = of.createLogin('vzebee', 'Veeble Zeebee', org,1)
            li.save()
            pwd = of.getNewPassword(name,1,login=li)
            pwd.password.value = '123456789a'
            pwd.save()
            result = of.getRecentPasswords(li, 12)
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
        
    def test_getNewTeam(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        result = None
        try:
            org = of.createOrganization('getNewTeam',1)
            result = of.getNewTeam('getNewTeam', 1, org)
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
  
    def test_getSecurityGroups(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        result1 = None
        result2 = None
        try:
            org = of.getOrganization(1)
            result1 = of.getSecurityGroups()
            result2 = of.getSecurityGroups(org)
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result1, "no output"
        assert len(result1) == 10, 'wrong count expected 10, but got ' + str(len(result1))
        assert result2, "no output w/ org"
        assert len(result2) == 5, 'wrong count expected 5, but got ' + str(len(result1))
 
    def test_getSkill(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        result = None
        try:
            org = of.createOrganization('name', 1)
            skill = of.getNewSkill('test_getSkill', 1,org)
            skill.save()
            result = of.getSkill(skill.getSkillID())
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getTask(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        result = None
        name = 'test_getTask'
        try:
            org = of.createOrganization(name,1)
            org.save()
            task = of.getNewTask(name,1,org)
            task.setPlannedTaskStart(DT.now())
            task.save()
            result = of.getTask(task.getTaskID())
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
        
    def test_getNewTask(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        result1 = None
        try:
            org = of.createOrganization('test_getNewTask',1)
            org.save()
            result1 = of.getNewTask('test_getNewTask',1,org)
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result1, "no output none"
        
    def test_getDeletedLogins(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        result = None
        try:
            org = of.createOrganization('test_getDeletedLogins', 1)
            li = of.createLogin('vzebee', 'Veeble Zeebee', org,1)
            li.save()
            li.delete()
            result = of.getDeletedLogins()
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getDeletedSkills(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        result = None
        name = 'test_getDeletedSkills'
        try:
            org = of.createOrganization(name, 1)
            skill1 = of.getNewSkill(name + '1', 1,org)
            skill1.setOrganization(org)
            skill1.save()
            skill1.delete()
            skill2 = of.getNewSkill(name + '2', 1,org)
            skill2.setOrganization(org)
            skill2.save()
            skill2.delete()
            result = of.getDeletedSkills() 
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
        assert len(result) == 2, 'wrong count expected 2. got ' + str(len(result))        
    
    def test_getLocation(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        result1 = None
        result2 = None
        name = 'test_getLocation'
        try:
            org = of.createOrganization(name, 1)
            org.save()
            loc = of.getNewLocation(name, 1,org)
            #print(loc)
            result1 = of.getLocation(oid=loc.getLocationID())
            result2 = of.getLocation(name=name,org=org)
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result1, "no output oid"
        assert result2, "no output name"
    
    def test_getLocations(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        result = None
        name = 'test_getLocations'
        try:
            org = of.createOrganization(name, 1)
            org.save()
            of.getNewLocation(name, 1, org)
            result = of.getLocations()
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
        assert len(result) == 1, 'Expected 1 got ' + str(len(result))
 
    def test_getNewHousehold(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        result = None
        name='test_getNewHousehold'
        try:
            org = of.createOrganization(name, 1)
            org.save()
            result = of.getNewHousehold('f',name,1,org=org)
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
    def test_addDefaultAuthorizations(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_addDefaultAuthorizations"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            of.addDefaultAuthorizations(org, 1)
            result = of.getSecurityGroups(org)
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output getSecurityGroups"
 
    def test_deleteReport(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_deleteReport"
        url = 'a@b.com'
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            rpt = of.getNewReport(name,1,url)
            rpt.save()
            rpt.delete()
            result = of.getDeletedReport(rpt.getReportID())
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
    
    def test_getActivities(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getActivities"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            hh = of.getNewHousehold('1',name,1,org)
            hh.setHouseholdFirstName('one')
            hh.setHouseholdLastName(name)
            hh.save()
            vol = of.getNewVolunteer(hh,1,org)
            vol.setVolunteerFirstName('two')
            vol.setVolunteerLastName(name)
            vol.save()
            act = of.getNewActivity(name,1,1,name)
            act.setDate(DT.now())
            act.save()
            vol.addActivity(act)
            vol.save()
            result = of.getActivities()
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
        assert len(result) == 1, 'wrong count. expected 1, got ' + str(len(result))
 
    def test_getActivity(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getActivity"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            hh = of.getNewHousehold('first',name,1,org)
            hh.setHouseholdFirstName('one')
            hh.setHouseholdLastName(name)
            hh.save()
            vol = of.getNewVolunteer(hh,1,org)
            vol.setVolunteerFirstName('two')
            vol.setVolunteerLastName(name)
            vol.save()
            act = of.getNewActivity(name,1,1,name)
            act.setDate(DT.now())
            act.save()
            vol.addActivity(act)
            vol.save()
            result = of.getActivity(act.getActivityID())
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
    
    def test_getAddress(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getAddress"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            add = of.getNewAddress(1)
            add.setCity(name)
            add.save()
            result = of.getAddress(add.getAddressID())
            #print(str(add.getAddressID()))
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getAddresses(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getAddresses"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            add = of.getNewAddress(1)
            add.setCity(name)
            add.save()
            result = of.getAddresses()
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
        assert len(result) == 1, 'wrong count. expected 1, got ' + str(len(result))
       
    def test_getAvailabilities(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getAvailabilities"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            av = of.getNewAvailability(1)
            av.save()
            result = of.getAvailabilities()
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
        assert result, "no output"
        assert len(result) == 1, 'wrong count. expected 1, got ' + str(len(result))
 
    def test_getAvailability(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getAvailability"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            av = of.getNewAvailability(1)
            av.save()
            result = of.getAvailability(av.getAvailabilityID())
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
     
    def test_getConfigurableProperty(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getConfigurableProperty"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            cps = of.getConfigurableProperties()
            i = cps[0].getPropertyID()
            result = of.getConfigurableProperty(i)
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
    
    def test_getConfigurationSet(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getConfigurationSet"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            result = of.getConfigurationSet(1)
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getDeletedActivity(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getDeletedActivity"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            hh = of.getNewHousehold('1',name,1,org)
            hh.setHouseholdFirstName('one')
            hh.setHouseholdLastName(name)
            hh.save()
            vol = of.getNewVolunteer(hh,1,org)
            vol.setVolunteerFirstName('two')
            vol.setVolunteerLastName(name)
            vol.save()
            act = of.getNewActivity(name,1,1,name)
            act.setDate(DT.now())
            act.save()
            vol.addActivity(act)
            vol.save()
            act.delete()
            result = of.getDeletedActivity(act.getActivityID())
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getDeletedAddress(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getDeletedAddress"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            org.save()
            add = of.getNewAddress(1)
            add.setCity(name)
            add.save()
            add.delete()
            i = add.getAddressID()
            result = of.getDeletedAddress(i)
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getDeletedAvailability(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getDeletedAvailability"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            av = of.getNewAvailability(1)
            av.save()
            av.delete()
            result = of.getDeletedAvailability(av.getAvailabilityID())
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getDeletedObject(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getDeletedObject"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            org.delete()
            result = of.getDeletedObject(Organization, org.getOrganizationID())
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
    
    def test_getDeletedConfigurableProperty(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getDeletedConfigurableProperty"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            cp = of.getNewConfigurableProperty(name,1,1,name,name)
            cp.save()
            cp.delete()
            result = of.getDeletedConfigurableProperty(cp.getPropertyID())
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getDeletedConfigurationSet(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getDeletedConfigurationSet"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            cs = of.getNewConfigurationSet(name,1)
            cs.save()
            cs.delete()
            result = of.getDeletedConfigurationSet(cs.getConfigurationSetID())
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getDeletedEventPreference(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getDeletedEventPreference"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            hh = of.getNewHousehold('1',name,1,org)
            hh.setHouseholdFirstName('one')
            hh.setHouseholdLastName(name)
            hh.save()
            vol = of.getNewVolunteer(hh,1,org)
            vol.setVolunteerFirstName('two')
            vol.setVolunteerLastName(name)
            vol.save()
            evt = of.getNewEvent(name, 1, org)
            evt.save()
            ep = of.getNewEventPreference(vol,evt,1)
            ep.setVolunteer(vol)
            ep.setEvent(evt)
            ep.save()
            ep.delete()
            result = of.getDeletedEventPreference(ep.getPreferenceID())
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
    
    def test_getDeletedEventRecurrence(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getDeletedEventRecurrence"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            er = of.getNewEventRecurrence(1,1,1)
            er.save()
            er.delete()
            result = of.getDeletedEventRecurrence(er.getRecurrenceID())
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getDeletedHousehold(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getDeletedHousehold"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            hh = of.getNewHousehold('1',name,1,org)
            hh.setHouseholdFirstName('one')
            hh.setHouseholdLastName(name)
            hh.save()
            hh.delete()
            result = of.getDeletedHousehold(hh.getHouseholdID())
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
     
    def test_getDeletedJob(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getDeletedJob"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            skill = of.getNewSkill(name,1,org)
            skill.save()
            evt = of.getNewEvent(name, 1, org)
            evt.save()
            job = of.getNewJob(skill,1,evt)
            job.delete()
            result = of.getDeletedJob(job.getJobID())
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getDeletedJobAssignment(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getDeletedJobAssignment"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            hh = of.getNewHousehold('1',name,1,org)
            vol = of.getNewVolunteer(hh,1,org)
            vol.setVolunteerFirstName('two')
            vol.setVolunteerLastName(name)
            vol.save()
            evt = of.getNewEvent(name, 1, org)
            skill = of.getNewSkill(name,1,org)
            job = of.getNewJob(skill,1,evt)
            evt.addJob(job)
            evt.save()
            ja = of.getNewJobAssignment(job,vol,1)
            ja.delete()
            result = of.getDeletedJobAssignment(ja.getJobAssignmentID())
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getDeletedJobAssignments(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getDeletedJobAssignments"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            hh = of.getNewHousehold('1',name,1,org)
            vol = of.getNewVolunteer(hh,1,org)
            vol.setVolunteerFirstName('two')
            vol.setVolunteerLastName(name)
            vol.save()
            evt = of.getNewEvent(name, 1, org)
            skill = of.getNewSkill(name,1,org)
            job = of.getNewJob(skill,1,evt)
            evt.addJob(job)
            evt.save()
            ja = of.getNewJobAssignment(job,vol,1)
            ja.delete()
            result = of.getDeletedJobAssignments()
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
        assert len(result) == 1, 'Wrong count. expected 1; got ' + len(result)
    
    def test_getDeletedLocation(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getDeletedLocation"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            loc = of.getNewLocation(name,1,org)
            loc.delete()
            result = of.getDeletedLocation(loc.getLocationID())
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getDeletedLocations(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getDeletedLocations"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            loc = of.getNewLocation(name,1,org)
            loc.delete()
            result = of.getDeletedLocations()
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
        assert len(result) == 1, 'Wrong count. expected 1; got ' + len(result)
    
    def test_getDeletedLogin(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getDeletedLogin"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            li = of.getNewLogin(name,1,org)
            li.save()
            li.delete()
            #print(li)
            result = of.getDeletedLogin(li.getLoginID())
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getDeletedLoginStatus(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getDeletedLoginStatus"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            li = of.getNewLoginStatus(name,1)
            li.loginStatusType.value=4
            li.loginStatusDescription.value = name
            li.save()
            li.delete()
            result = of.getDeletedLoginStatus(li.getLoginStatusID())
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getDeletedObjects(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getDeletedObjects"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            org.delete()
            result = of.getDeletedObjects(Organization)
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
        assert len(result) == 1, 'Wrong count. expected 1; got ' + len(result)
 
    def test_getDeletedOrganization(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getDeletedOrganization"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            org.delete()
            result = of.getDeletedOrganization(org.getOrganizationID())
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
    
    def test_getDeletedPassword(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getDeletedPassword"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            pwd = of.getNewPassword(name, 1)
            pwd.save()
            pwd.delete()
            result = of.getDeletedPassword(pwd.getPasswordID())
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getDeletedPrivilege(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getDeletedPrivilege"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            prv = of.getNewPrivilege(name, 1)
            prv.save()
            prv.delete()
            result = of.getDeletedPrivilege(prv.getPrivilegeID())
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getDeletedProject(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getDeletedProject"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            prj = of.getNewProject(name, 1,org)
            prj.save()
            prj.delete()
            result = of.getDeletedProject(prj.getProjectID())
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getDeletedProjectResource(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getDeletedProjectResource"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            pr = of.getNewProjectResource(name, 1, org)
            pr.save()
            pr.delete()
            result = of.getDeletedProjectResource(pr.getResourceID())
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getDeletedProjectStatus(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getDeletedProjectStatus"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            ps = of.getNewProjectStatus(name, 1)
            ps.save()
            ps.delete()
            result = of.getDeletedProjectStatus(ps.getProjectStatusID())
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
    
    def test_getDeletedRecurrenceType(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getDeletedRecurrenceType"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            ps = of.getNewRecurrenceType(name, 1)
            ps.save()
            ps.delete()
            result = of.getDeletedRecurrenceType(ps.getRecurrenceTypeID())
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getDeletedRelationship(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getDeletedRelationship"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            hh = of.getNewHousehold('1',name,1,org)
            hh.setHouseholdFirstName('one')
            hh.setHouseholdLastName(name)
            hh.save()
            v1 = DbVolunteer.objects.create(volunteerCreateUser=1,volunteerUpdateUser=1)
            v1.volunteerFirstName = 'two'
            v1.volunteerLastName = name
            v1.save()
            v2 = DbVolunteer.objects.create(volunteerCreateUser=1,volunteerUpdateUser=1)
            v2.volunteerFirstName = 'three'
            v2.volunteerLastName = (name + '2')
            v2.save()
            rel = DbRelationship()
            rel.relationshipCreateUser = 1
            rel.relationshipUpdateUser = 1
            rel.volunteerOne = v1
            rel.volunteerOne_ID = v1.volunteerID
            rel.volunteerTwo = v2
            rel.volunteerTwo_ID = v2.volunteerID
            rel.save()
            rel.deleteFlag = True
            rel.save()
            result = of.getDeletedRelationship(rel.relationshipID)
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getDeletedRelationshipType(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getDeletedRelationshipType"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            rt = of.getNewRelationshipType(name, 1)
            rt.save()
            rt.delete()
            result = of.getDeletedRelationshipType(rt.getRelationshipTypeID())
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getDeletedReport(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getDeletedReport"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            ps = of.getNewReport(name, 1)
            ps.save()
            ps.delete()
            result = of.getDeletedReport(ps.getID())
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getDeletedResource(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getDeletedResource"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            ps = of.getNewResource(name, 1, org)
            ps.save()
            ps.delete()
            result = of.getDeletedResource(ps.getResourceID())
        except Exception as e:
            err = e
        assert not err, "got an exception"
        assert result, "no output"
    
    def test_getDeletedResources(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getDeletedResources"
        result = None
        try:
            org = of.createOrganization(name, 1)
            ps = of.getNewResource(name, 1, org)
            ps.save()
            ps.delete()
            result = of.getDeletedResources()
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
        assert len(result) == 1, 'Wrong count. Expected 1. Got ' + len(result)
 
    def test_getDeletedSchedule(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getDeletedSchedule"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            sch = of.getNewSchedule(DT.now(), DT.now(), 1, org)
            #print('before delete() call ' + sch.__class__.__name__)
            sch.delete()
            result = of.getDeletedSchedule(sch.getScheduleID())
            #print('after delete() call ' + sch.__class__.__name__)
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getDeletedScheduleEvent(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getDeletedScheduleEvent"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            dbo = DbScheduleEvent()
            evt = ScheduleEvent(dbo)            
            evt.setEventName(name)
            evt.setEventStartTime('10:00:00')
            evt.setEventDate(super().now())
            evt.setEventCreateUser(1)
            evt.setEventUpdateUser(1)
            evt.setEventDuration(60)
            evt.save()
            evt.setOrganization(org)
            evt.save()
            evt.delete()
            result = of.getDeletedScheduleEvent(evt.getEventID())
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getDeletedScheduleStatus(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getDeletedScheduleStatus"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            ss = of.getNewScheduleStatus(name,5)
            ss.delete()
            result = of.getDeletedScheduleStatus(ss.getScheduleStatusID())
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getDeletedSecurityGroup(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getDeletedSecurityGroup"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            sg = of.getNewSecurityGroup(name,name,1,1,org)
            sg.delete()
            result = of.getDeletedSecurityGroup(sg.getSecurityGroupID())
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getDeletedSecurityGroups(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getDeletedSecurityGroups"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            sg = of.getNewSecurityGroup(name,name,1,1,org)
            sg.delete()
            result = of.getDeletedSecurityGroups()
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
        assert len(result) == 1, 'Wrong count. Expected 1. Got ' + len(result)
 
    def test_getDeletedSkill(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getDeletedSkill"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            sk = of.getNewSkill(name, 1, org)
            sk.save()
            sk.delete()
            result = of.getDeletedSkill(sk.getSkillID())
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getDeletedSkillRelationship(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getDeletedSkillRelationship"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            s1 = of.getNewSkill(name,1,org)
            s1.save()
            s2 = of.getNewSkill(name +'2',1,org)
            typ = of.getSkillRelationshipType(1)
            sr = of.getNewSkillRelationship(s1,s2,1,typ)
            sr.save()
            sr.delete()
            result = of.getDeletedSkillRelationship(sr.getSkillRelationshipID())
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getDeletedSkillRelationshipType(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getDeletedSkillRelationshipType"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            rt = of.getNewSkillRelationshipType(name,1)
            rt.delete()
            result = of.getDeletedSkillRelationshipType(rt.getSkillRelationshipTypeID())
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getDeletedStateCode(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getDeletedStateCode"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            sc = of.getNewStateCode('ab', name)
            sc.delete()
            #print(sc)
            result = DbStateCode.objects.filter(deleteFlag=True).filter(pk=sc.getSc_id())
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
    
    def test_getDeletedTask(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getDeletedTask"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            task = of.getNewTask(name,1,org)
            task.delete()
            result = of.getDeletedTask(task.getTaskID())
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getDeletedTasks(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getDeletedTasks"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            task = of.getNewTask(name,1,org)
            task.delete()
            result = of.getDeletedTasks()
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
        assert len(result) == 1, 'Wrong count. Expected 1. Got ' + len(result)
 
    def test_getDeletedTaskStatus(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getDeletedTaskStatus"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            ts = of.getNewTaskStatus(name, 1)
            ts.delete()
            result = of.getDeletedTaskStatus(ts.getTaskStatusID())
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getDeletedTeam(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getDeletedTeam"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            tm = of.getNewTeam(name,1,org)
            tm.delete()
            result = of.getDeletedTeam(tm.getTeamID())
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
        assert result.myDb.organization_id, 'org not fetched'
 
    def test_getDeletedVolunteer(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getDeletedVolunteer"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            hh = of.getNewHousehold('1',name,1,org)
            hh.setHouseholdFirstName('one')
            hh.setHouseholdLastName(name)
            hh.save()
            vol = of.getNewVolunteer(hh,1,org)
            vol.setVolunteerFirstName('two')
            vol.setVolunteerLastName(name)
            vol.save()
            vol.delete()
            result = of.getDeletedVolunteer(oid=vol.getVolunteerID())
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getDeletedVolunteerSkill(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getDeletedVolunteerSkill"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            sk = of.getNewSkill(name, 1, org)
            hh = of.getNewHousehold('1',name,1,org)
            vol = of.getNewVolunteer(hh,1,org)
            vs = of.getNewVolunteerSkill(vol,sk,1)
            vs.delete()
            result = of.getDeletedVolunteerSkill(vs.getVolunteerSkillID())
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getDeletedVolunteerSkillAssignment(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getDeletedVolunteerSkillAssignment"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            sk = of.getNewSkill(name, 1, org)
            hh = of.getNewHousehold('1',name,1,org)
            vol = of.getNewVolunteer(hh,1,org)
            vs = of.getNewVolunteerSkill(vol,sk,1)
            evt = of.getNewEvent(name,1,org)
            vsa = of.getNewVolunteerSkillAssignment(vs,evt,1)
            vsa.delete()
            result = of.getDeletedVolunteerSkillAssignment(vsa.getVolunteerSkillAssignmentID())
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getDeletedVolunteerSkillAssignments(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getDeletedVolunteerSkillAssignments"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            sk = of.getNewSkill(name, 1, org)
            hh = of.getNewHousehold('1',name,1,org)
            vol = of.getNewVolunteer(hh,1,org)
            vs = of.getNewVolunteerSkill(vol,sk,1)
            evt = of.getNewEvent(name,1,org)
            vsa = of.getNewVolunteerSkillAssignment(vs,evt,1)
            vsa.delete()
            result = of.getDeletedVolunteerSkillAssignments()
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
        assert len(result) == 1, 'Wrong count. Expected 1. Got ' + len(result)
 
    def test_getDeletedVolunteerSkills(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getDeletedVolunteerSkills"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            sk = of.getNewSkill(name, 1, org)
            hh = of.getNewHousehold('1',name,1,org)
            vol = of.getNewVolunteer(hh,1,org)
            vs = of.getNewVolunteerSkill(vol,sk,1)
            vs.delete()
            result = of.getDeletedVolunteerSkills()
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
        assert len(result) == 1, 'Wrong count. Expected 1. Got ' + len(result)
 
    def test_getDeletedWorkAddress(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getDeletedWorkAddress"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            add = of.getNewAddress(1)
            wa = of.getNewWorkAddress(add,1)
            wa.delete()
            result = of.getDeletedWorkAddress(wa.getWorkAddressID())
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
    
    
    def test_getEvent(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getEvent"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            evt = of.getNewEvent(name,1,org)
            result = of.getEvent(evt.getEventID())
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getEventPreference(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getEventPreference"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            hh = of.getNewHousehold('1',name,1,org)
            hh.setHouseholdFirstName('one')
            hh.setHouseholdLastName(name)
            hh.save()
            vol = of.getNewVolunteer(hh,1,org)
            vol.setVolunteerFirstName('two')
            vol.setVolunteerLastName(name)
            vol.save()
            evt = of.getNewEvent(name, 1, org)
            ep = of.getNewEventPreference(vol,evt,1)
            result = of.getEventPreference(oid=ep.getPreferenceID())
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getEventPreferences(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getEventPreferences"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            hh = of.getNewHousehold('1',name,1,org)
            hh.setHouseholdFirstName('one')
            hh.setHouseholdLastName(name)
            hh.save()
            vol = of.getNewVolunteer(hh,1,org)
            vol.setVolunteerFirstName('two')
            vol.setVolunteerLastName(name)
            vol.save()
            evt = of.getNewEvent(name, 1, org)
            of.getNewEventPreference(vol,evt,1)
            result = of.getEventPreferences()
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
        assert len(result) == 1, 'Wrong count. Expected 1. Got ' + len(result)
 
    def test_getEventRecurrence(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getEventRecurrence"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            er = of.getNewEventRecurrence(1)
            result = of.getEventRecurrence(er.getRecurrenceID())
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getEventRecurrences(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getEventRecurrences"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            of.getNewEventRecurrence(1)
            result = of.getEventRecurrences()
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
        assert len(result) == 1, 'Wrong count. Expected 1. Got ' + len(result)
 
    def test_getEventResources(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getEventResources"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            evt = of.getNewEvent(name, 1, org)
            res = of.getNewResource(name, 1, org)
            evt.addResource(res)
            result = of.getEventResources()
            result2 = of.getEventResources(evt)
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
        assert len(result) == 1, 'Wrong count. Expected 1. Got ' + len(result)
        assert result2, "no output"
        assert len(result2) == 1, 'Wrong count. Expected 1. Got ' + len(result)
 
    def test_getEvents(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getEvents"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            of.getNewEvent(name, 1, org)
            result =  of.getEvents()
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
        assert len(result) == 1, 'Wrong count. Expected 1. Got ' + len(result)
 
    def test_getHousehold(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getHousehold"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            hh = of.getNewHousehold('1',name,1,org)
            #print(hh)
            result = of.getHousehold(hh.getHouseholdID())
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getHouseholds(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getHouseholds"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            of.getNewHousehold('1',name,1,org)
            result = of.getHouseholds()
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
        assert len(result) == 1, 'Wrong count. Expected 1. Got ' + len(result)
 
    def test_getJob(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getJob"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            skill = of.getNewSkill(name,1,org)
            evt = of.getNewEvent(name, 1, org)
            job = of.getNewJob(skill, 1,evt)
            result = of.getJob(job.getJobID())
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
    
    
    def test_getJobAssignment(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getJobAssignment"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            hh = of.getNewHousehold('1',name,1,org)
            vol = of.getNewVolunteer(hh,1,org)
            vol.setVolunteerFirstName('two')
            vol.setVolunteerLastName(name)
            vol.save()
            evt = of.getNewEvent(name, 1, org)
            skill = of.getNewSkill(name,1,org)
            job = of.getNewJob(skill,1,evt)
            evt.addJob(job)
            evt.save()
            ja = of.getNewJobAssignment(job,vol,1)
            result = of.getJobAssignment(ja.getJobAssignmentID())
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getJobAssignments(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getJobAssignments"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            hh = of.getNewHousehold('1',name,1,org)
            vol = of.getNewVolunteer(hh,1,org)
            vol.setVolunteerFirstName('two')
            vol.setVolunteerLastName(name)
            vol.save()
            evt = of.getNewEvent(name, 1, org)
            skill = of.getNewSkill(name,1,org)
            job = of.getNewJob(skill,1,evt)
            of.getNewJobAssignment(job,vol,1)
            result = of.getJobAssignments()
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
        assert len(result) == 1, 'wrong count. expected 1 but got ' + str(len(result))
 
    def test_getJobs(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getJobs"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            skill = of.getNewSkill(name,1,org)
            evt1 = of.getNewEvent(name + '1', 1, org)
            job1 = of.getNewJob(skill,1,evt1)
            result = of.getJobs()
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getJobsOverlapping(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getJobsOverlapping"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            skill = of.getNewSkill(name,1,org)
            evtDbo1 = of.getNewEvent(name + '1', 1, org, dbo=True)
            evtDbo1.eventDuration = 60
            evtDbo1.save()
            of.getNewJob(skill,1,evtDbo1,dbo=True)
            evtDbo2 = of.getNewEvent(name + '2', 1, org, dbo=True)
            job2 = of.getNewJob(skill,1,evtDbo2,dbo=True )
            #for dbo in DbScheduleEvent.objects.all():
            #    print(str(dbo.organization_id) + ' ') 
            result = of.getJobsOverlapping(evtDbo1, dbo=True)
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getLogin(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getLogin"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            result = of.getLogin(oid=1)
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getLoginStatus(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getLoginStatus"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            result = of.getLoginStatus(1)
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getLoginStatuses(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getLoginStatuses"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            result = of.getLoginStatuses()
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
        assert len(result) == 4, 'wrong count. expected 4 but got ' + str(len(result))
 
    def test_getNewActivity(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getNewActivity"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            result = of.getNewActivity(name,1,1,name)
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getNewAddress(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getNewAddress"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            result = of.getNewAddress(1)
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getNewAvailability(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getNewAvailability"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            result = of.getNewAvailability(1)
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
    
    def test_getNewConfigurableProperty(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getNewConfigurableProperty"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            result = of.getNewConfigurableProperty(name,1,1,name,name)
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getNewEvent(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getNewEvent"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            result = of.getNewEvent(name, 1, org)
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getNewEventJoinToResource(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getNewEventJoinToResource"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            evt = of.getNewEvent(name, 1, org)
            res = of.getNewResource(name,1,org)
            result = of.getNewEventJoinToResource(evt,res,1)
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getNewEventPreference(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getNewEventPreference"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            hh = of.getNewHousehold('1',name,1,org)
            hh.setHouseholdFirstName('one')
            hh.setHouseholdLastName(name)
            hh.save()
            vol = of.getNewVolunteer(hh,1,org)
            vol.setVolunteerFirstName('two')
            vol.setVolunteerLastName(name)
            vol.save()
            evt = of.getNewEvent(name, 1, org)
            result = of.getNewEventPreference(vol,evt,1)
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getNewEventRecurrence(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getNewEventRecurrence"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            result = of.getNewEventRecurrence(1,1,1)
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getNewJob(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getNewJob"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            evt = of.getNewEvent(name, 1, org)
            skill = of.getNewSkill(name,1,org)
            result = of.getNewJob(skill,1,evt)
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getNewJobAssignment(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getNewJobAssignment"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            hh = of.getNewHousehold('1',name,1,org)
            vol = of.getNewVolunteer(hh,1,org)
            vol.setVolunteerFirstName('two')
            vol.setVolunteerLastName(name)
            vol.save()
            evt = of.getNewEvent(name, 1, org)
            skill = of.getNewSkill(name,1,org)
            job = of.getNewJob(skill,1,evt)
            evt.addJob(job)
            evt.save()
            result = of.getNewJobAssignment(job,vol,1)
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getNewLocation(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getNewLocation"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            result = of.getNewLocation(name,1,org)
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getNewLogin(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getNewLogin"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            result = of.getNewLogin(name,1,org)
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getNewLoginStatus(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getNewLoginStatus"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            result = of.getNewLoginStatus(name,1)
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
    
    def test_getNewOrganization(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getNewOrganization"
        result = None
        try:
            result = of.createOrganization(name, 1)
            result.save()
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getNewPrivilege(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getNewPrivilege"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            result = of.getNewPrivilege(name, 1)
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getNewProject(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getNewProject"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            result = of.getNewProject(name, 1, org)
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getNewProjectResource(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getNewProjectResource"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            result = of.getNewProjectResource(name,1,org,1,100.00,True)
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
        assert str(result.cost) == '100.0', 'wrong cost expected 100.0 but got ' + str(result.cost)
 
    def test_getNewProjectStatus(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getNewProjectStatus"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            result = of.getNewProjectStatus(name, 1)
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getNewRecurrenceType(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getNewRecurrenceType"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            result = of.getNewRecurrenceType(name,1)
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getNewRelationship(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getNewRelationship"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            hh = of.getNewHousehold('1',name,1,org)
            vol1 = of.getNewVolunteer(hh,1,org)
            vol1.setVolunteerFirstName('one')
            vol1.setVolunteerLastName(name)
            vol1.save()
            vol2 = of.getNewVolunteer(hh,1,org)
            vol2.setVolunteerFirstName('two')
            vol2.setVolunteerLastName(name)
            vol2.save()
            result = of.getNewRelationship(vol1, vol2, 1, org)
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getNewRelationshipType(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getNewRelationshipType"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            hh = of.getNewHousehold('1',name,1,org)
            vol1 = of.getNewVolunteer(hh,1,org)
            vol1.setVolunteerFirstName('1')
            vol1.save()
            vol2 = of.getNewVolunteer(hh,1,org)
            vol2.setVolunteerFirstName('2')
            vol2.save()
            typ = of.getRelationshipType(1)
            result = of.getNewRelationship(vol1,vol2,1,org,typ)
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getNewReport(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getNewReport"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            result = of.getNewReport(name,1,'a@b.net')
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getNewResource(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getNewResource"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            result = of.getNewResource(name,1,org)
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
     
    def test_getNewSchedule(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getNewSchedule"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            result = of.getNewSchedule(DT.now(),DT.now(),1,org)
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getNewScheduleEvent(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getNewScheduleEvent"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            result = of.getNewScheduleEvent(name,1,org)
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getNewScheduleStatus(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getNewScheduleStatus"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            result = of.getNewScheduleStatus(name,1)
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getNewSecurityGroup(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getNewSecurityGroup"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            result = of.getNewSecurityGroup(name,name,1,1,org)
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getNewSkill(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getNewSkill"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            result = of.getNewSkill(name,1,org)
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getNewSkillRelationship(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getNewSkillRelationship"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            s1 = of.getNewSkill('1', 1,org)
            s2 = of.getNewSkill('2', 1,org)
            result = of.getNewSkillRelationship(s1,s2,1)
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getNewSkillRelationshipType(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getNewSkillRelationshipType"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            result = of.getNewSkillRelationshipType(name,1)
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getNewStateCode(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getNewStateCode"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            result = of.getNewStateCode('zq',name)
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getNewTaskStatus(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getNewTaskStatus"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            result = of.getNewTaskStatus(name,1)
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
    
    
    def test_getNewVolunteer(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getNewVolunteer"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            hh = of.getNewHousehold('1',name,1,org)
            result = of.getNewVolunteer(hh,1,org)
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getNewVolunteerSkill(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getNewVolunteerSkill"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            sk = of.getNewSkill(name, 1, org)
            hh = of.getNewHousehold('1',name,1,org)
            vol = of.getNewVolunteer(hh,1,org)
            result = of.getNewVolunteerSkill(vol,sk,1)
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getNewVolunteerSkillAssignment(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getNewVolunteerSkillAssignment"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            hh = of.getNewHousehold('1',name,1,org)
            vol = of.getNewVolunteer(hh,1,org)
            skill = of.getNewSkill(name,1,org)
            vs = of.getNewVolunteerSkill(vol,skill,1)
            evt = of.getNewEvent(name,1,org)
            result = of.getNewVolunteerSkillAssignment(vs,evt,1)
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getNewWorkAddress(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getNewWorkAddress"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            add = of.getNewAddress(1)
            result = of.getNewWorkAddress(add,1)
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
    
    def test_getObject(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getObject"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            result = of.getObject(Organization,org.getOrganizationID())
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getObjects(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getObjects"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            result = of.getObjects(StateCode)
            result2 = of.getObjects('StateCode')
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
        assert len(result) > 0, 'nothing returned using class'
        assert result2, "no output"
        assert len(result2) > 0, 'nothing returned using string'
    
    def test_getOpenDatesBefore(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getOpenDatesBefore"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            of.getNewEvent(name, 1, org)
            end = DT.strptime('2100-01-01', '%Y-%m-%d')
            result = of.getOpenDatesBefore(end, org)
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getOtherEvents(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getOtherEvents"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            loc = of.getNewLocation(name,1,org)
            evt1 = of.getNewEvent(name, 1, org)
            e1id = evt1.getEventID()
            evt1.setLocation(loc)
            evt1.save()
            evt2 = of.getNewEvent('evt2', 1, org)
            evt2.setLocation(loc)
            evt2.save()
            result = of.getOtherEvents(e1id,org)
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
        assert len(result) == 1, 'wrong count expected 1 got ' + str(len(result))
 
    def test_getOtherFamilyVolunteers(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getOtherFamilyVolunteers"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            hh = of.getNewHousehold('1',name,1,org)
            hid = hh.getHouseholdID()
            vol1 = of.getNewVolunteer(hh,1,org)
            vid = vol1.getVolunteerID()
            vol1.setVolunteerFirstName('1')
            vol1.save()
            vol2 = of.getNewVolunteer(hh,1,org)
            vol2.setVolunteerFirstName('2')
            vol2.save()
            vol3 = of.getNewVolunteer(hh,1,org)
            vol3.setVolunteerFirstName('3')
            vol3.save()
            result = of.getOtherFamilyVolunteers(hid,vid)
            #for obj in result:
            #    print(obj)
            #print(DbVolunteer.objects.exclude(volunteerID=5).filter(household_id=4))
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
        assert len(result) == 2, 'wrong count expected 2 got ' + str(len(result))
 
    def test_getPrivilege(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getPrivilege"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            pr = of.getNewPrivilege(name,1)
            result = of.getPrivilege(pr.getPrivilegeID())
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getPrivileges(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getPrivileges"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            of.getNewPrivilege(name,1)
            result = of.getPrivileges()
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
        assert len(result) > 0, 'Failed to get anything'
    
    def test_getProjectResource(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getProjectResource"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            pr = of.getNewProjectResource(name,1,org,1,1.0,True)
            result = of.getProjectResource(pr.getResourceID())
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getProjectResources(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getProjectResources"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            of.getNewProjectResource(name,1,org,1,1.0,True)
            result = of.getProjectResources(org)
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getProjectStatus(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getProjectStatus"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            result = of.getProjectStatus(1)
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getRecurrenceType(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getRecurrenceType"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            result = of.getRecurrenceType(1)
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getRecurrenceTypes(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getRecurrenceTypes"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            result = of.getRecurrenceTypes()
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
        assert len(result) == 5, 'wrong count. expected 5, got ' + str(len(result))
 
    def test_getRecurringEvents(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getRecurringEvents"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            evt = of.getNewEvent(name,1,org)
            er = of.getNewEventRecurrence(1,1,1)
            evt.setRecurrence(er)
            evt.save()
            result = of.getRecurringEvents(org)
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
        assert len(result) == 1, 'wrong count. expected 1, got ' + str(len(result))
 
    def test_getRelationship(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getRelationship"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            hh = of.getNewHousehold('1',name,1,org)
            vol1 = of.getNewVolunteer(hh,1,org)
            vol1.setVolunteerFirstName('1')
            vol1.save()
            vol2 = of.getNewVolunteer(hh,1,org)
            vol2.setVolunteerFirstName('2')
            vol2.save()
            typ = of.getRelationshipType(1)
            rel = of.getNewRelationship(vol1,vol2,1,org,typ)
            result = of.getRelationship(rel.getRelationshipID())
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getRelationships(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getRelationships"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            hh = of.getNewHousehold('1',name,1,org)
            vol1 = of.getNewVolunteer(hh,1,org)
            vol1.setVolunteerFirstName('1')
            vol1.save()
            vol2 = of.getNewVolunteer(hh,1,org)
            vol2.setVolunteerFirstName('2')
            vol2.save()
            typ = of.getRelationshipType(1)
            of.getNewRelationship(vol1,vol2,1,org,typ)
            result = of.getRelationships(org)
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
        assert len(result) == 1, 'wrong count. expected 1, got ' + str(len(result))
 
    def test_getRelationshipType(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getRelationshipType"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            result = of.getRelationshipType(1)
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getRelationshipTypes(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getRelationshipTypes"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            result = of.getRelationshipTypes()
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
        assert len(result) == 4, 'wrong count. expected 4, got ' + str(len(result))
    
    def test_getReport(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getReport"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            rpt = of.getNewReport(name,1)
            result = of.getReport(rpt.getReportID())
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getReports(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getReports"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            rpt = of.getNewReport(name,1)
            result = of.getReports()
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
        assert len(result) == 1, 'invalID row count expected 1, but got: ' + str(len(result))
 
    def test_getResource(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getResource"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            res = of.getNewResource(name,1,org)
            result = of.getResource(res.getResourceID())
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getResourceAvailabilities(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getResourceAvailabilities"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            res = of.getNewResource(name,1,org)
            res.setCount(10)
            res.save()
            evt = of.getNewEvent(name,1,org)
            result = of.getResourceAvailabilities(evt)
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
        assert len(result) == 1, 'invalID row count expected 1, but got: ' + str(len(result))
 
    def test_getResources(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getResources"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            res = of.getNewResource(name,1,org)
            result = of.getResources(org)
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
        assert len(result) == 1, 'invalID row count expected 1, but got: ' + str(len(result))
 
    def test_getResourceUsage(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getResourceUsage"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            evt = of.getNewEvent(name,1,org)
            res = of.getNewResource(name,1,org)
            of.getNewEventJoinToResource(evt,res,1, 5)
            result = of.getResourceUsage(evt,res)
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
        assert result == 5, 'wrong result expected 5, but got: ' + str(result)
 
    def test_getSchedule(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getSchedule"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            of.getNewSchedule(DT.now(),DT.now(),1,org)
            result = of.getSchedules(org)
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getScheduleEvent(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getScheduleEvent"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            evt = of.getNewEvent(name,1,org)
            result = of.getScheduleEvent(evt.getEventID())
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getScheduleEvents(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getScheduleEvents"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            of.getNewEvent(name,1,org)
            result = of.getScheduleEvents()
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
        assert len(result) == 1, 'invalID row count expected 1, but got: ' + str(len(result))
 
    def test_getSchedules(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getSchedules"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            of.getNewSchedule(DT.now(),DT.now(),1,org)
            result = of.getSchedules(org)
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
        assert len(result) == 1, 'invalID row count expected 1, but got: ' + str(len(result))
    
    def test_getScheduleStatus(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getScheduleStatus"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            result = of.getScheduleStatus(1)
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getScheduleStatuses(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getScheduleStatuses"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            result = of.getScheduleStatuses()
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
        assert len(result) == 3, 'invalID row count expected 3, but got: ' + str(len(result))
 
    def test_getSecurityGroup(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getSecurityGroup"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            result = of.getSecurityGroup(1)
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getSkillRelationship(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getSkillRelationship"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            skill1 = of.getNewSkill(name,1,org)
            skill2 = of.getNewSkill('name1',1,org)
            sr = of.getNewSkillRelationship(skill1, skill2, 1)
            result = of.getSkillRelationship(sr.getSkillRelationshipID())
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getSkillRelationships(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getSkillRelationships"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            skill1 = of.getNewSkill(name,1,org)
            skill2 = of.getNewSkill('name1',1,org)
            of.getNewSkillRelationship(skill1, skill2, 1)
            result = of.getSkillRelationships()
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
        assert len(result) == 1, 'invalID row count expected 1, but got: ' + str(len(result))
 
    def test_getSkillRelationshipType(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getSkillRelationshipType"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            result = of.getSkillRelationshipType(1)
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getSkillRelationshipTypes(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getSkillRelationshipTypes"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            result = of.getSkillRelationshipTypes()
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
        assert len(result) == 2, 'invalID row count expected 2, but got: ' + str(len(result))
 
    def test_getSkills(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getSkills"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            of.getNewSkill(name,1,org)
            result = of.getSkills(org)
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
        assert len(result) == 1, 'invalID row count expected 1, but got: ' + str(len(result))
 
    def test_getStateCode(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getStateCode"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            sc = of.getStateCodes()[0]
            result = of.getStateCode(sc.getSc_id())
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getStateCodes(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getStateCodes"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            result = of.getStateCodes()
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
        assert len(result) == 52, 'invalID row count expected 52, but got: ' + str(len(result))
    
    
    def test_getTasks(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getTasks"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            of.getNewTask(name,1,org)
            result = of.getTasks()
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
        assert len(result) == 1, 'invalID row count expected 1, but got: ' + str(len(result))
 
    def test_getTaskStatus(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getTaskStatus"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            result = of.getTaskStatus(1)
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getTeam(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getTeam"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            tm = of.getNewTeam(name,1,org)
            result = of.getTeam(tm.getTeamID())
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getTeams(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getTeams"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            of.getNewTeam(name,1,org)
            result = of.getTeams()
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
        assert len(result) == 1, 'invalID row count expected 1, but got: ' + str(len(result))
 
    def test_getVolunteer(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getVolunteer"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            hh = of.getNewHousehold('1',name,1,org)
            vol = of.getNewVolunteer(hh,1,org)
            result = of.getVolunteer(vol.getVolunteerID())
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getVolunteers(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getVolunteers"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            hh = of.getNewHousehold('1',name,1,org)
            of.getNewVolunteer(hh,1,org)
            result = of.getVolunteers(org)
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
        assert len(result) == 1, 'invalID row count expected 1, but got: ' + str(len(result))
 
    def test_getVolunteersFromTask(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getVolunteersFromTask"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            hh = of.getNewHousehold('1',name,1,org)
            vol = of.getNewVolunteer(hh,1,org)
            task = of.getNewTask(name,1,org)
            task.addVolunteer(vol)
            task.save()
            result = of.getVolunteersFromTask(task)
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getVolunteerSkill(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getVolunteerSkill"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            hh = of.getNewHousehold('1',name,1,org)
            vol = of.getNewVolunteer(hh,1,org)
            skill = of.getNewSkill(name,1,org)
            vs = of.getNewVolunteerSkill(vol,skill,1)
            result = of.getVolunteerSkill(vs.getVolunteerSkillID())
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getVolunteerSkillAssignment(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getVolunteerSkillAssignment"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            hh = of.getNewHousehold('1',name,1,org)
            vol = of.getNewVolunteer(hh,1,org)
            skill = of.getNewSkill(name,1,org)
            vs = of.getNewVolunteerSkill(vol,skill,1)
            evt = of.getNewEvent(name,1,org)
            vsa = of.getNewVolunteerSkillAssignment(vs,evt,1)
            result = of.getVolunteerSkillAssignment(vsa.volunteerSkillAssignmentID.value)
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getVolunteerSkillAssignments(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getVolunteerSkillAssignments"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            hh = of.getNewHousehold('1',name,1,org)
            vol = of.getNewVolunteer(hh,1,org)
            skill = of.getNewSkill(name,1,org)
            vs = of.getNewVolunteerSkill(vol,skill,1)
            evt = of.getNewEvent(name,1,org)
            of.getNewVolunteerSkillAssignment(vs,evt,1)
            result = of.getVolunteerSkillAssignments()
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
    
    def test_getVolunteerSkills(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getVolunteerSkills"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            hh = of.getNewHousehold('1',name,1,org)
            vol = of.getNewVolunteer(hh,1,org)
            skill = of.getNewSkill(name,1,org)
            of.getNewVolunteerSkill(vol,skill,1)
            #print(vol.myDb)
            result1 = of.getVolunteerSkills()
            result2 = of.getVolunteerSkills(vol=vol)
            result3 = of.getVolunteerSkills(skill=skill)
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result1, "no output"
        assert result2, "no output vol"
        assert result3, "no output skill"
 
    def test_getVolunteersNamed(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getVolunteersNamed"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            hh = of.getNewHousehold('1',name,1,org)
            of.getNewVolunteer(hh,1,org,'first',name)
            #print(vol.myDb)
            result = of.getVolunteersNamed(name,org)
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getWorkAddress(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getWorkAddress"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            add = of.getNewAddress(1)
            wa =of.getNewWorkAddress(add,1)
            result = of.getWorkAddress(wa.getWorkAddressID())
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getWorkAddresses(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getWorkAddresses"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            add = of.getNewAddress(1)
            of.getNewWorkAddress(add,1)
            result = of.getWorkAddresses()
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
        assert len(result) == 1, 'invalID row count expected 1, but got: ' + str(len(result))
 
    def test_rejectSchedule(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_rejectSchedule"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            sch = of.getNewSchedule(DT.now(),DT.now(),1,org)
            of.rejectSchedule(sch,1)
            result = of.getDeletedSchedule(sch.getScheduleID())
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
               
    def test_acceptEvent(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_acceptEvent"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            household = of.getNewHousehold('1',name,1, org)
            household.setHouseholdFirstName('1')
            household.setHouseholdLastName(name)
            household.setStreet('1 n Elm')
            household.save()
            vol = of.getNewVolunteer(household, 1,org)
            vol.setVolunteerFirstName('1')
            vol.setVolunteerLastName(name)
            vol.save()
            evt = of.getNewEvent(name, 1, org)
            skill = of.getNewSkill(name, 1, org)
            job = of.getNewJob(skill,1,evt)
            evt.setEventDate(DT.now())
            evt.setEventStartTime('10:00')
            evt.setEventDuration(90)
            evt.addJob(job)
            evt.save()
            evt = of.getEvent(evt.getEventID())
            ja = of.getNewJobAssignment(job, vol, 1)
            result = of.acceptEvent(evt, 1)
            ja2 = of.getJobAssignment(ja.getJobAssignmentID(),True)
            #print('\n' + str(ja2))
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
        assert result.isAccepted(), 'event not accepted'
        assert ja2.accepted, 'assignment not accepted'
    
    def test_acceptSchedule(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_acceptSchedule"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            sch = of.getNewSchedule(DT.now(),DT.now(),1,org)
            result = of.acceptSchedule(sch,1)
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
        assert result.isAccepted(), 'schedule not accepted'
    
    def test_getDeletedActivities(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getDeletedActivities"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            act = of.getNewActivity(name,1,1,name)
            act.delete()
            result = of.getDeletedActivities()
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getDeletedAddresses(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getDeletedAddresses"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            add = of.getNewAddress(1)
            add.delete()
            result = of.getDeletedAddresses()
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getDeletedAvailabilities(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getDeletedAvailabilities"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            av = of.getNewAvailability(1)
            av.delete()
            result = of.getDeletedAvailabilities()
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getDeletedConfigurableProperties(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getDeletedConfigurableProperties"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            cp = of.getNewConfigurableProperty(name,1,1,name,name)
            cp.delete()
            result = of.getDeletedConfigurableProperties()
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getDeletedConfigurationSets(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getDeletedConfigurationSets"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            cp = of.getNewConfigurationSet(name,1)
            cp.delete()
            result = of.getDeletedConfigurationSets()
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getDeletedEventPreferences(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getDeletedEventPreferences"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            hh = of.getNewHousehold('1',name,1,org)
            hh.setHouseholdFirstName('one')
            hh.setHouseholdLastName(name)
            hh.save()
            vol = of.getNewVolunteer(hh,1,org)
            vol.setVolunteerFirstName('two')
            vol.setVolunteerLastName(name)
            vol.save()
            evt = of.getNewEvent(name, 1, org)
            ep = of.getNewEventPreference(vol,evt,1)
            ep.delete()
            result = of.getDeletedEventPreferences()
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getDeletedEventRecurrences(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getDeletedEventRecurrences"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            evt = of.getNewEvent(name,1,org)
            er = of.getNewEventRecurrence(1,1,1)
            er.delete()
            result = of.getDeletedEventRecurrences()
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
    
    def test_getDeletedHouseholds(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getDeletedHouseholds"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            hh = of.getNewHousehold('1',name,1,org)
            hh.delete()
            result = of.getDeletedHouseholds()
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
    
    def test_getDeletedJobs(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getDeletedJobs"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            evt = of.getNewEvent(name, 1, org)
            skill = of.getNewSkill(name,1,org)
            j = of.getNewJob(skill,1,evt)
            j.delete()
            result = of.getDeletedJobs()
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getDeletedLoginStatuses(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getDeletedLoginStatuses"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            ls = of.getLoginStatus(1)
            ls.delete()
            result = of.getDeletedLoginStatuses()
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getDeletedOrganizations(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getDeletedOrganizations"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            org.delete()
            result = of.getDeletedOrganizations()
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getDeletedPasswords(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getDeletedPasswords"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            pwd = of.getNewPassword(name, 1)
            pwd.delete()
            result = of.getDeletedPasswords()
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getDeletedPrivileges(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getDeletedPrivileges"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            pr = of.getPrivilege(1)
            pr.delete()
            result = of.getDeletedPrivileges()
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getDeletedProjectResources(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getDeletedProjectResources"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            pr = of.getNewProjectResource(name,1,org,1,1.0,True)
            pr.delete()
            result = of.getDeletedProjectResources()
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getDeletedProjects(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getDeletedProjects"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            p = of.getNewProject(name,1,org)
            p.delete()
            result = of.getDeletedProjects()
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
    
    def test_getDeletedProjectStatuses(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getDeletedProjectStatuses"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            ps = of.getProjectStatus(1)
            ps.delete()
            result = of.getDeletedProjectStatuses()
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getDeletedRecurrenceTypes(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getDeletedRecurrenceTypes"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            rt = of.getNewRecurrenceType(name, 1)
            rt.delete()
            result = of.getDeletedRecurrenceTypes()
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getDeletedRelationships(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getDeletedRelationships"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            hh = of.getNewHousehold('1',name,1,org)
            vol1 = of.getNewVolunteer(hh,1,org)
            vol1.setVolunteerFirstName('1')
            vol1.save()
            vol2 = of.getNewVolunteer(hh,1,org)
            vol2.setVolunteerFirstName('2')
            vol2.save()
            typ = of.getRelationshipType(1)
            r = of.getNewRelationship(vol1,vol2,1,org,typ)
            r.delete()
            result = of.getDeletedRelationships()
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
   
    def test_getDeletedRelationshipTypes(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getDeletedRelationshipTypes"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            rt = of.getRelationshipType(1)
            rt.delete()
            result = of.getDeletedRelationshipTypes()
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getDeletedReports(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getDeletedReports"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            rpt = of.getNewReport(name,1)
            rpt.delete()
            result = of.getDeletedReports()
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getDeletedScheduleEvents(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getDeletedScheduleEvents"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            evt = of.getNewEvent(name,1,org)
            evt.delete()
            result = of.getDeletedScheduleEvents()
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getDeletedSchedules(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getDeletedSchedules"
        try:
            org = of.createOrganization(name, 1)
            org.save()
            sch = of.getNewSchedule(DT.now(),DT.now(),1,org)
            sch.delete()
            result = of.getDeletedSchedules()
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getDeletedScheduleStatuses(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getDeletedScheduleStatuses"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            ss = of.getScheduleStatus(1)
            ss.delete()
            result = of.getDeletedScheduleStatuses()
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getDeletedSkillRelationships(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getDeletedSkillRelationships"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            skill1 = of.getNewSkill(name,1,org)
            skill2 = of.getNewSkill('name1',1,org)
            sr = of.getNewSkillRelationship(skill1, skill2, 1)
            sr.delete()
            result = of.getDeletedSkillRelationships()
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getDeletedSkillRelationshipTypes(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getDeletedSkillRelationshipTypes"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            sr = of.getSkillRelationshipType(1)
            sr.delete()
            result = of.getDeletedSkillRelationshipTypes()
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getDeletedStateCodes(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getDeletedStateCodes"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            sc = of.getStateCodes()[0]
            sc.delete()
            result = of.getDeletedStateCodes()
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getDeletedTaskStatuses(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getDeletedTaskStatuses"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            ts = of.getTaskStatus(1)
            ts.delete()
            result = of.getDeletedTaskStatuses()
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getDeletedVolunteers(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getDeletedVolunteers"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            hh = of.getNewHousehold('1',name,1,org)
            vol = of.getNewVolunteer(hh,1,org)
            vol.delete()
            result = of.getDeletedVolunteers()
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getDeletedWorkAddresses(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getDeletedWorkAddresses"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            add = of.getNewAddress(1)
            wa = of.getNewWorkAddress(add,1)
            wa.delete()
            result = of.getDeletedWorkAddresses()
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getEventJoinToResource(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getEventJoinToResource"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            evt = of.getNewEvent(name,1,org)
            res = of.getNewResource(name,1,org)
            ejr = of.getNewEventJoinToResource(evt,res,1, 5)
            result = of.getEventJoinToResource(evt,res)
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getEventJoinToResources(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getEventJoinToResources"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            evt = of.getNewEvent(name,1,org)
            res = of.getNewResource(name,1,org)
            ejr = of.getNewEventJoinToResource(evt,res,1, 5)
            result = of.getEventJoinToResources()
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
 
    def test_getProjectStatuses(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getProjectStatuses"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            result = of.getProjectStatuses()
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
        assert len(result) > 1, 'Too few'
 
    def test_getTaskStatuses(self):
        LoaderManager().load()
        of = ObjectFactory()
        err = None
        name = "test_getTaskStatuses"
        result = None
        try:
            org = of.createOrganization(name, 1)
            org.save()
            result = of.getTaskStatuses() 
        except Exception as e:
            err = e
            super().handleException(e)
        assert not err, "got an exception"
        assert result, "no output"
        assert len(result) > 1, 'Too few'
    
    
    ''' 
    def test_methodNames(self):
        methods = inspect.getmembers(ObjectFactory, predicate=inspect.isfunction)
        method_names = [name for name, _ in methods]
        out = sorted(method_names)
        methodNames = {}
        for s in out:
            methodNames[s] = s
        missingMethods = [] 
        classNames = [] 
        count = 0      
        with open('D:\\eclipseWorkspace\\volsched\\vs\\models.py', "r", encoding="utf-8") as file:
            for l in file:
                if not l.startswith('class'):
                    continue
                if 'eventjointoresource' in (l.lower()):
                    continue
                l = l.removeprefix('class')
                l = l.strip()
                l = l.removeprefix('Db')
                l = l.removesuffix('(models.Model):')
                try:
                    nm = methodNames['getNew' + l]
                except:
                    count += 1
                    missingMethods.append('\tdef getNew'+ l + '(self):')
                    missingMethods.append('\t\tresult = None')
                    missingMethods.append('\t\tpass # TO' + 'DO')
                    missingMethods.append('\t\treturn result')
                    missingMethods.append('')
                try:
                    nm = methodNames['get' + l]
                except:
                    count += 1
                    missingMethods.append('\tdef get'+ l + '(self, oid):')
                    missingMethods.append('\t\tresult = None')
                    missingMethods.append('\t\tpass # TO' + 'DO')
                    missingMethods.append('\t\treturn result')
                    missingMethods.append('')
                s = self.getMethodPlural(l)
                try:
                    nm = methodNames['get' + s]     
                except:
                    count += 1
                    missingMethods.append('\tdef get'+ s + '(self):')
                    missingMethods.append('\t\tresult = None')
                    missingMethods.append('\t\tpass # TO' + 'DO')
                    missingMethods.append('\t\treturn result')
                    missingMethods.append('')
                try:
                    nm = methodNames['getDeleted' + l]
                except:
                    count += 1
                    missingMethods.append('\tdef getDeleted'+ l + '(self, oid):')
                    missingMethods.append('\t\tresult = None')
                    missingMethods.append('\t\tpass # TO' + 'DO')
                    missingMethods.append('\t\treturn result')
                    missingMethods.append('')
                try:
                    nm = methodNames['getDeleted' + s]  
                except:
                    count += 1
                    missingMethods.append('\tdef getDeleted'+ s + '(self):')
                    missingMethods.append('\t\tresult = None')
                    missingMethods.append('\t\tpass # TO' + 'DO')
                    missingMethods.append('\t\treturn result')
                    missingMethods.append('')
                                  
        with open('d:\\tmp\\method_names.txt', 'w') as file:
           for item in out:
                file.write(f"{item}\n") 
        
        if len(missingMethods) > 0:
            with open('d:\\tmp\\missing_methods.txt', 'w') as file:
                for item in missingMethods:
                    file.write(f"{item}\n")
            print('\nAdditional methods: ' + str(count))
        else:
            print('all methods defined')
             
    def getMethodPlural(self, name):
        result = name + 's'
        if name[-1] == 's':
            result = name + 'es'
        elif name[-1] == 'y':
            result = name[:-1] + 'ies'
        return result
    '''
    '''      
    def test_getRequiredTests(self):
        #print('running')
        needed = []
        ignored = [
            'debug', 
            'error',  
            'handleException',
            'info' ,
            'delete',
            'now', 
            'refresh', 
            'remove', 
            'resetSingleton', 
            'save',  
            'trace', 
            'warning']
        ofDict = ObjectFactory.__dict__
        myDict = ObjectFactoryTests.__dict__
        out = []
        for name, att in ofDict.items():
            #if att in ignored:
            #    pass
            if name in ignored:
                continue
            if name[:1] == '_':
                continue
            nm = 'test_' + name
            obj = myDict.get(nm)
            if not obj:
                needed.append(nm)
        count = len(needed)
        if len(needed) > 1:
            needed.sort(key=str.lower)
        for l in needed:
            out.append('    def ' + l + '(self):')
            out.append('        LoaderManager().load()')
            out.append('        of = ObjectFactory()')
            out.append('        err = None')
            out.append('        name = "' + l + '"')
            out.append('        result = None')
            out.append('        try:')
            out.append('            org = of.createOrganization(name, 1)') 
            out.append('            org.save()') 
            out.append('            pass #TO' + 'DO')    
            out.append('        except Exception as e:')
            out.append('            err = e')
            out.append('            super().handleException(e)')
            out.append('        assert not err, "got an exception"')
            out.append('        assert result, "no output"')
            out.append(' ')
            #print(out)
            #break        
        
        with open('d:\\tmp\\needed_tests.txt', 'w') as file:
            for item in out:
                file.write(f"{item}\n")
        if count:
            print('\nAdditions to tests: ' + str(count))
    '''