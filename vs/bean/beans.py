from datetime import datetime as DT
from django.contrib import messages
from django.template.context_processors import request
from email_validator import validate_email, EmailNotValidError
from enum import Enum
from loguru import logger

from vscode.base.base import VSBase
from vscode.base.business_objects import *
from vscode.comparator.comp import *
from vscode.utils.exceptions import PersistenceException
from vscode.utils.utils import Utils,ValuesHolder,Encrypter
from vscode.val.vals import *


class VSBaseBean(VSBase):
    def __init__(self):
        pass
         
    def handleException(self, err):
        super().handleException(err)        


class SkillCount(VSBase):

    def __init__(self, num=0):
        self.num = num;

    def getNum(self):
        return self.num

    def getDisplayString(self):
        result = ''
        if self.num:
            result = str(self.um)
        return result
      

class RequestType(Enum):
    activity = 1
    availability = 2
    event = 3
    household = 4 
    job = 5
    project = 6
    projectResource = 7
    relationship = 8
    report = 9
    resource = 10
    schedule = 11
    subtask =  12
    task = 13
    team = 14
    securityGroup = 15
    subproject =  16
    volunteer = 17
    volunteerSkill = 18


class AuthorizationManager():

    @staticmethod
    def isAuthorized(request, login):
        result = False
        if request is not None and login:
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
        if login:
            securityGroups = login.getSecurityGroups()
            if len(securityGroups) == 1:
                sg = securityGroups[0]
                if 'SECURITY_GROUP_VOLUNTEER'.lower() == sg.getSecurityGroupName().lower():
                    result = True
        return result;
    
    
class RequestParametersHolder():

    def __init__(self, request=None):
        self.activityID = None
        self.availabilityID = None
        self.eventID = None
        self.householdID = None
        self.jobID = None
        self.parentTaskID = None
        self.projectID = None
        self.projectResourceID = None
        self.parentProjectID = None
        self.relationshipID = None
        self.reportID = None
        self.request = None
        self.taskID = None
        self.teamID = None
        self.securityGroupID = None
        self.scheduleID = None
        self.volunteerID = None
        self.volunteerSkillID = None
        self.cameFrom = None
        self.cameFromHome = False
        self.cameFromHousehold = False
        self.cameFromHouseholds = False
        self.request = request
        
    def getActivityID(self):
        return self.activityID

    def setActivityID(self, activityID):
        self.activityID = activityID

    def getReportID(self):
        return self.reportID

    def getCameFrom(self):
        return self.cameFrom

    def setCameFrom(self, cameFrom):
        self.cameFrom = cameFrom

    def setReportID(self, reportID):
        self.reportID = reportID

    def getScheduleID(self):
        return self.scheduleID

    def setScheduleID(self, scheduleID):
        self.scheduleID = scheduleID

    def getSecurityGroupID(self):
        return self.securityGroupID

    def setSecurityGroupID(self, securityGroupID):
        self.securityGroupID = securityGroupID

    def getJobID(self):
        return self.jobID

    def setJobID(self, jobID):
        self.jobID = jobID

    def getRelationshipID(self):
        return self.relationshipID

    def setRelationshipID(self, relationshipID):
        self.relationshipID = relationshipID

    def getTeamID(self):
        return self.teamID

    def setTeamID(self, teamID):
        self.teamID = teamID

    def getAvailabilityID(self):
        return self.availabilityID

    def setAvailabilityID(self, availabilityID):
        self.availabilityID = availabilityID

    def getRequest(self):
        return self.request

    def setRequest(self, request):
        self.request = request

    def getEventID(self):
        return self.eventID


    def setEventID(self, eventID):
        self.eventID = eventID

    def cameFromHouseholds(self):
        return self.cameFromHouseholds

    def setCameFromHouseholds(self, cameFromHouseholds):
        self.cameFromHouseholds = cameFromHouseholds
    
    def cameFromHome(self):
        return self.cameFromHome

    def setCameFromHome(self, cameFromHome):
        self.cameFromHome = cameFromHome

    def cameFromHousehold(self):
        return self.cameFromHousehold

    def setCameFromHousehold(self, cameFromHousehold):
        self.cameFromHousehold = cameFromHousehold

    def getProjectResourceID(self):
        return self.projectResourceID

    def setProjectResourceID(self, projectResourceID):
        self.projectResourceID = projectResourceID

    def getHouseholdID(self):
        return self.householdID

    def setHouseholdID(self, householdID):
        self.householdID = householdID

    def getVolunteerID(self):
        return self.volunteerID

    def getVolunteerSkillID(self):
        return self.volunteerSkillID

    def setVolunteerSkillID(self, volunteerSkillID):
        self.volunteerSkillID = volunteerSkillID

    def setVolunteerID(self, volunteerID):
        self.volunteerID = volunteerID

    def getTaskID(self):
        return self.taskID

    def setTaskID(self, taskID):
        self.taskID = taskID

    def getParentTaskID(self):
        return self.parentTaskID

    def setParentTaskID(self, parentTaskID):
        self.parentTaskID = parentTaskID

    def getProjectID(self):
        return self.projectID

    def setProjectID(self, projectID):
        self.projectID = projectID

    def getParentProjectID(self):
        return self.parentProjectID

    def setParentProjectID(self, parentProjectID):
        self.parentProjectID = parentProjectID


    def toString(self):
        result = "?dummy=x"
        if (Utils.isNumeric(self.householdID)):
            result += ("&householdID=" + self.householdID)
    
        if (Utils.isNumeric(self.parentTaskID)):
            result += ("&parentTaskID=" + self.parentTaskID)
    
        if (Utils.isNumeric(self.projectID)):
            result += ("&projectID=" + self.projectID)
    
        if (Utils.isNumeric(self.projectResourceID)):
            result += ("&projectResourceID=" + self.projectResourceID)
    
        if (Utils.isNumeric(self.parentProjectID)):
            result += ("&parentProjectID=" + self.parentProjectID)
    
        if (Utils.isNumeric(self.taskID)):
            result += ("&taskID=" + self.taskID)
    
        if (Utils.isNumeric(self.volunteerID)):
            result += ("&volunteerID=" + self.volunteerID)
    
        if (Utils.isNumeric(self.volunteerSkillID)):
            result += ("&volunteerSkillID=" + self.volunteerSkillID)
    
        if (Utils.isNumeric(self.eventID)):
            result += ("&eventID=" + self.eventID)
    
        result += ("&cameFromHome=" + str(self.cameFromHome))
        result += ("&cameFromHousehold=" + str(self.cameFromHousehold))
        result += ("&cameFromHouseholds=" + str(self.cameFromHouseholds))
        return result


