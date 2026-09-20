from abc import ABC
import collections 
from cryptography.fernet import Fernet
from datetime import datetime as DT,date,timedelta,time
from decimal import Decimal
from django.conf import settings
import inspect
import jprops
from loguru import logger
import os
   
from vscode.utils.exceptions import InvalidArgumentException
from vscode.base.base import VSBase 
from vs.models import DbScheduleEvent
   
                           
class Constants():

    DEFAULT_ORGANIZATION = "$$default$$"
    DEFAULT_PASSWORD = "Password1"
    DEFAULT_PROP_FILE_SYSTEM_PROP = "com.courrier.propFile"
    DEFAULT_PROP_FILE = "volunteerscheduker.properties"
    
    
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
    EJB_SERVER_WILDFLY = "WILDFLY"
    
    EMAIL_SENDER_TARGET = "com.courrier.email"
    EMPLOYER_LENGTH = 255
      
    JMS_RMI_PORT = 8300
    JMS_RMI_BIND = "JmsMessageServer"
    
    JOB_TITLE_LENGTH = 255
    JSON_RMI_BIND = "VolschedJson"
    JSON_RMI_PORT = 8300
    
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

    PROPERTY_PDF_LOCATION = "com.courrier.PDF.Location"
    
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
    #PROPERTY_NAMING_FACTORY = Context.INITIAL_CONTEXT_FACTORY
    #PROPERTY_NAMING_FACTORY_STATE = Context.STATE_FACTORIES
    PROPERTY_NAMING_FACTORY_URL = "java.naming.provider.url"
    #PROPERTY_NAMING_FACTORY_URL_PKG = Context.URL_PKG_PREFIXES
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
    SECURITY__PROP = "com.courrier.login."
    SECURITY__PROP = 'com.courriwr.security.'

    SEPARATE_PREFERRED = "Separate preferred"
    SEPARATE_REQUIRED = "Separate required"
    TOGETHER_PREFERRED = "Together preferred"
    TOGETHER_REQUIRED = "Together required"
    
    SERVER_ADDRESS = "server.address"
    
    SYSTEM_DEFAULT_ORGANIZATION_NAME = "$$default$$"
    SYSTEM_ORGANIZATION_NAME = "Volunteer Scheduler"
    VOLUNTEER_SECURITY_GROUP_ID = 4
      
class PropertiesManager(VSBase): 
    _instance = None  # Class variable tracking our single instance

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            # Create the instance only if it does not exist yet
            cls._instance = super().__new__(cls)
        return cls._instance
    
    
    properties = {}  
     
    @staticmethod
    def resetSingleton():
        _instance = None
    
    def __init__(self, fileName=Constants.DEFAULT_PROP_FILE):
        s = os.environ.get(Constants.DEFAULT_PROP_FILE_SYSTEM_PROP, Constants.DEFAULT_PROP_FILE)
        if super().notBlank(s):
            Constants.DEFAULT_PROP_FILE = s
        self.propfileName = Constants.DEFAULT_PROP_FILE
        if super().notBlank(fileName):
            self.propfileName = fileName

    def setProperty(self, fileName=Constants.DEFAULT_PROP_FILE, key=None, value=None): 
        if super().notBlank(key) and Utils.notBlank(value):
            self.fetchProperties(fileName)[key] = value
    
    def getProperty(self, fileName=Constants.DEFAULT_PROP_FILE, key=None):
        result = None
        if fileName and key and super().notBlank(key) and super().notBlank(fileName): 
            result = self.fetchProperties(fileName).get(key)
        return result
    
    def getBoolean(self, key, default=False): 
        result = default
        if key:
            val = self.getProperty(key)
            if val:
                if not isinstance(val, bool):
                    result = self.booleanValueOf(val)
                else:
                    result = val
        return result
    
    def booleanValueOf(self, txt):
        result = False
        if isinstance(txt, str):
            if txt.casefold() in ['true', 't', 'y', 'yes', 'ok']:
                result = True
        return result
    
    def getValueSet(self, key): 
        result = []
        if key:
            props = self.fetchProperties(self.propfileName)
            if props: 
                for propKey in props:
                    if str(propKey).startsWith(key): 
                        result.append(props.get(propKey))
        return result
    
    def getParsedValues(self, key): 
        result = [] 
        s = self.getProperty(key)
        if s and Utils.notBlank(s): 
            vals = s.split(",")
            for val in vals:
                val = val.strip()
                if super().notBlank(val): 
                    result.append(val)
          
    def getDefaultedProperty(self, fileName=None, key=None, defaultVal=None): 
        result = defaultVal
        if not fileName or super().isBlank(fileName):
            fileName = self.propfileName
        props = self.fetchProperties(fileName)
        if props and key and super().notBlank(key): 
            result = props.get(key)
            if not result:
                result = defaultVal    

    def getProperties(self, fileName=None):
        if not fileName or not Utils.notBlank(fileName): 
            fileName = self.propfileName
        result = self.fetchProperties(fileName)
        if not result: 
            result = {}        
        return result
    
    def dump(self, fileName): 
        if super().notBlank(fileName): 
            props = self.fetchProperties(fileName)
            self.say(fileName + "[")
            for key, value in props:
                self.say(str(key) + ' : ' + str(value))            
            self.say("]")
    
    def getPropertiesFileNames(self):
        result = [] 
        for p in self.properties.keys():
            result.append(str(p))        
        return result

    def fetchProperties(self, fileName=None):
        result = 'None'
        if not fileName or Utils.isBlank(fileName): 
            fileName = self.propfileName 
        if super().notBlank(fileName): 
            result = PropertiesManager.properties.get(fileName)
            if not result:
                vsPath = os.path.join(settings.BASE_DIR, '.', fileName) 
                with open(vsPath, "r") as fp:
                    properties = jprops.load_properties(fp,  collections.OrderedDict)
                    #print(fileName +  =  + str(properties))
                    PropertiesManager.properties[fileName] = properties
                    result = properties
        return result
    
    def _say(self, msg):
        print(msg)

