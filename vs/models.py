from django.db import models

class DbProjectStatus(models.Model):
    projectStatusID = models.AutoField(primary_key=True)
    projectStatusDescription = models.CharField(max_length=255, null=True, blank=True)
    projectStatusType = models.IntegerField()
    deleteFlag = models.BooleanField(default=False)

    def __str__(self):
        return self.projectStatusDescription    

class DbStateCode(models.Model):
    sc_ID = models.AutoField(primary_key=True)
    sc_code = models.CharField(max_length=2, null=True, blank=True)
    sc_name = models.CharField(max_length=255, null=True, blank=True)
    deleteFlag = models.BooleanField(default=False)

    def __str__(self):
        return self.sc_name

class DbRecurrenceType(models.Model):
    recurrenceTypeID = models.AutoField(primary_key=True)
    recurrenceTypeKey = models.IntegerField()
    recurrenceTypeName = models.CharField(max_length=255, null=True, blank=True)
    deleteFlag = models.BooleanField(default=False)

    def __str__(self):
        return self.recurrenceTypeName

class DbAddress(models.Model):
    addressID = models.AutoField(primary_key=True)
    street = models.CharField(max_length=255, null=True, blank=True)
    addressLineTwo = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=2, null=True, blank=True)
    postalCode = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    mobilePhone = models.CharField(max_length=255, null=True, blank=True)
    fax = models.CharField(max_length=255, null=True, blank=True)
    pager = models.CharField(max_length=255, null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    addressCreateUser = models.IntegerField()
    addressUpdateUser = models.IntegerField()
    addressCreateDate = models.DateField(auto_now_add=True)
    addressUpdateDate = models.DateField(auto_now=True)
    deleteFlag = models.BooleanField(default=False)

    def __str__(self):
        s = '\n'
        for att in self.__dict__.values():
            s += str(type(att))
            s += '\n'  
            if isinstance(att,str):
                s += att
            #s += str(att)
        return s#elf.street + ", " + self.city + ,  + self.state    

class DbPrivilege(models.Model):
    privilegeID = models.AutoField(primary_key=True)
    privilegeName = models.CharField(max_length=255,unique=True)
    privilegeCreateDate = models.DateField(auto_now_add=True, null=True)
    privilegeUpdateDate = models.DateField(auto_now=True, null=True)
    privilegeCreateUser = models.IntegerField()
    privilegeUpdateUser = models.IntegerField()
    deleteFlag = models.BooleanField(default=False)

    def __str__(self):
        return str(self.privilegeID) + ' ' + self.privilegeName 


class DbOrganization(models.Model):
    organizationID = models.AutoField(primary_key=True)
    organizationName = models.CharField(max_length=255)
    organizationCreateUser = models.IntegerField()
    organizationUpdateUser = models.IntegerField()
    organizationCreateDate = models.DateField(auto_now_add=True)
    organizationUpdateDate = models.DateField(auto_now=True)
    deleteFlag = models.BooleanField(default=False)
    address = models.OneToOneField(DbAddress,
                                    on_delete=models.SET_NULL, 
                                    null=True, 
                                    blank=True)
    def hasAddress(self):
        result = False
        if self.organizationID and self.address:
            result = True
        return result
            
    def __str__(self):
        return str(self.organizationID) + ' ' + str(self.organizationName)
        
class DbSecurityGroup(models.Model):
    securityGroupID = models.AutoField(primary_key=True)
    level = models.IntegerField()
    securityGroupName = models.CharField(max_length=255)
    securityGroupDescription = models.CharField(max_length=255, null=True, blank=True)
    securityGroupCreateDate = models.DateField(auto_now_add=True)
    securityGroupUpdateDate = models.DateField(auto_now=True)
    securityGroupCreateUser = models.IntegerField()
    securityGroupUpdateUser = models.IntegerField()
    deleteFlag = models.BooleanField(default=False)
    privileges = models.ManyToManyField(DbPrivilege,
                                        related_name='securityGroups')
    organization = models.ForeignKey(DbOrganization, 
                                     on_delete=models.CASCADE,
                                     related_name='securityGroups')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['securityGroupName', 'organization'], 
                                    name='unique_login_securityGroup')
        ]

    def __str__(self):
        return str(self.securityGroupID) + ' ' + self.securityGroupName + ' ' + self.securityGroupDescription  
     
     
class DbLoginStatus(models.Model):
    loginStatusID = models.AutoField(primary_key=True)
    loginStatusType = models.IntegerField()
    loginStatusDescription = models.CharField(max_length=255, null=True, blank=True)
    deleteFlag = models.BooleanField(default=False)

    def __str__(self):
        return self.loginStatusDescription

