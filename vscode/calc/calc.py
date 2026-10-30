from vscode.base.base import VSBase,Constants
from vscode.msgr.msgr import *
from vscode.utils.exceptions import *
from vscode.utils.utils import *
from vscode.val.vals import *

class OrganizationBuilder(VSBase):

    def __init__(self):
        super().__init__()

    def build(self, name, login):
        from vs.bean.beans import SessionData
        #print('OrganizationBuilder ' + str(SessionData().currentLogin.login))
        from vscode.base.business_objects import ObjectFactory,ConfigurationSet,ConfigurableProperty,SecurityGroup
        of = ObjectFactory()
        if super().isBlank(name):
            raise Exception("you must supply an organization name")
        
        if not login:
            raise Exception("you must supply a valid login object")
        
        org = of.getOrganization(name=name)
        if org:
            raise Exception("There is already an organization named \"" + name + "\" in the database.")
        
        defaultOrg = of.getOrganization(name="Volunteer Scheduler")
        if not defaultOrg:
            raise Exception("Couldn't get default organization")
        org = of.getNewOrganization()
        org.setName(name)
        uid = login.getID()
        if not uid:
            uid = 1
        org.setOrganizationCreateUser(uid)
        org.setOrganizationUpdateUser(uid)
        org.setCreateDate(super().now())
        org.setUpdateDate(super().now())
        org.save()
        liNew = of.getNewLogin("Admin",uid,org)
        liNew.setLoginName("Admin")
        liNew.setPassword("Password1")
        liNew.setSecret("secret")
        liNew.setLastChange(super().now())
        liNew.setLoginCreateDate(super().now())
        liNew.setLoginUpdateDate(super().now())
        liNew.setLoginCreateUser(uid)
        liNew.setLoginUpdateUser(uid)
        ls = ValueTableManager().getValue("LoginStatus", str(LoginStatus.STATUS_READY))
        liNew.setLoginStatus(ls)
        liNew.save()
        liNew2 = of.getNewLogin("SystemUtilities",uid,org)
        liNew2.setLoginName("System Utilities")
        liNew2.setPassword("Password1")
        liNew2.setSecret("secret")
        liNew2.setLastChange(super().now())
        liNew2.setLoginCreateDate(super().now())
        liNew2.setLoginUpdateDate(super().now())
        liNew2.setLoginCreateUser(login.getID())
        liNew2.setLoginUpdateUser(login.getID())
        liNew2.setLoginStatus(ls)
        liNew2.save()
        for cs in of.getConfigurationSets(defaultOrg):
            csNew = ConfigurationSet(cs)
            csNew.setOrganization(org)
            csNew.setConfigurationSetCreateDate(super().now())
            csNew.setConfigurationSetUpdateDate(super().now())
            csNew.setConfigurationSetCreateUser(login.getID())
            csNew.setConfigurationSetUpdateUser(login.getID())
            csNew.save()
            for cp in cs.getProperties():
                cpNew = ConfigurableProperty(cp)
                cpNew.setPropertyConfigurationSetID(cs.getConfigurationSetID())
                cpNew.setPropertyCreateUser(uid)
                cpNew.setPropertyUpdateUser(uid)
                cpNew.save()
                csNew.addProperty(cpNew)
            csNew.save()
            for sg in of.getSecurityGroups(defaultOrg):
                newSg = SecurityGroup(sg)
                newSg.setOrganization(org)
                newSg.setSecurityGroupCreateUser(uid)
                newSg.setSecurityGroupUpdateUser(uid)
                newSg.save()
            for p in sg.getPrivileges():
                newSg.addPrivilege(p)
            newSg.save()
        SessionData().currentLogin = login  # got currupted 
        #print('OrganizationBuilder exit ' + str(SessionData().currentLogin.login))

        