class SystemOption(VSBase):
    _INI_FILE_NAME = ".\\SystemOption.INI"
    
    def __init__(self, fileName=None):
        if fileName:
            self.fileName = fileName
        else:
            self.fileName = SystemOption.INI_FILE_NAME
        PropertiesManager().getProperty(self.fileName, self.fileName)

    def set(self, key, value):
        if not key:
            super().complain("null key")
        PropertiesManager().setProperty(self.fileName, key, value)
    
    def get(self, key, allowNull=False):
        if not key:
            super().complain("null key")
        s = os.environ.get(key)
        if not s or super().isBlank(s):
            s = PropertiesManager().getProperty(self.fileName, key)
        if not s and not allowNull:
            super().complain('Nothing in table for key "'+ str(key) + '"')
        return s

    def dumpFile(self, fileName):
        PropertiesManager().dump(fileName)
        
    @staticmethod
    def dump():
        PropertiesManager().dump()

    def say(self, txt):
        print(txt)
        
    def complain(self, msg): 
        raise InvalidArgumentException(msg)  

class VSPersistableSystemOption(SystemOption):
    _configurableProps = None
    dynamicallyConfigurable = False
    
    @classmethod
    def isDynamicallyConfigurable(cls):
        return cls.dynamicallyConfigurable
    
    @classmethod
    def setDynamicallyConfigurable(cls, val):
        cls.dynamicallyConfigurable = val
    
    def __init__(self, fileName):
        super().__init__(fileName)

    def get(self, key):
        result = super().get(key, True)
        if VSPersistableSystemOption.isDynamicallyConfigurable():
            cps = VSPersistableSystemOption._getConfigurableProps()
            if cps:
                cp = VSPersistableSystemOption._configurableProps.get(key)
                if cp:
                    result = cp.getPropertyValue()
        return result
                   
class VSSystemOption(VSPersistableSystemOption):
    _iniFileName = "VolunteerScheduler.properties"
    _instance = None
     
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            # Create the instance if it doesn't exist yet
            cls._instance = super().__new__(cls)
        propFile = os.environ.get(Constants.PROPERTY_INI_FILE_PROPERTY)
        if propFile:                
            _iniFileName = propFile
        return cls._instance

    @staticmethod
    def resetSingleton():
        PropertiesManager.resetSingleton()
        _instance = None
    

    def __init__(self):
        super().__init__(fileName=VSSystemOption._iniFileName)
        
    @classmethod
    def getInifileName(cls):
        return cls._iniFileName
    
    @staticmethod
    def setDynamicallyConfigurable():
        VSPersistableSystemOption.setDynamicallyConfigurable(True)
        
    def get(self, prop):
        return PropertiesManager().getProperty(VSSystemOption._iniFileName, prop)
    
    def set(self, key, val):
        PropertiesManager().setProperty(VSSystemOption._iniFileName, key, val)