class Menu():
    ASSIGNMENTS = "vs/assignments.html"
    EVENTS = "vs/events.html"
    HOME = "vs/home.html"
    HOUSEHOLDS = "vs/households.html"
    LOCATIONS = "vs/locations.html"
    PASSWORD_CHANGE = "/passwordChange.html"
    ORGANIZATIONS = "vs/organizations.html"
    RESOURCES = "vs/resources.html"
    REPORTS = "vs/reports.html"
    SELECT_ORG = "vs/selectOrg.html"
    SCHEDULES = "vs/schedules.html"
    SKILLS = "vs/skills.html"
    UTILITIES = "vs/utilities.html"
    VOLUNTEER_HOME = "vs/volunteerHome.html"
    VOLUNTEER_AVAILABILITY = "vs/volunteerAvailability.html"
    VOLUNTEER_EVENT_PREFERENCE = "vs/volunteerEventPreferences.html"
    VOLUNTEER_JOB_ASSIGNMENTS = "vs/volunteerJobAssignments.html"
    VOLUNTEER_RELATIONSHIPS = "vs/volunteerRelationships.html"
    VOLUNTEERS = "vs/volunteers.html"

    
class SessionData(VSBaseBean):

    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            # Create the instance only if it does not exist yet
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self._initialProjectStatus = None
        self.orgs = []
        self.securityGroupIDs = []
        self.securityGroups = []
        self.eventNavigator = []
        self.projectNavigator = []
        self.taskNavigator = []
        self.volunteerNavigator = []
        self.currentLogin = None
        self.organization = None
        self.organizationID = None
        self.householdID = None
        self.locationID = None
        self.loginID = None
        self.organizationForDetailsID = None
        self.activityID = None
        self.availabilityID = None
        self.eventID = None
        self.householdID = None
        self.ID = None
        self.jobID = None
        self.loginID = None
        self.parentTaskID = None
        self.parentProjectID = None
        self.projectID = None
        self.projectResourceID = None
        self.relationshipID = None
        self.reportID = None
        self.resourceID = None
        self.securityGroupID = None
        self.scheduleID = None
        self.skillID = None
        self.skillRelationshipID = None
        self.taskID = None
        self.teamID = None
        self.volunteerID = None
        self.volunteerSkillID = None
        self.cameFrom = None
        self.cameFromSchedule = False
        self.cameFromVolunteer = False
        self.cameFromHome = False
        self.cameFromHousehold = False
        self.cameFromHouseholds = False
        self.currentLogin = None
        self.currentLoginPrivileges = []
        self.loginLevel = 10000
        self.initialized = False
        self.skillCounts = []
        self.privileges = []
        self.loginStatuses = []
        self.skillRelationshipTypes = []
        self.volunteerRelationshipTypes = []
        self.recurrenceTypes = []
        self.projectStatuses = []
        self.taskStatuses = []
        self.defaultTaskStatus = None
        self.initialProjectStatus = None
        self.resetStatus = None
        self.readyStatus = None
        self.userSecurityGroup = None
        self.autoclicked = None
        self.projectError = False
        self.activityError = False
        self.emailError = False
        self.resourceError = False
        self.skillError = False
        self.subTaskError = False
        self.taskError = False
        self.teamError = False
        self.volunteerError = False
        self.error = None
        self.errorMessage = None
        self.households = []
        self.volunteers = []
        try:
            self.resetStatus = ValueTableManager().getValue(table='LoginStatus', key=LoginStatus.STATUS_RESET)
        except Exception as e:
            super().handleException(e)
        try:
            self.readyStatus = ValueTableManager().getValue(table='LoginStatus', key=LoginStatus.STATUS_READY)
        except Exception as e:
            super().handleException(e)

        self._loadPrivileges()

    def _loadPrivileges(self):
        try:
            self.volunteerRelationshipTypes.extend(ObjectFactory().getRelationshipTypes())
            Collections.sort(self.volunteerRelationshipTypes, RelationshipTypeComparator())
        except PersistenceException as pe:
            self.handleException(pe)
        try:
            self.skillRelationshipTypes.extend(ObjectFactory().getSkillRelationshipTypes())
        except PersistenceException as pe:
            self.handleException(pe)
        try:
            self.recurrenceTypes.extend(ObjectFactory().getRecurrenceTypes())
            Collections.sort(self.recurrenceTypes, RecurrenceTypeComparator())
        except PersistenceException as pe:
            self.handleException(pe)
        try:
            self.loginStatuses.extend(ObjectFactory().getLoginStatuses())
            Collections.sort(self.loginStatuses, LoginStatusComparator())
        except Exception as e:
            self.handleException(e)
        try:
            needDefaultStatus = True
            for obj in ObjectFactory().getObjects(ProjectStatus):
                if needDefaultStatus:
                    self.initialProjectStatus = obj
                    needDefaultStatus = False
                self.projectStatuses.append(obj)
            needDefaultStatus = True
            for stat in ObjectFactory().getObjects(TaskStatus):
                if needDefaultStatus:
                    self.defaultTaskStatus = stat
                    needDefaultStatus = False
                self.taskStatuses.append(stat)            
        except Exception as e:
            self.handleException(e)
        loop = 1
        for loop in range(15):
            self.skillCounts.append(SkillCount(loop))
        self.init()

    def getLoginLevel(self):
        return self.loginLevel
    
    def setLoginLevel(self, loginLevel):
        self.loginLevel = loginLevel
    
    def getSecurityGroups(self):
        return self.securityGroups
    
    def setSecurityGroups(self, securityGroups):
        self.securityGroups = securityGroups
    
    def getInitialProjectStatus(self):
        return self.initialProjectStatus
    
    def setInitialProjectStatus(self, initialProjectStatus):
        self.initialProjectStatus = initialProjectStatus
    
    def init(self):
        try:
            for org in ObjectFactory().getOrganizations(dbo=True):
                #print(org)
                if org.organizationName.lower() == "system":
                    continue
                #print('got an org')
                self.orgs.append(Organization(org))            
            if len(self.orgs) == 1:
                self.organization = self.orgs[0]
        except Exception as e:
            self.handleException(e)
        if self.organization:
            self.init2()
        
    def init2(self):
        try:
            for sg in ObjectFactory().getSecurityGroups(self.getOrganization()):
                self.securityGroups.append(sg)
            if len(self.securityGroups) > 1:
                Collections.sort(self.securityGroups, SecurityGroupComparator())
        except Exception as e:
            self.handleException(e)

    def clearCache(self):
        self.eventNavigator.clear()
        self.projectNavigator.clear()
        self.taskNavigator.clear()
        self.volunteerNavigator.clear()
    
    def getEventNavigator(self):
        return self.eventNavigator
    
    def getVolunteerNavigator(self):
        return self.volunteerNavigator
    
    def cameFromSchedule(self):
        return self.cameFromSchedule
    
    def setCameFromSchedule(self, cameFromSchedule):
        self.cameFromSchedule = cameFromSchedule
    
    def cameFromVolunteer(self):
        return self.cameFromVolunteer
    
    def setCameFromVolunteer(self, cameFromVolunteer):
        self.cameFromVolunteer = cameFromVolunteer
    
    def pull(self, typ, remove=False):
        result = None
        stack = None
        match typ:
            case RequestType.event:
                stack = self.eventNavigator
            case RequestType.job:
                stack = self.eventNavigator
            case RequestType.report:
                stack = self.eventNavigator
            case RequestType.schedule:
                stack = self.eventNavigator
            case RequestType.resource:
                stack = self.eventNavigator
            case RequestType.project:
                stack = self.projectNavigator
            case RequestType.activity:
                stack = self.projectNavigator
            case RequestType.projectResource:
                stack = self.projectNavigator
            case RequestType.subproject:
                stack = self.projectNavigator
            case RequestType.task:
                stack = self.taskNavigator
            case RequestType.team:
                stack = self.taskNavigator
            case RequestType.subtask:
                stack = self.taskNavigator
            case RequestType.availability:
                stack = self.volunteerNavigator
            case RequestType.household:
                stack = self.volunteerNavigator
            case RequestType.relationship:
                stack = self.volunteerNavigator
            case RequestType.securityGroup:
                stack = self.volunteerNavigator
            case RequestType.volunteer:
                stack = self.volunteerNavigator
            case RequestType.volunteerSkill:
                stack = self.volunteerNavigator
            case _:
                try:
                    raise Exception("type \"" + typ + "\" is not valid")
                except Exception as e:
                    self.handleException(e)
        if stack  and len(stack) > 0:
            result = stack[len(stack) - 1]
            if remove:
                stack.pop()
        return result
    
    def getProjectId(self):
        return self.projectId
    
    def setProjectId(self, projectId):
        self.projectID = projectId
    
    def getSecurityGroupIDs(self):
        return self.securityGroupIDs
    
    def setSecurityGroupIDs(self, securityGroupIDs):
        self.securityGroupIDs = securityGroupIDs    

    def getLoginId(self):
        return self.loginId
    
    def setLoginId(self, loginId):
        self.loginID = loginId
    
    def getResourceId(self):
        return self.resourceId
    
    def setResourceId(self, resourceId):
        self.resourceID = resourceId
    
    def getLocationId(self):
        return self.locationId
    
    def setLocationId(self, locationId):
        self.locationID = locationId
    
    def getSecurityGroupId(self):
        return self.securityGroupId
    
    def getOrganizationForDetailsId(self):
        return self.organizationForDetailsId
    
    def setOrganizationForDetailsId(self, organizationForDetailsId):
        self.organizationForDetailsID = organizationForDetailsId
    
    def getHouseholdId(self):
        return self.householdId
    
    def setHouseholdId(self, householdId):
        self.householdID = householdId
    
    def getSkillRelationshipId(self):
        return self.skillRelationshipId
    
    def setSkillRelationshipId(self, skillRelationshipId):
        self.skillRelationshipID = skillRelationshipId
    
    def setSecurityGroupId(self, securityGroupId):
        self.securityGroupID = securityGroupId
    
    def getSkillId(self):
        return self.skillId
    
    def setSkillId(self, skillId):
        self.skillID = skillId
    
    def getSkillRelationshipTypes(self):
        return self.skillRelationshipTypes
    
    def addSecurityGroup(self, sg):
        if sg and not self.securityGroups.contains(sg):
            self.securityGroups.append(sg)
            if len(self.securityGroups) > 0:
                Collections.sort(self.securityGroups, SecurityGroupComparator())
      
    def getLoginPrivileges(self, li):
        result = []
        if li and isinstance(li, Login):
            if li.isAdmin():
                result = self.privileges
            else:
                for sg in li.getSecurityGroups():
                    for priv in sg.getPrivileges():
                        if result.contains(priv):
                            continue
                        result.append(priv)
            if len(result) > 1:
                Collections.sort(result, PrivilegeComparator())
        return result
    
    def loadPrivileges(self):
        try:
            self.privileges.extend(ObjectFactory().getPrivileges())      
        except Exception as pe:
            self.handleException(pe)
        
    def getVolunteerRelationshipTypes(self):
        return self.volunteerRelationshipTypes
    
    def getLoginStatuses(self):
        return self.loginStatuses
    
    def getOrganization(self):
        return self.organization
    
    def setOrganization(self, organization):
        self.organization = organization
    
    def getOrganizationId(self):
        return self.organization.getOrganizationID()
    
    def getOrgs(self):
        return self.orgs
    
    def getRecurrenceTypes(self):
        return self.recurrenceTypes
    
    def getSkillCounts(self):
        return self.skillCounts

    def setSkillCounts(self, skillCounts):
        self.skillCounts = skillCounts
    
    def getCurrentLogin(self):
        return self.currentLogin
    
    def setCurrentLogin(self, li):
        self.currentLogin = li
        mn = 10000
        for sg in li.getSecurityGroups():
            level = sg.getLevel()
            if level < mn:
                mn = level
        self.loginLevel = mn
    
    def setProjectStatuses(self, projectStatuses):
        self.projectStatuses = projectStatuses
    
    def setTaskStatuses(self, taskStatuses):
        self.taskStatuses = taskStatuses
    
    def getDefaultTaskStatus(self):
        return self.defaultTaskStatus
    
    def getProjectStatuses(self):
        return self.projectStatuses
    
    def getTaskStatuses(self):
        return self.taskStatuses
    
    def addEventParam(self, rph):
        if rph:
            self.eventNavigator.append(rph)
        
    def addProjectParam(self, rph):
        if rph:
            self.projectNavigator.append(rph)
        
    def addTaskParam(self, rph):
        if rph:
            self.taskNavigator.append(rph)
        
    def getEventParam(self):
        return self.eventNavigator.pop()
    
    def getTaskParam(self):
        return self.taskNavigator.pop()
    
    def addVolunteerParam(self, rph):
        if rph:
            self.volunteerNavigator.append(rph)
        
    def getVolunteerParam(self):
        return self.volunteerNavigator.pop()
    
    def getPreviousProjectID(self, currentId):
        result = None
        while True:
            rph = self.projectNavigator[-1] if self.projectNavigator else None
            if not rph:
                break 
            if not rph.getProjectID()\
                    or self.projectID == rph.getProjectID():
                self.projectNavigator.pop()
            else:
                break            
            if (self.projectNavigator.empty()):
                break
        if self.projectNavigator:
            rph = self.projectNavigator.pop()
            result = str(rph.getProjectID())        
        return result
    
    def getPreviousTaskID(self):
        result = None
        if self.taskNavigator:
            rph = self.taskNavigator.pop()
            result = str(rph.getTaskID())        
        return result

        