class DbLogin(models.Model):
    loginID = models.AutoField(primary_key=True)
    login = models.CharField(max_length=255,blank=True,null=True)
    loginName = models.CharField(max_length=255,blank=True,null=True)
    failures = models.IntegerField(default=0)
    lastChange = models.DateField(blank=True,null=True)
    secret = models.CharField(max_length=255,blank=True,null=True)
    loginCreateUser = models.IntegerField()
    loginUpdateUser = models.IntegerField()
    loginCreateDate = models.DateField(auto_now_add=True)
    loginUpdateDate = models.DateField(auto_now=True)
    deleteFlag = models.BooleanField(default=False)
    loginStatus = models.ForeignKey(DbLoginStatus, 
                                    on_delete=models.SET_NULL,
                                     null=True,
                                     blank=True,
                                     related_name='logins')
    organization = models.ForeignKey(DbOrganization, 
                                     on_delete=models.CASCADE,
                                     null=True,
                                     blank=True,
                                     related_name='orgLogins')
    securityGroups = models.ManyToManyField(DbSecurityGroup,
                                            related_name='logins')
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['login', 'organization'], 
                                    name='unique_login')
        ]
        
    def __str__(self):
        return ("Login{" +" loginID=" + str(self.loginID) 
            +", login=" + str(self.login)
            +", loginName=" + str(self.loginName)
            #+", password=" + str(self.passwords.first())
            +", lastChange=" + str(self.lastChange) 
            +", secret=" + str(self.secret)
            +", loginCreateUser=" + str(self.loginCreateUser) 
            +", loginUpdateUser=" + str(self.loginUpdateUser)
            +", loginCreateDate=" + str(self.loginCreateDate)
            +", loginUpdateDate=" + str(self.loginUpdateDate)
            +", failures=" + str(self.failures)
            #+", loginStatus=" + str(self.loginStatus) 
            #+", securityGroups=" + str(self.securityGroups) 
            + '}')
        
class DbAvailability(models.Model):
    availabilityID = models.AutoField(primary_key=True)
    availabilityStartDate = models.DateField(null=True,blank=True)
    availabilityEndDate = models.DateField(null=True,blank=True)
    availabilityCreateDate = models.DateField(auto_now_add=True)
    availabilityUpdateDate = models.DateField(auto_now=True)
    availabilityCreateUser = models.IntegerField()
    availabilityUpdateUser = models.IntegerField()
    deleteFlag = models.BooleanField(default=False)

    def __str__(self):
        return ""

    
class DbHousehold(models.Model):
    householdID = models.AutoField(primary_key=True)
    householdFirstName = models.CharField(max_length=255)
    householdLastName = models.CharField(max_length=255)
    householdCreateUser = models.IntegerField()
    householdUpdateUser = models.IntegerField()
    householdCreateDate = models.DateField(auto_now_add=True)
    householdUpdateDate = models.DateField(auto_now=True)
    deleteFlag = models.BooleanField(default=False)
    address = models.OneToOneField(DbAddress, 
                                   on_delete=models.CASCADE,
                                   null=True,
                                   blank=True)
    organization = models.ForeignKey(DbOrganization, 
                                     on_delete=models.CASCADE,
                                     null=True,
                                     blank=True,
                                     related_name='households')
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['householdFirstName', 'householdLastName', 'organization'], 
                                    name='unique_householdInOrg')
            
        ]
        
    def __str__(self):
        return self.householdFirstName + " " + self.householdLastName

class DbWorkAddress(models.Model):
    workAddressID = models.AutoField(primary_key=True)
    employer = models.CharField(max_length=255, null=True, blank=True)
    jobTitle = models.CharField(max_length=255, null=True, blank=True)
    waCreateUser = models.IntegerField()
    waUpdateUser = models.IntegerField()
    waCreateDate = models.DateField(auto_now_add=True)
    waUpdateDate = models.DateField(auto_now=True)
    deleteFlag = models.BooleanField(default=False)
    address = models.ForeignKey(DbAddress, on_delete=models.CASCADE)

    def __str__(self):
        return '\nworkAddressID: ' + str(self.workAddressID) + ' ' +\
            str(self.jobTitle) + " @ " + str(self.employer) +\
            ' deleteFlag; ' + str(self.deleteFlag)
    
class DbSkillRelationshipType(models.Model):
    skillRelationshipTypeID = models.AutoField(primary_key=True)
    skillRelationshipTypeKey = models.IntegerField()
    skillRelationshipTypeName = models.CharField(max_length=255, null=True, blank=True)
    deleteFlag = models.BooleanField(default=False)

    def __str__(self):
        return self.skillRelationshipTypeName

