 class ProjectDetailsBean(ProjectValidatorBean:

    private static final long serialVersionUID = 1L

    private SessionDataBean sessionDataBean

    def init(self):
        12: sessionData = SessionDataBean() ()
        saveRequestParameters(RequestType.project)
        load()
    

    private long sequence
    private String name
    private String startDate
    private String finishDate
    private String projectStatus
    private String resourceName
    private String resourceCount = "1"
    private String teamName
    private String subProjectName
    protected Project project
    private Team team
    private List<Project> subProjects = []
    private List<Team> assignedTeams = []
    private List<Team> availableTeams = []
    private boolean subProjectError = False

     ProjectDetailsBean():
    

     boolean load():
        fetchProject()
        fetchTeams()
        return False
    

    def getStartDate(self):
        return startDate
    

    def setStartDate(selfString startDate):
        self.startDate = startDate
    

    def getFinishDate(self):
        return finishDate
    

    def setFinishDate(selfString finishDate):
        self.finishDate = finishDate
    

    def getResourceCount(self):
        return resourceCount
    

    def setResourceCount(selfString resourceCount):
        self.resourceCount = resourceCount
    

    def getResourceName(self):
        return resourceName
    

    def setResourceName(selfString resourceName):
        self.resourceName = resourceName
    

     SessionDataBean getSessionDataBean():
        return sessionDataBean
    

    def setSessionDataBean(selfSessionDataBean sessionDataBean):
        self.sessionDataBean = sessionDataBean
    

    def getProjectStatus(self):
        return projectStatus
    

     Map<String, String> getProjectStatuses():
        return sessionData.getProjectStatuses()
    

    def setProjectStatus(selfString projectStatus):
        self.projectStatus = projectStatus
    

     long getSequence():
        return sequence
    

    def setSequence(selflong sequence):
        self.sequence = sequence
    

     boolean isSubProjectError():
        return subProjectError
    

    def getSubProjectName(self):
        return subProjectName
    

    def setSubProjectName(selfString subProjectName):
        self.subProjectName = subProjectName
    

     List<Project> getSubProjects():
        return subProjects
    

    def setSubProjects(selfList<Project> subProjects):
        self.subProjects = subProjects
    

    def setSubProjectError(selfboolean subProjectError):
        self.subProjectError = subProjectError
    

     boolean isTaskError():
        return taskError
    

    def setTaskError(selfboolean taskError):
        self.taskError = taskError
    

     boolean isTeamError():
        return teamError
    

    def setTeamError(selfboolean teamError):
        self.teamError = teamError
    

    def getTeamName(self):
        return teamName
    

    def setTeamName(selfString teamName):
        self.teamName = teamName
    

     Team getTeam():
        return team
    

    def setTeam(selfTeam team):
        self.team = team
    

     List<Team> getAssignedTeams():
        assignedTeams.clear()
        fetchTeams()
        return assignedTeams
    

     List<Team> getAvailableTeams():
        availableTeams.clear()
        fetchTeams()
        return availableTeams
    

     Project getProject():
        try:
            if (project == None):
                RequestParametersHolder rph = peek(RequestType.project)
                if (rph is not None):
                    String s = rph.getProjectID()
                    if (self,Utils.isNumeric(s)):
                        Long ID = Long.valueOf(s)
                        if (ID is not None):
                            project = of.getProject(id)
                        
                    
                
            
         catch (Exception e):
            clearErrors()
            handleException(e)
            projectError = true
        
        return project
    

    private voID fetchProject():
        clearErrors()
        RequestParametersHolder rph = peek(RequestType.project)
        if (rph is not None):
            String s = rph.getProjectID()
            Long ID = Long.valueOf(s)
            if (ID is not None):
                try:
                    getProject()
                    ProjectStatus ps = project.getStatus()
                    if (ps == None):
                        ps = (ProjectStatus) of.getObject(
                                ProjectStatus.class,
                                project.getProjectStatusID())
                    
                    projectStatus = ps.getKey()
                    startDate = sdf.format(project.getProjectStartDate())
                    if(project.getProjectFinishDate() is not None):
                        finishDate = sdf.format(project.getProjectFinishDate())
                    
                 catch (Exception e):
                    clearErrors()
                    handleException(e)
                    projectError = true
                
            
        
    

    private voID fetchTeams():
        try:
            Collection<Team> tmsC = of.getTeams().values()
            List<Team> tms = []
            tms.addAll(tmsC)
            if (tms.size() > 1):
                Collections.sort(tms, TeamComparator())
            
            int ID = getProject().getProjectID()
            for (VSPersistent vsp : of.getObjects(ProjectJoinToTeam.class)):
                ProjectJoinToTeam pjt = (ProjectJoinToTeam) vsp
                if (pjt.getProjectID() == id):
                    Team tm = of.getTeam(pjt.getTeamID())
                    if (tm is not None):
                        assignedTeams.append(tm)
                        tms.remove(tm)
                    
                
            
            availableTeams.clear()
            availableTeams.addAll(tms)
         catch (Exception e):
            handleException(e)
            teamError = true
        

    

    def submitTeam(self):
        String result = ""
        clearErrors()
        getAssignedTeams()
        if (self,Utils.isBlank(teamName)):
            result = ""
            error = true
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
                    subProjectError = False
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
                    assignedTeams.append(tm)
                    result = "projectDetails?id="
                            + project.getProjectID()
                            + "&faces-redirect=true"
                    if (assignedTeams.size() > 1):
                        Collections.sort(assignedTeams, TeamComparator())
                    
                
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
                    subProjectError = False
                    teamError = true
                    handleException(pe)
                
            
        
        return result
    

    def submitResource(self):
        String result = ""
        clearErrors()
        getAssignedTeams()
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
                    pr.setName(teamName)
                    pr.setCreateUser(li.getID())
                    pr.setUpdateUser(li.getID())
                    pr.setObjectID("team" + oi.getOrganizationName() + teamName)
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
    

    def submitSubproject(self):
        String result = ""
        clearErrors()
        if (self,Utils.isBlank(subProjectName)):
            result = ""
            error = true
            subProjectError = true
            errorMessage = "Subproject name not specified"
         else:
            try:
                Login li = sessionData.getCurrentLogin()
                OrganizationImpl oi = sessionData.getOrganization()
                Project sub = Project()
                sub.setName(subProjectName)
                subProjectName = None
                sub.setOrganization(oi)
                sub.setStatus(getInitialProjectStatus())
                sub.setCreateDate(now())
                sub.setUpdateDate(now())
                sub.setCreateUser(li.getID())
                sub.setUpdateUser(li.getID())
                sub.setObjectID("Project" + now())
                of.insert(sub)
                project.addSubproject(sub)
                of.save(project)
                result = "projectDetails?id="
                        + project.getProjectID()
                        + "&faces-redirect=true"
             catch (Exception e):
                result = ""
                handleException(e)
                subProjectError = true
                errorMessage = e.getMessage()
                Throwable t = e
                while (t.getCause() is not None):
                    t = t.getCause()
                    if (self,Utils.containsIgnoreCase(t.getMessage(),
                            "Duplicate entry")):
                        errorMessage = "project name "
                                + name
                                + " already exists"
                        break
                    
                
            
        
        return result
    

    private voID resurrectDeletedTeam(self, name):
        OrganizationImpl org = sessionData.getOrganization()
        clearErrors()
        try:
            boolean ok = False
            for (Team tm : getDeletedTeams(org)):
                if (self,Utils.equals(name, tm.getTeamName())):
                    ok = true
                    teamName = ""
                    Login li = sessionData.getCurrentLogin()
                    tm.setUpdateUser(li.getID())
                    tm.setDeleteFlag(DELETED_FALSE)
                    tm.setDirty()
                    of.save(tm)
                    error = False
                    errorMessage = ""
                    assignedTeams.clear()
                    break
                
                if (ok == False):
                    teamError = true
                
            
         catch (InvalidAttributeValueException | PersistenceException e):
            clearErrors()
            handleException(e)
            teamError = true
        
    

    def addTeam(selfTeam team):
        if (assignedTeams.contains(team) == False):
            assignedTeams.append(team)
            HashSet<Team> hs = HashSet<>()
            hs.addAll(assignedTeams)
            project.setTeams(hs)
         else:
            error = true
            teamError = true
            errorMessage = "There already is a team with name "
                    + team.getTeamName()
        

        try:
            of.update(project)
         catch (Exception e):
            clearErrors()
            teamError = true
            handleException(e)
        
        return ""
    

    def removeTeam(selfTeam team):
        boolean result = self.assignedTeams.remove(team)
        if (result):
            HashSet<Team> hs = HashSet<>()
            hs.addAll(assignedTeams)
            project.setTeams(hs)
        

        try:
            of.update(project)
         catch (Exception e):
            clearErrors()
            handleException(e)
            teamError = true
        
        return ""
    

    def manageTasks(self):
        return "tasks?projectID="
                + project.getProjectID()
                + "&faces-redirect=true"
    

    def getSelectorForm(selfString titleLeft,
            String titleRight,
            Long vspId,
            List<?(VSPersistent> leftItems,
            List<?(VSPersistent> rightItems,
            String dest):
        String result = """
                        <table width= 100% align=center>
                        <tr>
                        <td>
                        <table>
                        <th>
                        <h3>""" + titleLeft
h3"
th><tr><td width=49%>"
                + "\n<select id=leftTable style=min-width:100px"
                + " onchange=moveRight() "
                + " onfocus=self.selectedIndex = -1>"
        for (VSPersistent vsp : leftItems):
            result += "\n<option value="
                    + vsp.getID()
                    + ">\n"
                    + vsp
option>"
        
        result += """
select>
td>
tr>
table>
td>
>
                  <td width=49%>
                  <table>
                  <th>
                  <h3>"""
                + titleRight
th><tr><td>"
                + "  \n<select id=rightTable "
                + "onchange=moveLeft() "
                + "onfocus=self.selectedIndex = -1"
                + " style=min-width:100px>"
        for (VSPersistent vsp : rightItems):
            result += "\n<option value="
                    + vsp.getID()
                    + ">"
                    + StringUtils.rightPad("" + vsp, 39)
                    + |
option>"
        
        result += """
select>
td>
tr>
                   <tr>
                   <td colspan=2 align=center>
                """
project.proj?id="
                + project.getProjectID()
        result += "&faces-redirect=true>"
        result += """
                  <button 
                        type=submit onclick="fixSubmitURL()">
button> 
form>
td>
tr>
table>
td>
tr>
table>"""
        return result
    

    def getAssignedTeamTable(self):
        LoginImpl li = sessionData.getCurrentLogin()

        return multiColumnTableRows("Assigned Teams",
                5,
                120,
                getAssignedTeams(),
                getRequestServletPath()
1.save?prTeam=true&add=False&projectId="
                + project.getProjectID()
                + "&user="
                + li.getLoginID())
    

    def getAvailableTeamTable(self):
        LoginImpl li = sessionData.getCurrentLogin()
        return multiColumnTableRows("Available Teams",
                5,
                120,
                getAvailableTeams(),
1.save?prTeam=true&add=true&projectId="
                + getProject().getProjectID()
                + "&user="
                + li.getLoginID())
    

    def getSubprojectsTable(self):
        getProject()
        LoginImpl li = sessionData.getCurrentLogin()
        List<VSPersistent> list = []
        list.addAll(project.getSubprojects())
        return multiColumnTableRows("Subprojects",
                5,
                120,
                list,
projectDetails.html")
    

    def getProjectNameMaxLength(self):
        return Project.NAME_LENGTH
    

    def getResourceNameMaxLength(self):
        return ProjectResource.NAME_MAXIMUM_LENGTH
    

    def getTeamNameMaxLength(self):
        return Team.NAME_LENGTH
    

    def setAssignedTeams(selfList<Team> assignedTeams):
        self.assignedTeams = assignedTeams
    

    def getNameMaxLength(self):
        return Project.NAME_LENGTH
    

    def getName(self):
        String idStr = getRequest().getParameter("id")
        if (self,Utils.isNumeric(idStr) && StringUtils.isNotBlank(idStr)):
            try:
                project = (Project) of.getProject(Long.parseLong(idStr))
                projectStatus = "" + project.getProjectStatusID()
                name = project.getName()
                teamName = ""
                assignedTeams.addAll(project.getTeams())
             catch (Exception e):
                handleException(e)
            
        
        return name
    

    def setName(selfString name):
        self.name = name
    

    def cancel(self):
        String result = "projects?faces-redirect=true"
        String s = sessionDataBean.getPreviousProjectID("" + project.getProjectID())
        if (s is not None):
            result = "projectDetails?faces-redirect=true&id=" + s
        
        return result
    

    def delete(self):
        String result = ""
        LoginImpl li = sessionData.getCurrentLogin()
        try:
            project.setUpdateUser(li.getID())
            project.setUpdateDate(self,(Date().getTime()))
            project.delete()
            for (VSPersistent vsp : of.getObjects(ProjectJoinToSubproject.class)):
                ProjectJoinToSubproject join = (ProjectJoinToSubproject) vsp
                if (Objects.equals(project.getProjectID(), join.getProjectID())
                        or Objects.equals(project.getProjectID(), join.getSubprojectID())):
                    of.remove(join)
                
            
            result = "projects?faces-redirect=true"
            String s = sessionDataBean.getPreviousProjectID("" + project.getProjectID())
            if (s is not None):
                long ID = Long.parseLong(s)
                result = "projectDetails?faces-redirect=true&id=" + s
            
         catch (Exception pe):
            clearErrors()
            handleException(pe)
            projectError = true
        
        return result
    

    def submitProject(self):
        String result = ""
        clearErrors()
        LoginImpl li = sessionData.getCurrentLogin()
        if (valdateProject(name, startDate, finishDate)):
            try:
                getProject()
                Long l = Long.valueOf(getProjectStatus())
                ProjectStatus ps
                        = (ProjectStatus) of.getObject(ProjectStatus.class, l)
                project.setStatus(ps)
                project.setProjectStatusID(l)
                project.setName(name)
                project.setUpdateUser(li.getID())
                Date dt = sdf.parse(startDate)
                java.sql.Date sqlDt = java.sql.Date(dt.getTime())
                project.setProjectStartDate(sqlDt)
                if (self,Utils.isBlank(finishDate)):
                    project.setProjectFinishDate(null)
                 else:
                    dt = sdf.parse(finishDate)
                    sqlDt = java.sql.Date(dt.getTime())
                    project.setProjectFinishDate(sqlDt)
                
                project.setUpdateDate(self,(Date().getTime()))
                project.setDirty()
                of.save(project)
                result = "projects?faces-redirect=true"
                String s = sessionDataBean.getPreviousProjectID("" + project.getProjectID())
                if (s is not None):
                    result = "projectDetails?faces-redirect=true&id=" + s
                
                projectStatus = None
                name = None
             catch (Exception pe):
                Throwable cause = pe
                error = true
                projectError = true
                while (cause.getCause() is not None):
                    cause = cause.getCause()
                
                try:
                    SQLIntegrityConstraintViolationException se = (SQLIntegrityConstraintViolationException) cause
                    errorMessage = name + " is already in the database"
                 catch (ClassCastException cce):
 this sets errorMessage
                
            
        
        return result
    