class  SessionDataBean(VSBaseBean):
    
    def __init__(self, request):
        super().__init__()
        self.sessionData = SessionData()
        self.sessionData.request = request
        self.sessionData.session = request.session
        self.sessionData.valID = True
                
    def validateDateField(self, value, field):
        self.sessionData.valID = True
        err = False
        if value and isinstance(value, str): 
            s = str(value)
            if len(s) != 10:
                err = True
            else:
                try:
                    DT.strptime(s)
                except:
                    err = True
                    result = False
        else:
            err = True
        if err:
            messages.error(self.sessionData.request, field + " must be formatted mm/dd/yyyy")
        return result

    def setValidarg(self, arg):
        if isinstance(arg, bool):
            self.sessionData.valID = arg
        else:
            self.sessionData.valID = False 
            
    def getandClearMessages(self, request):
        result = messages.get_messages(request)
        for _ in messages.get_messages(request):
            pass
        return result
        
    def getInitialProjectStatus(self):
        if not self.sessionData._initialProjectStatus:
            try:
                objs = ObjectFactory().getObjects(ProjectStatus)
                for ps in objs:
                    if ps.getProjectStatusType() == ProjectStatus.DEFINED:
                        self.sessionData._initialProjectStatus = ps
                        break
            except Exception as e:
                super().handleException(e)
        return self.sessionData._initialProjectStatus

    def isValidTimetimeString(self, timeString):
        result = True
        try:
            DT.strptime(timeString, "%H:%M:%S")
        except:
            try:
                DT.strptime(timeString, "%H:%M") 
            except:
                result = False
        return result
   
    def isValidDatedateStr(self, dateStr, fmt='%/-%d/%Y'):
        result = True
        try:
            DT.strptime(dateStr, fmt)
        except:
            result = False    
        return result
    
    def isValidEmailAddress(self, email):
        result = True
        try:
            validate_email(email, check_deliverability=False)
        except EmailNotValidError:
            #logger.opt(exception=True).debug(e)
            result = False
        return result

    def getTeamID(self):
        return self.sessionData.teamID
    
    def setTeamID(self, teamID): 
        self.sessionData.teamID = teamID
    
    def getJobID(self): 
        return self.sessionData.jobID
    
    def setJobID(self, jobID): 
        self.sessionData.jobID = jobID
    
    def getHouseholds(self): 
        return self.sessionData.households
    
    def setHouseholds(self, households): 
        self.sessionData.households = households
    
    def getVolunteers(self): 
        return self.sessionData.volunteers
    
    def setVolunteers(self, volunteers): 
        self.sessionData.volunteers = volunteers
    
    def isActivityError(self): 
        return self.sessionData.activityError

    def setActivityErrora(self, activityError): 
        self.sessionData.activityError = activityError
    
    def isResourceError(self): 
        return self.sessionData.resourceError
    
    def getRelationshipID(self): 
        return self.sessionData.relationshipID
    
    def setRelationshipID(self, relationshipID): 
        self.sessionData.relationshipID = relationshipID
    
    def getReportID(self): 
        return self.sessionData.reportID
    
    def setReportID(self, reportID): 
        self.sessionData.reportID = reportID
    
    def setResourceError(self, resourceError): 
        self.sessionData.resourceError = resourceError
    
    def isSkillError(self): 
        return self.sessionData.skillError
    
    def setSkillError(self, skillError): 
        self.sessionData.skillError = skillError

    def isSubTaskError(self): 
        return self.sessionData.subTaskError

    def setSubTaskError(self, subTaskError): 
        self.sessionData.subTaskError = subTaskError
    
    def isTaskError(self): 
        return self.sessionData.taskError
    
    def setTaskError(self, taskError): 
        self.sessionData.taskError = taskError
    
    def isTeamError(self): 
        return self.sessionData.teamError

    def setTeamError(self, teamError): 
        self.sessionData.teamError = teamError

    def isVolunteerError(self): 
        return self.sessionData.volunteerError
    
    def setVolunteerError(self, volunteerError): 
        self.sessionData.volunteerError = volunteerError

    def isError(self): 
        return self.sessionData.error

    def setError(self, error): 
        self.sessionData.error = error
    
    def getErrorMessage(self): 
        return self.sessionData.errorMessage
    
    def setErrorMessage(self, errorMessage): 
        self.sessionData.errorMessage = errorMessage

    def saveRequestParameters(self, request, requestType=None): 
        self.sessionData.householdID = request.POST.get("householdID")
        self.sessionData.ID = request.POST.get("id")
        self.sessionData.activityID = request.POST.get("activityID")
        self.sessionData.availabilityID = request.POST.get("availabilityID")
        self.sessionData.eventID = request.POST.get("eventID")
        self.sessionData.jobID = request.POST.get("jobID")
        self.sessionData.parentTaskID = request.POST.get("parentTaskID")
        self.sessionData.parentProjectID = request.POST.get("parentProjectID")
        self.sessionData.projectID = request.POST.get("projectID")
        self.sessionData.projectResourceID = request.POST.get("projectResourceID")
        self.sessionData.relationshipID = request.POST.get("relationshipID")
        self.sessionData.reportID = request.POST.get("reportID")
        self.sessionData.securityGroupID = request.POST.get("securityGroupID")
        self.sessionData.scheduleID = request.POST.get("scheduleID")
        self.sessionData.taskID = request.POST.get("taskID")
        self.sessionData.teamID = request.POST.get("teamID")
        self.sessionData.volunteerID = request.POST.get("volunteerID")
        self.sessionData.volunteerSkillID = request.POST.get("volunteerSkillID")
        self.sessionData.cameFromHome = request.POST.get("cameFromHome")
        self.sessionData.cameFromHousehold = request.POST.get("cameFromHousehold")
        self.sessionData.cameFromHouseholds = request.POST.get("cameFromHouseholds")
        s2 = request.POST.get("cameFrom")
        rph = RequestParametersHolder(self.sessionData.getRequestURL(request))
        if Utils.isNotBlank(s2): 
            rph.setCameFrom(s2)
        if self.sessionData.ID or self.sessionData.activityID or self.sessionData.availabilityID or self.sessionData.householdID\
         or self.sessionData.jobID or self.sessionData.parentProjectID\
            or self.sessionData.parentTaskID or self.sessionData.projectID or self.sessionData.projectResourceID or self.sessionData.relationshipID\
            or self.sessionData.reportID or self.sessionData.securityGroupID\
            or self.sessionData.scheduleID or self.sessionData.taskID or self.sessionData.teamID or self.sessionData.volunteerID or self.sessionData.volunteerSkillID\
            or self.sessionData.cameFromHome or self.sessionData.cameFromHousehold or self.sessionData.cameFromHouseholds\
            or Utils.notBlank(s2):
                match requestType:
                    case RequestType.availability:
                        if Utils.isBlank(self.sessionData.availabilityID): 
                            self.sessionData.availabilityID = id
                        self._populateRPH(rph)
                        self.sessionData.addVolunteerParam(rph)
                    case RequestType.event:
                        if Utils.isBlank(self.sessionData.eventID):
                            self.sessionData.eventID = id
                        self._populateRPH(rph)
                        self.sessionData.addEventParam(rph)
                    case RequestType.household:
                        if Utils.isBlank(self.sessionData.householdID): 
                            self.sessionData.householdID = id
                        self._populateRPH(rph)
                        self.sessionData.addVolunteerParam(rph)
                    case RequestType.job:
                        if Utils.isBlank(self.sessionData.jobID): 
                            self.sessionData.jobID = id
                        self._populateRPH(rph)
                        self.sessionData.addEventParam(rph)
                    case RequestType.relationship:
                        if Utils.isBlank(self.sessionData.relationshipID): 
                            self.sessionData.relationshipID = id
                        self._populateRPH(rph)
                        self.sessionData.addVolunteerParam(rph)
                    case RequestType.report:
                        if Utils.isBlank(self.sessionData.reportID):
                            self.sessionData.reportID = id
                        self._populateRPH(rph)
                        self.sessionData.addEventParam(rph)
                    case RequestType.securityGroup:
                        if Utils.isBlank(self.sessionData.securityGroupID): 
                            self.sessionData.securityGroupID = id
                        self._populateRPH(rph)
                        self.sessionData.addVolunteerParam(rph)
                    case RequestType.schedule:
                        if Utils.isBlank(self.sessionData.scheduleID): 
                            self.sessionData.scheduleID = id
                        self._populateRPH(rph)
                        self.sessionData.addEventParam(rph)
                    case RequestType.volunteerSkill:
                        if Utils.isBlank(self.sessionData.volunteerSkillID): 
                            self.sessionData.volunteerSkillID = id
                        self._populateRPH(rph)
                        self.sessionData.addVolunteerParam(rph)
                    case RequestType.project:
                        if Utils.isBlank(self.sessionData.projectID):
                            self.sessionData.projectID = id
                        self._populateRPH(rph)
                        self.sessionData.addProjectParam(rph)
                    case RequestType.activity:
                        if Utils.isBlank(self.sessionData.activityID): 
                            self.sessionData.activityID = id
                        self._populateRPH(rph)
                        self.sessionData.addProjectParam(rph)
                    case RequestType.projectResource:
                        if Utils.isBlank(self.sessionData.projectResourceID): 
                            self.sessionData.projectResourceID = id
                        self._populateRPH(rph)
                        self.sessionData.addProjectParam(rph)
                    case RequestType.task:
                        if Utils.isBlank(self.sessionData.taskID): 
                            self.sessionData.taskID = id
                        self._populateRPH(rph)
                        self.sessionData.addTaskParam(rph)
                    case RequestType.team:
                        if Utils.isBlank(self.sessionData.teamID): 
                            self.sessionData.teamID = id
                        self._populateRPH(rph)
                        self.sessionData.addTaskParam(rph)
                    case RequestType.volunteer:
                        if Utils.isBlank(self.sessionData.volunteerID): 
                            self.sessionData.volunteerID = id
                        self._populateRPH(rph)
                        self.sessionData.addVolunteerParam(rph)
                    case _:
                        self.sessionData.projectID = id
                        self._populateRPH(rph)
                        self.sessionData.addProjectParam(rph)

    def _populateRPH(self, rph): 
        rph.setActivityID(self.sessionData.activityID)
        rph.setAvailabilityID(self.sessionData.availabilityID)
        rph.setEventID(self.sessionData.eventID)
        rph.setHouseholdID(self.sessionData.householdID)
        rph.setJobID(self.sessionData.jobID)
        rph.setParentProjectID(self.sessionData.parentProjectID)
        rph.setParentTaskID(self.sessionData.parentTaskID)
        rph.setProjectID(self.sessionData.projectID)
        rph.setProjectResourceID(self.sessionData.projectResourceID)
        rph.setRelationshipID(self.sessionData.relationshipID)
        rph.setReportID(self.sessionData.reportID)
        rph.setSecurityGroupID(self.sessionData.securityGroupID)
        rph.setScheduleID(self.sessionData.scheduleID)
        rph.setTaskID(self.sessionData.taskID)
        rph.setTeamID(self.sessionData.teamID)
        rph.setVolunteerID(self.sessionData.volunteerID)
        rph.setVolunteerSkillID(self.sessionData.volunteerSkillID)
        rph.setCameFromHome(self.sessionData.cameFromHome)
        rph.setCameFromHousehold(self.sessionData.cameFromHousehold)
        rph.setCameFromHouseholds(self.sessionData.cameFromHouseholds)
    
    def peek(self, requestType): 
        result = None
        match requestType: 
            case RequestType.project:
                result = self.sessionData.pull(RequestType.project, False)
            case RequestType.task:
                result = self.sessionData.pull(RequestType.task, False)
            case _:
                pass        
        return result
    

    def pop(self, typ): 
        result = None
        match typ:
            case RequestType.project:
                result = self.sessionData.pull(RequestType.project, True)
            case RequestType.task:
                result = self.sessionData.pull(RequestType.task, True)
            case _:
                pass        
        return result
    

    def clearErrors(self): 
        self.sessionData.projectError = False
        self.sessionData.activityError = False
        self.sessionData.resourceError = False
        self.sessionData.skillError = False
        self.sessionData.subTaskError = False
        self.sessionData.taskError = False
        self.sessionData.teamError = False
        self.sessionData.volunteerError = False
        self.sessionData.error = False
        self.sessionData.errorMessage = ""
    

    def getRequestProjectID(self, request): 
        result = request.POST.get("projectId")
        if Utils.isBlank(result):
            result = request.POST.get("id")        
        return result

    def isProjectError(self):
        return self.sessionData.projectError

    def setProjectError(self, projectError): 
        self.sessionData.projectError = projectError
    
    @abstractmethod
    def setup(self):
        pass 

    def getCurrentLoginId(self):
        result = None
        li = self.sessionData.getCurrentLogin()
        if li:
            result = li.getLoginID()
        return result
    
    def getNewTeam(self):
        org = self.sessionData.getOrganization 
        dbt = DbTeam()
        dbt.organization = org.myDb
        result = Team(dbt)
        li = self.sessionData.getCurrentLogin()
        lID = li.getLoginID()
        try:
            result.setObjectID("x" + str(DT.now()))
            result.setTeamCreateDate(DT.now())
            result.setTeamUpdateDate(DT.now())
            result.setTeamCreateUser(lID)
            result.setTeamUpdateUser(lID)
        except InvalidAttributeValueException as unlikely: 
            super().handleException(unlikely)        
        return result    

    def getTaskWithNameInProject(self, name, project): 
        result = None
        if name and project and project.getProjectID(): 
            result = ObjectFactory().getTaskWithNameInProject(name, project)
        return result
    
    def getCameFrom(self):
        if not self.sessionData.cameFrom:
            self.sessionData.cameFrom = self.getRequest().POST.get("cameFrom")
        return self.sessionData.cameFrom
    
    def setCameFrom(self, cameFrm): 
        self.sessionData.cameFrom = cameFrm
    
    def isAutoclicked(self): 
        return self.sessionData.autoclicked
    
    def autoClick(self): 
        self.sessionData.autoclicked = not self.sessionData.autoclicked
        return str(self.sessionData.autoclicked)
    
    def setAutoclicked(self, autoclicked):
        self.sessionData.autoclicked = autoclicked

    def handleException(self, e):
        self.clearErrors()
        self.sessionData.error = True
        self.sessionData.cameFrom = ""
        self.handleException(e)
        self._sendErrorMail(e)
        
    def now(self): 
        return DT.now()
    
    def _sendErrorMail(self, e): 
        pass
    
    def getDeletedOrganizationProjects(self, org): 
        return ObjectFactory().getDeletedOrganizationProjects()

    def getDeletedTasks(self):
        return ObjectFactory().getDeletedTasks() 
        
    def getDeletedTeams(self, org): 
        return ObjectFactory().getDeletedTeams(org)
    

    def getProjectsInOrganization(self, org):
        return ObjectFactory().getProjectsInOrganization(org)

    def isVolunteer(self): 
        li = self.sessionData.getCurrentLogin()
        return AuthorizationManager.isVolunteerUser(li)

    def encrypt(self, s):
        return Encrypter().encrypt(s)
    
    def decrypt(self, s):
        return Encrypter().decrypt(s)
    
    def getSession(self): 
        return self.request.getSession()
    
    def getRequest(self):
        return self.request

    def getRequestURL(self, request): 
        return request.build_absolute_uri()

    def validateErr(self, errs): 
        result = "<table align='center'>"
        for s in errs:
            result += "<tr><td>"
            result += str(s)
            result += "</td></tr>"        
        result += "</table>"
        return result    

    def getSelecterPair(self, 
        leftTitle,
        rightTitle,
        buttonLabel,
        items,
        target): 
        now = DT.now().strftime("%m/%d/%Y")
        result = "<form action='"\
                + str(target)\
                + "'>\n"\
                + "<table align='center'><table align='center'><th>"\
                + str(leftTitle)\
                + "</th>"\
                + "<tr><td><select name='>"\
                + str(leftTitle)\
                + "' id='"\
                + str(leftTitle)\
                + now\
                + "' onchange='moveRight()' "\
                + "onfocus='self.sessionData.selectedIndex = -1'>"
        for vsp in items: 
            result += ("\n<option value='>"\
                    + str(vsp.getID())\
                    + "'>"\
                    + str(vsp)\
                    + "</option>"\
                    + "\n</select>")
        result += ("</td><td>"
                + "</tr>"\
                + "<tr><td>"\
                + "<input type='button' value='"\
                + str(buttonLabel)\
                + "'>"\
                + "</td></tr>"\
                + "</table></form>")
        return result

    def multiColumnTableRows (self,
                                title=None,
                                size=1,
                                height=400,
                                items=[],
                                dest=None,
                                color=False,
                                extra=None): 
        result = ""
        if len(items) > 0: 
            index = 0
            sb =  "<table align='center'><th"
            if color:
                sb += " class=''>"
            else: 
                sb += "><h3>"            
            sb += str(title)
            if not color: 
                sb += "</h3>"            
            sb += "</th>\n</table>\n"
            sb += "<div style='overflow-y: auto"
            sb += "height: "
            sb += str(height)
            sb += "px'>\n<table class='listTable' border=1>\n<tr>"
            for vsp in items: 
                if index % size == 0 and index > 0: 
                    sb += "</tr><tr>\n"
                index += 1
                try:
                    style = vsp.getStyle()
                    sb += "<td "
                    sb += str(style)
                    sb += ">//"
                except: 
                    sb += "<td class='listTable'>"                
                if Utils.isNotBlank(dest):
                    sb += "<a "
                    try: 
                        style = vsp.getStyle()
                        sb += str(style)
                    except: 
                        pass
                    if extra: 
                        sb += str(extra)
                    sb += " href='"
                    sb += dest
                    if Utils.contains(dest, "?"): 
                        sb += "&id="
                    else: 
                        sb += "?id="                    
                    sb += str(vsp.getID())
                    if vsp.hasQuantity(): 
                        sb += "&qty="
                        sb += str(vsp.getQuantity())
                        sb += "'>"
                sb += vsp.getDisplayString()
                if Utils.isNotBlank(dest): 
                    sb += "</a>"
                sb += "</td>\n"
            sb += "</tr>\n</table>"
            sb += "</div>"
            result = sb        
        return result
    
    def createNewLogin(self, vol, admLoginId): 
        name = vol.getVolunteerName()
        strippedName = name.strip().replace(" ", '')
        li = ObjectFactory().getLogin(
            vol.getVolunteerFirstName(), 
            vol.getVolunteerLastName(), 
            self.sessionData.getOrganization())
        if not li: 
            org = self.sessionData.getOrganization()
            li = ObjectFactory().createLogin(strippedName, name, org,admLoginId)
            li.setLoginStatus(self.sessionData.resetStatus)
            li.save()
        vol.setLogin(li)
        vol.save()
        return vol    

    def validateDates(self, start=None, end=None, requireBoth=False): 
        msg = ""
        ok = True
        fmt = "%m/%d/%Y"
        if requireBoth: 
            if Utils.isBlank(start) or Utils.isBlank(end): 
                msg += "You must specify both start date and end date"
                ok = False            
        else: 
            if Utils.isNotBlank(start): 
                try:
                    DT.strptime(start, fmt).date()
                except: 
                    ok = False
                    msg += "Start Date is invalid<br/>"
            else:
                msg = 'Start Date was missing'
                ok = False
            if Utils.isNotBlank(end): 
                try:
                    DT.strptime(start, format).date()
                except: 
                    ok = False
                    msg += "End Date is invalid<br/>"            
            if Utils.isBlank(start) and Utils.isBlank(end): 
                ok = False
                msg += "Neither Start Date nor End Date is specified<br/>"
            if start and end:
                if start > end: 
                    ok = False
                    msg += "Start Date not before End Date<br/>"
        if not ok: 
            raise InvalidDateException(msg)
        return True

    def loadHouseholds(self): 
        try: 
            for obj in ObjectFactory().getHouseholds(self.sessionData.getOrganization()):
                self.sessionData.households.append(obj)
            
            if len(self.sessionData.households) > 1: 
                Collections.sort(self.sessionData.households, HouseholdComparator())
        except Exception as e:
            self.handleException(e)
        
    def loadVolunteers(self): 
        try: 
            for obj in ObjectFactory().getVolunteers(self.sessionData.getOrganization()):
                self.sessionData.volunteers.append(obj)
            if len(self.sessionData.volunteers)  > 1:
                Collections.sort(self.sessionData.volunteers, VolunteerComparator())
        except Exception as e: 
            super().handleException(e)