class DbSkill(models.Model):
    skillID = models.AutoField(primary_key=True)
    skillName = models.CharField(max_length=255)
    skillCreateUser = models.IntegerField()
    skillUpdateUser = models.IntegerField()
    skillCreateDate = models.DateField(auto_now_add=True)
    skillUpdateDate = models.DateField(auto_now=True)
    deleteFlag = models.BooleanField(default=False)
    organization = models.ForeignKey(DbOrganization, 
                                     on_delete=models.CASCADE,
                                     blank=True,
                                     null=True,
                                     related_name='skills')
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['skillName', 'organization'], 
                                            name='unique_skill')
        ]

    def __str__(self):
        return self.skillName

class DbSkillRelationship(models.Model):
    skillRelationshipID = models.AutoField(primary_key=True)
    skillRelationshipCreateUser = models.IntegerField()
    skillRelationshipUpdateUser = models.IntegerField()
    skillRelationshipCreateDate = models.DateField(auto_now_add=True)
    skillRelationshipUpdateDate = models.DateField(auto_now=True)
    skillOne = models.ForeignKey(DbSkill, 
                                 on_delete=models.CASCADE, 
                                 related_name='skillOne')
    skillTwo = models.ForeignKey(DbSkill, 
                                 on_delete=models.CASCADE, 
                                 related_name='skillTwo')
    deleteFlag = models.BooleanField(default=False)
    skillRelationshipType = models.ForeignKey(DbSkillRelationshipType,
                                on_delete=models.CASCADE,
                                blank=True,
                                null=True, 
                                related_name='relationships')

    def __str__(self):
        return "DbSkillRelationship {skillRelationshipID: " + str(self.skillRelationshipID)\
                + ' deleteFlag: ' + str(self.deleteFlag)\
                + ' skillOne: ' + str(self.skillOne)\
                + ' skillTwo: ' + str(self.skillTwo)\
                + '}'

class DbActivity(models.Model):
    activityID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    hoursWorked = models.DecimalField(
                    max_digits=6, 
                    decimal_places=2,
                    blank=True,
                    null=True)
    date = models.DateField(blank=True,
                    null=True)
    activityCreateUser = models.IntegerField()
    activityUpdateUser = models.IntegerField()
    activityCreateDate = models.DateField(auto_now_add=True)
    activityUpdateDate = models.DateField(auto_now_add=True)
    deleteFlag = models.BooleanField(default=False)
    

    def __str__(self):
        return self.name
    
class DbVolunteer(models.Model):
    volunteerID = models.AutoField(primary_key=True)
    volunteerFirstName = models.CharField(max_length=255, null=True, blank=True)
    volunteerLastName = models.CharField(max_length=255, null=True, blank=True)
    volunteerBirthDate = models.DateField(null=True,blank=True)
    cost = models.DecimalField(max_digits=10, 
                               decimal_places=2,
                               null=True,
                               blank=True,
                               default=0.00)
    staff = models.BooleanField(default=False)
    volunteerCreateUser = models.IntegerField()
    volunteerUpdateUser = models.IntegerField()
    volunteerCreateDate = models.DateField(auto_now_add=True)
    volunteerUpdateDate = models.DateField(auto_now=True)
    deleteFlag = models.BooleanField(default=False)
    household = models.ForeignKey(DbHousehold, 
                                  on_delete=models.CASCADE,
                                  blank=True,
                                  null=True)
    address = models.ManyToManyField(DbAddress,
                                     related_name='volunteers',
                                  blank=True,
                                  null=True)
    workAddress = models.ManyToManyField(DbWorkAddress,
                                          related_name='volunteers',
                                          blank=True)
    login = models.OneToOneField(DbAddress, 
                                   on_delete=models.CASCADE,
                                   null=True,
                                   blank=True,
                                   related_name='volunteer')
    organization = models.ForeignKey(DbOrganization, 
                                     on_delete=models.CASCADE,
                                      blank=True,
                                      null=True)
    skills = models.ManyToManyField('DbVolunteerSkill',
                                    related_name='volunteers',
                                  blank=True)
    activities = models.ManyToManyField(DbActivity,
                                        related_name='volunteers',
                                        blank=True) 
    availability = models.OneToOneField(DbAvailability,
                                    on_delete=models.SET_NULL, 
                                    null=True, 
                                    blank=True) 
                      
    address = models.OneToOneField(DbAddress,
                                    on_delete=models.SET_NULL, 
                                    null=True, 
                                    blank=True)                               
    def __str__(self):
        return '\nDbVolunteer{volunteerID: ' + str(self.volunteerID) +\
            ' volunteerFirstName: ' + str(self.volunteerFirstName) +\
            ' volunteerLastName: ' + str(self.volunteerLastName) +\
            ' volunteerCreateUser: ' + str(self.volunteerCreateUser) +\
            ' volunteerUpdateUser: ' + str(self.volunteerUpdateUser) +\
            ' household_id: ' + str(self.household_id) +\
            ' organization_id: ' + str(self.organization_id) +\
            '}'

