from abc import abstractmethod,ABC
import functools

from vscode.base.base import VSBase
from vscode.base.business_objects import *
from vscode.utils.utils import Utils

class DefaultComparator(VSBase):
    
    def compareInt(self, o1, o2):
        return Utils.compareInt(o1, o2)

    def compareDates(self, d1, d2):
        return Utils.compareDates(d1, d2)
    
    def compareTimes(self, d1, d2):
        return Utils.compareTimes(d1, d2)
    
    def isNull(self, o1, o2):
        return Utils.isNull(o1, o2)
    
    def compareNull(self, o1, o2):
        return Utils.compareNull(o1, o2)
    
    def compareIgnoreCase(self, o1, o2):
        return Utils.compareIgnoreCase(o1, o2)
    
    def setup(self,o1,o2):
        result = 0
        if Utils.isNull(o1, o2):
            result = Utils.compareNull(o1, o2)
        return result
    
    def compare(self, o1, o2):
        result = self.setup(o1,o2)
        if not result:
            s1 = str(o1)
            s2 = str(o2)
            if s1 > s2:
                result = 1
            elif s1 < s2:
                result = -1
        return result
class ActivityComparator(DefaultComparator):

    def compare(self, o1, o2):
        result = 0
        if super().isNull(o1, o2):
            result = super().compareNull(o1, o2)
        else:
            result = o1.getDescription().lower() == o2.getDescription().lower()
        
        return result
   
class AvailabilityComparator(DefaultComparator):

    def compare(self, o1, o2):
        result = 0
        if super().isNull(o1, 2):
            result = super().compareNull(o1, o2)
        else:
            if not o1.getAvailabilityStartDate():
                result = super().compareNull(o1.getAvailabilityStartDate(),
                        o2.getAvailabilityStartDate())
                if result == 0:
                    if not o1.getAvailabilityEndDate():
                        result = super().compareNull(o1.getAvailabilityEndDate(),
                                o2.getAvailabilityEndDate())
                    else:
                        result = o1.getAvailabilityEndDate().compareTo(o2.getAvailabilityEndDate())
            else:
                if (o1.getAvailabilityStartDate() is None or o2.getAvailabilityStartDate() is None):
                    result = super().compareNull(o1.getAvailabilityStartDate(),
                            o2.getAvailabilityStartDate())
                else:
                    result = super().compareDates(o1.getAvailabilityStartDate(), o2.getAvailabilityStartDate())
        return result

class ConfigurablePropertyComparator(DefaultComparator):

    def compare(self, o1, o2):
        result = 0
        if super().isNull(o1, 2):
            result = super().compareNull(o1, o2)
        else:
            if (result == 0):
                result = super().compareIgnoreCase(o1.propertyDescription, o2.propertyDescription)
        return result
    
class HouseholdComparator(DefaultComparator):

    def compare(self, o1, o2):
        result = 0
        if super().isNull(o1, 2):
            result = super().compareNull(o1, o2)
        else:
            result = super().compareIgnoreCase(o1.getHouseholdLastName(), o2.getHouseholdLastName())
            if result == 0:
                result = super().compareIgnoreCase(o1.getHouseholdFirstName(), o2.getHouseholdFirstName())
        return result
 
class JobAssignmentComparator(DefaultComparator):

    def compare(self, o1, o2):
        result = 0
        if super().isNull(o1, 2):
            result = super().compareNull(o1, o2)
        else:
            if result == 0:
                result = super().compareIgnoreCase(o1.getJob().getSkill().getSkillName(), o2.getJob().getSkill().getSkillName())
        return result
    
class JobComparator(DefaultComparator):

    def compare(self, o1, o2):
        result = 0
        if super().isNull(o1, 2):
            result = super().compareNull(o1, o2)
        else:
            if (result == 0):
                result = super().compareIgnoreCase(o1.getSkill().getSkillName(), o2.getSkill().getSkillName())
        return result
    
class LocationComparator(DefaultComparator):

    def compare(self, o1, o2):
        result = 0
        if super().isNull(o1, 2):
            result = super().compareNull(o1, o2)
        else:
            result = super().compareIgnoreCase(o1.getLocationName(), o2.getLocationName())     
        return result
     
class LoginComparator(DefaultComparator):

    def compare(self, o1, o2):
        result = 0
        if super().isNull(o1, 2):
            result = super().compareNull(o1, o2)
        else:
            super().compareIgnoreCase(o1.getLogin(), o2.getLogin())
        return result
         