class VolunteerSchedulerSystemOption(SystemOption):

    INI_FILE_NAME = "VolunteerScheduler.properties"
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        super.__init__(VolunteerSchedulerSystemOption.INI_FILE_NAME)
    
    def get(self, key, defaultVal=None): 
        result = None
        s = super().get(key)
        if Utils.isBlank(s):
            result = defaultVal 
        else: 
            result = s
        return result

class Utils():
    systemAdminID = None
    
    @staticmethod
    def getMethods(obj=None, cls=None):
        methods = []
        if cls:
            methods_info = inspect.getmembers(cls, predicate=inspect.isroutine)
            methods = [name for name, val in methods_info if not name.startswith('_')]
        else:
            methods = [m for m in dir(obj) if callable(getattr(obj, m))]
        return methods

    @staticmethod   
    def compareNull(o1, o2):
        result = 0
        if o1 and not o2:
            result = 1
        elif not o1 and o2:
            result = 1
        return result
    
    @staticmethod   
    def isNull(o1, o2):
        return not o1 or not o2
    
    @staticmethod
    def equals(obj1, obj2):
        result = True
        if Utils.isNull(obj1,obj2):
            result = Utils.compareNull(obj1, obj2) == 0
        elif not obj1.__class__.__name == obj2.__class__.__name__:
            result = False
        elif isinstance(obj1, str):
            result = obj1 == obj2
        elif getattr(obj1, "equals"):
            result = obj1.equals(obj2)
        else: 
            try:
                result = obj1 == obj2
            except Exception as e:
                result = False
                logger.opt(exception=True).debug(e)
        return result 
    
    @staticmethod   
    def compareStrings(o1, o2): #assumes args, if present, are strings 
        result = 0
        if Utils.isNull(o1, o2):
            result = Utils.compareNull(o1, o2)
        else:
            s1 = o1
            s2 = o2
            if s1 > s2:
                result = 1
            elif s1 < s2:
                result = -1
        return result
    
    @staticmethod   
    def compareIgnoreCase(o1, o2): #assumes args, if present, are strings 
        from vscode.att.attribute import Attribute
        result = 0
        if Utils.isNull(o1, o2):
            result = Utils.compareNull(o1, o2)
        else:
            if isinstance(o1, Attribute):
                s1 = o1.value.lower()
            else:
                s1 = o1.lower()
            if isinstance(o2,Attribute):
                s2 =o2.value.lower()
            else:
                s2 = o2.lower()
            if s1 > s2:
                result = 1
            elif s1 < s2:
                result = -1
        return result
        
    @staticmethod   
    def compareInt(o1, o2):
        result = 0
        if Utils.isNull(o1, o2):
            result = Utils.compareNull(o1, o2)
        else:
            if  o1 > o2:
                result = 1
            elif o1 < o2:
                result = -1
        return result
        
    @staticmethod   
    def compareTimes(o1, o2):
        result = 0
        if Utils.isNull(o1, o2):
            result = Utils.compareNull(o1, o2)
        else:
            if isinstance(o1, DT):
                o1 = o1.time()
            if isinstance(o2, DT):
                o2 = o2.time()
            if o1 > o2:
                result = 1
            elif o1 < o2:
                result = -1
        return result
                 
    @staticmethod   
    def compareDates(o1, o2): #assumes args are either date or datetime
        result = 0
        if Utils.isNull(o1, o2):
            result = Utils.compareNull(o1, o2)
        else:
            if (isinstance(o1, DT) and isinstance(o2, DT)) or \
                (isinstance(o1, date) and isinstance(o2, date)):
                if o1 > o2:
                    result = 1
                elif o1 < o2:
                    result = -1
            else:
                d1 = o1
                d2 = o2
                if isinstance(d1, DT):
                    d1 = d1.date()
                else:
                    d2 = d2.date()
                if d1 > 22:
                    result = 1
                elif d1 < d2:
                    result = -1
                
        return result

    @staticmethod
    def reset():
        Utils.systemAdminID = None

    @staticmethod
    def getUniqueString():
        return 'STR' + DT.now().strftime("%Y-%m-%d-%H:%M:%S")
     
    @staticmethod
    def getSystemAdminId():
        if not Utils.systemAdminId:
            of = ObjectFactory()
            adminName = VSSystemOption().get(Constants.PROPERTY_SYSTEM_ID)
            org = None
            for oi in of.getOrganizations():
                if oi.getName() != Constants.SYSTEM_DEFAULT_ORGANIZATION_NAME:
                    continue
                org = oi
                break
            if org:
                li = of.getLogin(adminName, org)
                if li:
                    systemAdminID = li.getLoginID()
            return systemAdminId
    
    @staticmethod
    def isSameDay(event1, event2):
        result = True
        if not event1 or not event2:
            result = false
        else: 
            d1 = event1.getEventDate()
            d2 = event2.getEventDate()
            if d1 and d2:
                if isinstance(d1, DT):
                    d1 = d1.date()
                if isinstance(d2, DT):
                    d2 = d2.date()
                result = d1 == d2
            else:
                result = false
        return result
    

    @staticmethod
    def compareMaps(map1, map2, checkObjects):
        result = map1 is not None and map2 is not None and isinstance(map1, dict) \
            and isinstance(map2, dict) 
        if result:
            result = map1.size() == map2.size()
        if result:
            for key, vsp1 in map1:
                vsp2 = map2.get(key)
                if not vsp2:
                    result = False
                    break
                if checkObjects:
                    result = vsp1.isSameState(vsp2)
        if result:
            for key, vsp2 in map2:
                vsp1 = map1.get(key)
                if not vsp1:
                    result = False
                    break
                if checkObjects:
                    result = vsp1.isSameState(vsp2)
        return result
    
    @staticmethod
    def eventsOverlap(se1, se2, dbo=False):
        if dbo:
            return Utils._eventsOverlapDbo(se1, se2)
        else:
            return Utils._eventsOverlapNotDbo(se1, se2)
    
    @staticmethod     
    def _eventsOverlapDbo(se1, se2):
        result = False
        from vscode.base.business_objects import ScheduleEvent
        if se1 and isinstance(se1, ScheduleEvent):
            se1 = se1.myDb
        if se2 and isinstance(se2, ScheduleEvent):
            se2 = se2.myDb
        if se1 and se2:
            #print(se1.eventDate.__class__.__name__ + ' ' + se2.eventDate.__class__.__name__)
            if isinstance(se1.eventDate, DT):
                s1 = se1.eventDate.replace(hour=0, minute=0, second=0)
            else:
                s2 = se1.eventDate.combine(hour=0, minute=0, second=0)
            if isinstance(se2.eventDate, DT):
                s2 = se2.eventDate.replace(hour=0, minute=0, second=0)
            else:
                tm = time(hour=0, minute=0, second=0) 
                s2 = DT.combine(se2.eventDate, tm)
            tm1 = DT.strptime(se1.eventStartTime, '%H:%M').time()
            tm2 = DT.strptime(se2.eventStartTime, '%H:%M').time()
            start1 = DT.combine(s1,tm1)
            start2 = DT.combine(s2,tm2)
            dur1 = se1.eventDuration
            dur2 = se2.eventDuration
            result = Utils._eventsOverlap(start1, start2, dur1,dur2)
        return result
    
    @staticmethod
    def _eventsOverlapNotDbo(se1, se2):
        result = False
        if se1 and se2:
            s1 = se1.getEventDate().replace(hour=0,minute=0,second=0)
            s2 = se2.getEventDate().replace(hour=0,minute=0,second=0)
            tm1 = DT.strptime(se1.getStartTime(), '%H:%M').time()
            tm2 = DT.strptime(se2.getStartTime(), '%H:%M').time()
            start1 = DT.combine(s1,tm1)
            start2 = DT.combine(s2,tm2)
            dur1 = se1.getEventDuration()
            dur2 = se2.getEventDuration()
            result = Utils._eventsOverlap(start1, start2, dur1,dur2)
        return result
    
    @staticmethod     
    def _eventsOverlap(start1, start2, dur1, dur2):
        result = False
        #print('start1 ' + str(start1) + ' start2 ' +str(start2) + ' dur1 ' + str(dur1) +' dur2 ' + str(dur2))
        end1 = start1 + timedelta(minutes=dur1)
        end2 = start2 + timedelta(minutes=dur2)
        #print('end1 ' + str(end1) + ' end2 ' + str(end2))
        if start2 >= start1 and start2 <= end1:
            result = True
        elif end2 >= start1 and end2 <= end1:
            result = True    
        elif start1 >= start2 and start1 <= end2:
            result = True
        elif end1 >= start2 and end1 <= end2:
            result = True
        return result
    
    @staticmethod
    def compareCollections(coll1, coll2, checkObjects=True):
        result = coll1 and coll2  and isinstance(coll1, list) \
            and isinstance(coll2, list) and len(coll1) == len(coll2)
        if result and checkObjects and len(coll1) > 0:
            while True:
                vsp1 = coll1.pop()
                vsp2 = coll2.pop()
                result = vsp1.isSameState(vsp2)
                if not result:
                    break
        return result
    
    @staticmethod   
    def isBlank(s):
        return not Utils.notBlank(s)
    
    @staticmethod   
    def notBlank(s):
        result = True
        if s and isinstance(s, bytes):
            s = s.decode()
        if not s or not isinstance(s, str):
            result = False
        elif s.strip() == '':
            result = False 
        return result;
    
    @staticmethod 
    def isNotBlank(s):
        return Utils.notBlank(s)
    
    @staticmethod 
    def isBoolean(s):
        result = False
        if s is True or s is False:
            result = True
        return result
        
    @staticmethod 
    def isNumeric(s, allowNone=True):
        result = True
        if allowNone and not s:
            pass
        else:
            if not s and not s == 0:
                result = False
            elif not isinstance(s, int) and not isinstance(s, float) and not isinstance(s, Decimal):
                try:
                    s = float(s)
                except:
                    logger.opt(exception=True).debug("isnumeric failed str(type(s")
                    result = False
        return result

    @staticmethod   
    def compareLists(coll1, coll2, checkObjects=True):
        result = coll1 and coll2
        if result:
            result = len(coll1) == len(coll2)
       
        if result:
            for idx, vsp1 in enumerate(coll1):
                vsp2 = coll2[idx]                
                result = (vsp1 and vsp2) or (not vsp1 and not vsp2)
                if result and checkObjects and vsp1:
                    result = vsp1.isSameState(vsp2)
                if not result:
                    break
        return result
   
    @staticmethod   
    def  getProperty(key):
        result = os.environ.get(key)
        if Utils.usBlank(result):
            try:
                result = VSSystemOption().get(key)
            except Exception as e:
                logger.debug(e)
        return result
    
    @staticmethod   
    def  contains(string, value):
        result = False
        if string and isinstance(string, str) and value and isinstance(value, str):
            result = value in string
        return result
    
    @staticmethod
    def startsWith(string, substring):
        result = False
        if string and isinstance(string, str) and substring \
            and isinstance(substring, str):
            result = string.startswith(substring)
        return result    
    