class DbTeam(models.Model):
    teamID = models.AutoField(primary_key=True)
    teamName = models.CharField(max_length=255)
    teamCreateUser = models.IntegerField()
    teamUpdateUser = models.IntegerField()
    teamCreateDate = models.DateField(auto_now_add=True)
    teamUpdateDate = models.DateField(auto_now=True)
    deleteFlag = models.BooleanField(default=False)
    organization = models.ForeignKey(
                    DbOrganization, 
                    related_name='teams',
                    on_delete=models.CASCADE,
                    blank=True,
                    null=True)
    volunteers = models.ManyToManyField(DbVolunteer,
                    related_name='teams',
                    blank=True)
    activities = models.ManyToManyField(DbActivity,
                    related_name='teams',
                    blank=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['teamName', 'organization'], 
                                            name='unique_teamName')
        ]

    def __str__(self):
        return self.teamName

class DbTaskStatus(models.Model):
    taskStatusID = models.AutoField(primary_key=True)
    taskStatusType = models.IntegerField()
    taskStatusDescription = models.CharField(max_length=255, null=True, blank=True)
    deleteFlag = models.BooleanField(default=False)

    def __str__(self):
        return self.taskStatusDescription

class DbProjectResource(models.Model):
    resourceID = models.AutoField(primary_key=True)
    count = models.IntegerField(default=0)
    cost = models.DecimalField(max_digits=10, decimal_places=2, default = 0.0)
    reusable = models.BooleanField(default=False)
    name = models.CharField(max_length=255, null=True, blank=True)
    resourceCreateUser = models.IntegerField()
    resourceUpdateUser = models.IntegerField()
    resourceCreateDate = models.DateField(auto_now_add=True)
    resourceUpdateDate = models.DateField(auto_now_add=True)
    deleteFlag = models.BooleanField(default=False)
    organization = models.ForeignKey(DbOrganization, 
                                    on_delete=models.CASCADE,
                                    null=True,
                                    blank=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'organization'], 
                                            name='unique_ProjectResource')
        ]

class DbVolunteerSkill(models.Model):
    volunteerSkillID = models.AutoField(primary_key=True)
    vsExpert = models.BooleanField(default=False)
    vsLastAssignment = models.DateField(null=True,blank=True)
    vsPreviousAssignment = models.DateField(null=True,blank=True)
    vsCreateUser = models.IntegerField()
    vsUpdateUser = models.IntegerField()
    vsCreateDate = models.DateField(auto_now_add=True)
    vsUpdateDate = models.DateField(auto_now=True)
    deleteFlag = models.BooleanField(default=False)
    volunteer = models.ForeignKey(
                                DbVolunteer, 
                                on_delete=models.CASCADE,
                                null=True,
                                blank=True)
    skill = models.ForeignKey(
                                DbSkill, 
                                on_delete=models.CASCADE,
                                null=True,
                                blank=True)

    def __str__(self):
        return "volunteerSkillID: " + str(self.volunteerSkillID)\
            + ' volunteerID: ' + str(self.volunteer_id)\
            + ' skillID: ' + str(self.skill_id)\
            + ' expert: ' + str(self.vsExpert)


class DbRelationshipType(models.Model):
    relationshipTypeID = models.AutoField(primary_key=True)
    relationshipTypeKey = models.IntegerField()
    relationshipTypeName = models.CharField(max_length=255, null=True, blank=True)
    deleteFlag = models.BooleanField(default=False)

    def __str__(self):
        return self.relationshipTypeName

class DbJob(models.Model):
    jobID = models.AutoField(primary_key=True)
    expertRequired = models.BooleanField(default=False)
    jobCreateUser = models.IntegerField()
    jobUpdateUser = models.IntegerField()
    jobCreateDate = models.DateField(auto_now_add=True)
    jobUpdateDate = models.DateField(auto_now=True)
    optional = models.BooleanField(default=False)
    deleteFlag = models.BooleanField(default=False)
    jobAssignmentID = models.IntegerField( null=True, blank=True)
    jobEventID = models.IntegerField(null=True, blank=True)
    jobSkillID = models.IntegerField(null=True, blank=True)
    count = models.IntegerField(default=1)
    skill = models.ForeignKey(DbSkill, 
                                     on_delete=models.CASCADE,
                                     null=True,
                                     blank=True,
                                   related_name='jobs')
    event = models.ForeignKey('DbScheduleEvent', 
                                     on_delete=models.CASCADE,
                                     null=True,
                                     blank=True,
                                   related_name='jobs')

    def __str__(self):
        return str(self.jobID) + ' ' + str(self.skill) + ' ' + str(self.event)