class BreadCrumb(SessionDataBean):
    
    def __init__(self, name, url):
        self.name = name;
        self.url = url
        
    def getName(self):
        return self.name

    def getUrl(self):
        return self.url


class BreadCrumbManager(SessionDataBean):

    breadcrumbs = []

    @staticmethod
    def getBreadcrumbs():
        return BreadCrumbManager.breadcrumbs

    @staticmethod
    def getLastBreadcrumb():
        result = None;
        if BreadCrumbManager.breadcrumbs:
            result = BreadCrumbManager.breadcrumbs[-1]
        return result
    
    @staticmethod
    def removeLastBreadcrumb():
        result = None
        if BreadCrumbManager.breadcrumbs:
            result = BreadCrumbManager.breadcrumbs.pop()
        return result

    @staticmethod
    def add(breadcrumb):
        if ("home" in breadcrumb.getName() and "/help/" not in breadcrumb.getUrl().lower())\
        or (breadcrumb.getName().endswith("login") and "/help/" not in breadcrumb.getUrl().lower()):
            BreadCrumbManager.breadcrumbs = []
        else:
            if "/help/" not in breadcrumb.getUrl().lower() and \
            'passwordchange' not in breadcrumb.getUrl().lower():
                found = False;
                idx = 0
                for b in BreadCrumbManager.breadcrumbs:
                    if breadcrumb.getUrl() == b.getUrl():
                        found = True;
                        break
                    idx += 1
                if found:
                    try:
                        BreadCrumbManager.breadcrumbs.pop(idx)
                    except:
                        pass
                else:
                    BreadCrumbManager.breadcrumbs.append(breadcrumb)