class VSMessageFactory():

    @staticmethod 
    def getDateSequenceError(start,  end):
        startText = "null"
        endText = "null"
        sdf = 'M/d.yyyy'
        if start:
            startText = start.strfmt(sdf)
        if end:
            endText = end.strfmt(sdf)
        msg = VSMessages.getDateSequenceError(startText, endText)
        return msg

    @staticmethod 
    def getScheduleGapError(start, end):
        sdf = 'M/d.yyyy'
        startText = "null"
        endText = "null"
        if start:
            startText = start.strfmt(sdf)
        if end:
            endText = end.strfmt(sdf)
        msg = VSMessages.getScheduleGapError(startText, endText)
        return msg

    @staticmethod 
    def getScheduleOverlapError(start, end):
        sdf = 'M/d.yyyy'
        startText = "null"
        endText = "null"
        if start:
            startText = start.strfmt(sdf)
        if end:
            endText = end.strfmt(sdf)
        msg = VSMessages.getScheduleOverlapError(startText, endText)
        return msg

    @staticmethod 
    def getExceptionError(msg):
        return msg

    @staticmethod 
    def getAvailabilityOverlapError():
        msg = VSMessages.getAvailabilityOverlapError()
        return msg

    @staticmethod 
    def getExistingEventError():
        msg = VSMessages.getExistingEventError()
        return msg

    @staticmethod 
    def getMissingAddressError(where):
        msg = VSMessages.getMissingAddressError(where)
        return msg

    @staticmethod 
    def getMissingEventLocationError():
        msg = VSMessages.getMissingEventLocationError()
        return msg

    @staticmethod 
    def getMissingOrganizationError(where):
        msg = VSMessages.getMissingAddressError(where)
        return msg

    @staticmethod 
    def getMissingValueError(name, where=None):
        if where:
            msg = VSMessages.getMissingValueError(name, where)
        else:
            msg = VSMessages.getMissingValueError(name)
        return msg

    @staticmethod 
    def getNoAvailableVolunteerError(skill):
        msg = VSMessages.getNoAvailableVolunteerError(skill)
        return msg
    
    @staticmethod 
    def getNoExpertError(skill):
        msg = VSMessages.getNoExpertError(skill)
        return msg

    @staticmethod 
    def getInvalidArgumentError():
        msg = VSMessages.getInvalidArgumentError()
        return msg

    @staticmethod 
    def getDuplicateSkillsRelationshipError():
        msg = VSMessages.getDuplicateSkillsRelationshipError()
        return msg

    @staticmethod 
    def getInvalidPasswordError():
        msg = VSMessages.getInvalidPasswordError()
        return msg

    @staticmethod 
    def getRelationshipSameJobsError():
        msg = VSMessages.getRelationshipSameJobsError()
        return msg

    @staticmethod 
    def getRelationshipSameSkillsError():
        msg = VSMessages.getRelationshipSameSkillsError()
        return msg

    @staticmethod 
    def getEventScheduleDateChangeError():
        return VSMessages.getEventScheduleDateChangeError()

