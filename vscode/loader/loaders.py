from datetime import datetime as DT
from vs.models  import DbConfigurableProperty,DbConfigurationSet,\
DbSecurityGroup,DbPrivilege,DbProjectStatus,DbRecurrenceType,\
DbRelationshipType,DbScheduleStatus,DbSkillRelationshipType,DbStateCode,\
DbTaskStatus, DbPassword
from vs.models import DbLogin,DbOrganization,DbLoginStatus
from vscode.utils.utils import Encrypter

class LoaderManager(object):
        
    def load(self):
        ppf = True
        loader = LoginStatusLoader(ppf)
        loader.load()
        loader = ProjectStatusLoader(ppf)
        loader.load()
        loader = TaskStatusLoader(ppf)
        loader.load()
        loader = StateCodeLoader(ppf)
        loader.load()
        loader = RecurrenceTypeLoader(ppf)
        loader.load()
        loader = RelationshipTypeLoader(ppf)
        loader.load()
        loader = SkillRelationshipTypeLoader(ppf)
        loader.load()
        loader = ScheduleStatusLoader(ppf)
        loader.load()
        loader = OrganizationLoader()
        orgs = loader.load()
        loopNum = 0
        for org in orgs:
            ll = LoginLoader()
            ll.load(org, loopNum)
            loopNum += 2
        adminID = 1
        loader = PrivilegeLoader()
        loader.load(adminID)
        loopNum = 0
        for org in orgs:
            loader = SecurityGroupLoader()
            loader.load(adminID, org, loopNum)
            loopNum += 5
        loader = SecurityGroupPrivilegeLoader()
        loader.load(adminID)
        sLoop = 0 
        pLoop = 0
        for org in orgs:
            loader = ConfigurablePropertiesLoader()
            loader.load(org, sLoop, pLoop)
            sLoop += 2
            pLoop += 18
        for li in DbLogin.objects.all():
            oi = li.organization
            for sg in oi.securityGroups.all():
                li.securityGroups.add(sg)
            li.save()
        loader  = LoginSecurityGroupLoader()
        
class LoginSecurityGroupLoader:

    def load(self):
        for org in DbOrganization.objects.all():
            for li in DbLogin.objects.all():
                if li.organization.organizationID == org.organizationID:
                    for sg in org.securityGroups:
                        li.securityGroups.add(sg)
                    li.save()

class ConfigurablePropertiesLoader:
    
    def load(self, org, sLoop, pLoop):
        try:
            cs = DbConfigurationSet.objects.get(pk=(1 + sLoop))
        except DbConfigurationSet.DoesNotExist:
            cs = DbConfigurationSet()
            cs.organization = org
            cs.configurationSetID = (1 + sLoop)
            cs.configurationSetName ="System"
            cs.configurationSetCreateUser = 1
            cs.configurationSetUpdateUser = 1
            cs.save()
        self.loadProperties(cs, 1 + pLoop)
        
        try:
            cs = DbConfigurationSet.objects.get(pk=(2 + sLoop))
        except DbConfigurationSet.DoesNotExist:
            cs = DbConfigurationSet()
            cs.organization = org
            cs.configurationSetID = (2 + sLoop)
            cs.configurationSetName = "Volunteer Scheduler"
            cs.configurationSetCreateUser = 1
            cs.configurationSetUpdateUser = 1
            cs.save()
        self.loadProperties(cs, 10 + pLoop)
    
    def loadProperties(self, cs, ctr): 
        try:
            DbConfigurableProperty.objects.get(pk=(ctr))
            return
        except DbConfigurableProperty.DoesNotExist:
            cp = DbConfigurableProperty()
            cp.propertyID = ctr
            cp.propertyCreateUser = 1
            cp.propertyUpdateUser = 1
            cp.propertyDescription = "Minimum length of a password. Must be greater than 0 and less than, or equal to, 40"
            cp.propertyName = "minLength"
            cp.propertyType = 1
            cp.propertyValue = "8"
            cp.save()
            cs.properties.add(cp)
             
        cp = DbConfigurableProperty()
        cp.propertyID = ctr + 1
        cp.propertyCreateUser = 1
        cp.propertyUpdateUser = 1
        cp.propertyDescription = "Number of inva1ID password tries that will lock a users login. Must be positive or 0. If zero, there is no limit."
        cp.propertyName = "maxFails"
        cp.propertyType = 1
        cp.propertyValue = "3"
        cp.save()
        cs.properties.add(cp)
        
        cp = DbConfigurableProperty()
        cp.propertyID = ctr + 2
        cp.propertyCreateUser = 1
        cp.propertyUpdateUser = 1
        cp.propertyDescription = "Number of Number of days before password automatically expires. Must be positive or 0. If zero, logins do not automatically expire"
        cp.propertyName = "expireDays"
        cp.propertyType = 1
        cp.propertyValue = "0"
        cp.save()
        cs.properties.add(cp)
        
        cp = DbConfigurableProperty()
        cp.propertyID = ctr + 3
        cp.propertyCreateUser = 1
        cp.propertyUpdateUser = 1
        cp.propertyDescription = "Number of previous passwords to retain. Must be positive or 0. If zero, there is no limit."
        cp.propertyName = "pwdRetain"
        cp.propertyType = 1
        cp.propertyValue = "12"
        cp.save()
        cs.properties.add(cp)
        
        cp = DbConfigurableProperty()
        cp.propertyID = ctr + 4
        cp.propertyCreateUser = 1
        cp.propertyUpdateUser = 1
        cp.propertyDescription = "Activate email support? Must be True or False"
        cp.propertyName = "email"
        cp.propertyType = 1
        cp.propertyValue = "False"
        cp.save()
        cs.properties.add(cp)
        
        cp = DbConfigurableProperty()
        cp.propertyID = ctr + 5
        cp.propertyCreateUser = 1
        cp.propertyUpdateUser = 1
        cp.propertyDescription = "Email host SMTP server name"
        cp.propertyName = "emailHost"
        cp.propertyType = 1
        cp.propertyValue = "smtp.gmail.com"
        cp.save()
        cs.properties.add(cp)
        
        cp = DbConfigurableProperty()
        cp.propertyID = ctr + 6
        cp.propertyCreateUser = 1
        cp.propertyUpdateUser = 1
        cp.propertyDescription = "Email host TCP port"
        cp.propertyName = "emailPort"
        cp.propertyType = 1
        cp.propertyValue = "465"
        cp.save()
        cs.properties.add(cp)
        
        cp = DbConfigurableProperty()
        cp.propertyID = ctr + 7
        cp.propertyCreateUser = 1
        cp.propertyUpdateUser = 1
        cp.propertyDescription = "Email account"
        cp.propertyName = "emailAccount"
        cp.propertyType = 1
        cp.propertyValue = "darrelcourrier@gmail.com"
        cp.save()
        cs.properties.add(cp)
        
        cp = DbConfigurableProperty()
        cp.propertyID = ctr + 8
        cp.propertyCreateUser = 1
        cp.propertyUpdateUser = 1
        cp.propertyDescription = "Email password"
        cp.propertyName = "emailPassword"
        cp.propertyType = 1
        cp.propertyValue = "cmmc ktgl gswl adka"
        cp.save()
        cs.properties.add(cp)
        cs.save()

