from abc import ABC
from datetime import datetime as DT
from loguru import logger

from vscode.utils.exceptions import InvalidArgumentException

logger.add("D:/tmp/PythonVolsched.log", backtrace=True, diagnose=True)

class Constants(ABC):

    VOLUNTEER_SECURITY_GROUP_ID = 4

    DEFAULT_ORGANIZATION = "$$default$$"
    DEFAULT_PASSWORD = "Password1"
    
    DERBY_DB_LOCATION = "db.derby.databaseLocation"
    DERBY_EMBEDDED_DRIVER = "db.derby.embedded.driver"
    DERBY_EMBEDDED_URL = "db.derby.embedded.connectInfo"
    DERBY_HOME = "derby.system.home"
    DERBY_HOST = "db.derby.host"
    DERBY_PORT = "db.derby.port"
    DERBY_SCHEMA = "db.derby.schema"
    
    EJB_SERVER_GLASSFISH = "GLASSFISH"
    EJB_SERVER_JBOSS = "JBOSS"
    EJB_SERVER_PAYARA = "PAYARA"
    EJB_SERVER_RMI = "RMI"
    EJB_SERVER_WEBLOGIC = "WEBLOGIC"  
    
    EMAIL_SENDER_TARGET = "com.courrier.email"
      
    JMS_RMI_PORT = 8300
    JMS_RMI_BIND = "JmsMessageServer"
    JSON_RMI_BIND = "VolschedJson"
    JSON_RMI_PORT = 8300
    EJB_SERVER_WILDFLY = "WILDFLY"
    JNDI_VS_REMOTE_INTERFACE = "ejb/VolunteerScheduler#com/courrier/volunteer/persistence/ejb/VolunteerSchedulerBeanRemote"
    #JNDI_VS_REMOTE_INTERFACE = "ejb/VolunteerScheduler"
    PERSISTENCE_TYPE_DERBY = "DERBY"
    PERSISTENCE_TYPE_DERBYNET = "DERBYNET"
    PERSISTENCE_TYPE_EJB = "EJB"
    PERSISTENCE_TYPE_EJBLOCAL = "EJBLOCAL"
    PERSISTENCE_TYPE_HIBERNATE = "HIBERNATE"
    PERSISTENCE_TYPE_JMS = "JMS"
    PERSISTENCE_TYPE_JNDI = "JNDI"
    PERSISTENCE_TYPE_JPA = "JPA"
    PERSISTENCE_TYPE_JPARMI = "JPARMI"
    PERSISTENCE_TYPE_JSON = "JSON"
    PERSISTENCE_TYPE_ODB = "ODB"
    PERSISTENCE_TYPE_RELATIONAL = "RDBMS"
    PERSISTENCE_TYPE_REST = "REST"
    PERSISTENCE_TYPE_REST_DOTNET = "DOTNET"
    PERSISTENCE_TYPE_RMI = "RMI"
    PERSISTENCE_TYPE_SIMPLE_FILE = "simple file"
    PERSISTENCE_TYPE_XML = "XML"
    PERSISTENCE_TYPE_WS = "WEBSERVICE"
    
    PROPERTY_DERBY_HOST = "db.derby.host"
    PROPERTY_DERBY_PORT = "db.derby.port"
    PROPERTY_DERBY_URL = "db.derby.driver.connectInfo"
    
    PROPERTY_DOTNET_URL = "com.courrier.DOTNET.url"
    
    PROPERTY_REST_URL = "com.courrier.REST.url"

    PROPERTY_EJB_CONNECT_TIMEOUT = "com.courrier.EJB.connect.timeout"
    PROPERTY_EJB_SERVER_TYPE = "com.courrier.EJB.Server.Type"
    PROPERTY_EJB_INTERFACE = "com.courrier.volsched.EJB.Interface"
    PROPERTY_EJBLOCAL_INTERFACE = "com.courrier.volsched.EJB.local.Interface"
    PROPERTY_ENTITY_MAP_NAME = "com.courrier.entityMap"
    PROPERTY_ERROR_HANDLER_LEVEL = "com.courrier.errorHandler.messageLevel"

    PROPERTY_GLASSFISH_HOST = "com.courrier.EJB.Glassfish.host"
    PROPERTY_GLASSFISH_NAMING_FACTORY = "com.courrier.EJB.Glassfish.namingFactory"
    PROPERTY_GLASSFISH_NAMING_FACTORY_STATE = "com.courrier.EJB.Glassfish.namingFactory.state"
    PROPERTY_GLASSFISH_NAMING_FACTORY_URL = "com.courrier.EJB.Glassfish.namingFactory.url"
    PROPERTY_GLASSFISH_PORT = "com.courrier.EJB.Glassfish.port"
    PROPERTY_GLASSFISH_URL_PKG = "com.courrier.EJB.Glassfish.url.pkg"
    PROPERTY_GLASSFISH_VOLSCHED_EJB_REMOTE = "com.courrier.EJB.Glassfish.volshed.remoteInterface"
    PROPERTY_GLASSFISH_VOLSCHED_EJB_LOCAL = "com.courrier.EJB.Glassfish.volshed.localInterface"

    PROPERTY_JBOSS_NAMING_FACTORY = "com.courrier.EJB.JBOSS.namingFactory"
    PROPERTY_JBOSS_URL = "com.courrier.EJB.JBOSS.url"
    PROPERTY_JBOSS_PORT = "com.courrier.EJB.JBOSS.port"
    PROPERTY_JBOSS_HOST = "com.courrier.EJB.JBOSS.host"
    PROPERTY_JBOSS_VOLSCHED_EJB_REMOTE = "com.courrier.EJB.JBOSS.volshed.remoteInterface"

    PROPERTY_PERST_FILE_NAME = "com.courrier.perst.file"   
    PROPERTY_PERST_FILE_PAGE_POOL_SIZE = "com.courrier.perst.pagePoolSize"    
    
    PROPERTY_PAYARA_HOST = "com.courrier.EJB.Payara.host"
    PROPERTY_PAYARA_NAMING_FACTORY = "com.courrier.EJB.Payara.namingFactory"
    PROPERTY_PAYARA_NAMING_FACTORY_STATE = "com.courrier.EJB.Payara.namingFactory.state"
    PROPERTY_PAYARA_PORT = "com.courrier.EJB.Payara.port"
    PROPERTY_PAYARA_URL_PKG = "com.courrier.EJB.Payara.url.pkg"
    PROPERTY_PAYARA_VOLSCHED_EJB_REMOTE = "com.courrier.EJB.Payara.volshed.remoteInterface"
    PROPERTY_PAYARA_VOLSCHED_EJB_LOCAL = "com.courrier.EJB.Payara.volshed.localInterface"
    PROPERTY_PAYARA_NAMING_FACTORY_URL = "com.courrier.EJB.Payara.namingFactory.url"

    PROPERTY_INI_FILE_PROPERTY = "com.courrier.volunteer.propFile"
    PROPERTY_JNDI_BUFFERSIZE = "com.courrier.JNDI.BufferSize"
    PROPERTY_JNDI_INITIAL_CONTEXT_FACTORY = "com.courrier.JNDI.INITIAL_CONTEXT_FACTORY"
    PROPERTY_JNDI_PROVIDER_URL = "com.courrier.JNDI.PROVIDER_URL"
    PROPERTY_JNDI_ROOT = "com.courrier.JNDI.ROOT"
    PROPERTY_JNDI_SECURITY_CREDENTIALS = "com.courrier.JNDI.SECURITY_CREDENTIALS"
    PROPERTY_JNDI_SECURITY_PRINCIPAL = "com.courrier.JNDI.SECURITY_PRINCIPAL"
    PROPERTY_ORB_HOST = "org.omg.CORBA.ORBInitialHost"
    PROPERTY_LOGIN_OLD_PASSWORD_CHECK = "com.courrier.login.old.password.check.months"
    PROPERTY_ORB_PORT = "org.omg.CORBA.ORBInitialPort"
    PROPERTY_NAMING_FACTORY = 'Context.INITIAL_CONTEXT_FACTORY'
    PROPERTY_NAMING_FACTORY_STATE = 'Context.STATE_FACTORIES'
    PROPERTY_NAMING_FACTORY_URL = "java.naming.provider.url"
    PROPERTY_NAMING_FACTORY_URL_PKG = 'Context.URL_PKG_PREFIXES'
    PROPERTY_PERSISTENCE_FACTORY_CLASS = "com.courrier.PersistenceFactoryClass"
    PROPERTY_PERSISTENCE_LOCATION = "com.courrier.PersistenceLocation"   
    PROPERTY_PERSISTENCE_TYPE = "com.courrier.PersistenceType"
    PROPERTY_QUERY_MAP_NAME = "com.courrier.queryMap"
    PROPERTY_SAVE_COUNT = "com.courrier.maxSaveCount"
    PROPERTY_SIMPLE_FILE_NAME = "com.courrier.SimpleFileName"
    PROPERTY_SYSTEM_ID = "com.courrier.login.system.id"
    PROPERTY_SYSTEM_ADMIN_ID = "com.courrier.login.admin"
    PROPERTY_WEBLOGIC_HOST = "com.courrier.EJB.Weblogic.host"
    PROPERTY_WEBLOGIC_NAMING_FACTORY = "com.courrier.EJB.Weblogic.namingFactory"
    PROPERTY_WEBLOGIC_PORT = "com.courrier.EJB.Weblogic.port"
    PROPERTY_WEBLOGIC_URL = "com.courrier.EJB.Weblogic.url"
    PROPERTY_WEBLOGIC_VOLSCHED_EJB_REMOTE = "com.courrier.EJB.Weblogic.volshed.remoteInterface"
    PROPERTY_XML_FILE = "com.courrier.XMLFile"
    PROPERTY_XML_DTD_DEFINITION = "com.courrier.XMLDocTypeDef"

    REPORT_PAGE_MAX_LINES = 44
    
    RESOURCE_ADD_AVAILABILITY = "Add Availability"
    RESOURCE_ADD_CONFIGURABLE_PROPERTY = "Add Configurable Property"
    RESOURCE_ADD_EVENT = "Add Event"
    RESOURCE_ADD_HOUSEHOLD = "Add Household"
    RESOURCE_ADD_JOB = "Add Job"
    RESOURCE_ADD_LOCATION = "Add Location"
    RESOURCE_ADD_LOGIN = "Add Login"
    RESOURCE_ADD_ORGANIZATION = "Add Oganization"
    RESOURCE_ADD_PRIVILEGE = "Add Privilege"
    RESOURCE_ADD_RELATIONSHIP = "Add Relationship"
    RESOURCE_ADD_RESOURCE = "Add Resource"
    RESOURCE_ADD_REPORT = "Add Report"
    RESOURCE_ADD_SCHEDULE = "Add Schedule"
    RESOURCE_ADD_SECURITY_GROUP = "Add Security Group"
    RESOURCE_ADD_SECURITY_GROUP_PRIVILEGE = "Add Security Group Privilege"
    RESOURCE_ADD_SKILL = "Add Skill"
    RESOURCE_ADD_SKILL_RELATIONSHIP = "Add Skill Relationship"
    RESOURCE_ADD_VOLUNTEER = "Add Volunteer"
    RESOURCE_ADD_VOLUNTEER_SKILL = "Add Volunteer Skill"
    RESOURCE_ADD_WORK_ADDRESS = "Add Work Address"
    RESOURCE_BUILD_SCHEDULE = "Build Schedule"
    RESOURCE_DELETE_AVAILABILITY = "Delete Availability"
    RESOURCE_DELETE_CONFIGURABLE_PROPERTY = "Delete Configurable Property"
    RESOURCE_DELETE_EVENT = "Delete Event"
    RESOURCE_DELETE_HOUSEHOLD = "Delete Household"
    RESOURCE_DELETE_JOB = "Delete Job"
    RESOURCE_DELETE_LOCATION = "Delete Location"
    RESOURCE_DELETE_ORGANIZATION = "Delete Organization"
    RESOURCE_DELETE_RELATIONSHIP = "Delete Relationship"
    RESOURCE_DELETE_SCHEDULE = "Delete Schedule"
    RESOURCE_DELETE_RESOURCE = "Delete Resource"
    RESOURCE_DELETE_SKILL = "Delete Skill"
    RESOURCE_DELETE_SKILL_RELATIONSHIP = "Delete Skill Relationship"
    RESOURCE_DELETE_VOLUNTEER = "Delete Volunteer"
    RESOURCE_DELETE_VOLUNTEER_SKILL = "Delete Volunteer Skill"
    RESOURCE_DELETE_WORK_ADDRESS = "Delete Work Address"
    RESOURCE_HOME = "Home"
    RESOURCE_NOT_AUTHORIZED = "Not Authorized"
    RESOURCE_PASSWORD_RESET = "Password Reset"
    RESOURCE_SELECT_ORGANIZATION = "Select Organization"
    RESOURCE_UPDATE_AUTHORIZATION = "Update Authorization"
    RESOURCE_UPDATE_AVAILABILITY = "Update Availability"
    RESOURCE_UPDATE_CONFIGURABLE_PROPERTY = "Update Configurable Property"
    RESOURCE_UPDATE_EVENT = "Update Event"
    RESOURCE_UPDATE_EVENT_PREFERENCE = "Update Event Preference"
    RESOURCE_UPDATE_HOUSEHOLD = "Update Household"
    RESOURCE_UPDATE_JOB = "Update Job"
    RESOURCE_UPDATE_LOCATION = "Update Location"
    RESOURCE_UPDATE_LOGIN = "Update Login"
    RESOURCE_UPDATE_ORGANIZATION = "Update Organization"
    RESOURCE_UPDATE_PRIVILEGE = "Update Privilege"
    RESOURCE_UPDATE_RELATIONSHIP = "Update Relationship"
    RESOURCE_UPDATE_REPORT = "Update Report"
    RESOURCE_UPDATE_RESOURCE = "Update Resource"
    RESOURCE_UPDATE_SCHEDULE = "Update Schedule"
    RESOURCE_UPDATE_SECURITY_GROUP = "Update Security Group"
    RESOURCE_UPDATE_SECURITY_GROUP_PRIVILEGE = "Update Security Group Privilege"
    RESOURCE_UPDATE_SKILL = "Update Skill"
    RESOURCE_UPDATE_SKILL_RELATIONSHIP = "Update Skill Relationship"
    HELP_SKILL_RELATIONSHIP_UPDATE = "Update Skill"
    RESOURCE_UPDATE_VOLUNTEER = "Update Volunteer"
    RESOURCE_UPDATE_VOLUNTEER_SKILL = "Update Volunteer Skill"
    RESOURCE_UPDATE_WORK_ADDRESS = "Update Work Address"
    RESOURCE_UTILITIES = "Utilities"
    RESOURCE_VALIDATE_RELATIONSHIP = "Validate Relationship"
    RESOURCE_VIEW_AVAILABILITY = "View Availability"
    RESOURCE_VIEW_CONFIGURABLE_PROPERTIES = "View Configurable Properties"
    RESOURCE_VIEW_EVENT = "View Event"
    RESOURCE_VIEW_EVENT_PREFERENCE = "View Event Preference"
    RESOURCE_VIEW_EVENTS = "View Events"
    RESOURCE_VIEW_HELP = "View Help"
    RESOURCE_VIEW_HOUSEHOLD = "View Household"
    RESOURCE_VIEW_HOUSEHOLDS = "View Households"
    RESOURCE_VIEW_JOB = "View Job"
    RESOURCE_VIEW_JOB_ASSIGNMENTS = "View Job Assignments"
    RESOURCE_VIEW_JOBS = "View Jobs"
    RESOURCE_VIEW_LOCATION = "View Location"
    RESOURCE_VIEW_LOCATIONS = "View Locations"
    RESOURCE_VIEW_LOGINS = "View Logins"
    RESOURCE_VIEW_ORGANIZATIONS = "View Organizations"
    RESOURCE_VIEW_PRIVILEGES = "View Privileges"
    RESOURCE_VIEW_RELATIONSHIP = "View Relationship"
    RESOURCE_VIEW_RELATIONSHIPS = "View Relationships"
    RESOURCE_VIEW_REPORTS = "View Reports"
    RESOURCE_VIEW_RESOURCE = "View Resource"
    RESOURCE_VIEW_RESOURCES = "View Resources"
    RESOURCE_VIEW_VOLUNTEERS = "View Volunteers"
    RESOURCE_VIEW_VOLUNTEER = "View Volunteer"
    RESOURCE_VIEW_VOLUNTEER_SKILL = "View Volunteer Skill"
    RESOURCE_VIEW_SECURITY_GROUPS = "View Security Groups"
    RESOURCE_VIEW_SECURITY_GROUP_PRIVILEGE = "View Security Group Privilege"
    RESOURCE_VIEW_SCHEDULE = "View Schedule"
    RESOURCE_VIEW_SCHEDULES = "View Schedules"
    RESOURCE_VIEW_SKILL = "View Skill"
    RESOURCE_VIEW_SKILL_RELATIONSHIP = "View Skill Relationship"
    RESOURCE_VIEW_SKILLS = "View Skills"
    RESOURCE_VIEW_WORK_ADDRESS = "View Work Address" 
    RESOURCE_ADD_PROJECT_GROUPS = "Add Project Groups"
    RESOURCE_UPDATE_PROJECT_GROUPS = "Update Project Groups"
    RESOURCE_DELETE_PROJECT_GROUPS = "Delete Project Groups"
    RESOURCE_VIEW_PROJECT_GROUPS = "View Project Groups"
    RESOURCE_ADD_PROJECT_TASKS = "Add Project Tasks"
    RESOURCE_UPDATE_PROJECT_TASKS = "Update Project Tasks"
    RESOURCE_DELETE_PROJECT_TASKS = "Delete Project Tasks"
    RESOURCE_VIEW_PROJECT_TASKS = "View Project Tasks"
    RESOURCE_ADD_PROJECT_TASKFORCE = "Add Project Taskforce"
    RESOURCE_UPDATE_PROJECT_TASKFORCE = "Update Project Taskforce"
    RESOURCE_DELETE_PROJECT_TASKFORCE = "Delete Project Taskforce"
    RESOURCE_VIEW_PROJECT_TASKFORCE = "View Project Taskforces"
    RESOURCE_ADD_PROJECT_ACTIVITY = "Add Project Activity"
    RESOURCE_UPDATE_PROJECT_ACTIVITY = "Update Project Activity"
    RESOURCE_DELETE_PROJECT_ACTIVITY = "Delete Project Activity"
    RESOURCE_VIEW_PROJECT_ACTIVITIES = "View Project Activities"
    RESOURCE_VIEW_SECURITY_GROUP_PRIVILEGEs = "View Security Group Privileges"
    RESOURCE_ADD_PROJECTS = "Add Projects"
    RESOURCE_UPDATE_PROJECTS = "Update Projects"
    RESOURCE_DELETE_PROJECTS = "Delete Projects"
    RESOURCE_VIEW_PROJECTS = "View Projects"
    RESOURCE_ADD_TASKFORCE = "Add Taskforces"
    RESOURCE_UPDATE_TASKFORCE = "Update Taskforces"
    RESOURCE_DELETE_TASKFORCE= "Delete Taskforces"
    RESOURCE_VIEW_TASKFORCES = "View Taskforces"
    RESOURCE_ADD_TASK = "Add Task"
    RESOURCE_UPDATE_TASK = "Update Task"
    RESOURCE_DELETE_TASK= "Delete Task"
    RESOURCE_VIEW_TASKS = "View Tasks"
    RESOURCE_ADD_VOLUNTEER_GROUP = "Add Volunteer Groups"
    RESOURCE_UPDATE_VOLUNTEER_GROUP = "Update Volunteer Groups"
    RESOURCE_DELETE_VOLUNTEER_GROUP = "Delete Volunteer Groups"
    RESOURCE_VIEW_VOLUNTEER_GROUPS = "View Volunteer Groups"
    RESOURCE_ADD_ACTIVITIES = "Add Activities"
    RESOURCE_UPDATE_ACTIVITIES = "Update Activities"
    RESOURCE_DELETE_ACTIVITIES = "Delete Activities"
    RESOURCE_VIEW_ACTIVITIES = "View Activities"

    SECURITY_GROUP_VOLUNTEER = "Volunteers"
    SECURITY_ADMIN_PROP = "com.courrier.login.admin"
    SECURITY_PUBLIC_PROP = "com.courrier.login.public"
    PROPERTY_PDF_LOCATION = "com.courrier.PDF.Location"

    SEPARATE_PREFERRED = "Separate preferred"
    SEPARATE_REQUIRED = "Separate required"
    TOGETHER_PREFERRED = "Together preferred"
    TOGETHER_REQUIRED = "Together required"
    
    SYSTEM_DEFAULT_ORGANIZATION_NAME = "$$default$$"
    SYSTEM_ORGANIZATION_NAME = "Volunteer Scheduler"
    
    
