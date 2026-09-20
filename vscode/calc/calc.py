from vscode.base.base import VSBase,ObjectFactoryBase
from vscode.base.business_objects import *
from vscode.utils.utils import *

class OrganizationBuilder(VSBase):

    def __init__(self):
        super(self).__init__()

    def build(self, name, login):
        of = ObjectFactoryBase()
        if super().isBlank(name):
            raise Exception("you must supply an organization name")
        
        if not login:
            raise Exception("you must supply a valID login object")
        
        org = of.getOrganizationByName(name)
        if org:
            raise Exception("There is already an organization named \"" + name + "\" in the database.")
        
        defaultOrg = of.getOrganizationByName("$$default$$")
        if not defaultOrg:
            raise Exception("Couldn't get default organization")
        org = of.getNewOrganization()
        org.setName(name)
        org.setCreateUser(login.getID())
        org.setUpdateUser(login.getID())
        org.setCreateDate(super().now())
        org.setUpdateDate(super().now())
        of.save(org)
        liNew = of.getNewLogin()
        liNew.setLogin("Admin")
        liNew.setLoginName("Admin")
        liNew.setOrganization(org)
        liNew.setPassword("Password1")
        liNew.setSecret("secret")
        liNew.setLastChange(super().now())
        liNew.setCreateDate(super().now())
        liNew.setUpdateDate(super().now())
        liNew.setCreateUser(login.getID())
        liNew.setUpdateUser(login.getID())
        ls = ValueTableManager().getValue("LoginStatus", str(LoginStatus.STATUS_READY))
        liNew.setLoginStatus(ls)
        of.save(liNew)
        liNew = of.getNewLogin()
        liNew.setLogin("SystemUtilities")
        liNew.setLoginName("System Utilities")
        liNew.setOrganization(org)
        liNew.setPassword("Password1")
        liNew.setSecret("secret")
        liNew.setLastChange(super().now())
        liNew.setCreateDate(super().now())
        liNew.setUpdateDate(super().now())
        liNew.setCreateUser(login.getID())
        liNew.setUpdateUser(login.getID())
        liNew.setLoginStatus(ls)
        of.save(liNew)
        for cs in of.getConfigurationSets(defaultOrg):
            csNew = ConfigurationSet(cs)
            csNew.setOrganization(org)
            csNew.setCreateDate(super().now())
            csNew.setUpdateDate(super().now())
            csNew.setCreateUser(login.getID())
            csNew.setUpdateUser(login.getID())
            of.save(csNew)
            of.refresh(csNew)
            for cp in cs.getProperties():
                cpNew = ConfigurableProperty(cp)
                cpNew.setPropertyConfigurationSetID(cs.getConfigurationSetID())
                of.save(cpNew)
                csNew.addProperty(cpNew)
            of.save(csNew)
            for sg in of.getSecurityGroups(defaultOrg):
                newSg = SecurityGroup(sg)
                newSg.setOrganization(org)
                of.save(newSg)
            for p in sg.getPrivileges():
                newSg.addPrivilege(p)
            newSg.save()

        
class EventRejecter(VSBase):

    def __init__(self, schedule, uid): 
        self.schedule = schedule
        self.start = schedule.getScheduleStartDate()    
        self.end = schedule.getScheduleEndDate()
        self.org = schedule.getOrganization()
        self.loginID = uid
        self.of = ObjectFactory()
        super()

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
    
    