class LoginLoader:
    
    def load(self, org, loop):
        now = DT.now()
        encrypter = Encrypter()
        ls = DbLoginStatus.objects.get(pk=1)
        try:
            li = DbLogin.objects.get(pk=(1 + loop))
        except DbLogin.DoesNotExist:
            li = DbLogin()
            li.loginID = (1 + loop)
            li.organization = org
            li.loginStatus = ls
            li.login = "Admin"
            li.loginName = "System Administrator"
            li.password = encrypter.encrypt("Password1")
            li.secret = encrypter.encrypt("secret")
            li.lastChange = now
            li.loginCreateUser = 1
            li.loginUpdateUser = 1
            li.save()
            pwd = DbPassword()
            pwd.login = li
            pwd.password = li.password
            pwd.passwordCreateUser = 1
            pwd.passwordUpdateUser = 1
            pwd.save()
        try:
            li = DbLogin.objects.get(pk=(2 + loop))
        except DbLogin.DoesNotExist:
            li = DbLogin()
            li.loginID = (2 + loop)
            li.login = "SystemUtilities"
            li.loginName = "System Utilities"
            li.organization = org
            li.loginStatus = ls
            li.password = encrypter.encrypt("Password1")
            li.secret = encrypter.encrypt("Adminpw1")
            li.lastChange = now
            li.loginCreateUser = 1
            li.loginUpdateUser = 1
            li.save()
            pwd = DbPassword()
            pwd.login = li
            pwd.password = li.password
            pwd.passwordCreateUser = 1
            pwd.passwordUpdateUser = 1
            pwd.save()

class LoginStatusLoader():
    MINIMUM = 1
    MAXIMUM = 4
    READY = 1
    LOCKED = 2
    RESET = 3
    EXPIRED = 4
    
    def __init__(self, params):
         
        self.codes = [
        "1,Ready,1,1",
        "2,Locked,2,2",
        "3,Reset,3,3",
        "4,Expired,4,4"]
        
    def load(self):
        for code in self.codes:
            ls = DbLoginStatus()
            coll = code.split(',')
            ls.loginStatusID = int(coll[0])
            ls.loginStatusType = int(coll[2])
            ls.loginStatusDescription = coll[1]
            ls.save()
            #print(str(LoginStatus(ls)) +  :  + str(ls))
        #print(ValueTableManager()._getMap(LoginStatus))
        #print(str(len(DbLoginStatus.objects.all())))
       

class OrganizationLoader:
        
    def load(self):
        result =  [None] * 2
        try:
            oi = DbOrganization.objects.get(organizationName='Volunteer Scheduler')
        except DbOrganization.DoesNotExist:
            oi = DbOrganization()
            oi.organizationID = 1
            oi.organizationName = 'Volunteer Scheduler'
            oi.organizationCreateUser = 1
            oi.organizationUpdateUser = 1
            oi.organizationCreateDate = DT.now()
            oi.organizationUpdateDate = DT.now()
            oi.save()
        result[0] = oi
        
        try:
            oi = DbOrganization.objects.get(organizationName='System')
        except DbOrganization.DoesNotExist:
            oi = DbOrganization()
            oi.organizationID = 2
            oi.organizationName = 'System'
            oi.organizationCreateUser = 1
            oi.organizationUpdateUser = 1
            oi.organizationCreateDate = DT.now()
            oi.organizationUpdateDate = DT.now()
            oi.save()
        result[1] = oi
        return result
  