class LoginStatusComparator(DefaultComparator):

    def compare(self, o1, o2):
        result = 0
        if super().isNull(o1, 2):
            result = super().compareNull(o1, o2)
        else:
            result = super().compareIgnoreCase(o1.getDisplayString(), o2.getDisplayString())
        return result
    
class OrganizationComparator(DefaultComparator):

    def compare(self, o1, o2):
        result = 0
        if super().isNull(o1, o2):
            result = super().compareNull(o1, o2)
        else:
            result = super().compareIgnoreCase(o1.getName(), o2.getName())
        return result
    
class PrivilegeComparator(DefaultComparator):

    def compare(self, o1, o2):
        result = 0
        if super().isNull(o1, o2):
            result = super().compareNull(o1, o2)
        else:
            result = super().compareIgnoreCase(o1.getPrivilegeName(), o2.getPrivilegeName())
        return result
     
class ProjectComparator(DefaultComparator):

    def compare(self, o1, o2):
        result = 0
        if super().isNull(o1, o2):
            result = super().compareNull(o1, o2)
        else:
            result = super().compareIgnoreCase(o1.getProjectName(), o2.getProjectName())
        return result
    
class RecurrenceTypeComparator(DefaultComparator):

    def compare(self, o1, o2):
        result = 0
        if super().isNull(o1, 2):
            result = super().compareNull(o1, o2)
        else:
            result = super().compareIgnoreCase(o1.getDisplayString(), o2.getDisplayString())
        return result
     
class RelationshipTypeComparator(DefaultComparator):

    def compare(self, o1, o2):
        result = 0
        if super().isNull(o1, o2):
            result = super().compareNull(o1, o2)
        else:
            result = super().compareIgnoreCase(o1.getDisplayString(), o2.getDisplayString())
        return result
     
class ReportComparator(DefaultComparator):

    def compare(self, o1, o2):
        result = 0
        if super().isNull(o1, 2):
            result = super().compareNull(o1, o2)
        else:
            s1 = o1.getReportName()
            s2 = o2.getReportName()
            result = super().compareIgnoreCase(s1, s2)
        return result
     
class ResourceAvailabilityComparator(DefaultComparator):

    def compare(self, o1, o2):
        result = 0
        if super().isNull(o1, o2):
            result = super().compareNull(o1, o2)
        else:
            r1 = o1.getResource()
            r2 = o2.getResource()
            if super().isNull(r1, r2):
                result = super().compareNull(r1, r2)
            else:
                result = super().compareIgnoreCase(r1.getName(), r2.getName())
        return result
 
class ResourceComparator(DefaultComparator):

    def compare(self, o1, o2):
        result = 0
        if super().isNull(o1, o2):
            result = super().compareNull(o1, o2)
        else:
            result = super().compareIgnoreCase(o1.getName(), o2.getName())
        return result
    
class ScheduleComparator(DefaultComparator):

    def compare(self, o1, o2):
        result = 0
        if super().isNull(o1, o2):
            result = super().compareNull(o1, o2)
        else:
            d1 = o1.getScheduleStartDate()
            d2 = o2.getScheduleStartDate()
            result = super().compareDates(d1, d2)
        return result
    
class ScheduleEventComparator(DefaultComparator):

    def compare(self, o1, o2):
        result = 0
        if super().isNull(o1, o2):
            result = super().compareNull(o1, o2)
        else:
            result = super().compareDates(o1.getEventDate(), o2.getEventDate())
            if result == 0:
                result = super().compareTimes(o1.getEventStartTime(), o2.getEventStartTime())
            if result == 0:
                result = super().compareIgnoreCase(o1.getEventName(), o2.getEventName())
            return result
    
class SecurityGroupComparator(DefaultComparator):

    def compare(self, o1, o2):
        result = 0
        if super().isNull(o1, o2):
            result = super().compareNull(o1, o2)
        else:
            result = super().compareIgnoreCase(o1.getSecurityGroupName(), o2.getSecurityGroupName())
        return result

class SkillComparator(DefaultComparator):

    def compare(self, o1, o2):
        result = 0
        if super().isNull(o1, o2):
            result = super().compareNull(o1, o2)
        else:
            result = super().compareIgnoreCase(o1.getSkillName(), o2.getSkillName())
        return result
     