class VSMessages:
      
    msgs = {
    'availabilityOverlapError' : 'There is an availability date overlap',
    'dateSequenceError' : 'Start date: {0} is not before end date: {1}',
    'duplicateKeyError' : 'Attempting to insert an entry for existing key: {0} into: {1}',
    'duplicateSkillsRelationshipError' : 'Attempting to define a relationship for a skill to itself',
    'eventNull' : 'Schedule Event object is null',
    'eventIdNull' : 'Schedule Event object has not been saved',
    'eventScheduleDateChangeError' : 'Changing date of an event assigned to a schedule which is outside schedule date range',
    'existingEventError' : 'There is already an event for that time in that location',
    'invalidArgumentError' : 'InvalID Argument Error',
    'invalidIntegerKeyValueError' : 'The key must be an between (0) and {1}. Received: {2}',
    'invalidPassword' : 'The password is invalid',
    'invalidPasswordError' :  'Password must be be at least 8 characters containing at least one one lower case letter, one upper case letter, & one digit',
    'invalidRecurrenceType' :  'Recurrence Type {0} is invalid',
    'invalidSecretText' :  'The secret text {0} is invalid',
    'missingAddressError' :  'Address was not supplied in {0}',
    'missingArgumentError' :  'Required argument: {0} missing in: {1}',
    'missingEventLocationError' :  'The event has no assigned location',
    'missingOrganizationError' :  'Organization was not supplied in {0}',
    'missingValueError' :  'Value of {0) is null',
    'missingValueError2' :  'Value of {0} is null in {1}',
    'multipleObjectsFromQueryError' :  'The database returned {0} entries when 0 or 1 are expected',
    'noAvailableVolunteerError' :  'No volunteers with skill {0}',
    'noExpertError' :  'Unable to assign any experts with skill:{0}',
    'noJobVolunteerError' :  'Job had no volunteer',
    'noVolunteerError' :  'No available volunteers with skill: {0}',
    'notLoginError' :  ' The argument must be None or a DbLogin or a Login',
    'nullKeyError' :  'The key was null',
    'projectNull' :  'The project was not provided',
    'relationshipSameJobsError' :  'Relationship of a job with itself',
    'relationshipSameSkillsError' :  'Relationship of a skill with itself',
    'resourceIdNull' :  'Resource object has not been saved',
    'resourceNull' :  'Resource object is null',
    'resourceCollectionNull' :  'Resource collection is null',
    'resourceCountTooSmall' :  'Number of resources specified0 is less than one',
    'scheduleCannotBePrepared' :  'Schedule cannot be prepared',
    'scheduleCreateUserNotSet' :  'Could not set create and update user',
    'scheduleGapError' :  'Schedule starting at {0} and ending at: {1} leaves a gap',
    'scheduleNoExpert' :  'Could not assign expert',
    'scheduleNotBuiltError' :  'Could not createSchedule',
    'scheduleNoVolunteer' :  'Could not assign volunteer',
    'scheduleOverlapError' :  'Schedule starting at {0} and ending at: {1} overlaps an existing schedule',
    'unsupportedPersistable' :  'The database does not contain objects of type: {0}',
    'wrongKeyClassError' :  'The key was of the wrong class.  Expected: {0} Received:{1}'
    }
    
    @staticmethod
    def notValidLogin():
        return VSMessages.getText("notLoginError")
    
    @staticmethod
    def unsupportedPersistable(arg0):
        return VSMessages.getText("unsupportedPersistable", arg0)

    @staticmethod
    def duplicateKeyError(key, table):
        return VSMessages.getText("duplicateKeyError", str(key), table)

    @staticmethod
    def noExpertError(skillName):
        return VSMessages.getText("noExpertError", skillName)
    
    @staticmethod
    def noVolunteerError(volName):
        return VSMessages.getText("noVolunteerError", volName)

    @staticmethod
    def missingArgumentError(name, where):
        return VSMessages.getText("missingArgumentError", name, where)

    @staticmethod
    def nullKeyError():
        return VSMessages.getText("nullKeyError")

    @staticmethod
    def wrongKeyClassError(expected, actual):
        return VSMessages.getText("wrongKeyClassError", str(expected), str(actual))

    @staticmethod
    def invalidIntegerKeyValueError(value, minV, maxV):        
        return VSMessages.getText("invalidIntegerKeyValueError", str(minV), str(maxV), str(value))

    @staticmethod
    def multipleObjectsFromQueryError(value):
        return VSMessages.getText("multipleObjectsFromQueryError", str(value))

    @staticmethod
    def invalidSecretText(text):
        return VSMessages.getText("invalidSecretText", text)

    @staticmethod
    def invalidPassword():
        return VSMessages.getText("invalidPassword")

    @staticmethod
    def invalidRecurrenceType(val):
        return VSMessages.getText("invalidRecurrenceType", str(val))

    @staticmethod
    def resourceIdNull():
        return VSMessages.getText("resourceIdNull")

    @staticmethod
    def resourceNull():
        return VSMessages.getText("resourceNull")

    @staticmethod
    def resourceCollectionNull():
        return VSMessages.getText("resourceCollectionNull")

    @staticmethod
    def eventNull():
        return VSMessages.getText("eventNull")

    @staticmethod
    def projectNull():
        return VSMessages.getText("projectNull")

    @staticmethod
    def eventIdNull():
        return VSMessages.getText("eventIdNull")

    @staticmethod
    def resourceCountTooSmall(size):
        return VSMessages.getText("resourceCountTooSmall", str(size))

    @staticmethod
    def getDateSequenceError(start, end):
        return VSMessages.getText("dateSequenceError", start, end)

    @staticmethod
    def getScheduleGapError(start, end):
        return VSMessages.getText("scheduleGapError", start, end)

    @staticmethod
    def getScheduleOverlapError(start, end):
        return VSMessages.getText("scheduleOverlapError", start, end)

    @staticmethod
    def getAvailabilityOverlapError():
        return VSMessages.getText("availabilityOverlapError")

    @staticmethod
    def getExistingEventError():
        return VSMessages.getText("existingEventError")

    @staticmethod
    def getMissingAddressError(text):
        return VSMessages.getText("missingAddressError", text)

    @staticmethod
    def getMissingEventLocationError():
        return VSMessages.getText("missingEventLocationError")

    @staticmethod
    def getMissingOrganizationError(text):
        return VSMessages.getText("missingOrganizationError", text)

    @staticmethod
    def getMissingValueError(text):
        return VSMessages.getText("missingValueError", text)

    @staticmethod
    def getMissingValueError2(text, where):
        return VSMessages.getText("missingValueError2", text, where)

    @staticmethod
    def getNoAvailableVolunteerError(text):
        return VSMessages.getText("noAvailableVolunteerError", text)

    @staticmethod
    def getNoExpertError(text):
        return VSMessages.getText("noExpertError", text)

    @staticmethod
    def getInvalidArgumentError():
        return VSMessages.getText("invalidArgumentError")

    @staticmethod
    def getDuplicateSkillsRelationshipError():
        return VSMessages.getText("duplicateSkillsRelationshipError")

    @staticmethod
    def getInvalidPasswordError():
        return VSMessages.getText("invalidPasswordError")

    @staticmethod
    def getRelationshipSameJobsError():
        return VSMessages.getText("relationshipSameJobsError")

    @staticmethod
    def getRelationshipSameSkillsError():
        return VSMessages.getText("relationshipSameSkillsError")

    @staticmethod
    def getEventScheduleDateChangeError():
        return VSMessages.getText("eventScheduleDateChangeError")

    @staticmethod
    def getNoJobVolunteerError():
        return VSMessages.getText("noJobVolunteerError")

    @staticmethod
    def getScheduleCannotBePreparedError():
        return VSMessages.getText("scheduleCannotBePrepared")

    @staticmethod
    def getScheduleCreateUserNotSetError():
        return VSMessages.getText("scheduleCreateUserNotSet")

    @staticmethod
    def getScheduleNotBuiltError():
        return VSMessages.getText("scheduleNotBuiltError")

    @staticmethod
    def getScheduleNoExpertError():
        return VSMessages.getText("scheduleNoExpert")

    @staticmethod
    def getScheduleNoVolunteerError():
        return VSMessages.getText("scheduleNoVolunteer")
   
    
    @staticmethod
    def getText(key, arg0=None, arg1=None, arg2=None, arg3=None, arg4=None):
        result = VSMessages.msgs.get(key)
        if result is not None:
            if arg0 is not None:
                result = result.replace("{0", arg0)
            else:
                result = result.replace("{0", "")
                
            if arg1 is not None:
                result = result.replace("{1", arg1)
            else:
                result = result.replace("{1", "")
           
            if arg2 is not None:
                result = result.replace("{2", arg2)
            else:
                result = result.replace("{2", "")
           
            if arg3 is not None:
                result = result.replace("{3", arg3)
            else:
                result = result.replace("{3", "")
           
            if arg4 is not None:
                result = result.replace("{4", arg4)
            else:
                result = result.replace("{4", "")
           
        return result
    