class PrivilegeLoader:
    
    def __init__(self):
         
        self.codes = [
        "1,Home,1,1,8",
        "2,Utilities,1,1,19",
        "3,View Help,1,1,26",
        "4,Password Reset,1,1,28",
        "5,Validate Relationship,1,1,18",
        "6,Update Authorization,1,1,27",
        "7,Add Availability,1,1,55",
        "8,Delete Availability,1,1,58",
        "9,Update Availability,1,1,9",
        "10,View Availability,1,1,20",
        "11,Add Event,1,1,1",
        "12,Delete Event,1,1,59",
        "13,Update Event,1,1,10",
        "14,View Event,1,1,30",
        "15,View Events,1,1,22",
        "16,Add Household,1,1,2",
        "17,Delete Household,1,1,60",
        "18,Update Household,1,1,11",
        "19,View Household,1,1,31",
        "20,View Households,1,1,23",
        "21,Add Job,1,1,3",
        "22,Delete Job,1,1,61",
        "23,Update Job,1,1,12",
        "24,View Job,1,1,32",
        "25,View Jobs,1,1,52",
        "26,Add Relationship,1,1,4",
        "27,Delete Relationship,1,1,62",
        "28,Update Relationship,1,1,13",
        "29,View Relationship,1,1,33",
        "30,View Relationships,1,1,29",
        "31,Add Skill,1,1,5",
        "32,Delete Skill,1,1,64",
        "33,Update Skill,1,1,15",
        "34,View Skill,1,1,35",
        "35,View Skills,1,1,25",
        "36,Add Volunteer,1,1,6",
        "37,Delete Volunteer,1,1,65",
        "38,Update Volunteer,1,1,16",
        "39,View Volunteer,1,1,36",
        "40,View Volunteers,1,1,24",
        "41,Add Volunteer Skill,1,1,7",
        "42,Delete Volunteer Skill,1,1,66",
        "43,Update Volunteer Skill,1,1,17",
        "44,View Volunteer Skill,1,1,37",
        "45,Add Schedule,1,1,56",
        "46,Update Schedule,1,1,14",
        "47,Delete Schedule,1,1,63",
        "48,View Schedule,1,1,34",
        "49,View Schedules,1,1,21",
        "50,Add Privilege,1,1,39",
        "51,Delete Privilege,1,1,67",
        "52,Update Privilege,1,1,40",
        "53,View Privileges,1,1,38",
        "54,Add Login,1,1,42",
        "55,Delete Login,1,1,86",
        "56,Update Login,1,1,43",
        "57,View Logins,1,1,41",
        "58,Add Security Group,1,1,45",
        "59,Delete Security Group,1,1,90",
        "60,Update Security Group,1,1,46",
        "61,View Security Groups,1,1,44",
        "62,Add Security Group Privilege,1,1,47",
        "63,Delete Security Group Privilege,1,1,91",
        "64,Update Security Group Privilege,1,1,48",
        "65,View Security Group Privilege,1,1,44",
        "66,View Security Group Privileges,1,1,116",
        "67,Add Resource,1,1,49",
        "68,Delete Resource,1,1,87",
        "69,Update Resource,1,1,50",
        "70,View Resources,1,1,51",
        "71,Add Event Preference,1,1,88",
        "72,Delete Event Preference,1,1,89",
        "73,Update Event Preference,1,1,54",
        "74,View Event Preference,1,1,53",
        "75,Add Work Address,1,1,57",
        "76,Delete Work Address,1,1,67",
        "77,Update Work Address,1,1,68",
        "78,View Work Address,1,1,69",
        "79,Add Job Relationship,1,1,70",
        "80,Delete Job Relationship,1,1,71",
        "81,Update Job Relationship,1,1,72",
        "82,View Job Relationship,1,1,73",
        "83,Add Job Assignments, 1,1,75",
        "84,Delete Job Assignments, 1,1,77",
        "85,Update Job Assignments, 1,1,76",
        "86,View Job Assignments, 1,1,74",
        "87,Update Configurable Properties,1,1,7",
        "88,View Configurable Properties,1,1,78",
        "89,Add Configuration Set,1,1,96",
        "90,Delete Configuration Set,1,1,97",
        "91,Update Configuration Set,1,1,98",
        "92,View Configuration Sets,1,1,99",
        "93,Add Location,1,1,83",
        "94,Delete Location,1,1,84",
        "95,Update Location,1,1,85",
        "96,Add Report,1,1,92",
        "97,Delete Report,1,1,94",
        "98,Update Report,1,1,93",
        "99,View Reports,1,1,95",
        "100,Add Organization,1,1,100",
        "101,Delete Organization,1,1,101",
        "102,Update Organization,1,1,102",
        "103,View Organizations,1,1,103",
        "104,Add Project Team,1,1,104",
        "105,Delete Project Team,1,1,112",
        "106,Update Project Team,1,1,105",
        "107,View Project Team,1,1,106",
        "108,View Project Teams,1,1,106",
        "109,Add Project Task,1,1,107",
        "110,Delete Project Task,1,1,109",
        "111,Update Project Task,1,1,108",
        "112,View Project Task,1,1,138",
        "113,View Project Tasks,1,1,138",
        "114,Add Project Activity,1,1,113",
        "115,Update Project Activity,1,1,114",
        "116,Delete Project Activity,1,1,115",
        "117,View Project Activity,1,1,115",
        "118,View Project Activities,1,1,115",
        "119,Add Project,1,1,117",
        "120,Delete Project,1,1,120",
        "121,Update Project,1,1,118",
        "122,View Project,1,1,119",
        "123,View Projects,1,1,119",
        "124,Add Project Resources,1,1,119",
        "125,Delete Project Resources,1,1,119",
        "126,Update Project Resources,1,1,119",
        "127,View Project Resources,1,1,119"]
    def load(self, login):
        for code in self.codes:
            fields = code.split(",")
            privID = int(fields[0])
            p = DbPrivilege()
            p.privilegeID = privID
            p.privilegeName = fields[1]
            p.privilegeCreateUser = login
            p.privilegeUpdateUser = login
            p.privilegeCreateDate = DT.now()
            p.privilegeUpdateDate = DT.now()
            p.save()
 