class TaskComparator(DefaultComparator):

    def compare(self, o1, o2):
        result = 0
        if super().isNull(o1, o2):
            result = super().compareNull(o1, o2)
        else:
            result = super().compareIgnoreCase(o1.getTaskName(), o2.getTaskName())
            if not result:                                     
                if super().isNull(o1.getTaskID(), o2.getTaskID()):
                    result = super().compareNull(o1.getTaskID(), o2.getTaskID())
                else:
                    result = super().compareInt(o1.getTaskID(), o2.getTaskID())
        return result
 
class TeamComparator(DefaultComparator):

    def compare(self, o1, o2):
        result = 0
        if super().isNull(o1, o2):
            result = super().compareNull(o1, o2)
        else:
            result = super().compareIgnoreCase(o1.getTeamName(), o2.getTeamName())
        return result
    
class VolunteerComparator(DefaultComparator):

    def compare(self, o1, o2):
        result = 0
        if super().isNull(o1, o2):
            result = super().compareNull(o1, o2)
        else:
            result = HouseholdComparator().compare(o1.getHousehold(), o2.getHousehold())
            if (result == 0):
                result = super().compareIgnoreCase(o1.getVolunteerLastName(), o2.getVolunteerLastName())
            if result == 0:
                result = super().compareIgnoreCase(o1.getVolunteerFirstName(), o2.getVolunteerFirstName())
            return result
    
class RelationshipComparator(DefaultComparator):

    def compare(self, o1, o2):
        result = 0
        if super().isNull(o1, o2):
            result = super().compareNull(o1, o2)
        else:
            result = VolunteerComparator().compare(o1.getVolunteerOne(), o2.getVolunteerTwo())
            if result == 0:
                result = super().compareInt(o1.getRelationshipTypeID(), o2.getRelationshipTypeID())
        return result
   
class VolunteerSkillComparator(DefaultComparator):

    def compare(self, o1, o2):
        result = 0
        if super().isNull(o1, o2):
            result = super().compareNull(o1, o2)
        else:
            result = VolunteerComparator().compare(o1.getVolunteer(), o2.getVolunteer())
            if result == 0:
                result = SkillComparator().compare(o1.getSkill(), o2.getSkill())
        return result       
class ComparatorFactory(VSBase):
    @staticmethod
    def getComparator(obj):
        from vscode.base.business_objects import Activity,Availability,Household,ConfigurableProperty,Job,Location,Login,Organization,Privilege,Project,Relationship,Report,Resource,Schedule,ScheduleEvent,SecurityGroup,Skill,Task,Team,Volunteer,VolunteerSkill 
        result = None
        if isinstance(obj, Activity):
            result = ActivityComparator()
        elif isinstance(obj, Availability):
            result = AvailabilityComparator()
        elif isinstance(obj, Household):
            result = HouseholdComparator()
        elif isinstance(obj, ConfigurableProperty):
            result = ConfigurablePropertyComparator()
        elif isinstance(obj, Job):
            result = JobComparator()
        elif isinstance(obj, Location):
            result = LocationComparator()
        elif isinstance(obj, Login):
            result = LoginComparator()
        elif isinstance(obj, Organization):
            result = OrganizationComparator()
        elif isinstance(obj, Privilege):
            result = PrivilegeComparator()
        elif isinstance(obj, Project):
            result = ProjectComparator()
        elif isinstance(obj, Relationship):
            result = RelationshipComparator()
        elif isinstance(obj, Report):
            result = ReportComparator()
        elif isinstance(obj, Resource):
            result = ResourceComparator()
        #elif isinstance(obj, ResourceAvailability):
        #    result = ResourceAvailabilityComparator()
        elif isinstance(obj, Schedule):
            result = ScheduleComparator()
        elif isinstance(obj, ScheduleEvent):
            result = ScheduleEventComparator()
        elif isinstance(obj, SecurityGroup):
            result = SecurityGroupComparator()
        elif isinstance(obj, Skill):
            result = SkillComparator()
        elif isinstance(obj, Task):
            result = TaskComparator()
        elif isinstance(obj, Team):
            result = TeamComparator()
        elif isinstance(obj, Volunteer):
            result = VolunteerComparator()
        elif isinstance(obj, VolunteerSkill):
            result = VolunteerSkillComparator()
        else:
            result = DefaultComparator()
        return result
    
class Collections(ABC):
    @staticmethod
    def sort(lst,  comparator=None):
        if lst and isinstance(lst,list) and len(lst) > 1:
            if not comparator:
                comparator = ComparatorFactory.getComparator(lst[0])
        lst = sorted(lst, key=functools.cmp_to_key(comparator.compare))