class DbProject(models.Model):
    projectID = models.AutoField(primary_key=True)
    projectName = models.CharField(max_length=255, null=True, blank=True)
    projectCreateUser = models.IntegerField()
    projectUpdateUser = models.IntegerField()
    projectStartDate = models.DateField(null=True,blank=True)
    projectFinishDate = models.DateField(null=True,blank=True)
    projectCreateDate = models.DateField(auto_now_add=True)
    projectUpdateDate = models.DateField(auto_now=True)
    deleteFlag = models.BooleanField(default=False)
    organization = models.ForeignKey(DbOrganization, 
                                     on_delete=models.CASCADE,
                                     null=True,
                                     blank=True)
    teams = models.ManyToManyField(DbTeam,
                                   related_name='projects')
    parent = models.ForeignKey(
        'self', 
        null=True, 
        blank=True, 
        on_delete=models.CASCADE, 
        related_name='subprojects'
    )
    #subprojects = models.ManyToManyField(Projectt)
    projectStatus = models.ForeignKey(DbProjectStatus, 
                                      on_delete=models.CASCADE,
                                      blank=True,
                                      null=True)

    def __str__(self):
        return self.projectName
    
class DbTask(models.Model):
    taskID = models.AutoField(primary_key=True)
    taskProjectID = models.IntegerField(
                                   blank=True,
                                   null=True)
    taskSequence = models.IntegerField(
                                   blank=True,
                                   null=True)
    taskName = models.CharField(max_length=255)
    plannedTaskStart = models.DateField(auto_now_add=False,
                                   blank=True,
                                   null=True)
    actualTaskStart = models.DateField(auto_now_add=False,
                                   blank=True,
                                   null=True)
    estimatedTaskEffort = models.IntegerField(
                                   blank=True,
                                   null=True)
    actualTaskEffort = models.IntegerField(
                                   blank=True,
                                   null=True)
    plannedTaskFinish = models.DateField(auto_now_add=False,
                                   blank=True,
                                   null=True)
    actualTaskFinish = models.DateField(auto_now_add=False,
                                   blank=True,
                                   null=True)
    taskCreateUser = models.IntegerField()
    taskUpdateUser = models.IntegerField()
    taskCreateDate = models.DateField(auto_now_add=True)
    taskUpdateDate = models.DateField(auto_now=True)
    deleteFlag = models.BooleanField(default=False)
    organization = models.ForeignKey(DbOrganization,
                              on_delete=models.SET_NULL,
                              null=True,
                              blank=True,
                              related_name='tasks')
    activities = models.ManyToManyField(DbActivity,
                                   blank=True,
                                        related_name='tasks')
    project = models.ForeignKey(DbProject,
                              on_delete=models.SET_NULL,
                              null=True,
                              blank=True,
                              related_name='tasks')
    parent = models.ForeignKey(
        'self', 
        null=True, 
        blank=True, 
        on_delete=models.SET_NULL, 
        related_name='subtasks'
    )
    resources = models.ManyToManyField(DbProjectResource,
                                       blank=True,
                                       related_name='tasks')
    skills = models.ManyToManyField(DbSkill,
                                   blank=True,
                                    related_name='tasks')
    teams = models.ManyToManyField(DbTeam,
                                   blank=True,
                                   related_name='tasks')
    volunteers = models.ManyToManyField(DbVolunteer,
                                   blank=True,
                                        related_name='tasks')
    taskStatus = models.ForeignKey(DbTaskStatus,
                                   null=True,
                                   blank=True,
                                   on_delete=models.SET_NULL)

    def __str__(self):
        if self.taskName:
            return str(self.taskName)
        else:
            return'None'

    
class DbResource(models.Model):
    resourceID = models.AutoField(primary_key=True)
    count = models.IntegerField(default=0)
    name = models.CharField(max_length=255)
    resourceCreateUser = models.IntegerField()
    resourceUpdateUser = models.IntegerField()
    resourceCreateDate = models.DateField(auto_now_add=True)
    resourceUpdateDate = models.DateField(auto_now=True)
    deleteFlag = models.BooleanField(default=False)
    organization = models.ForeignKey(DbOrganization, 
                                      on_delete=models.CASCADE,
                                      blank=True,
                                      null=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['organization', 'name'], 
                name='unique_org_resourcename'
            )
        ]
        
    def __str__(self):
        return self.name + ' : ' + str(self.count)