class VSBase(ABC):
    SPACE = '                                                                                                                        '
    DATE_FMT = '%b %d, %Y'
    DATE_FMT_SLASH = '%m/%d/%Y'
    TIME_FMT = '%H:%M'
    
    def __init__(self):
        pass

    def stringToBool(self,val):
        truthMapping = {
            "true": True, "yes": True, "t": True, "1": True, "on": True,
            "false": False, "no": False, "f": False, "0": False, "off": False
        }
        # Normalize the string to lowercase and strip whitespace
        cleanedVal = str(val).strip().lower()
        
        if cleanedVal in truthMapping:
            return truthMapping[cleanedVal]
        raise ValueError(f"Cannot convert '{val}' to a boolean.")
         
    def handleException(self, err):
        logger.opt(exception=True).debug(err)  
        
    def trace(self, msg, exception=None):
        if msg and isinstance(msg, str):
            logger.trace(msg)
            if exception:
                logger.opt(exception=True).trace(exception)
            
    def debug(self, msg, exception=None):
        if msg and isinstance(msg, str):
            logger.debug(msg)
            if exception:
                logger.opt(exception=True).debug(exception)
            
    def info(self, msg, exception=None):
        if msg and isinstance(msg, str):
            logger.info(msg)
            if exception:
                logger.opt(exception=True).info(exception)
            
    def warning(self, msg, exception=None):
        if msg and isinstance(msg, str):
            logger.warning(msg)
            if exception:
                logger.opt(exception=True).warning(exception)
            
    def error(self, msg, exception=None):
        if msg and isinstance(msg, str):
            logger.error(msg)
            if exception:
                logger.opt(exception=True).error(exception)
            
    def complain(self,msg):
        raise InvalidArgumentException(msg)
    
    def isBlank(self, txt):
        result = True 
        if txt and isinstance(txt, str) and len(txt.strip()) > 1:
            result = False
        return result
    
    def notBlank(self, txt):
        return not self.isBlank(txt)

    def now(self):
        return DT.now()
    
