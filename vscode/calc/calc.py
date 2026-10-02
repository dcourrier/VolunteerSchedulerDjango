from vscode.base.base import VSBase,ObjectFactoryBase
from vscode.utils.exceptions import *
from vscode.utils.utils import *
from vscode.val.vals import *

class OrganizationBuilder(VSBase):

    def __init__(self):
        super().__init__()

    def build(self, name, login):
        from vscode.base.business_objects import ObjectFactory,ConfigurationSet,ConfigurableProperty,SecurityGroup
        of = ObjectFactory()
        if super().isBlank(name):
            raise Exception("you must supply an organization name")
        
        if not login:
            raise Exception("you must supply a valID login object")
        
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
        liNew.setLogintCreateDate(super().now())
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

        
class EventRejecter(VSBase):

    def __init__(self, schedule, uid):
        super().__init__() 
        self.schedule = schedule
        self.start = schedule.getScheduleStartDate()    
        self.end = schedule.getScheduleEndDate()
        self.org = schedule.getOrganization()
        self.loginID = uid

    def rejectEvents(self):
        assignments = []
        assignments.extend(self.of.getVolunteerSkillAssignments())
        for sei in self.of.getEvents(schedule=self.schedule):
            self.resetSkillDates(sei, assignments)
        ''' what's this?
        self.of.rejectEvents(self.start, self.end, self.org, self.loginId)
        '''
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
                        of = ObjectFactory()
                        sched = of.getSchedule(event)
                        if sched:
                            sStart = sched.getScheduleStartDate()
                            sEnd = sched.getScheduleEndDate()
                            eDate = event.getEventDate()
                            if eDate < sStart or eDate > sEnd:
                                m = VSMessageFactory.getEventScheduleDateChangeError(MessageSeverity.RECOVERABLE)
                                raise EventDateScheduleDateConflictException(m, event.getDisplayString())
                            lst = of.getOtherEvents(event)
                        if len(lst) > 0:
                            for sei in lst:
                                if self.eventsOverlap(event, sei):
                                    m = VSMessageFactory.getExistingEventError(MessageSeverity.RECOVERABLE)
                                    raise EventInSameLocationException(m, event.getDisplayString())
                except PersistenceException as pe:
                    raise InvalidAttributeValueException(pe)
                
    def eventsOverlap(self,  event1,  event2, ignoreLocation=False):
        result = False
        if event1 != None and event2 != None:
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
    
    