class EventRejecter(VSBase):

    def __init__(self, schedule, uid):
        super().__init__() 
        self.schedule = schedule
        self.start = schedule.getScheduleStartDate()    
        self.end = schedule.getScheduleEndDate()
        self.org = schedule.getOrganization()
        self.loginID = uid
        from vscode.base.business_objects import ObjectFactory
        self.of = ObjectFactory()

    def rejectEvents(self):
        assignments = []
        assignments.extend(self.of.getVolunteerSkillAssignments())
        for sei in self.of.getEvents(schedule=self.schedule):
            self.resetSkillDates(sei, assignments)
        self.of.rejectEvents(self.start, self.end, self.org, self.loginId)
        for vsa in assignments:
            vsa.delete()

    def resetSkillDates(self, sei, assignments):
        for ji in self.of.getJobs(sei):
            ja = ji.getAssignment()
            if ja == None:
                if ji.getJobAssignmentID() != None:
                    ja = self.of.getJobAssignment(ji.getJobAssignmentID())
                if ja == None:
                    continue
            vol = ja.getVolunteer()
            skillID = ji.getJobSkillID()
            for vsi in self.of.getVolunteerSkills(vol):
                if skillID == vsi.getVsSkillID():
                    self.setLastAssignment(vsi, sei, ja, assignments)
                    vsi.setVsUpdateUser(self.loginId)
                    vsi.save()
                    break
                
    def setLastAssignment(self, vsi, sei, ja, assignments):
        for vsAssgn in assignments:
            if vsAssgn.getVsaVolunteerSkillID() == vsi.getVsaVolunteerSkillID() \
                    and vsAssgn.getVsaEventID() == sei.getEventID():
                if vsi.getLastAssignment():
                    vsi.setPreviousAssignment(vsi.getLastAssignment())
                    vsi.setVsLastAssignment(None)
                else:
                    dat = ja.getPreviousAssignmentDate()
                    vsi.setLastAssignment(dat)
     
     
class EventValidator(VSBase):
    
    def __init__(self):
        super().__init__()
        from vscode.base.business_objects import ObjectFactory
        self.of = ObjectFactory()
        
    def validate(self, event):
        if not event.isDeleted():
            if event.getLocation():
                m = VSMessageFactory.getMissingEventLocationError(MessageSeverity.RECOVERABLE)
                raise InvalidAttributeValueException(m, event.getDisplayString())
            else:
                try:
                    ignore = False
                    try:
                        s = VSSystemOption().get("ignoreEventValidation")
                        ignore = super().stringToBool(s)
                    except:
                        pass
                    if not ignore:
                        sched = self.of.getSchedule(event)
                        if sched:
                            sStart = sched.getScheduleStartDate()
                            sEnd = sched.getScheduleEndDate()
                            eDate = event.getEventDate()
                            if eDate < sStart or eDate > sEnd:
                                m = VSMessageFactory.getEventScheduleDateChangeError(MessageSeverity.RECOVERABLE)
                                raise EventDateScheduleDateConflictException(m, event.getDisplayString())
                            lst = self.of.getOtherEvents(event)
                        if len(lst) > 0:
                            for sei in lst:
                                if self.eventsOverlap(event, sei):
                                    m = VSMessageFactory.getExistingEventError(MessageSeverity.RECOVERABLE)
                                    raise EventInSameLocationException(m, event.getDisplayString())
                except PersistenceException as pe:
                    raise InvalidAttributeValueException(pe)
                
    def eventsOverlap(self,  event1,  event2, ignoreLocation=False):
        result = False
        from vscode.base.business_objects import ScheduleEvent
        if isinstance(event1, ScheduleEvent) and isinstance(event2, ScheduleEvent) and \
        event1.getEventDate() and event2.getEventDate():
            date1 = event1.getEventDate().strftime(VSBase.DATE_FMT)
            date2 = event2.getEventDate().strftime(VSBase.DATE_FMT)
            if date1 == date2:
                time1 = event1.getEventStartTime().strftime(VSBase.TIME_FMT)
                time2 = event2.getEventStartTime().strftime(VSBase.TIME_FMT)
                end1 = event1.getEventStartTime() + timedelta(minutes=event1.getEventDuration()) 
                end2 = event2.getEventStartTime() + timedelta(minutes=event2.getEventDuration())
                if time1 >= time2 and end1 <= end2:
                    result = True
                elif time2 >= time1 and end2 <= end1:
                    result = True
                if result and not ignoreLocation:
                    if event1.location.getLocationID() != event2.location.getLocationID():
                        result = False                      
        return result   

    