class BusinessObjectBase(VSBase):
    
    @staticmethod
    def validateAttributes(attList):
        from vscode.att.attribute import InvalidAttributeValueException
        result = True
        message = None
        for att in attList:
            try:
                att.validate()
            except InvalidAttributeValueException as e:
                message = ('\n' + att.getName() + ' : ' + e.getMsg())
                result = False
        if not result:
            raise InvalidAttributeValueException(msg=message, attr=att.name)
    
    def __init__(self):
        pass
    
    def setIdProperties(self, att):
        att.allowInvalID = False
        att.nullAllowed = True  # needed because database generates an ID when the object is inserted.
        att.hasMinimum = True
        att.minimum = 0
        
    def setTrackingAttributes(self,
        createUser,
        updateUser,
        createDate,
        updateDate):

        createUser.allowInvalID = False
        createUser.nullAllowed = False
        createUser.hasMinimum = True
        createUser.setMinimum = 0

        updateUser.allowInvalID = False
        updateUser.nullAllowed = False
        updateUser.hasMinimum = True
        updateUser.setMinimum = 0

        createDate.allowInvalID = False
        createDate.nullAllowed = False
        
        updateDate.allowInvalID = False
        updateDate.nullAllowed = False

    def now(self): 
        return DT.now()
    
class ObjectFactoryBase(ABC):
    
    def __init__(self):
        pass