class DbLocation(models.Model):
    locationID = models.AutoField(primary_key=True)
    locationName = models.CharField(max_length=255, null=True, blank=True)
    locationCreateUser = models.IntegerField()
    locationUpdateUser = models.IntegerField()
    locationCreateDate = models.DateField(auto_now_add=True)
    locationUpdateDate = models.DateField(auto_now=True)
    deleteFlag = models.BooleanField(default=False)
    organization = models.ForeignKey(DbOrganization, 
                                     on_delete=models.CASCADE,
                                     related_name = 'locations')
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['locationName', 'organization'], 
                                            name='unique_locationName')
        ]

    def __str__(self):
        return str(self.locationID) + ' ' + self.locationName + str(self.organization)

class DbEventRecurrence(models.Model):
    recurrenceID = models.AutoField(primary_key=True)
    intervalAmount = models.IntegerField(null=True,blank=True)
    typeID = models.IntegerField(null=True,blank=True)
    endDate = models.DateField(null=True,blank=True)
    startDate = models.DateField(null=True,blank=True)
    recurrenceCreateUser = models.IntegerField()
    recurrenceUpdateUser = models.IntegerField()
    recurrenceCreateDate = models.DateField(auto_now_add=True)
    recurrenceUpdateDate = models.DateField(auto_now=True)
    completelyBuilt = models.BooleanField(default=False)
    deleteFlag = models.BooleanField(default=False)
    recurrenceType = models.ForeignKey(DbRecurrenceType,
                                        on_delete=models.CASCADE,
                                        null=True,
                                        blank=True,
                                        related_name='recurrences')

    def __str__(self):
        return str(self.recurrenceID) + ' start: ' + str(self.startDate)\
            + ' end: ' + str(self.endDate) + ' completely built: ' + str(self.completelyBuilt)

class DbScheduleEvent(models.Model):
    eventID = models.AutoField(primary_key=True)
    eventName = models.CharField(max_length=255)
    eventDate = models.DateField()
    eventStartTime = models.CharField(max_length=8)
    eventDuration = models.IntegerField()
    eventCreateUser = models.IntegerField()
    eventUpdateUser = models.IntegerField()
    eventCreateDate = models.DateField(auto_now_add=True)
    eventUpdateDate = models.DateField(auto_now=True)
    acccepted = models.BooleanField(default=False)
    deleteFlag = models.BooleanField(default=False)
    location = models.ForeignKey(DbLocation,
                                    on_delete=models.CASCADE,
                                    null=True,
                                    blank=True,
                                    related_name='events')
    recurrence = models.ForeignKey(DbEventRecurrence,
                                    on_delete=models.CASCADE,
                                    null=True,
                                    blank=True,
                                    related_name='events')
    organization = models.ForeignKey(
                                    DbOrganization, 
                                    on_delete=models.CASCADE,
                                    null=True,
                                    blank=True,
                                    related_name='events')
    resources = models.ManyToManyField(DbResource,
                                    through='DbEventJoinToResource',
                                    related_name='events')
    schedule = models.ForeignKey(
        "DbSchedule",
            on_delete=models.SET_NULL,
            null=True,
            blank=True,
            related_name='events')

    def __str__(self): 
        return 'DbScheduleEvent {eventID: ' + str(self.eventID) +\
                ' eventName ' + str(self.eventName)
    
class DbEventJoinToResource(models.Model):
    event = models.ForeignKey(DbScheduleEvent, on_delete=models.CASCADE)
    resource = models.ForeignKey(DbResource, on_delete=models.CASCADE)
    count = models.IntegerField(null=True,blank=True)
    createUser = models.IntegerField(default=1)
    updateUser = models.IntegerField(default=1)
    createDate = models.DateField(auto_now_add=True)
    updateDate = models.DateField(auto_now=True)
    deleteFlag = models.BooleanField(default=False)

class DbRelationship(models.Model):
    relationshipID = models.AutoField(primary_key=True)
    relationshipCreateUser = models.IntegerField()
    relationshipUpdateUser = models.IntegerField()
    relationshipCreateDate = models.DateField(auto_now_add=True)
    relationshipUpdateDate = models.DateField(auto_now=True)
    deleteFlag = models.BooleanField(default=False)
    relationshipType = models.ForeignKey(DbRelationshipType,
                                    on_delete=models.CASCADE,
                                    blank=True,
                                    null=True, 
                                    related_name='relationships')
    volunteerOne = models.ForeignKey(DbVolunteer, 
                                     on_delete=models.CASCADE, 
                                     related_name='vol1')
    volunteerTwo = models.ForeignKey(DbVolunteer, 
                                     on_delete=models.CASCADE, 
                                     related_name='vol2')
    organization = models.ForeignKey(
                                    DbOrganization, 
                                    on_delete=models.CASCADE,
                                    null=True,
                                    blank=True,
                                    related_name='rrelationships')

    def __str__(self):
        result = "DbRelationship { relationshipID: " + str(self.relationshipID)
        if self.volunteerOne_id:
            result += ' volunteerOne: ' + str(self.volunteerOne)
        if self.volunteerTwo_id:
            result += ' volunteerTwo: ' + str(self.volunteerTwo) 
        result += '}'
        return result