class ProjectStatusLoader:
 
    def __init__(self, params):
        
        
        self.codes = [
        "1,Defined,1,1",
        "2,On hold,2,2",
        "3,Underway,3,3",
        "4,Complete,4,4",
        "5,Canceled,5,5"]
    def load(self):
        for  code in self.codes:
            fields = code.split(",")
            ps = DbProjectStatus()
            ps.projectStatusID = int(fields[0])
            ps.projectStatusDescription = fields[1]
            ps.projectStatusType = int(fields[2])
            ps.save()
    
class RecurrenceTypeLoader:
    
    def __init__(self, params):
         
        self.codes = [
        "1,Daily,1,1",
        "2,Weekly,2,2",
        "3,Date in month,3,3",
        "4,Day of week in month,4,4",
        "5,Yearly,5,5"]
        
    def load(self):
        for code in self.codes:
            fields = code.split(",")
            rt = DbRecurrenceType()
            rt.recurrenceTypeID = int(fields[0])
            rt.recurrenceTypeName = fields[1]
            rt.recurrenceTypeKey = int(fields[2])
            rt.save()
            
class RelationshipTypeLoader:
    def __init__(self, params):
        
         
        self.codes = [
        "1,Together required,1,1",
        "2,Separate required,2,2",
        "3,Together preferred,3,3",
        "4,Separate preferred,4,4"]

    def load(self):
        for code in self.codes:
            fields = code.split(",")
            rt = DbRelationshipType()
            rt.relationshipTypeID = int(fields[0])
            rt.relationshipTypeName = fields[1]
            rt.relationshipTypeKey = int(fields[2])
            rt.save()

class ScheduleStatusLoader:
    def __init__(self, params):
        self.codes = [
            "1,Not set,1,1,F",
            "2,Accepted,2,2,F",
            "3,Rejected,3,3,F"]
    
    def load(self):
        for code in self.codes:
            fields = code.split(",")
            ss = DbScheduleStatus()
            ss.scheduleStatusID = int(fields[0])
            ss.scheduleStatusKey = int(fields[2])
            ss.scheduleStatusName = fields[1]
            ss.save()

class SecurityGroupLoader:
    def __init__(self):
        self.codes = [
            "1,1,Administrators,Persons who are authorized to perform all system functions",
            "2,2,Login Administrators,Privileges required to manage Logins",
            "3,3,Normal Users,Have all privileges except security",
            "4,5,Volunteers,Volunteers",
            "5,4,Project Administrators,Privileges necessary to manage projects"]
    

    def load(self, login, org, loop):
        for code in self.codes:
            fields = code.split(",")
            objID = (int(fields[0]) + loop)
            try:
                sg = DbSecurityGroup.objects.get(pk=objID)
            except :
                sg = DbSecurityGroup()
                sg.securityGroupID = objID
                sg.level = int(fields[1])
                sg.securityGroupName = fields[2]
                sg.securityGroupDescription = fields[3]
                sg.securityGroupCreateUser = login
                sg.securityGroupUpdateUser = login
                sg.organization = org
                sg.save()
                for li in DbLogin.objects.all():
                    li.securityGroups.add(sg)
                    li.save() 
 