class RequestType():
    availability = 'availability'
    event = 'event'
    household = 'household'
    job = 'job'
    relationship = 'relationship'
    report = 'report'
    securityGroup = 'securityGroup'
    schedule = 'schedule'
    volunteerSkill = 'volunteerSkill'
    project = 'project'
    activity = 'activity'
    projectResource = 'projectResource'
    task  = 'team'
    team = 'team'
    volunteer = 'volunteer'

class ValuesHolder():
        _currentLogin = None
        _currentOrganizatiion = None
        
        @classmethod
        def getCurrentLogin(cls):
            return cls._currentLogin
        
        @classmethod
        def setCurrentLogin(cls, li):
            cls._currentLogin = li
        
        @classmethod
        def getCurrentOrganizatiion(cls):
            return cls._currentOrganizatiion
        
        @classmethod
        def setCurrentOrganizatiion(cls, li):
            cls._currentOrganizatiion = li
        
        def __init__(self):
            pass
        
class Encrypter:
    key = "SHTptueuR4NYn521OaabLoZRUVVmaK99Kp9PJYgClCg="
    def __init__(self):
        pass
    
    def encrypt(self, text):
        cipherSuite = Fernet(Encrypter.key)                
        textBytes = text.encode() # Convert string to bytes
        return cipherSuite.encrypt(textBytes).decode('utf-8')
    
    def decrypt(self, text):
        #print(type(text))
        cipherSuite = Fernet(Encrypter.key)
        textBytes = cipherSuite.decrypt(text)
        return textBytes.decode('utf-8')
    
    