class DbJobAssignment(models.Model):
    jobAssignmentID = models.AutoField(primary_key=True)
    assignmentDate = models.DateField(auto_now=True)
    previousAssignmentDate = models.DateField(null=True,blank=True)
    accepted = models.BooleanField(default=False)
    jobAssignmentCreateUser = models.IntegerField()
    jobAssignmentUpdateUser = models.IntegerField()
    jobAssignmentCreateDate = models.DateField(auto_now_add=True)
    jobAssignmentUpdateDate = models.DateField(auto_now=True)
    deleteFlag = models.BooleanField(default=False)
    volunteer = models.ForeignKey(
        DbVolunteer, 
        on_delete=models.CASCADE,
        related_name='assignments')
    job = models.ForeignKey(
        DbJob, 
        on_delete=models.CASCADE,
        related_name='assignments')

    def __str__(self):
        return 'DbJobAssignment { jobAssignmentID = ' +  str(self.jobAssignmentID)\
            + ' assignmentDate = ' + str(self.assignmentDate)\
            + ' previousAssignmentDate =  ' + str(self.previousAssignmentDate)\
            + ' accepted = ' + str(self.accepted)\
            + ' jobAssignmentCreateUser = ' + str(self.jobAssignmentCreateUser)\
            + ' jobAssignmentUpdateUser = ' + str(self.jobAssignmentUpdateUser)\
            + ' volunteer_ID = ' + str(self.volunteer_id)\
            + ' job_ID = ' + str(self.job_id)\
            +'}'
    
class DbEventPreference(models.Model):
    preferenceID = models.AutoField(primary_key=True)
    required = models.BooleanField(default=False)
    preferenceCreateUser = models.IntegerField()
    preferenceUpdateUser = models.IntegerField()
    preferenceCreateDate = models.DateField(auto_now_add=True)
    preferenceUpdateDate = models.DateField(auto_now=True)
    deleteFlag = models.BooleanField(default=False)
    volunteer = models.ForeignKey(DbVolunteer, 
                                  on_delete=models.CASCADE,
                                  null=True,
                                  blank=True)
    event = models.ForeignKey(DbScheduleEvent, 
                                  on_delete=models.CASCADE,
                                  null=True,
                                  blank=True)

    def __str__(self):
        return ""

class DbConfigurableProperty(models.Model):
    propertyID = models.AutoField(primary_key=True)
    propertyName = models.CharField(max_length=255)
    propertyType = models.IntegerField()
    propertyValue = models.CharField(max_length=255, null=True, blank=True)
    propertyDescription = models.CharField(max_length=255, null=True, blank=True)
    propertyCreateUser = models.IntegerField()
    propertyUpdateUser = models.IntegerField()
    propertyCreateDate = models.DateField(auto_now_add=True)
    propertyUpdateDate = models.DateField(auto_now=True)
    deleteFlag = models.BooleanField(default=False)

    def __str__(self):
        return self.propertyName or "Unnamed property"

class DbConfigurationSet(models.Model):
    configurationSetID = models.AutoField(primary_key=True)
    configurationSetName = models.CharField(max_length=255, null=True, blank=True)
    configurationSetCreateUser = models.IntegerField()
    configurationSetUpdateUser = models.IntegerField()
    configurationSetCreateDate = models.DateField(auto_now_add=True)
    configurationSetUpdateDate = models.DateField(auto_now=True)
    deleteFlag = models.BooleanField(default=False)
    properties = models.ManyToManyField(DbConfigurableProperty,
                                        related_name='configurationSets')
    organization = models.ForeignKey(DbOrganization, 
                                     on_delete=models.CASCADE, 
                                     null=True, blank=True,
                                     related_name='configurationSets')
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['configurationSetName', 'organization'], 
                                            name='unique_configurationSetName')
        ]

    def __str__(self):
        result = 'DbConfigurationSet (configurationSetID='
        if self.configurationSetID:
            result += str(self.configurationSetID)
        else:
            result += 'None'
            
        result += ', configurationSetName='
        if self.configurationSetName:
            result += str(self.configurationSetName)
        else:
            result += 'None'
            
        result += ', configurationSetCreateUser='
        if self.configurationSetCreateUser:
            result += str(self.configurationSetCreateUser)
        else:
            result += 'None'
        
        result += ', configurationSetUpdateUser='
        if self.configurationSetUpdateUser:
            result += str(self.configurationSetUpdateUser)
        else:
            result += 'None'
        
        result += ', configurationSetCreateDate='
        if self.configurationSetCreateDate:
            result += str(self.configurationSetCreateDate)
        else:
            result += 'None'
        
        result += ', configurationSetUpdateDate='
        if self.configurationSetUpdateDate:
            result += str(self.configurationSetUpdateDate)
        else:
            result += 'None'
        
        result += ', deleteFlag='
        if self.deleteFlag:
            result += str(self.deleteFlag)
        else:
            result += 'False'
        '''
        result += ', properties='
        if self.properties.count() == 0:
            result += 'None'
        else:
            for cp in self.properties.all():
                #print(type(cp))
                result += str(cp)
        '''
        result += ', organization='
        if self.organization:
            result += str(self.organization)
        else:
            result += 'None'
        return result

