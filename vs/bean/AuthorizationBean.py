from vs.bean.beans import SessionDataBean
 class AuthorizationBean(SessionDataBean):
    

    def authorize(self, action):
        boolean result = False
        LoginImpl login = sessionData.getCurrentLogin()
        if (login is not None):
            result = SecurityUtils.isAuthorized(login, action)
        
        return result
    

    def getRESOURCE_ADD_ORGANIZATION(self):
        return "Add Organization"
    

    def getRESOURCE_DELETE_ORGANIZATION(self):
        return "Delete Organization"
    

    def getRESOURCE_UPDATE_ORGANIZATION(self):
        return "Update Organization"
    

    def getRESOURCE_VIEW_EVENTS(self):
        return "View Events"
    

    def getRESOURCE_ORGANIZATIONS(self):
        return "Update Organizations"
    

    def getRESOURCE_ADD_ACTIVITY(self):
        return "Add Activity"
    

    def getRESOURCE_DELETE_ACTIVITY(self):
        return "Delete Activity"
    

    def getRESOURCE_UPDATE_ACTIVITY(self):
        return "Update Activity"
    

    def getRESOURCE_VIEW_ACTIVITIES(self):
        return "View Activities"
    

    def getRESOURCE_ADD_PROJECT(self):
        return "add Project"
    

    def getRESOURCE_DELETE_PROJECT(self):
        return "Delete Project"
    

    def getRESOURCE_UPDATE_PROJECT(self):
        return "Update Project"
    

    def getRESOURCE_VIEW_PROJECTS(self):
        return "View Projects"
    

    def getRESOURCE_ADD_TASK(self):
        return "Add Project Task"
    

    def getRESOURCE_DELETE_TASK(self):
        return "Delete Project Task"
    

    def getRESOURCE_UPDATE_TASK(self):
        return "Update Project Task"
    

    def getRESOURCE_VIEW_TASKS(self):
        return "View Project Tasks"
    

    def getRESOURCE_ADD_TEAM(self):
        return "Add Project Team"
    

    def getRESOURCE_DELETE_TEAM(self):
        return "Delete Project Team"
    

    def getRESOURCE_UPDATE_TEAM(self):
        return "Update Project Team"
    

    def getRESOURCE_VIEW_TEAMS(self):
        return "View Project Teams"
    

    def getRESOURCE_VIEW_LOGINS(self):
        return "View Logins"
    

    def getRESOURCE_DELETE_WORK_ADDRESS(self):
        return "Delete Work Address"
    

    def getRESOURCE_UPDATE_VOLUNTEER(self):
        return "Update Volunteer"
    

    def getRESOURCE_DELETE_SKILL(self):
        return "Delete Skill"
    

    def getRESOURCE_ADD_SCHEDULE(self):
        return "Add Schedule"
    

    def getRESOURCE_UPDATE_REPORT(self):
        return "Update Report"
    

    def getRESOURCE_VIEW_WORK_ADDRESS(self):
        return "View Work Address"
    

    def getRESOURCE_DELETE_RELATIONSHIP(self):
        return "Delete Relationship"
    

    def getRESOURCE_DELETE_SCHEDULE(self):
        return "Delete Schedule"
    

    def getRESOURCE_ADD_VOLUNTEER_SKILL(self):
        return "Add Volunteer Skill"
    

    def getRESOURCE_ADD_SECURITY_GROUP(self):
        return "Add Security Group"
    

    def getRESOURCE_VIEW_VOLUNTEERS(self):
        return "View Volunteers"
    

    def getRESOURCE_ADD_WORK_ADDRESS(self):
        return "Add Work Address"
    

    def getRESOURCE_UPDATE_AUTHORIZATION(self):
        return "Update Authorization"
    

    def getRESOURCE_VIEW_HOUSEHOLD(self):
        return "View Household"
    

    def getRESOURCE_VIEW_LOCATIONS(self):
        return "View Locations"
    

    def getRESOURCE_VIEW_SKILL_RELATIONSHIP(self):
        return "View Skill Relationship"
    

    def getRESOURCE_VIEW_JOB_ASSIGNMENTS(self):
        return "View Job Assignments"
    

    def getRESOURCE_BUILD_SCHEDULE(self):
        return "Build Schedule"
    

    def getRESOURCE_DELETE_EVENT(self):
        return "Delete Event"
    

    def getRESOURCE_UPDATE_AVAILABILITY(self):
        return "Update Availability"
    

    def getRESOURCE_UPDATE_WORK_ADDRESS(self):
        return "Update Work Address"
    

    def getRESOURCE_UPDATE_LOCATION(self):
        return "Update Location"
    

    def getRESOURCE_VIEW_VOLUNTEER(self):
        return "View Volunteer"
    

    def getRESOURCE_ADD_EVENT(self):
        return "Add Event"
    

    def getRESOURCE_UPDATE_SKILL(self):
        return "Update Skill"
    

    def getRESOURCE_VIEW_JOBS(self):
        return "View Jobs"
    

    def getRESOURCE_VIEW_RESOURCES(self):
        return "View Resources"
    

    def getRESOURCE_UPDATE_RELATIONSHIP(self):
        return "Update Relationship"
    

    def getRESOURCE_VIEW_EVENT(self):
        return "View Event"
    

    def getRESOURCE_VIEW_LOCATION(self):
        return "View Location"
    

    def getRESOURCE_VIEW_VOLUNTEER_SKILL(self):
        return "View Volunteer Skill"
    

    def getRESOURCE_VIEW_EVENT_PREFERENCE(self):
        return "View Event Preference"
    

    def getRESOURCE_ADD_SKILL(self):
        return "Add Skill"
    

    def getRESOURCE_UPDATE_SECURITY_GROUP_PRIVILEGE(self):
        return "Update Security Group Privilege"
    

    def getRESOURCE_UPDATE_SKILL_RELATIONSHIP(self):
        return "Update Skill Relationship"
    

    def getRESOURCE_VIEW_PRIVILEGES(self):
        return "View Privileges"
    

    def getRESOURCE_VIEW_RELATIONSHIP(self):
        return "View Relationship"
    

    def getRESOURCE_HOME(self):
        return "Home"
    

    def getRESOURCE_ADD_AVAILABILITY(self):
        return "Add Availability"
    

    def getRESOURCE_UPDATE_SCHEDULE(self):
        return "Update Schedule"
    

    def getRESOURCE_VALIDATE_RELATIONSHIP(self):
        return "Validate Relationship"
    

    def getRESOURCE_VIEW_SKILL(self):
        return "View Skill"
    

    def getRESOURCE_UPDATE_HOUSEHOLD(self):
        return "Update Household"
    

    def getRESOURCE_UPDATE_VOLUNTEER_SKILL(self):
        return "Update Volunteer Skill"
    

    def getRESOURCE_VIEW_SECURITY_GROUPS(self):
        return "View Security Groups"
    

    def getRESOURCE_PASSWORD_RESET(self):
        return "Password Reset"
    

    def getRESOURCE_ADD_JOB(self):
        return "Add Job"
    

    def getRESOURCE_DELETE_VOLUNTEER(self):
        return "Delete Volunteer"
    

    def getRESOURCE_VIEW_RELATIONSHIPS(self):
        return "View Relationships"
    

    def getRESOURCE_VIEW_HELP(self):
        return "View Help"
    

    def getRESOURCE_UPDATE_JOB(self):
        return "Update Job"
    

    def getRESOURCE_VIEW_JOB_ASSIGNMRNTS(self):
        return "View Job Assignments"
    

    def getRESOURCE_ADD_JOB_ASSIGNMRNTS(self):
        return "Add Job Assignments"
    

    def getRESOURCE_UPDATE_JOB_ASSIGNMRNTS(self):
        return "Update Job Assignments"
    

    def getRESOURCE_DELETE_JOB_ASSIGNMRNTS(self):
        return "Delete Job Assignments"
    

    def getRESOURCE_DELETE_CONFIGURABLE_PROPERTY(self):
        return "Delete Configurable Property"
    

    def getRESOURCE_UPDATE_EVENT(self):
        return "Update Event"
    

    def getRESOURCE_ADD_SKILL_RELATIONSHIP(self):
        return "Add Skill Relationship"
    

    def getRESOURCE_DELETE_LOCATION(self):
        return "Delete Location"
    

    def getRESOURCE_DELETE_RESOURCE(self):
        return "Delete Resource"
    

    def getRESOURCE_VIEW_REPORTS(self):
        return "View Reports"
    

    def getRESOURCE_DELETE_JOB(self):
        return "Delete Job"
    

    def getRESOURCE_VIEW_SCHEDULE(self):
        return "View Schedule"
    

    def getRESOURCE_ADD_LOCATION(self):
        return "Add Location"
    

    def getRESOURCE_UPDATE_CONFIGURABLE_PROPERTY(self):
        return "Update Configurable Property"
    

    def getHELP_SKILL_RELATIONSHIP_UPDATE(self):
        return "Update Skill"
    

    def getRESOURCE_ADD_LOGIN(self):
        return "Add Login"
    

    def getRESOURCE_ADD_SECURITY_GROUP_PRIVILEGE(self):
        return "Add Security Group Privilege"
    

    def getRESOURCE_VIEW_JOB(self):
        return "View Job"
    

    def getRESOURCE_ADD_HOUSEHOLD(self):
        return "Add Household"
    

    def getRESOURCE_UTILITIES(self):
        return "Utilities"
    

    def getRESOURCE_DELETE_VOLUNTEER_SKILL(self):
        return "Delete Volunteer Skill"
    

    def getRESOURCE_ADD_REPORT(self):
        return "Add Report"
    

    def getRESOURCE_ADD_VOLUNTEER(self):
        return "Add Volunteer"
    

    def getRESOURCE_NOT_AUTHORIZED(self):
        return "Not Authorized"
    

    def getRESOURCE_VIEW_SECURITY_GROUP_PRIVILEGE(self):
        return "View Security Group Privilege"
    

    def getRESOURCE_VIEW_RESOURCE(self):
        return "View Resource"
    

    def getRESOURCE_VIEW_SKILLS(self):
        return "View Skills"
    

    def getRESOURCE_UPDATE_RESOURCE(self):
        return "Update Resource"
    

    def getRESOURCE_VIEW_SCHEDULES(self):
        return "View Schedules"
    

    def getRESOURCE_ADD_RELATIONSHIP(self):
        return "Add Relationship"
    

    def getRESOURCE_DELETE_SKILL_RELATIONSHIP(self):
        return "Delete Skill Relationship"
    

    def getRESOURCE_UPDATE_PRIVILEGE(self):
        return "Update Privilege"
    

    def getRESOURCE_UPDATE_LOGIN(self):
        return "Update Login"
    

    def getRESOURCE_UPDATE_EVENT_PREFERENCE(self):
        return "Update Event Preference"
    

    def getRESOURCE_UPDATE_SECURITY_GROUP(self):
        return "Update Security Group"
    

    def getRESOURCE_VIEW_CONFIGURABLE_PROPERTIES(self):
        return "View Configurable Properties"
    

    def getRESOURCE_DELETE_HOUSEHOLD(self):
        return "Delete Household"
    

    def getRESOURCE_ADD_RESOURCE(self):
        return "Add Resource"
    

    def getRESOURCE_DELETE_AVAILABILITY(self):
        return "Delete Availability"
    

    def getRESOURCE_VIEW_HOUSEHOLDS(self):
        return "View Households"
    

    def getRESOURCE_ADD_PRIVILEGE(self):
        return "Add Privilege"
    

    def getRESOURCE_ADD_CONFIGURABLE_PROPERTY(self):
        return "Add Configurable Property"
    

    def getRESOURCE_VIEW_AVAILABILITY(self):
        return "View Availability"
    