class HelpBean(SessionDataBean):
    HELP_FOOTER_VOLUNTEER_ENTRIES = [
        "<BR/>",
        "<table class=\"helpMenuTable\" width=\"100%\">",
        "    <thead class=\"helpMenuTable\">Click below for help on:</thead>",
        "    <tr>",
        "        <!--td class=\"helpMenuTable\">",
        "            <A class='inText' href=\"$$WEBAPP$$/volsched/help/volunteerOverview.html\" title=\"overview\">",
        "                Volunteer Scheduler overview</A>",
        "        </td-->",
        "        <td class=\"helpMenuTable\">",
        "            <A class='inText' href=\"$$WEBAPP$$/volsched/help/menuVolunteer.html\" title=\"Menu help\">",
        "                Menu</A>",
        "        </td>",
        "        <td class=\"helpMenuTable\">",
        "            <A class='inText' href=\"$$WEBAPP$$/volsched/help/volunteerUpdateLimited.html\" title=\"Home Page help\">",
        "                Home Page</A>",
        "        </td>",
        "    </tr>",
        "</table>"
    ]

    HELP_FOOTER_ENTRIES = [
        "<BR/>",
        "<table class=\"helpMenuTable\" width=\"100%\">",
        "    <thead class=\"helpMenuTable\">Click below for help on:</thead>",
        "    <tr>",
        "        <td class=\"helpMenuTable\">",
        "            <A class='inText' href=\"$$WEBAPP$$/volsched/help/overview.html\" title=\"Overview\">",
        "                Volunteer Scheduler overview</A>",
        "        </td>",
        "        <td class=\"helpMenuTable\">",
        "            <A class='inText' href=\"$$WEBAPP$$/volsched/help/menu.html\" title=\"Menu help\">",
        "                Menu</A>",
        "        </td>",
        "        <td class=\"helpMenuTable\">",
        "            <A class='inText' href=\"$$WEBAPP$$/volsched/help/home.html\" title=\"Home Page help\">",
        "                Home Page</A>",
        "        </td>",
        "        <td class=\"helpMenuTable\">",
        "            <A class='inText' href=\"$$WEBAPP$$/volsched/help/organizations.html\" title=\"Organizationss List Page help\">",
        "               Organizations</A>",
        "        </td>",
        "        <td class=\"helpMenuTable\">",
        "            <A class='inText' href=\"$$WEBAPP$$/volsched/help/projects.html\" title=\"Projects List Page help\">",
        "               Projects</A>",
        "        </td>",
        "        <td class=\"helpMenuTable\">",
        "            <A class='inText' href=\"$$WEBAPP$$/volsched/help/schedules.html\" title=\"Schedules List Page help\">",
        "               Schedules</A>",
        "        </td>",
        "        <td class=\"helpMenuTable\">",
        "            <A class='inText' href=\"$$WEBAPP$$/volsched/help/locations.html\" title=\"Locations List Page help\">",
        "               Locations</A>",
        "        </td>",
        "        <td class=\"helpMenuTable\">",
        "            <A class='inText' href=\"$$WEBAPP$$/volsched/help/resources.html\" title=\"Resources List Page help\">Resources</A>",
        "        </td>",
        "        <td class=\"helpMenuTable\">",
        "            <A class='inText' href=\"$$WEBAPP$$/volsched/help/events.html\" title=\"Events List Page help\">Events</A>",
        "        </td>",
        "        <td class=\"helpMenuTable\">",
        "            <A class='inText' href=\"$$WEBAPP$$/volsched/help/households.html\" title=\"Households List Page help\">",
        "               Households</A>",
        "        </td>",
        "        <td class=\"helpMenuTable\">",
        "            <A class='inText' href=\"$$WEBAPP$$/volsched/help/volunteerDetails.html\" title=\"Volunteer Edit Page help\">",
        "               Volunteers</A>",
        "        </td>",
        "        <td class=\"helpMenuTable\">",
        "            <A class='inText' href=\"$$WEBAPP$$/volsched/help/skills.html\" title=\"Skills List Page help\">Skills</A>",
        "        </td>",
        "        <td class=\"helpMenuTable\">",
        "            <A class='inText' href=\"$$WEBAPP$$/volsched/help/reports.html\" title=\"Reports Page help\">Reports</A>",
        "        </td>",
        "        <td class=\"helpMenuTable\">",
        "            <A class='inText' href=\"$$WEBAPP$$/volsched/help/utilities.html\" title=\"Utilities Page help\">",
        "               Utilities</A>",
        "        </td>",
        "    </tr>",
        "</table>"
    ]

    def __init__(self, arg):
        self.arg = arg
        print(arg)
        self.menuName = 'menu'
        
    def setup(self):
        pass
    
    def getWebapp(self):
        return self.getRequestServletPath()

    def getHelpHeader(self):
        if self.isVolunteer():
            self.menuName = "menuVolunteer"
        result = "\n<script>\n"
        result += "function loaded() {\n"
        result += "setHeader(\"Help\")\n"
        result += "}\n"
        result += "</script>"
        result += "From this page you can:\n"
        result += "<ol>\n"
        result += "<li><div class=\"helpItem\">Logout</div>Click on the hyperlink in the title bar.</li>\n"
        result += "<li><div class=\"helpItem\">Get help</div>Click on the hyperlink in the title bar.</li>\n"
        result += "<li><div class=\"helpItem\">Select one of the options from the <A  href=\""
        result += self.getRequestServletPath()
        result += ("/volsched/help/" + self.menuName + ".html\"")
        result += " title=\"Menu Page help\">Menu</A></div> on the left side of the page.</li>\n"
        result += "<li>If you have visited more than one page, you can return to sny "
        result += "of those pages by clicking on the appropriate hyperlink in the title bar.</li>\n"
        return result

    def getMenuHeader(self):
        if self.isVolunteer():
            self.menuName = "menuVolunteer"
        result = "\n<script>\n"
        result += "function loaded() {\n"
        result += "setHeader(\"Help\")\n"
        result += "}\n"
        result += "</script>"
        result += "From this page you can:\n"
        result += "<ol>\n"
        result += "<li><div class=\"helpItem\">Logout</div>Click on the hyperlink in the title bar.</li>\n"
        result += "<li><div class=\"helpItem\">Get help</div>Click on the hyperlink in the title bar.</li>\n"
        result += "<li>If you have visited more than one page, you can return to sny "
        result += "of those pages by clicking on the appropriate hyperlink in the title bar.</li>\n"
        return result

    def getHelpReturn(self):
        result = ""
        bc = BreadCrumbManager.getLastBreadcrumb()
        result += "Click <a href=\""
        if bc:
            result += bc.getUrl()
        else:
            result += (self.getRequestServletPath() + Menu.HOME)
        result += "\">here</a> to return to the Volunteer Scheduler.<br/>"
        return result

    def getHelpFooter(self):
        replacementString = self.getRequestServletPath()
        result = "</ol>"
        result += self.getHelpReturn()
        text = HelpBean.HELP_FOOTER_ENTRIES
        if self.isVolunteer():
            text = HelpBean.HELP_FOOTER_VOLUNTEER_ENTRIES
        for  s in text:
            s = s.replace('$$WEBAPP$$', replacementString)
            result += s
            result += "\n"
        return result