class SecurityGroupPrivilegeLoader:

    def __init__(self):
        self.codes = [
            "1,1,1,CURRENT_TIMESTAMP, CURRENT_TIMESTAMP,1,1",
            "2,1,1,CURRENT_TIMESTAMP, CURRENT_TIMESTAMP,2,1",
            "3,1,1,CURRENT_TIMESTAMP, CURRENT_TIMESTAMP,3,1",
            "5,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,4,1",
            "6,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,5,1",
            "7,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,6,1",
            "8,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,7,1",
            "9,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,8,1",
            "10,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,9,1",
            "11,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,10,1",
            "12,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,11,1",
            "13,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,12,1",
            "15,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,13,1",
            "16,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,14,1",
            "17,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,15,1",
            "18,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,16,1",
            "14,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,17,1",
            "19,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,18,1",
            "20,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,19,1",
            "21,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,20,1",
            "22,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,21,1",
            "23,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,23,1",
            "24,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,24,1",
            "25,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,25,1",
            "27,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,26,1",
            "28,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,27,1",
            "30,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,28,1",
            "31,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,29,1",
            "33,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,30,1",
            "32,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,31,1",
            "34,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,32,1",
            "35,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,33,1",
            "36,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,34,1",
            "37,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,35,1",
            "38,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,36,1",
            "39,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,37,1",
            "40,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,38,1",
            "41,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,39,1",
            "42,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,40,1",
            "43,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,41,1",
            "44,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,42,1",
            "45,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,43,1",
            "46,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,44,1",
            "47,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,45,1",
            "48,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,46,1",
            "49,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,47,1",
            "50,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,48,1",
            "51,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,49,1",
            "54,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,50,1",
            "57,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,51,1",
            "58,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,52,1",
            "59,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,53,1",
            "60,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,54,1",
            "61,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,55,1",
            "62,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,56,1",
            "63,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,57,1",
            "64,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,58,1",
            "67,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,59,1",
            "68,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,60,1",
            "71,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,61,1",
            "72,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,62,1",
            "73,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,63,1",
            "74,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,64,1",
            "75,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,65,1",
            "76,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,66,1",
            "77,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,67,1",
            "78,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,68,1",
            "79,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,69,1",
            "80,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,70,1",
            "81,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,71,1",
            "82,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,72,1",
            "85,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,73,1",
            "86,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,74,1",
            "87,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,75,1",
            "88,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,76,1",
            "90,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,77,1",
            "91,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,78,1",
            "92,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,79,1",
            "93,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,80,1",
            "94,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,81,1",
            "96,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,82,1",
            "97,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,83,1",
            "98,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,83,1",
            "99,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,84,1",
            "100,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,85,1",
            "101,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,86,1",
            "102,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,87,1",
            "103,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,88,1",
            "104,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,89,1",
            "105,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,90,1",
            "106,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,91,1",
            "107,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,92,1",
            "108,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,93,1",
            "109,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,94,1",
            "110,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,95,1",
            "111,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,96,1",
            "112,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,97,1",
            "113,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,98,1",
            "114,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,99,1",
            "115,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,100,1",
            "116,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,101,1",
            "117,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,102,1",
            "118,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,103,1",
            "119,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,104,1",
            "120,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,105,1",
            "121,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,106,1",
            "122,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,107,1",
            "123,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,108,1",
            "124,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,109,1",
            "125,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,110,1",
            "126,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,111,1",
            "127,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,112,1",
            "128,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,113,1",
            "129,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,114,1",
            "130,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,115,1",
            "131,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,116,1",
            "132,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,117,1",
            "133,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,118,1",
            "134,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,119,1",
            "135,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,120,1",
            "136,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,121,1",
            "137,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,122,1",
            "138,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,123,1",
            "139,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,1,6",
            "140,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,2,6",
            "141,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,3,6",
            "142,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,4,6",
            "143,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,5,6",
            "144,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,6,6",
            "145,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,7,6",
            "146,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,8,6",
            "147,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,9,6",
            "148,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,10,6",
            "149,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,11,6",
            "150,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,12,6",
            "151,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,13,6",
            "152,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,14,6",
            "153,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,15,6",
            "154,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,16,6",
            "155,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,17,6",
            "156,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,18,6",
            "157,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,19,6",
            "158,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,20,6",
            "159,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,21,6",
            "160,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,22,6",
            "161,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,23,6",
            "162,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,24,6",
            "163,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,25,6",
            "164,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,26,6",
            "165,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,27,6",
            "166,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,28,6",
            "167,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,29,6",
            "168,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,30,6",
            "169,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,31,6",
            "170,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,32,6",
            "171,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,33,6",
            "172,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,34,6",
            "173,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,35,6",
            "174,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,36,6",
            "175,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,37,6",
            "176,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,38,6",
            "177,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,39,6",
            "178,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,40,6",
            "179,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,41,6",
            "180,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,42,6",
            "181,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,43,6",
            "182,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,44,6",
            "183,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,45,6",
            "184,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,46,6",
            "185,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,47,6",
            "186,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,48,6",
            "187,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,49,6",
            "188,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,50,6",
            "189,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,51,6",
            "190,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,52,6",
            "191,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,53,6",
            "192,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,54,6",
            "193,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,55,6",
            "194,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,56,6",
            "195,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,57,6",
            "196,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,58,6",
            "197,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,59,6",
            "198,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,60,6",
            "199,None,None,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,61,6",
            "200,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,62,6",
            "201,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,63,6",
            "202,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,64,6",
            "203,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,65,6",
            "204,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,66,6",
            "205,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,67,6",
            "206,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,68,6",
            "207,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,69,6",
            "208,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,70,6",
            "209,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,71,6",
            "210,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,72,6",
            "211,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,73,6",
            "212,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,74,6",
            "213,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,75,6",
            "214,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,76,6",
            "215,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,77,6",
            "216,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,78,6",
            "217,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,79,6",
            "218,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,80,6",
            "219,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,81,6",
            "220,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,82,6",
            "221,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,83,6",
            "222,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,84,6",
            "223,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,85,6",
            "224,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,86,6",
            "225,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,87,6",
            "226,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,88,6",
            "227,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,89,6",
            "228,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,90,6",
            "229,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,91,6",
            "230,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,92,6",
            "231,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,93,6",
            "232,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,94,6",
            "233,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,95,6",
            "234,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,96,6",
            "235,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,97,6",
            "236,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,98,6",
            "237,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,99,6",
            "238,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,100,6",
            "239,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,101,6",
            "240,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,102,6",
            "241,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,103,6",
            "242,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,104,6",
            "243,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,105,6",
            "244,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,106,6",
            "245,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,107,6",
            "246,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,108,6",
            "247,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,109,6",
            "248,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,110,6",
            "249,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,111,6",
            "250,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,112,6",
            "251,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,113,6",
            "252,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,114,6",
            "253,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,115,6",
            "254,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,116,6",
            "255,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,117,6",
            "256,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,118,6",
            "257,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,119,6",
            "258,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,120,6",
            "259,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,121,6",
            "260,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,122,6",
            "261,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,123,6",
            "262,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,124,1",
            "263,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,124,6",
            "264,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,125,1",
            "265,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,125,6",
            "266,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,126,1",
            "267,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,126,6",
            "268,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,127,1",
            "269,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,127,6",
            "270,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,104,5",
            "271,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,105,5",
            "272,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,106,5",
            "273,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,107,5",
            "274,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,108,5",
            "275,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,109,5",
            "276,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,110,5",
            "277,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,111,5",
            "278,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,112,5",
            "279,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,113,5",
            "280,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,114,5",
            "281,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,115,5",
            "282,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,116,5",
            "283,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,117,5",
            "284,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,118,5",
            "285,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,119,5",
            "286,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,120,5",
            "287,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,121,5",
            "288,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,122,5",
            "289,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,123,5",
            "290,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,124,5",
            "291,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,125,5",
            "292,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,126,5",
            "293,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,127,5",
            "294,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,104,10",
            "295,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,105,10",
            "296,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,106,10",
            "297,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,107,10",
            "298,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,108,10",
            "299,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,109,10",
            "300,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,110,10",
            "301,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,111,10",
            "302,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,112,10",
            "303,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,113,10",
            "304,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,114,10",
            "305,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,115,10",
            "306,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,116,10",
            "307,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,117,10",
            "308,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,118,10",
            "309,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,119,10",
            "310,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,120,10",
            "311,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,121,10",
            "312,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,122,10",
            "313,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,123,10",
            "314,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,124,10",
            "315,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,125,10",
            "316,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,126,10",
            "317,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,127,10",
            "318,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,127,3",
            "319,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,7,4",
            "320,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,7,9",
            "321,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,71,4",
            "322,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,71,9",
            "323,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,114,4",
            "324,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,114,9",
            "326,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,75,4",
            "327,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,75,9",
            "328,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,8,4",
            "329,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,8,9",
            "330,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,72,4",
            "331,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,72,9",
            "332,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,76,4",
            "333,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,76,9",
            "334,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,1,4",
            "335,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,1,9",
            "336,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,9,4",
            "337,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,9,9",
            "338,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,73,4",
            "339,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,73,9",
            "340,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,38,4",
            "341,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,38,9",
            "342,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,77,4",
            "343,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,77,9",
            "344,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,10,4",
            "345,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,10,9",
            "346,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,14,4",
            "347,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,14,9",
            "348,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,74,4",
            "349,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,74,9",
            "350,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,15,4",
            "351,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,15,9",
            "352,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,3,4",
            "353,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,3,9",
            "355,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,86,4",
            "356,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,86,9",
            "357,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,39,4",
            "358,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,39,9",
            "359,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,78,4",
            "360,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,78,9",
            "361,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,1,2",
            "362,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,2,2",
            "363,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,3,2",
            "364,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,4,2",
            "365,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,5,2",
            "366,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,6,2",
            "367,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,7,2",
            "368,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,8,2",
            "369,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,9,2",
            "370,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,10,2",
            "371,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,11,2",
            "372,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,12,2",
            "373,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,13,2",
            "374,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,14,2",
            "375,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,15,2",
            "376,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,16,2",
            "377,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,17,2",
            "378,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,18,2",
            "379,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,19,2",
            "380,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,20,2",
            "381,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,21,2",
            "382,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,22,2",
            "383,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,23,2",
            "384,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,24,2",
            "385,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,25,2",
            "386,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,26,2",
            "387,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,27,2",
            "388,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,28,2",
            "389,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,29,2",
            "390,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,30,2",
            "391,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,31,2",
            "392,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,32,2",
            "393,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,33,2",
            "394,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,34,2",
            "395,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,35,2",
            "396,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,36,2",
            "397,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,37,2",
            "398,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,38,2",
            "399,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,39,2",
            "400,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,40,2",
            "401,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,41,2",
            "402,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,42,2",
            "403,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,43,2",
            "404,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,44,2",
            "405,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,45,2",
            "406,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,46,2",
            "407,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,47,2",
            "408,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,48,2",
            "409,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,49,2",
            "410,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,53,2",
            "411,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,1,7",
            "412,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,2,7",
            "413,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,3,7",
            "414,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,4,7",
            "415,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,5,7",
            "416,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,6,7",
            "417,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,7,7",
            "418,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,8,7",
            "419,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,9,7",
            "420,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,10,7",
            "421,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,11,7",
            "422,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,12,7",
            "423,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,13,7",
            "424,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,14,7",
            "425,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,15,7",
            "426,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,16,7",
            "427,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,17,7",
            "428,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,18,7",
            "429,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,19,7",
            "430,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,20,7",
            "431,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,21,7",
            "432,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,22,7",
            "433,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,23,7",
            "434,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,24,7",
            "435,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,25,7",
            "436,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,26,7",
            "437,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,27,7",
            "438,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,28,7",
            "439,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,29,7",
            "440,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,30,7",
            "441,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,31,7",
            "442,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,32,7",
            "443,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,33,7",
            "444,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,34,7",
            "445,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,35,7",
            "446,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,36,7",
            "447,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,37,7",
            "448,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,38,7",
            "449,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,39,7",
            "450,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,40,7",
            "451,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,41,7",
            "452,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,42,7",
            "453,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,43,7",
            "454,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,44,7",
            "455,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,45,7",
            "456,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,46,7",
            "457,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,47,7",
            "458,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,48,7",
            "459,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,49,7",
            "460,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,53,7",
            "461,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,54,2",
            "462,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,55,2",
            "463,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,56,2",
            "464,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,57,2",
            "465,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,58,2",
            "466,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,59,2",
            "467,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,60,2",
            "468,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,61,2",
            "469,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,62,2",
            "470,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,63,2",
            "471,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,64,2",
            "472,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,65,2",
            "473,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,66,2",
            "474,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,67,2",
            "475,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,68,2",
            "476,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,69,2",
            "477,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,70,2",
            "478,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,71,2",
            "479,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,72,2",
            "480,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,73,2",
            "481,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,74,2",
            "482,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,75,2",
            "483,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,76,2",
            "484,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,77,2",
            "485,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,78,2",
            "486,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,79,2",
            "487,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,80,2",
            "488,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,81,2",
            "489,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,82,2",
            "490,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,83,2",
            "491,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,84,2",
            "492,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,85,2",
            "505,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,86,2",
            "506,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,87,2",
            "507,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,88,2",
            "508,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,89,2",
            "509,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,90,2",
            "510,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,91,2",
            "511,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,92,2",
            "512,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,93,2",
            "513,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,94,2",
            "514,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,95,2",
            "515,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,96,2",
            "516,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,97,2",
            "517,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,98,2",
            "518,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,99,2",
            "520,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,104,2",
            "521,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,105,2",
            "523,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,106,2",
            "524,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,107,2",
            "525,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,108,2",
            "526,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,109,2",
            "527,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,110,2",
            "528,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,111,2",
            "529,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,112,2",
            "530,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,113,2",
            "531,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,114,2",
            "532,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,115,2",
            "533,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,116,2",
            "534,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,117,2",
            "535,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,118,2",
            "536,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,119,2",
            "537,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,120,2",
            "538,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,121,2",
            "539,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,122,2",
            "540,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,123,2",
            "541,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,124,2",
            "542,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,125,2",
            "543,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,126,2",
            "544,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,127,2",
            "545,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,54,7",
            "546,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,55,7",
            "547,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,56,7",
            "548,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,57,7",
            "549,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,58,7",
            "550,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,59,7",
            "551,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,60,7",
            "552,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,61,7",
            "553,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,62,7",
            "554,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,63,7",
            "555,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,64,7",
            "556,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,65,7",
            "557,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,66,7",
            "558,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,67,7",
            "559,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,68,7",
            "560,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,69,7",
            "561,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,70,7",
            "562,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,71,7",
            "563,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,72,7",
            "564,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,73,7",
            "565,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,74,7",
            "566,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,75,7",
            "567,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,76,7",
            "568,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,77,7",
            "569,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,78,7",
            "570,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,79,7",
            "571,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,80,7",
            "572,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,81,7",
            "573,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,82,7",
            "574,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,83,7",
            "575,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,84,7",
            "576,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,85,7",
            "577,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,86,7",
            "578,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,87,7",
            "579,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,88,7",
            "580,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,89,7",
            "581,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,90,7",
            "582,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,91,7",
            "583,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,92,7",
            "584,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,93,7",
            "585,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,94,7",
            "586,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,95,7",
            "587,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,96,7",
            "588,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,97,7",
            "589,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,98,7",
            "590,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,99,7",
            "591,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,104,7",
            "592,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,105,7",
            "593,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,106,7",
            "594,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,107,7",
            "595,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,108,7",
            "596,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,109,7",
            "597,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,110,7",
            "598,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,111,7",
            "599,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,112,7",
            "600,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,113,7",
            "601,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,114,7",
            "602,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,115,7",
            "603,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,116,7",
            "604,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,117,7",
            "605,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,118,7",
            "606,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,119,7",
            "607,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,120,7",
            "608,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,121,7",
            "609,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,122,7",
            "610,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,123,7",
            "611,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,124,7",
            "612,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,125,7",
            "613,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,126,7",
            "614,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,127,7",
            "615,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,1,3",
            "616,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,3,3",
            "617,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,7,3",
            "618,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,9,3",
            "619,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,10,3",
            "620,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,11,3",
            "621,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,12,3",
            "622,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,13,3",
            "623,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,14,3",
            "624,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,15,3",
            "625,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,16,3",
            "626,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,17,3",
            "627,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,18,3",
            "628,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,19,3",
            "629,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,20,3",
            "630,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,21,3",
            "631,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,22,3",
            "632,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,23,3",
            "633,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,24,3",
            "634,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,25,3",
            "635,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,26,3",
            "636,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,27,3",
            "637,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,28,3",
            "638,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,29,3",
            "639,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,30,3",
            "640,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,31,3",
            "641,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,32,3",
            "642,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,33,3",
            "643,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,34,3",
            "644,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,35,3",
            "645,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,36,3",
            "646,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,37,3",
            "647,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,38,3",
            "648,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,39,3",
            "649,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,40,3",
            "650,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,41,3",
            "651,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,42,3",
            "652,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,43,3",
            "653,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,44,3",
            "654,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,45,3",
            "655,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,46,3",
            "656,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,47,3",
            "657,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,48,3",
            "658,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,49,3",
            "659,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,57,3",
            "660,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,58,3",
            "661,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,59,3",
            "662,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,60,3",
            "663,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,61,3",
            "664,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,62,3",
            "665,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,63,3",
            "666,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,64,3",
            "667,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,65,3",
            "668,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,66,3",
            "669,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,67,3",
            "670,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,69,3",
            "671,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,70,3",
            "672,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,71,3",
            "673,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,72,3",
            "674,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,73,3",
            "675,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,74,3",
            "676,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,75,3",
            "677,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,76,3",
            "678,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,77,3",
            "679,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,78,3",
            "680,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,79,3",
            "681,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,80,3",
            "682,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,81,3",
            "683,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,82,3",
            "684,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,83,3",
            "685,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,84,3",
            "686,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,85,3",
            "687,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,86,3",
            "688,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,93,3",
            "689,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,94,3",
            "690,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,95,3",
            "691,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,96,3",
            "692,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,97,3",
            "693,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,98,3",
            "694,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,99,3",
            "695,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,1,8",
            "696,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,3,8",
            "697,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,7,8",
            "698,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,9,8",
            "699,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,10,8",
            "700,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,11,8",
            "701,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,12,8",
            "702,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,13,8",
            "703,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,14,8",
            "704,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,15,8",
            "705,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,16,8",
            "706,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,17,8",
            "707,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,18,8",
            "708,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,19,8",
            "709,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,20,8",
            "710,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,21,8",
            "711,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,22,8",
            "712,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,23,8",
            "713,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,24,8",
            "714,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,25,8",
            "715,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,26,8",
            "716,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,27,8",
            "717,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,28,8",
            "718,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,29,8",
            "719,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,30,8",
            "720,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,31,8",
            "721,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,32,8",
            "722,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,33,8",
            "723,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,34,8",
            "724,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,35,8",
            "725,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,36,8",
            "726,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,37,8",
            "727,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,38,8",
            "728,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,39,8",
            "729,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,40,8",
            "730,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,41,8",
            "731,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,42,8",
            "732,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,43,8",
            "733,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,44,8",
            "734,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,45,8",
            "735,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,46,8",
            "736,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,47,8",
            "737,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,48,8",
            "738,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,49,8",
            "739,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,57,8",
            "740,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,58,8",
            "741,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,59,8",
            "742,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,60,8",
            "743,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,61,8",
            "744,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,62,8",
            "745,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,63,8",
            "746,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,64,8",
            "747,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,65,8",
            "748,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,66,8",
            "749,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,67,8",
            "4,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,68,8",
            "750,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,69,8",
            "751,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,70,8",
            "752,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,71,8",
            "753,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,72,8",
            "754,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,73,8",
            "755,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,74,8",
            "756,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,75,8",
            "757,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,76,8",
            "758,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,77,8",
            "759,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,78,8",
            "760,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,79,8",
            "761,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,80,8",
            "762,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,81,8",
            "763,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,82,8",
            "764,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,83,8",
            "765,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,84,8",
            "766,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,85,8",
            "767,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,86,8",
            "768,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,93,8",
            "769,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,94,8",
            "770,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,95,8",
            "771,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,96,8",
            "772,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,97,8",
            "773,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,98,8",
            "774,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,99,3",
            "775,1,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,68,3"]

    def load(self, login):
        for code in self.codes:
            fields = code.split(",")
            privilegeID = int(fields[5])
            securityGroupID = int(fields[6])
            p = DbPrivilege.objects.get(pk=privilegeID)
            sg = DbSecurityGroup.objects.get(pk=securityGroupID)
            sg.privileges.add(p)
            sg.save()

