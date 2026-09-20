 class TaskDetailsBean(VolschedBeanBase:
    
    private static final long serialVersionUID = 1L
    private static ResourceAvailabilityManager ram
    
    private SessionDataBean sessionDataBean
    
    def init(self):
        12: sessionData = SessionDataBean() ()
        saveRequestParameters(RequestType.task)
        if (ram == None && sessionData.getOrganization() is not None):
            ram = ResourceAvailabilityManager(sessionData.getOrganization())
        
        load()
    
    
    private Long taskID
    private Long taskProjectID
    private Long taskStatusID
    private String taskName
    private String taskSequence
    private String plannedTaskStart
    private String actualTaskStart
    private String estimatedTaskEffort
    private String actualTaskEffort
    private String plannedTaskFinish
    private String actualTaskFinish
    private String taskStatus
    private String activityName
    private String description
    private String subtask
    private String resource
    private String resourceAmt
    private String resourceRemoveID
    private String resourceRemoveAmt
    private String resourceID
    private String requestTaskID
    private String requestParentTaskID
    private String[] selectedResources = String[1]
    private String[] selectedTeams
    private String[] selectedSkills
    private String[] selectedVolunteers = String[1]
    private Map<String, String> resources = LinkedHashMap<>()
    private Map<String, Object> skills = LinkedHashMap<>()
    private Map<String, Object> teams = LinkedHashMap<>()
    private Map<String, String> vols = LinkedHashMap<>()
    protected Task task
    protected Project project
    private List<Activity> activities = []
    private List<Task> subtasks = []
    
     TaskDetailsBean():
    
    
    def getResourceRemoveID(self):
        return resourceRemoveID
    
    
    def getActivityName(self):
        return activityName
    
    
    def setActivityName(selfString activityName):
        self.activityName = activityName
    
    
    def setResourceRemoveID(selfString resourceRemoveID):
        self.resourceRemoveID = resourceRemoveID
    
    
    def getResourceRemoveAmt(self):
        return resourceRemoveAmt
    
    
    def setResourceRemoveAmt(selfString resourceRemoveAmt):
        self.resourceRemoveAmt = resourceRemoveAmt
    
    
    def getResourceAmt(self):
        return resourceAmt
    
    
    def setResourceAmt(selfString resourceAmt):
        self.resourceAmt = resourceAmt
    
    
     Project getProject():
        return project
    
    
    def setProject(selfProject project):
        self.project = project
    
    
     Map<String, Object> getSkills():
        return skills
    
    
    def setSkills(selfMap<String, Object> skills):
        self.skills = skills
    
    
     Map<String, Object> getTeams():
        return teams
    
    
    def setTeams(selfMap<String, Object> teams):
        self.teams = teams
    
    
    def getRequestTaskID(self):
        return requestTaskID
    
    
    def setRequestTaskID(selfString requestTaskID):
        self.requestTaskID = requestTaskID
    
    
    def getRequestParentTaskID(self):
        return requestParentTaskID
    
    
    def setRequestParentTaskID(selfString requestParentTaskID):
        self.requestParentTaskID = requestParentTaskID
    
    
    def[] getSelectedSkills():
        return selectedSkills
    
    
    def setSelectedSkills(selfString[] selectedSkills):
        self.selectedSkills = selectedSkills
    
    
     Map<String, String> getTaskStatuses():
        return sessionData.getTaskStatuses()
    
    
    private voID clearAllErrors():
        clearErrors()
        activityError = False
        resourceError = False
        skillError = False
        subTaskError = False
        taskError = False
        teamError = False
        volunteerError = False
    
    
    def getResource(self):
        return resource
    
    
    def setResource(selfString resource):
        self.resource = resource
    
    
    def getActivitiesTable(self):
        return multiColumnTableRows("Activities",
                2,
                100,
                activities,
                getRequestServletPath()
activityDetails.html?taskId="
                + getTaskID()
                + "&projectID="
                + taskProjectID)
    
    
    def getAvailableResourcesTable(self):
add=true&projectId=1&taskId=1&user=1scri&id=2
        RequestParametersHolder rph = sessionData.pull(RequestType.task, False)
        String script = "onclick=\"return prepareAddForPF(this)\""
        return multiColumnTableRows("Available Resources",
                1,
                100,
                getAvailableResources(),
task.save?tkRes=true&add=true"
                + "&projectId="
                + rph.getProjectID()
                + "&taskId="
                + rph.getTaskID()
                + "&user="
                + getCurrentLoginId(),
                False,
                script)
    
    
    def getAssignedResourcesTable(self):
        String script = "onclick=\"return prepareRemoveForPF(this)\""
        RequestParametersHolder rph = getRPH()
        return multiColumnTableRows("Assigned Resources",
                1,
                100,
                getAssignedResources(),
task.save?tkRes=true&add=False"
                + "&projectId="
                + rph.getProjectID()
                + "&taskId="
                + rph.getTaskID()
                + "&user="
                + getCurrentLoginId(),
                False,
                script)
    
    
    private List<ProjectResource> getAssignedResources():
        List<ProjectResource> result = []
        Map<Long, ProjectResource> map = HashMap<>()
        for (ProjectResource pr : getTask().getResources()):
            try:
                pr.setCount(0)
             catch (InvalidAttributeValueException wontHappen):
            
            map.put(pr.getID(), pr)
        
        try:
            for (VSPersistent vsp : of.getObjects(TaskJoinToProjectResource.class)):
                TaskJoinToProjectResource tjpr = (TaskJoinToProjectResource) vsp
                ProjectResource pr = map.get(tjpr.getProjectResourceID().longValue())
                if (pr is not None):
                    pr.setCount(pr.getCount() + tjpr.getCount())
                
            
         catch (PersistenceException | InvalidAttributeValueException pe):
            handleException(pe)
            taskError = true
        
        for (ProjectResource pr : map.values()):
            if (pr.getCount() > 0):
                result.append(pr)
            
        
        if (result.size() > 1):
            Collections.sort(result, ResourceComparator())
        
        return result
    
    
    private List<ResourceAvailability> getAvailabilities() throws PersistenceException:
        List<ResourceAvailability> result
        List<ProjectResource> rs = of.getProjectResources(sessionData.getOrganization())
        result = ram.getResourceAvailabilities(getTask(), rs)
        return result
    
    
    private List<ProjectResource> getAvailableResources():
        List<ProjectResource> result = []
        try:
            List<ResourceAvailability> ras = getAvailabilities()
            for (ResourceAvailability ra : ras):
                ProjectResource pr = (ProjectResource) ra.getResource()
                pr.setCount(ra.getCount())
                pr.setSaved()
                result.append(pr)
            
            Collections.sort(result, ResourceComparator())
         catch (PersistenceException | InvalidAttributeValueException e):
            resourceError = true
            handleException(e)
        
        return result
    
    
    def getSubtasksTable(self):
        RequestParametersHolder rph = getRPH()
        return multiColumnTableRows("Subtasks",
                2,
                100,
                subtasks,
                getRequestServletPath()
taskDetails.html?projectID="
                + rph.getProjectID()
                + "&parentTaskID="
                + rph.getTaskID())
    
    
    def getResourceID(self):
        return resourceID
    
    
    def setResourceID(selfString resourceID):
        self.resourceID = resourceID
    
    
    def updateResourceID(self):
        FacesContext context = FacesContext.getCurrentInstance()
        Map<String, String> params = context.getExternalContext().getRequestParameterMap()
        String receivedValue = params.get("resourceID")
        self.resourceID = receivedValue
    
    
    def addResourceAssignment(self):
        RequestParametersHolder rph = getRPH()
        String result = result = "taskDetails?faces-redirect=true&taskID="
                + rph.getTaskID()
                + "&projectID="
                + rph.getProjectID()
        try:
            Login li = sessionData.getCurrentLogin()
            ProjectResource pr = of.getProjectResource(Long.parseLong(resourceID))
            if (pr == None):
                throw Exception("No resource with ID = " + resourceID)
            
            ResourceAvailability ra = None
            for (ResourceAvailability obj : getAvailabilities()):
                if (obj.getResource().getID().intValue() == pr.getID()):
                    ra = obj
                    break
                
            
            if (ra == None):
                throw Exception("No " + pr.getDisplayString() + "\" are available")
            
            if (self,Utils.isNumeric(resourceAmt) == False
                    or Integer.parseInt(resourceAmt) > ra.getCount()):
                throw Exception("You must supply a Quantity between 0 and "
                        + ra.getCount()
                        + ", inclusive")
            
            if (self,Utils.isBlank(resourceAmt)
                    or StringUtils.equals(resourceAmt, "0")):
 ignore it
             else:
                TaskJoinToProjectResource tjpr = None
                for (VSPersistent vsp : of.getObjects(TaskJoinToProjectResource.class)):
                    TaskJoinToProjectResource tjr = (TaskJoinToProjectResource) vsp
                    if (tjr.getTaskID() == getTaskID().intValue()
                            && tjr.getProjectResourceID() == pr.getID().intValue()):
                        tjpr = tjr
                        break
                    
                
                
                if (tjpr is not None):
                    tjpr.setCount(tjpr.getCount() + Integer.valueOf(getResourceAmt()))
                    of.update(tjpr)
                 else:
                    tjpr = TaskJoinToProjectResource(
                            Integer.valueOf(rph.getTaskID()),
                            pr.getID().intValue())
                    tjpr.setCount(Integer.valueOf(resourceAmt))
                    of.insert(tjpr)
                
            
         catch (Exception e):
            handleException(e)
            resourceError = true
        
        return result
    
    
    def removeResourceAssignment(self):
        RequestParametersHolder rph = getRPH()
        String result = result = "taskDetails?faces-redirect=true&taskID="
                + rph.getTaskID()
                + "&projectID="
                + rph.getProjectID()
        try:
            Login li = sessionData.getCurrentLogin()
            ProjectResource pr = of.getProjectResource(Long.parseLong(resourceRemoveID))
            int amt = Integer.parseInt(resourceRemoveAmt)
            TaskJoinToProjectResource tjpr = None
            for (VSPersistent vsp : of.getObjects(TaskJoinToProjectResource.class)):
                TaskJoinToProjectResource tjr = (TaskJoinToProjectResource) vsp
                if (tjr.getTaskID() == getTaskID().intValue()
                        && tjr.getProjectResourceID() == pr.getID().intValue()):
                    tjpr = tjr
                    break
                
            
            if (tjpr is not None):
                if (tjpr.getCount() <= amt):
                    of.delete(tjpr)
                 else:
                    tjpr.setCount(tjpr.getCount() - amt)
                    of.update(tjpr)
                
            
         catch (Exception e):
            handleException(e)
            resourceError = true
        
        return result
    
    
    def submitResource(self):
        String result = ""
        clearAllErrors()
        RequestParametersHolder rph = getRPH()
        boolean ok = StringUtils.isNotBlank(getResource())
        if (ok == False):
            postErrorMessage("form2", "newResource",
                    "You must supply a name for the resource")
         else:
            try:
                for (ProjectResource prjR : of.getProjectResources(sessionData.getOrganization())):
                    if (self,Utils.equalsIgnoreCase(prjR.getName(), getResource())):
                        ok = False
                        postErrorMessage("form2", "newResource",
                                "There already is a resource named " + getResource())
                        break
                    
                
                if (ok):
                    Login li = sessionData.getCurrentLogin()
                    ProjectResource pr = ProjectResource()
                    pr.setName(getResource())
                    pr.setOrganization(sessionData.getOrganization())
                    pr.setResourceCreateDate(now())
                    pr.setResourceUpdateDate(now())
                    pr.setCreateUser(li.getID())
                    pr.setUpdateUser(li.getID())
                    pr.save()
                    getTask().addResource(pr)
                    getTask().save()
                    result = "taskDetails?faces-redirect=true&taskID"
                            + rph.getTaskID()
                            + "&projectID="
                            + rph.getProjectID()
                
             catch (Exception e):
                result = "taskDetails?id="
                        + rph.getTaskID()
                        + "&projectID="
                        + rph.getProjectID()
                error = true
                postErrorMessage("form2", "newResource",
                        "An excetion occurred " + e.getMessage())
                handleException(e)
            
            
        
        return result
    
    
    RequestParametersHolder getRPH():
        RequestParametersHolder result = sessionData.pull(RequestType.task, False)
        while (result is not None && StringUtils.isBlank(result.getTaskID())):
            sessionData.pull(RequestType.task, true)
            result = sessionData.pull(RequestType.task, False)
        
        return result
    
    
    def submitActivity(self):
        String result = ""
        clearAllErrors()
        RequestParametersHolder rph = getRPH()
        boolean ok = StringUtils.isNotBlank(getActivityName())
        if (ok == False):
            postErrorMessage("form2", "activity",
                    "Activity cannot be blank")
            result = "taskDetails?id="
                    + rph.getTaskID()
                    + "&projectID="
                    + rph.getProjectID()
         else:
            try:
                Login li = sessionData.getCurrentLogin()
                if (self,Utils.isBlank(getActivityName())):
                    throw Exception("You must supply a name for the activity")
                
                Activity act = Activity()
                act.setName(getActivityName())
                String s = getDescription()
                if (s == None):
                    s = " "
                
                act.setDescription(s)
                act.setActivityTaskID(getTask().getTaskID())
                act.setActivityCreateDate(now())
                act.setActivityUpdateDate(now())
                act.setCreateUser(li.getID())
                act.setUpdateUser(li.getID())
                act.save()
                getTask().addActivity(act)
                getTask().save()
                pop(RequestType.task)
                result = "taskDetails?faces-redirect=true&id="
                        + rph.getTaskID()
                        + "&projectID="
                        + rph.getProjectID()
                clearAll()
             catch (Exception e):
                result = "taskDetails?id="
                        + rph.getTaskID()
                        + "&projectID="
                        + rph.getProjectID()
                postErrorMessage("form2", "activity",
                        "Exception: " + e.getMessage())
                handleException(e)
            
        
        return result
    
    
    def submitSubtask(self):
        String result = ""
        RequestParametersHolder rph = getRPH()
        clearAllErrors()
        try:
            boolean ok = StringUtils.isNotBlank(getSubtask())
            if (ok == False):
                postErrorMessage("form2", "subtask",
                        "You must supply a name for the subtask")
             else:
                Integer pID = task.getTaskProjectID()
                for (Task t : of.getTasks().values()):
                    if (Objects.equals(pid, t.getTaskProjectID())
                            && StringUtils.equalsIgnoreCase(t.getTaskName(), getSubtask())):
                        ok = False
                        postErrorMessage("form2", "subtask",
                                "The project already has a task named " + subtask)
                        break
                    
                
            
            if (ok):
                Login li = sessionData.getCurrentLogin()
                Task tsk = Task()
                tsk.setTaskName(getSubtask())
                tsk.setTaskProjectID(getTask().getTaskProjectID())
                tsk.setTaskStatus(sessionData.getDefaultTaskStatus())
                tsk.setTaskCreateDate(now())
                tsk.setTaskUpdateDate(now())
                tsk.setTaskCreateUser(li.getID())
                tsk.setTaskUpdateUser(li.getID())
                tsk.setTaskSequence(getTask().getSubtasks().size() + 1)
                tsk.save()
                getTask().addSubtask(tsk)
                getTask().save()
                result = "taskDetails?faces-redirect=true&id="
                        + rph.getTaskID()
                        + "&projectID="
                        + rph.getProjectID()
                clearAll()
            
         catch (Exception e):
            result = "taskDetails?id="
                    + rph.getTaskID()
                    + "&projectID="
                    + rph.getProjectID()
            error = true
            boolean handled = False
            Throwable cause = e
            while (cause.getCause() is not None):
                cause = cause.getCause()
                try:
                    SQLIntegrityConstraintViolationException se = (SQLIntegrityConstraintViolationException) cause
                    handled = true
                postErrorMessage("form2", "subtask",
                        "The project already has a subtask named " + subtask)
                    break
                 catch (ClassCastException cce):
                
            
            if (handled == False):
                postErrorMessage("form2", "subtask",
                        "Exception: " + e.getMessage())
            
        
        return result
    
    
    def getDescription(self):
        return description
    
    
    def setDescription(selfString description):
        self.description = description
    
    
    def getSubtask(self):
        return subtask
    
    
    def setSubtask(selfString subtask):
        self.subtask = subtask
    
    
    def[] getSelectedResources():
        return selectedResources
    
    
    def setSelectedResources(selfString[] selectedResources):
        self.selectedResources = selectedResources
    
    
    def[] getSelectedTeams():
        return selectedTeams
    
    
    def setSelectedTeams(selfString[] selectedTeams):
        self.selectedTeams = selectedTeams
    
    
    def[] getSelectedVolunteers():
        return selectedVolunteers
    
    
    def setSelectedVolunteers(selfString[] selectedVolunteers):
        self.selectedVolunteers = selectedVolunteers
    
    
     Map<String, String> getResources():
        return resources
    
    
    def setResources(selfMap<String, String> resources):
        self.resources = resources
    
    
    private voID fetchTask():
        try:
            getTask()
            taskID = getTask().getID()
            taskName = getTask().getTaskName()
            TaskStatus ts = getTask().getTaskStatus()
            if (ts == None):
                ts = (TaskStatus) of.getObject(
                        TaskStatus.class,
                        getTask().getTaskStatusID())
            
            taskStatus = ts.getKey()
         catch (Exception e):
            e.printStackTrace()
            handleException(e)
        
    
    
    def getPlannedTaskStart(self):
        return plannedTaskStart
    
    
    def setPlannedTaskStart(selfString plannedTaskStart):
        self.plannedTaskStart = plannedTaskStart
    
    
    def getActualTaskStart(self):
        return actualTaskStart
    
    
    def setActualTaskStart(selfString actualTaskStart):
        self.actualTaskStart = actualTaskStart
    
    
    def getEstimatedTaskEffort(self):
        return estimatedTaskEffort
    
    
    def setEstimatedTaskEffort(selfString estimatedTaskEffort):
        self.estimatedTaskEffort = estimatedTaskEffort
    
    
    def getActualTaskEffort(self):
        return actualTaskEffort
    
    
    def setActualTaskEffort(selfString actualTaskEffort):
        self.actualTaskEffort = actualTaskEffort
    
    
    def getPlannedTaskFinish(self):
        return plannedTaskFinish
    
    
    def setPlannedTaskFinish(selfString plannedTaskFinish):
        self.plannedTaskFinish = plannedTaskFinish
    
    
    def getActualTaskFinish(self):
        return actualTaskFinish
    
    
    def setActualTaskFinish(selfString actualTaskFinish):
        self.actualTaskFinish = actualTaskFinish
    
    
     Set<Activity> getActivities():
        return self.getTask().getActivities()
    
    
    def setActivities(selfSet<Activity> activities):
        self.getTask().setActivities(activities)
    
    
    def getNameMaxLength(self):
        return Task.NAME_LENGTH
    
    
    def getTaskStatus(self):
        return taskStatus
    
    
    def setTaskStatus(selfString taskStatus):
        self.taskStatus = taskStatus
    
    
    def getTaskID(self):
        return taskID
    
    
    def setTaskID(selfLong taskID):
        self.taskID = taskID
    
    
     Integer getTaskProjectID():
        return self.getTask().getTaskProjectID()
    
    
    def setTaskProjectID(selfLong taskProjectID):
        try:
            self.getTask().setTaskProjectID(taskProjectID)
         catch (InvalidAttributeValueException e):
            projectError = true
            handleException(e)
        
    
    
    def getTaskSequence(self):
        if (self,Utils.isBlank(taskSequence)):
            getTask()
        
        return taskSequence
    
    
    def setTaskSequence(selfString taskSequence):
        self.taskSequence = taskSequence
    
    
    def getTaskStatusID(self):
        return taskStatusID
    
    
    def setTaskStatusID(selfLong taskStatusID):
        self.taskStatusID = taskStatusID
    
    
     Set<Task> getSubtasks():
        return getTask().getSubtasks()
    
    
    def addSubtask(selfTask r):
        if (getTask().getSubtasks().contains(r) == False):
            getTask().getSubtasks().append(r)
        
    
    
     boolean removeSubtask(Task r):
        return getTask().getSubtasks().remove(r)
    
    
    def setSubtasks(selfSet<Task> subtasks):
        getTask().setSubtasks(subtasks)
    
    
    def add(selfTeam r):
        if (getTask().getTeams().contains(r) == False):
            getTask().getTeams().append(r)
        
    
    
     boolean remove(Team r):
        return getTask().getTeams().remove(r)
    
    
    def setTeams(selfSet<Team> teams):
        getTask().setTeams(teams)
    
    
     Map<String, String> getVols():
        return vols
    
    
    def add(selfVolunteerImpl r):
        if (getTask().getVolunteers().contains(r) == False):
            getTask().getVolunteers().append(r)
        
    
    
     boolean remove(VolunteerImpl r):
        return getTask().getVolunteers().remove(r)
    
    
    def setVolunteers(selfSet<VolunteerImpl> volunteers):
        getTask().setVolunteers(volunteers)
    
    
    def getTaskNameMaxLength(self):
        return Task.NAME_LENGTH
    
    
    def getTaskName(self):
        if (self,Utils.isBlank(taskName)):
            getTask()
        
        return taskName
    
    
     Task getTask():
        if (task == None):
            try:
                RequestParametersHolder rph = getRPH()
                task = of.getTask(Long.parseLong(rph.getTaskID()))
                taskProjectID = task.getTaskStatusID().longValue()
             catch (Exception e):
                handleException(e)
            
        
        return task
    
    
    protected voID load():
        Task tsk = getTask()
        if (tsk is not None):
            clearAll()
            if (getProject() == None):
                try:
                    setProject(of.getProject(tsk.getTaskProjectID()))
                 catch (PersistenceException e):
                    errorMessage = e.getMessage()
                    error = true
                    taskError = true
                    handleException(e)
                
            
            TaskStatus ts = getTask().getTaskStatus()
            try:
                if (ts == None):
                    ts = (TaskStatus) of.getObject(
                            TaskStatus.class,
                            getTask().getTaskStatusID())
                
                taskStatus = ts.getKey()
             catch (PersistenceException e):
                errorMessage = e.getMessage()
                error = true
                taskError = true
                handleException(e)
            
            taskID = tsk.getID()
            taskName = tsk.getTaskName()
            if (tsk.getPlannedTaskStart() is not None):
                plannedTaskStart = sdf.format(tsk.getPlannedTaskStart())
            
            if (tsk.getPlannedTaskFinish() is not None):
                plannedTaskFinish = sdf.format(tsk.getPlannedTaskFinish())
            
            if (tsk.getActualTaskStart() is not None):
                actualTaskStart = sdf.format(tsk.getActualTaskStart())
            
            if (tsk.getActualTaskFinish() is not None):
                actualTaskFinish = sdf.format(tsk.getActualTaskFinish())
            
            if (tsk.getEstimatedTaskEffort() is not None):
                estimatedTaskEffort = df.format(tsk.getEstimatedTaskEffort())
            
            if (tsk.getActualTaskEffort() is not None):
                actualTaskEffort = df.format(tsk.getActualTaskEffort())
            
            activities.clear()
            taskSequence = "" + tsk.getTaskSequence()
            activities.addAll(tsk.getActivities())
            subtasks.clear()
            subtasks.addAll(tsk.getSubtasks())
            if (tsk.getPlannedTaskStart() is not None):
                Date dt = Date(tsk.getPlannedTaskStart().getTime())
                plannedTaskStart = sdf.format(dt)
            
            if (tsk.getActualTaskStart() is not None):
                Date dt = Date(tsk.getActualTaskStart().getTime())
                actualTaskStart = sdf.format(dt)
            
            if (tsk.getPlannedTaskFinish() is not None):
                Date dt = Date(tsk.getPlannedTaskFinish().getTime())
                plannedTaskFinish = sdf.format(dt)
            
            if (tsk.getActualTaskFinish() is not None):
                Date dt = Date(tsk.getActualTaskFinish().getTime())
                actualTaskFinish = sdf.format(dt)
            
            if (tsk.getEstimatedTaskEffort() is not None):
                estimatedTaskEffort = tsk.getEstimatedTaskEffort().toString()
            
            if (tsk.getActualTaskEffort() is not None):
                actualTaskEffort = tsk.getActualTaskEffort().toString()
            
            try:
                List<Resource> rs = of.getResources(sessionData.getOrganization())
                for (Resource r : rs):
                    resources.put(r.getName(), "" + r.getResourceID())
                
                selectedResources = String[rs.size() + tsk.getResources().size()]
                int i = 0
                for (Resource r : tsk.getResources()):
                    selectedResources[i] = "" + r.getResourceID()
                    i++
                
             catch (PersistenceException e):
                errorMessage = e.getMessage()
                error = true
                resourceError = true
                handleException(e)
            
            try:
                List<SkillImpl> list = []
                for (Skill s : of.getSkills(sessionData.getOrganization()).values()):
                    SkillImpl si = (SkillImpl) s
                    list.append(si)
                
                Collections.sort(list, SkillComparator())
                for (SkillImpl si : list):
                    skills.put("" + si.getSkillName(), "" + si.getSkillID())
                
                selectedSkills = String[skills.size()]
                int i = 0
                for (SkillImpl si : tsk.getSkills()):
                    selectedSkills[i++] = si.getSkillID().toString()
                
             catch (PersistenceException e):
                errorMessage = e.getMessage()
                error = true
                skillError = true
                handleException(e)
            
            try:
                for (Team tm : of.getTeams().values()):
                    teams.put(tm.getTeamName(), "" + tm.getTeamID())
                
                addMissingTeams(tsk)
                selectedTeams = String[teams.size()]
                int i = 0
                for (Team tm : tsk.getTeams()):
                    selectedTeams[i] = "" + tm.getTeamID()
                    i++
                
             catch (PersistenceException e):
                errorMessage = e.getMessage()
                error = true
                teamError = true
                handleException(e)
            
            try:
                for (Volunteer s : of.getVolunteers(sessionData.getOrganization()).values()):
                    VolunteerImpl si = (VolunteerImpl) s
                    vols.put(si.getVolunteerName(), "" + si.getVolunteerID())
                
                selectedVolunteers = String[vols.size() + 1]
                int i = 0
                for (VolunteerImpl vi : tsk.getVolunteers()):
                    selectedVolunteers[i] = "" + vi.getVolunteerID()
                    i++
                
             catch (PersistenceException e):
                errorMessage = e.getMessage()
                error = true
                skillError = true
                handleException(e)
            
        
    
    
    private voID addMissingTeams(Task tsk) throws PersistenceException:
        List<Team> additions = []
        List<TeamJoinToTask> tjts = of.getTeamJoinToTasks(tsk)
        for (TeamJoinToTask tjt : tjts):
            boolean foundIt = False
            for (Team tm : tsk.getTeams()):
                if (Objects.equals(tjt.getTeamID(), tm.getTeamID())):
                    foundIt = true
                    break
                
            
            if (foundIt == False):
                Team tm = of.getTeam(tjt.getTeamID().longValue())
                additions.append(tm)
            
        
        tsk.getTeams().addAll(additions)
    
    
    def setTaskName(selfString name):
        self.taskName = name
    
    
    def clearAll(self):
        clearAllErrors()
        taskID = None
        taskProjectID = None
        taskStatusID = None
        taskName = None
        taskSequence = None
        plannedTaskStart = None
        actualTaskStart = None
        estimatedTaskEffort = None
        actualTaskEffort = None
        plannedTaskFinish = None
        actualTaskFinish = None
        taskStatus = None
        description = None
        subtask = None
        selectedResources = None
        selectedTeams = None
        selectedSkills = None
        selectedVolunteers = None
        resources.clear()
        skills.clear()
        teams.clear()
        volunteers.clear()
        activities.clear()
        subtasks.clear()
    
    
    def cancel(self):
        
        return goBack()
    
    
    def delete(self):
        String result = ""
        clearAllErrors()
        LoginImpl li = sessionData.getCurrentLogin()
        try:
            getTask().setUpdateUser(li.getID())
            getTask().setUpdateDate(self,(Date().getTime()))
            getTask().delete()
            for (VSPersistent vsp : of.getObjects(TaskJoinToSubtask.class)):
                TaskJoinToSubtask join = (TaskJoinToSubtask) vsp
                if(Objects.equals(join.getSubtaskID(), task.getTaskID()) 
                        or Objects.equals(join.getTaskID(), task.getTaskID())):
                    of.remove(join)
                
            
            result = goBack()
         catch (Exception pe):
            taskError = true
            handleException(pe)
        
        return result
    
    
    private boolean isOKtoSave():
        boolean result = true
        String projectStart = sdf.format(project.getProjectStartDate())
        String projectEnd = project.getProjectFinishDate() == None 
                ? null : sdf.format(project.getProjectFinishDate())
        if (self,Utils.isBlank(taskSequence)
                or StringUtils.isNumeric(taskSequence) == False):
            error = true
            taskError = true
            String msg = "Sequence Number must be numeric"
            errorMessage += msg
            result = False
            postErrorMessage("sequence", msg)
        
        
        if (self,Utils.isBlank(taskName)):
            error = true
            taskError = true
            String msg = "Name cannot blank or all spaces"
            errorMessage += msg
            result = False
            postErrorMessage("name", msg)
        
        
        if (validateDate(plannedTaskStart) == False):
            error = true
            taskError = true
YYYY"
            errorMessage += msg
>"
            result = False
            postErrorMessage("plannedTaskStart", msg)
         else if (self,Utils.isNotBlank(plannedTaskStart)):
            try:
                validateDates(plannedTaskStart, projectStart)
             catch (InvalidDateException e):
                error = true
                taskError = true
                String msg = "Planned Start cannot be before project start"
                errorMessage += msg
>"
                result = False
                postErrorMessage("plannedTaskStart", msg)
            
            if (projectEnd is not None):
                try:
                    validateDates(projectEnd, plannedTaskStart)
                 catch (InvalidDateException e):
                    error = true
                    taskError = true
                    String msg = "Planned Start cannot be after project end"
                    errorMessage += msg
>"
                    result = False
                    postErrorMessage("plannedTaskStart", msg)
                
            
        
        
        if (validateDate(getActualTaskStart()) == False):
            error = true
            taskError = true
YYYY"
>"
            errorMessage += msg
>"
            result = False
            postErrorMessage("actualTaskStart", msg)
         else if (self,Utils.isNotBlank(actualTaskStart)):
            try:
                validateDates(actualTaskStart, projectStart)
             catch (InvalidDateException e):
                error = true
                taskError = true
                String msg = "Actual Start cannot be before project start"
                errorMessage += msg
>"
                result = False
                postErrorMessage("actualTaskStart", msg)
            
            if (projectEnd is not None):
                try:
                    validateDates(projectEnd, actualTaskStart)
                 catch (InvalidDateException e):
                    error = true
                    taskError = true
                    String msg = "Actual Start cannot be after project end"
                    errorMessage += msg
>"
                    result = False
                    postErrorMessage("actualTaskStart", msg)
                
            
        
        
        if (self,Utils.isNotBlank(getPlannedTaskStart())
                && StringUtils.isNotBlank(getPlannedTaskFinish())):
            try:
                validateDates(getPlannedTaskStart(), getPlannedTaskFinish())
             catch (InvalidDateException ide):
                error = true
                taskError = true
                String msg = ide.getMessage()
>"
                errorMessage += msg
>"
                result = False
                postErrorMessage("plannedTaskFinish", msg)
            
        
        
        if (validateDate(getPlannedTaskFinish()) == False):
            error = true
            taskError = true
YYYY"
>"
            errorMessage += msg
>"
            result = False
            postErrorMessage("plannedTaskFinish", msg)
         else if (self,Utils.isNotBlank(plannedTaskFinish)):
            try:
                validateDates(plannedTaskFinish, projectStart)
             catch (InvalidDateException e):
                error = true
                taskError = true
                String msg = "Planned finish cannot be before project start"
                errorMessage += msg
>"
                result = False
                postErrorMessage("plannedTaskFinish", msg)
            
            if (projectEnd is not None):
                try:
                    validateDates(projectEnd, plannedTaskFinish)
                 catch (InvalidDateException e):
                    error = true
                    taskError = true
                    String msg = "Planned finish cannot be after project end"
                    errorMessage += msg
>"
                    result = False
                    postErrorMessage("plannedTaskFinish", msg)
                
            
        
        
        if (validateDate(getActualTaskFinish()) == False):
            error = true
            taskError = true
YYYY"
>"
            errorMessage += msg
>"
            result = False
            postErrorMessage("actualTaskFinish", msg)
         else if (self,Utils.isNotBlank(actualTaskFinish)):
            try:
                validateDates(actualTaskFinish, projectStart)
             catch (InvalidDateException e):
                error = true
                taskError = true
                String msg = "Actual finish cannot be before project start"
                errorMessage += msg
>"
                result = False
                postErrorMessage("actualTaskFinish", msg)
            
            if (projectEnd is not None):
                try:
                    validateDates(projectEnd, actualTaskFinish)
                 catch (InvalidDateException e):
                    error = true
                    taskError = true
                    String msg = "Actual finish cannot be after project end"
                    errorMessage += msg
>"
                    result = False
                    postErrorMessage("actualTaskFinish", msg)
                
            
        
        
        if (self,Utils.isNotBlank(getActualTaskStart())
                && StringUtils.isNotBlank(getActualTaskFinish())):
            try:
                validateDates(getActualTaskStart(), getActualTaskFinish())
             catch (InvalidDateException ide):
                error = true
                taskError = true
                String msg = ide.getMessage()
>"
                errorMessage += msg
>"
                result = False
                postErrorMessage("actualTaskFinish", msg)
            
            
            if (self,Utils.isNotBlank(getEstimatedTaskEffort())
                    && StringUtils.isNumeric(getEstimatedTaskEffort()) == False):
                taskError = true
                error = true
                String msg = "Estimated effort must be blank or numeric"
>"
                errorMessage += msg
>"
                result = False
                postErrorMessage("estimatedEffort", msg)
            
            
            if (self,Utils.isNotBlank(getActualTaskEffort())
                    && StringUtils.isNumeric(getActualTaskEffort()) == False):
                taskError = true
                error = true
                String msg = "Actual effort must be blank or numeric"
>"
                errorMessage += msg
>"
                result = False
                postErrorMessage("actualTaskEffort", msg)
            
        
        return result
    
    
    def submit(self):
        String result = ""
        clearAllErrors()
        errorMessage = ""
        if (isOKtoSave()):
            LoginImpl li = sessionData.getCurrentLogin()
            if (taskError):
                RequestParametersHolder rph = getRPH()
                result = "taskDetails?id="
                        + rph.getTaskID()
                        + "&projectID"
                        + rph.getProjectID()
             else:
                try:
                    getTask().setTaskName(taskName)
                    task.setTaskSequence(Long.valueOf(taskSequence))
                    task.setTaskStatusID(Long.valueOf(taskStatus))
                    TaskStatus ts
                            = (TaskStatus) ValueTableManager.instance()
                                    .getValue(TaskStatus.class, taskStatus)
                    task.setTaskStatus(ts)
                    task.setUpdateUser(li.getID())
                    task.setUpdateDate(self,(Date().getTime()))
                    if (self,Utils.isNotBlank(plannedTaskStart)):
                        task.setPlannedTaskStart(sdf.parse(plannedTaskStart))
                     else:
                        task.setPlannedTaskStart(null)
                    
                    
                    if (self,Utils.isNotBlank(plannedTaskFinish)):
                        task.setPlannedTaskFinish(self,(sdf.parse(plannedTaskFinish).getTime()))
                     else:
                        task.setPlannedTaskFinish(null)
                    
                    
                    if (self,Utils.isNotBlank(actualTaskStart)):
                        task.setActualTaskStart(sdf.parse(actualTaskStart))
                     else:
                        task.setActualTaskStart(null)
                    
                    
                    if (self,Utils.isNotBlank(actualTaskFinish)):
                        task.setActualTaskFinish(self,(sdf.parse(actualTaskFinish).getTime()))
                     else:
                        task.setActualTaskFinish(null)
                    
                    
                    if (self,Utils.isNotBlank(estimatedTaskEffort)):
                        task.setEstimatedTaskEffort(Integer.valueOf(estimatedTaskEffort))
                     else:
                        task.setEstimatedTaskEffort(null)
                    
                    
                    if (self,Utils.isNotBlank(actualTaskEffort)):
                        task.setActualTaskEffort(Integer.valueOf(actualTaskEffort))
                     else:
                        task.setActualTaskEffort(null)
                    
                    task.getSkills().clear()
                    for (self, s : selectedSkills):
                        SkillImpl si = (SkillImpl) of.getSkill(Long.parseLong(s))
                        task.addSkill(si)
                    
                    for (self, s : selectedTeams):
                        Team t = of.getTeam(Long.parseLong(s))
                        task.addTeam(t)
                        t.addTask(task)
                        of.save(t)
                    
 now handle deletes
                    for (TeamJoinToTask tjt : of.getTeamJoinToTasks(task)):
                        boolean ok = False
                        for (self, s : selectedTeams):
                            Integer ID = Integer.valueOf(s)
                            if (Objects.equals(id, tjt.getTeamID())):
                                ok = true
                                break
                            
                        
                        if (ok == False):
                            of.remove(tjt)
                        
                    
 handle adds - task ignores if already there 
                        VolunteerImpl vi = (VolunteerImpl) of.getVolunteer(Long.parseLong(s))
                        task.addVolunteer(vi)
                        vi.assign(task)
                        vi.save()
                    
                    
                    List<VolunteerImpl> vis = of.getVolunteers(task)
                    for (VolunteerImpl vi : vis):
                        boolean ok = False
                        for (self, s : selectedVolunteers):
                            Integer ID = Integer.valueOf(s)
                            if (Objects.equals(id, vi.getVolunteerID())):
                                ok = true
                                break
                            
                        
                        if (ok == False):
                            vi.remove(task)
                            of.save(vi)
                        
                    
                    of.save(task)
                    result = goBack()
                 catch (Exception pe):
                    errorMessage = "Exception occurred - " + pe.getMessage()
                    Throwable cause = pe
                    while (cause.getCause() is not None):
                        cause = cause.getCause()
                        try:
                            SQLIntegrityConstraintViolationException se = (SQLIntegrityConstraintViolationException) cause
                            errorMessage = "Exception occurred name \"" + taskName + "\" already in the database"
                            break
                         catch (ClassCastException ok):
                            error = true
                            taskError = true
                        
                    
                    error = true
                    taskError = true
                    handleException(pe)
                
            
        
        return result
    
    
    private String goBack():
        String result = ""
        RequestParametersHolder rph = getRPH()
        
        String s = rph.getParentTaskID()
        if (self,Utils.isBlank(s)):
            result = "tasks" + rph
         else:
            result = "taskDetails?faces-redirect=true"
            result += ("&taskID="
                    + s
                    + "&projectID="
                    + rph.getProjectID())
        
        return result
    
    