class HomeBean(SessionDataBean):

    def __init__(self, request):
        super().__init__(request)
        self.volunteer = self.getVolunteer()
        self.loadHouseholds()
        self.loadVolunteers()  

    def getLogin(self):
        return self.sessionData.getCurrentLogin()
    
    def setup(self):
        pass

    def getVolunteer(self):
        if not self.volunteer:
            try:
                self.volunteer = ObjectFactory().getVolunteer(self.getLogin())
            except Exception as e:
                super().handleException(e)         
        return self.volunteer
    

    def getHouseholdsTable(self):
        return super().multiColumnTableRows("Households",
                5,
                125,
                self.getHouseholds(),
                "householdDetails.html" +  "?cameFromHome=true")
    

    def getVolunteersTable(self):
        return super().multiColumnTableRows("Volunteers",
                5,
                125,
                self.getVolunteers(),
                "volunteerDetails.html" + "?cameFromHome=true")
    

    def redirect(self):
        return "volunteerDetails?cameFrom=home&id=" + self.getVolunteer().getID()
   
   
class LoginBean(SessionDataBean):
    LOGIN_CANCEL = ''
    LOGIN_FAILED = 'vs/login.html'
    LOGIN_GET_ORG = "vs/selectOrg,html"
    LOGIN_HELP = "vs/help/login.html"
    LOGIN_MAIN = "vs/login.html"
    LOGIN_RESET_HELP = "vs/help/resetLogin.html"
    LOGIN_PWD_CHANGE_HELP = "/vs/help/passwordChange.html"
    LOGIN_RESET = "vs/resetLogin.html"
    
    def __init__(self, request):
        super().__init__(request)
        self.name = None
        self.password = None
        self.secret = None
        self.error = False
        self.errorMessage = None
        
    def setup(self):
        pass

    def getLoginID(self):
        return self.sessionData.loginID
    
    def setLoginID(self, loginID):
        self.sessionData.loginID = loginID
    
    def getOrganizationId(self):
        return self.sessionData.organizationId

    def getSecret(self):
        return self.secret
    
    def setSecret(self, secret):
        self.secret = secret
    
    def getName(self):
        return self.name
    
    def setName(self, name):
        self.name = name
    
    def getPassword(self):
        return self.password
    
    def getResetLogin(self):
        return LoginBean.LOGIN_RESET
    
    def setPassword(self, password):
        self.password = password
    
    def getMaxNameLength(self):
        return Login.LOGIN_NAME_MAX_SIZE
    
    def getMaxPasswordLength(self):
        return Login.PASSWORD_MAX_ENCRYPTED_SIZE
    
    def getMaxSecretLength(self):
        return Login.SECRET_MAX_ENCRYPTED_SIZE
    
    def getOrgs(self):
        result = self.sessionData.getOrgs()
        if result.size() > 1:
            Collections.sort(result, OrganizationComparator())
        return result
    
    def invalidTries(self):
        return str(Login.getMaxFailedLogins())
    
    def loginPage(self):
        return LoginBean.LOGIN_MAIN
    
    def loginSelectOrgPage(self):
        return LoginBean.LOGIN_GET_ORG 
    
    def passwordChangeHelp(self):
        return LoginBean.LOGIN_PWD_CHANGE_HELP
    
    def resetLoginHelp(self):
        return LoginBean.LOGIN_RESET_HELP
    
    def loginHelp(self):
        return LoginBean.LOGIN_HELP
    
    def cancel(self):
        self.error = False
        self.errorMessage = ""
        return LoginBean.LOGIN_CANCEL
    
    def reset(self):
        result = ""
        errs = self._validateReset()
        if len(errs) > 0:
            self.error = True
            self.errorMessage += self.validateErr(errs)
        else:
            try:
                li = ObjectFactory().getLogin(self.sessionData.loginID, self.sessionData.getOrganization())
                li.reset()
                li.save()
                result = LoginBean.LOGIN_CANCEL
            except Exception as e:
                super().handleException(e)
        return result
    
    def _validateReset(self):
        err = False
        result = []
        if Utils.isBlank(self.sessionData.loginID):
            err = True
            result.append("Login ID is blank")
        
        if Utils.isBlank(self.secret):
            err = True
            result.append("Secret Text is blank")
        
        if not err:
            try:
                li = ObjectFactory().getLogin(self.loginID, self.sessionData.getOrganization())
                if not li:
                    err = True
                    result.append("No such login")
                else:
                    encodedSecret = Encrypter().encrypt(self.secret)
                    if not encodedSecret == li.getSecret():
                        err = True
                        result.append("Secret is invalid")
            except Exception as e:
                self.handleException(e)
                self.errs.append(e.getMsg())
        return result
    
    def selectOrganization(self):
        try:
            org = ObjectFactory().getOrganization(self.getOrganizationId())
            if org:
                self.sessionData.setOrganization(org)
        except Exception as e:
            self.handleException(e)
        if org:
            return org
        else:
            return None 

    def attempt(self, loginName, password):
        error = False
        result = None
        org = self.sessionData.getOrganization()
        #print(self.sessionData.orgs)
        if not org:
            result = Menu.SELECT_ORG
        else:
            login = None
            try:
                login = ObjectFactory().getLogin(login=loginName, org=org)
            except NoLoginFoundException:
                    pass
            except Exception as e:
                self.handleException(e)
            if not login:
                result = None
                error = True
                self.sessionData.errorMessage = "No such login \"" + loginName + "\""
            else:
                self.sessionData.setCurrentLogin(login)
                if login.isLocked():
                    self.sessionData.setCurrentLogin(None)
                    result = None
                    error = True
                    self.sessionData.errorMessage = "Account is locked. Contact the administrator."
                elif not login.isAdmin() and login.isExpired():
                    result = Login.PASSWORD_EXPIRED
                elif login.isReset():
                    result = Login.LOGIN_STATUS_RESET
                else:
                    try:
                        login.attempt(password)
                    except AccountLockedException as e:
                        result = None
                        error = True
                        self.sessionData.errorMessage = "account is locked"
                    except AccountExpiredException as e:
                        result = None
                        error = True
                        self.sessionData.errorMessage = "account is expired"
                    except InvalidPasswordException as e:
                        result = None
                        error = True
                        self.sessionData.errorMessage = "wrong password"
                    if not error:
                        login.succeed()
                        self.sessionData.errorMessage = None
                        self.sessionData.setCurrentLogin(login)
                        self.currentLoginPrivileges = ObjectFactory().getCurrentUsersPrivileges(login)
                        result = Menu.HOME                        
        return result

    def getOrgname(self, val):
        result = None
        try:
            count = 0
            lis = ObjectFactory().getLogins()
            for li in lis:
                if val == li.getLogin():
                    if li.getOrganization():
                        result = li.getOrganization()
                        count += 1 
                    elif li.getLoginOrganizationID():
                        result = ObjectFactory().getOrganization(li.getLoginOrganizationID())
                        count += 1
            if (count > 1):
                result = None
        except Exception as e:
            self.handleException(e)
        return result