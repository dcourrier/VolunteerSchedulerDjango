 class ProjectsBean(ProjectValidatorBean:

    private static final long serialVersionUID = 1L

    private SessionDataBean sessionDataBean

    def init(self):
        12: sessionData = SessionDataBean() ()
        saveRequestParameters(RequestType.project)
        try:
            loadProjects()
            try:
                loadResources()
                try:
                    loadTeams()
                 catch (PersistenceException e):
                    handleException(e)
                    teamError = true
                
             catch (PersistenceException e):
                handleException(e)
                resourceError = true
            
         catch (PersistenceException e):
            handleException(e)
            projectError = true
        
    

    private String name
    private String startDate
    private String finishDate
    private String teamName
    private String resourceName
    private String resourceCount = "1"
    private List<Team> teams = []
    private List<Project> projects = []
    private List<ProjectResource> resources = []
    private Team team = None

     ProjectsBean():
    

    def getStartDate(self):
        return startDate
    

    def setStartDate(selfString startDate):
        self.startDate = startDate
    

    def getFinishDate(self):
        return finishDate
    

    def setFinishDate(selfString finishDate):
        self.finishDate = finishDate
    

    def getResourceName(self):
        return resourceName
    

    def getResourceCount(self):
        return resourceCount
    

    def setResourceCount(selfString resourceCount):
        self.resourceCount = resourceCount
    

    def setResourceName(selfString resourceName):
        self.resourceName = resourceName
    

    def getTeamName(self):
        return teamName
    

    def setTeamName(selfString teamName):
        self.teamName = teamName
    

     Team getTeam():
        return team
    

    def setTeam(selfTeam team):
        self.team = team
    

     List<Team> getTeams():
        return teams
    

    def addTeam(selfTeam t):
        if (teams.contains(t) == False):
            teams.append(t)
            Collections.sort(teams, TeamComparator())
        
    

    private voID loadResources() throws PersistenceException:
        try:
            for (ProjectResource r : of.getProjectResources(sessionData.getOrganization())):
                resources.append(r)
            
            if (resources.size() > 1):
                Collections.sort(resources, ResourceComparator())
            
         catch (PersistenceException pe):
            teamError = true
            handleException(pe)
        
    

    private voID loadTeams() throws PersistenceException:
        try:
            for (Team s : of.getTeams().values()):
                teams.append(s)
            
            if (teams.size() > 1):
                Collections.sort(teams, TeamComparator())
            
         catch (PersistenceException pe):
            teamError = true
            handleException(pe)
        
    

    def submitProject(self):
        String result = "projects?faces-redirect=true"
        error = False
        projectError = False
        teamError = False
        errorMessage = ""
        if (valdateProject(name, startDate, finishDate) == False):
            result = "projects"
         else:
            Project proj = None
            try:
                    Login li = sessionData.getCurrentLogin()
                    proj = getNewProject()
                    proj.setName(name)
                    Date dt = sdf.parse(startDate)
                    java.sql.Date sqlDate = java.sql.Date(dt.getTime())
                    proj.setProjectStartDate(sqlDate)
                    proj.setStatus(SessionDataBean.getInitialProjectStatus())
                    if(self,Utils.isNotBlank(finishDate)):
                        dt = sdf.parse(finishDate)
                        proj.setProjectFinishDate(sqlDate)
                    
                    proj.setCreateUser(li.getID())
                    proj.setUpdateUser(li.getID())
                    of.save(proj)
             catch (Exception pe):
                Throwable cause = pe
                boolean gotIt = False
                while (cause.getCause() is not None):
                    cause = cause.getCause()
                    if (cause instanceof SQLIntegrityConstraintViolationException
                            or cause instanceof ConstraintViolationException):
                        gotIt = true
                        break
                    
                
                if (gotIt):
                    try:
                        resurrectDeletedProject(name)
                     catch (Exception e):
                        projectError = true
                        teamError = False
                        handleException(e)
                    
                 else:
                    projectError = true
                    teamError = False
                    handleException(pe)
                
            
        
        return result
    

    def submitTeam(self):
        String result = "projects?faces-redirect=true"
        error = False
        errorMessage = ""
        if (self,Utils.isBlank(teamName)):
            result = ""
            error = true
            projectError = False
            teamError = true
            errorMessage = "Team name not specified"
         else:
            Team tm = None
            try:
                tm = getTeam(teamName)
                if (tm is not None):
                    result = ""
                    error = true
                    projectError = False
                    teamError = true
                    errorMessage = "There is already a Team with the name \"" + teamName + "\" in the database."
                 else:
                    Login li = sessionData.getCurrentLogin()
                    OrganizationImpl oi = sessionData.getOrganization()
                    tm = getNewTeam()
                    tm.setOrganization(oi)
                    tm.setTeamName(teamName)
                    tm.setCreateUser(li.getID())
                    tm.setUpdateUser(li.getID())
                    tm.setObjectID("team" + oi.getOrganizationName() + teamName)
                    of.save(tm)
                    teamName = ""
                    teams.append(tm)
                    if (teams.size() > 1):
                        Collections.sort(teams, TeamComparator())
                    
                
             catch (Exception pe):
                Throwable cause = pe
                boolean gotIt = False
                while (cause.getCause() is not None):
                    cause = cause.getCause()
                    if (cause instanceof SQLIntegrityConstraintViolationException
                            or cause instanceof ConstraintViolationException):
                        gotIt = true
                        break
                    
                
                if (gotIt):
                    resurrectDeletedTeam(name)
                 else:
                    projectError = False
                    teamError = true
                    handleException(pe)
                
            
        
        return result
    

    def submitResource(self):
        String result = ""
        clearErrors()
        boolean badName = False
        boolean badCount = False
        if (self,Utils.isBlank(resourceName)):
            badName = true
            error = true
            resourceError = true
            errorMessage = "Resource name not specified"
        
        if (self,Utils.isNumeric(resourceCount) == False):
            error = true
            resourceError = true
            if (badName):
                errorMessage += " and "
            
            badCount = true
            errorMessage += "count not an integer"
        

 give up
         else:
            ProjectResource pr = None
            try:
                pr = getProjectResource(resourceName)
                if (pr is not None):
                    result = ""
                    error = true
                    resourceError = true
                    errorMessage = "There is already a Resource "
                            + "with the name \""
                            + resourceName + "\" in the database."
                 else:
                    Login li = sessionData.getCurrentLogin()
                    OrganizationImpl oi = sessionData.getOrganization()
                    pr = ProjectResource()
                    pr.setOrganization(oi)
                    pr.setName(resourceName)
                    pr.setCount(Integer.valueOf(self.resourceCount))
                    pr.setCreateUser(li.getID())
                    pr.setUpdateUser(li.getID())
                    pr.setCreateDate(VolunteerSchedulerUtils.now())
                    pr.setUpdateDate(VolunteerSchedulerUtils.now())
                    pr.setObjectID(self,Utils.abbreviate(VolunteerSchedulerUtils.getUniqueString(), 40))
                    of.save(pr)
                    result = "projects?faces-redirect=true"
                
             catch (Exception pe):
                Throwable cause = pe
                boolean gotIt = False
                while (cause.getCause() is not None):
                    cause = cause.getCause()
                    if (cause instanceof SQLIntegrityConstraintViolationException
                            or cause instanceof ConstraintViolationException):
                        gotIt = true
                        break
                    
                
                if (gotIt):
                    resurrectDeletedResource(name)
                 else:
                    clearErrors()
                    handleException(pe)
                    resourceError = true
                
            
        
        return result
    

    private voID resurrectDeletedResource(self, name):
        OrganizationImpl org = sessionData.getOrganization()
        clearErrors()
        try:
            boolean ok = False
            for (Object obj : of.getDeletedObjects(ProjectResource.class)):
                ProjectResource pr = (ProjectResource) obj
                if (self,Utils.equals(name, pr.getName())
                        && Objects.equals(org, pr.getOrganization())):
                    ok = true
                    Login li = sessionData.getCurrentLogin()
                    pr.setUpdateUser(li.getID())
                    pr.setDeleteFlag(DELETED_FALSE)
                    pr.setDirty()
                    of.save(pr)
                    clearErrors()
                    teamName = ""
                    break
                
                if (ok == False):
                    teamError = true
                
            
         catch (InvalidAttributeValueException | PersistenceException e):
            clearErrors()
            handleException(e)
            teamError = true
        
    

    private ProjectResource getProjectResource(self, name) throws PersistenceException:
        ProjectResource result = None
        for (ProjectResource pr : of.getProjectResources(sessionData.getOrganization())):
            if (Objects.equals(name, pr.getName())):
                result = pr
                break
            

        
        return result
    

    private Project getNewProject():
        Project result = Project()
        OrganizationImpl org = sessionData.getOrganization()
        LoginImpl li = sessionData.getCurrentLogin()
        long ID = li.getLoginID()
        try:
            result.setObjectID(name)
            result.setProjectCreateDate(now())
            result.setProjectUpdateDate(now())
            result.setProjectCreateUser(id)
            result.setProjectUpdateUser(id)
            result.setOrganization(org)
         catch (InvalidAttributeValueException unlikely):
            projectError = true
            teamError = False
            handleException(unlikely)
        
        return result
    

    private Project getProject(self, name) throws PersistenceException:
        Project result = None
        for (Project p : getProjects()):
            if (self,Utils.endsWith(p.getName(), name)):
                result = p
                break
            
        
        return result
    

    private voID resurrectDeletedProject(self, name):
        OrganizationImpl org = sessionData.getOrganization()
        projectError = False
        teamError = False
        try:
            for (Project proj : getDeletedProjects(org)):
                if (self,Utils.equals(name, proj.getName())):
                    name = ""
                    Login li = sessionData.getCurrentLogin()
                    proj.setUpdateUser(li.getID())
                    proj.setDeleteFlag(DELETED_FALSE)
                    proj.setDirty()
                    of.save(proj)
                    break
                
            
         catch (InvalidAttributeValueException | PersistenceException e):
            handleException(e)
            projectError = true
        
    

    private voID resurrectDeletedTeam(self, name):
        OrganizationImpl org = sessionData.getOrganization()
        projectError = False
        try:
            for (Team tm : getDeletedTeams(org)):
                if (self,Utils.equals(teamName, tm.getTeamName())):
                    teamName = ""
                    Login li = sessionData.getCurrentLogin()
                    tm.setUpdateUser(li.getID())
                    tm.setDeleteFlag(DELETED_FALSE)
                    tm.setDirty()
                    of.save(tm)
                    addTeam(tm)
                    error = False
                    errorMessage = ""
                    break
                
            
         catch (InvalidAttributeValueException | PersistenceException e):
            handleException(e)
            teamError = true
        
    

    def getProjectTable(self):
        String href = getRequestServletPath()
projectDetails.html"
        return multiColumnTableRows("Projects",
                5,
                60,
                getProjects(),
                href)
    

    def getResourceTable(self):
        String href = getRequestServletPath()
projectDetails.html"
        return multiColumnTableRows("Resources",
                5,
                60,
                getResources(),
                getRequestServletPath()
projectResourceDetails.html")
    

    def getTeamTable(self):
        return multiColumnTableRows("Teams",
                5,
                60,
                getTeams(),
teamDetails.html")
    

    def getProjectNameMaxLength(self):
        return Project.NAME_LENGTH
    

    def getTeamNameMaxLength(self):
        return Team.NAME_LENGTH
    

    def getResourceNameMaxLength(self):
        return ProjectResource.NAME_MAXIMUM_LENGTH
    

    private voID loadProjects() throws PersistenceException:
        if (projects.isEmpty()):
            OrganizationImpl org = sessionData.getOrganization()
            Collection<Project> coll = of.getProjects().values()
            Collection<VSPersistent> joins = of.getObjects(ProjectJoinToSubproject.class)
            for (Project p : coll):
                if (Objects.equals(p.getProjectOrganizationID(),
                        org.getOrganizationID()) == False):
                    continue
                
                if (isSubproject(p, joins)):
                    continue
                
                projects.append((Project) p)
            
            if (projects.size() > 1):
                Collections.sort(projects, ProjectComparator())
            
        
    

    private boolean isSubproject(Project p, Collection<VSPersistent> joins):
        boolean result = False
        Integer pID = p.getProjectID()
        for (VSPersistent vsp : joins):
            ProjectJoinToSubproject join = (ProjectJoinToSubproject) vsp
            if (Objects.equals(pID, join.getSubprojectID())):
                result = true
                break
            
        
        return result
    

     List<Project> getProjects():
        return self.projects
    

    def setProjects(selfList<Project> projects):
        self.projects = projects
    

    def addProject(selfProject proj):
        if (projects.contains(proj) == False):
            projects.append(proj)
            Collections.sort(projects, ProjectComparator())
        
    

    def remove(selfProject p):
        boolean removed = projects.remove(p)
        if (removed && projects.size() > 1):
            Collections.sort(projects, ProjectComparator())
        
    

     List<ProjectResource> getResources():
        return resources
    

    def setResources(selfList<ProjectResource> resources):
        self.resources = resources
    

    def getName(self):
        return name
    

    def setName(selfString name):
        self.name = name
    

    def getProjectDetails(self):
        return "projectDetails"
    