class DbScheduleStatus(models.Model):
    scheduleStatusID = models.AutoField(primary_key=True)
    scheduleStatusKey = models.IntegerField()
    scheduleStatusName = models.CharField(max_length=255)  
    deleteFlag = models.BooleanField(default=False)

    def __str__(self):
        return self.scheduleStatusName

class DbSchedule(models.Model):
    scheduleID = models.AutoField(primary_key=True)
    scheduleStartDate = models.DateField()
    scheduleEndDate = models.DateField()
    scheduleCreateUser = models.IntegerField()
    scheduleUpdateUser = models.IntegerField()
    scheduleCreateDate = models.DateField(auto_now_add=True)
    scheduleUpdateDate = models.DateField(auto_now=True)
    accepted = models.BooleanField(default=False)
    deleteFlag = models.BooleanField(default=False)
    scheduleStatus = models.ForeignKey(DbScheduleStatus, 
                                     on_delete=models.CASCADE, 
                                     null=True, blank=True,
                                     related_name='schedules')
    organization = models.ForeignKey(DbOrganization, 
                                     on_delete=models.CASCADE, 
                                     null=True, blank=True,
                                     related_name='schedules')
    def __str__(self):
        return 'DbSchedule{scheduleID: ' + str(self.scheduleID) +\
            ' scheduleStartDate: ' + str(self.scheduleStartDate) +\
            ' scheduleEndDate: ' + str(self.scheduleEndDate) +\
            ' status : ' + str(self.scheduleStatus) +\
            ' org: ' + str(self.organization)
    
class DbVolunteerSkillAssignment(models.Model):
    volunteerSkillAssignmentID = models.AutoField(primary_key=True)
    volunteerSkill = models.ForeignKey(DbVolunteerSkill, 
                                       on_delete=models.CASCADE,
                                       null=True,
                                       blank=True,
                                       related_name='assignments')
    event = models.ForeignKey(DbScheduleEvent, 
                              on_delete=models.CASCADE,
                                       null=True,
                                       blank=True,
                              related_name='assignments')
    assignmentDate = models.DateField(auto_now=True)
    vsaCreateUser = models.IntegerField()
    vsaUpdateUser = models.IntegerField()
    vsaCreateDate = models.DateField(auto_now_add=True)
    vsaUpdateDate = models.DateField(auto_now=True)
    deleteFlag = models.BooleanField(default=False)

    def __str__(self):
        return ""
    
class DbReport(models.Model):
    reportID = models.AutoField(primary_key=True)
    reportName = models.CharField(max_length=255,unique=True)
    reportURL = models.CharField(max_length=255)
    reportScheduleID = models.IntegerField(null=True, blank=True)
    reportCreateUser = models.IntegerField()
    reportUpdateUser = models.IntegerField()
    reportCreateDate = models.DateField(auto_now_add=True)
    reportUpdateDate = models.DateField(auto_now=True)
    deleteFlag = models.BooleanField(default=False)
    schedule = models.OneToOneField(DbSchedule, 
                                    on_delete=models.CASCADE,
                                    null=True,
                                    blank=True)

    def __str__(self):
        return self.reportName


class DbPassword(models.Model):
    passwordID = models.AutoField(primary_key=True)
    password = models.CharField(max_length=255)
    passwordCreateDate = models.DateField(auto_now_add=True)
    passwordUpdateDate = models.DateField(auto_now=True)
    passwordCreateUser = models.IntegerField()
    passwordUpdateUser = models.IntegerField()
    deleteFlag = models.BooleanField(default=False)
    login = models.ForeignKey(DbLogin, 
                                on_delete=models.CASCADE,
                                related_name='passwords',
                                blank=True, 
                                null=True)
    def __str__(self):
        return self.password