class VolunteerLoginManager(VSBase):
    resetStatus = None
    
    def __init__(self):
        super().__init__()
        from vscode.base.business_objects import ObjectFactory 
        self.of = ObjectFactory()
        
    def getResetStatus(self):
        if VolunteerLoginManager.resetStatus == None:
            for lis in self.of.getLoginStatuses():
                if lis.getLoginStatusID() == LoginStatus.STATUS_RESET:
                    VolunteerLoginManager.resetStatus = lis
                    break
        return VolunteerLoginManager.resetStatus

    def save(self, vol, loginId):  
        if vol:
            if vol.isNew():
                self.addLogin(vol, loginId)
            else:
                if vol.getVolunteerLoginID():     
                    li = self.of.getLogin(vol.getVolunteerLoginID())
                    vol.setLogin(li)
                    if self.needSecurityGroup(li):
                        li.addSecurityGroup(self.of.getSecurityGroup(Constants.VOLUNTEER_SECURITY_GROUP_ID))
                    email = vol.getEmail()
                    if Utils.notBlank(email) and li.getEmail() != email:
                        try:
                            li.setEmail(email)
                            li.save()
                        except Exception as iave:
                            super().handleException(iave)
                else:
                    self.addLogin(vol, loginId)
            vol.save()
            
    def addLogin(self, vol, loginId):
        if self.checkForDuplicate(vol, False):
            raise DuplicateLoginException()
        deleted = self.checkForDuplicate(vol, True)
        if deleted:
            self.resurrect(vol, loginId)
        else:
            li = vol.getLogin()
            if not li:
                name = "".join(vol.getVolunteerName().split())
                li = self.of.getNewLogin()
                li.setLogin(name)
                li.setOrganization(vol.getOrganization())
                li.setLoginName(vol.getVolunteerName())
                li.setSecret(name)
                if len(name) > 20:
                    li.setSecret("secret")
                else:
                    li.setSecret(name)
                li.setPassword("Password1")
                li.setLastChange(DT.now())
                li.setLoginCreateUser(loginId)
                li.setLoginUpdateUser(loginId)
                li.setLoginStatus(self.getResetStatus())
                li.save()
                vol.setLogin(li)
                li.addSecurityGroup(self.of.getSecurityGroup(Constants.VOLUNTEER_SECURITY_GROUP_ID))
            else:
                if self.needSecurityGroup(li):
                    li.addSecurityGroup(self.of.getSecurityGroup(Constants.VOLUNTEER_SECURITY_GROUP_ID))

    def resurrect(self, vol, loginId):
        from vscode.base.business_objects import Volunteer
        vols = self.of.getDeletedObjects(Volunteer.__class__)
        vol2 = None
        for v in vols:
            if Utils.equals(vol.getVolunteerFirstName(), v.getVolunteerFirstName())\
                    and vol.getVolunteerLastName() == v.getVolunteerLastName():
                vol2 = v
                break
        if vol2:
            vol2.setDeleted(False)
            vol2.setUpdateUser(loginId)
            vol2.save()
            li = vol2.getLogin()
            if li:
                li.setDeleted(False)
                li.setUpdateUser(loginId)
                self.of.save(li)
                
    def checkForDuplicate(self, vol ,deleted=False):
        from vscode.base.business_objects import Login
        result = False
        if deleted:
            for li in self.of.getDeletedObjects(Login.__class__):
                if Utils.equals(vol.getVolunteerName(), li.getLoginName()):
                    result = True
                    break
        else:
            org = vol.getOrganization()
            for li in self.of.getLogins(org):
                if Utils.equals(vol.getVolunteerName(), li.getLoginName()):
                    result = True
                    break
        return result
    

    def needSecurityGroup(self, li):
        result = True
        if li.getSecurityGroups():
            for sg in li.getSecurityGroups():
                if (sg.getSecurityGroupID() == Constants.VOLUNTEER_SECURITY_GROUP_ID):
                    result = False
                    break
        return result
    