class SkillRelationshipTypeLoader:
    
    def __init__(self, params):
        self.codes = [
        "1,Together allowed,1,1",
        "2,Separate required,2,2"]
        
    def load(self):
        for code in self.codes:
            fields = code.split(",")
            rt = DbSkillRelationshipType()
            rt.skillRelationshipTypeID = int(fields[0])
            rt.skillRelationshipTypeName = fields[1]
            rt.skillRelationshipTypeKey = int(fields[2])
            rt.save()
        #print(DbSkillRelationshipType.objects.all())

class StateCodeLoader:
    
    def __init__(self, params):
        self.codes = [
            "1,Alabama,AL,1",
            "2,Alaska,AK,2",
            "3,Minnesota,MN,3",
            "4,California,CA,4",
            "5,Not specified,--,5",
            "6,Arkansas,AR,6",
            "7,Washington,WA,7",
            "8,Oregon,OR,8",
            "9,Hawaii,HA,9",
            "10,Arizona,AZ,10",
            "11,Idaho,ID,11",
            "12,Nevada,NV,12",
            "13,Mexico,NM,13",
            "14,Montana,MT,14",
            "15,Wyoming,WY,15",
            "16,Utah,UT,16",
            "17,Colorado,CO,17",
            "18,North Dakota,ND,18",
            "19,South Dakota,SD,19",
            "20,Nebraska,NE,20",
            "21,Kansas,KS,21",
            "22,Oklahoma,OK,22",
            "23,Texas,TX,23",
            "24,Iowa,IA,24",
            "25,Missouri,MO,25",
            "26,Wisconsin,WI,26",
            "27,Illinois,IL,27",
            "28,Tennessee,TN,28",
            "29,Kentucky,KY,29",
            "30,Ohio,OH,30",
            "31,Louisiana,LA,31",
            "32,Mississippi,MS,32",
            "33,Georgia,GA,33",
            "34,Florida,FL,34",
            "35,District of Columbia,DC,35",
            "36,North Carolina,NC,36",
            "37,Virginia,VA,37",
            "38,West Virginia,WV,38",
            "39,Maryland,MD,39",
            "40,Pennsylvania,PA,40",
            "41,Delaware,DE,41",
            "42,Jersey,NJ,42",
            "43,York,NY,43",
            "44,Massachusetts,MA,44",
            "45,Rhode Island,RI,45",
            "46,Connecticut,CT,46",
            "47,Vermont,VT,47",
            "48,Hampshire,NH,48",
            "49,Maine,ME,49",
            "50,Indiana,IN,50",
            "51,South Carolina,SC,51",
            "52,Michigan,MI,52"]

    def load(self):
        for code in self.codes:
            fields = code.split(",")
            sc = DbStateCode()
            sc.sc_name = fields[1]
            sc.sc_code = fields[2]
            sc.sc_ID = int(fields[0])
            sc.save()

class TaskStatusLoader:
    def __init__(self, params):
        self.codes = [
        "1,Not Started,1,1",
        "2,On hold,2,2",
        "3,Assigned,3,3",
        "4,Active,4,4",
        "5,Complete,5,5",
        "6,Canceled,6,6"]
    

    def load(self):
        for code in self.codes:
            fields = code.split(",")
            ts = DbTaskStatus()
            ts.taskStatusID = int(fields[0])
            ts.taskStatusDescription = fields[1]
            ts.taskStatusType = int(fields[2])
            ts.save()
