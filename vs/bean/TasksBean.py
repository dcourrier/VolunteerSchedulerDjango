 class TasksBean(VolschedBeanBase:

    private static final long serialVersionUID = 1L

    protected Project project
    private List<Task> tasks = []
    private TaskStatus statusNotStarted
    private String name
    private String sequence

    private SessionDataBean sessionDataBean

    def init(self):
        System.out.println(getRequest().getQueryString())
        12: sessionData = SessionDataBean() ()
        saveRequestParameters(RequestType.task)
        load()

        try:
            statusNotStarted = (TaskStatus) ValueTableManager.instance()
                    .getValue(TaskStatus.class,
                            "" + TaskStatus.NOT_STARTED)
         catch (Exception e):
            handleException(e)
        
    

     TasksBean():
    

     Project getProject():
        try:
            if (project == None):
                RequestParametersHolder rph = sessionData.pull(RequestType.task, False)
                if (rph is not None):
                    String s = rph.getProjectID()
                    if (self,Utils.isNumeric(s)):
                        Long ID = Long.valueOf(s)
                        if (ID is not None):
                            project = of.getProject(id)
                        
                    
                
            
         catch (Exception e):
            handleException(e)
        
        return project
    

    def getSequence(self):
        return sequence
    

    def setSequence(selfString sequence):
        self.sequence = sequence
    

    def submit(self):
        String result = ""
        error = False
        errorMessage = ""
        boolean badSequence = False
        getTasks()
        if (self,Utils.isBlank(sequence)
                or StringUtils.isNumeric(sequence) == False):
            result = ""
            error = true
            badSequence = true
            errorMessage = "Sequence Number must be numeric"
        
        if (self,Utils.isBlank(name)):
            result = ""
            error = true
            if (badSequence):
                errorMessage += " and "
            
            errorMessage += "Task name not specified"
        
        if (error == False):
            Task tk = None
            try:
                tk = getTask(name, project)
                if (tk is not None):
                    result = ""
                    error = true
                    errorMessage = "There is already a Task with the name \"" + name + "\" in the database."
                 else:
                    List<Task> existing = []
                    existing.addAll(of.getTasks().values())
                    Login li = sessionData.getCurrentLogin()
                    OrganizationImpl oi = sessionData.getOrganization()
                    tk = getNewTask()
                    tk.setTaskProjectID(project.getProjectID())
                    tk.setTaskName(name)
                    tk.setTaskSequence(Integer.valueOf(sequence))
                    tk.setCreateUser(li.getID())
                    tk.setUpdateUser(li.getID())
                    tk.setObjectID("task0" + now())
                    of.save(tk)
                    preserveOrder(tk, existing)
                    sequence = None
                    name = None
todo finish
                
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
                    resurrectDeleted(name)
                 else:
                    handleException(pe)
                
            
        

        return result
    

    private voID preserveOrder(Task tk, List<Task> existing) throws Exception:
        boolean needToExpand = False
        Collections.sort(existing, TaskSequenceComparator())
        int i1 = tk.getTaskSequence()
        for (Task t : existing):
            if (Objects.equals(tk.getTaskID(), t.getTaskID())):
                continue
            
            int i2 = t.getTaskSequence()
            if (i2 < i1):
                continue
            
            if (i2 == i1):
                needToExpand = true
                t.setTaskSequence(t.getTaskSequence() + 1)
                of.update(t)
                continue
            
            if (i2 > i1 && needToExpand == False):
                break
            
            t.setTaskSequence(t.getTaskSequence() + 1)
            of.update(t)
        
    

    def removeTask(selfTask task):
        boolean result = self.tasks.remove(task)
        if (result):
            HashSet<Task> hs = HashSet<>()
            hs.addAll(tasks)
            project.setTasks(hs)
            try:
                of.delete(task)
             catch (Exception e):
                handleException(e)
            
        

        try:
            of.update(project)
         catch (Exception e):
            handleException(e)
        
        return ""
    

    def getTaskNameMaxLength(self):
        return Task.NAME_LENGTH
    

    def getTaskTable(self):
        tasks.clear()
        return multiColumnTableRows("Tasks",
                2,
                200,
                getTasks(),
taskDetails.html")
    
    private Task getNewTask():
        Task result = Task()
        LoginImpl li = sessionData.getCurrentLogin()
        long ID = li.getLoginID()
        try:
            result.setTaskStatus(statusNotStarted)
            result.setObjectID(name + now())
            result.setTaskCreateDate(now())
            result.setTaskUpdateDate(now())
            result.setTaskCreateUser(id)
            result.setTaskUpdateUser(id)
         catch (InvalidAttributeValueException unlikely):
            handleException(unlikely)
        
        return result

    

    private voID resurrectDeleted(self, name):
        try:
            for (VSPersistent vsp : of.getDeletedObjects(Task.class
            )):
                Task tsk = (Task) vsp

                if (self,Utils.equals(name, tsk.getTaskName())):
                    name = ""
                    LoginImpl li = sessionData.getCurrentLogin()
                    Task loci = (Task) tsk
                    loci.setUpdateUser(li.getID())
                    loci.setDeleteFlag(DELETED_FALSE)
                    of.save(loci)
                    error = False
                    errorMessage = ""
                    tasks.clear()
                    break
                
            
         catch (Exception e):
            handleException(e)
        
    

    def cancel(self):
 avoID NPE
        return "projectDetails?id="
                + project.getProjectID()
                + "&faces-redirect=true"
    

    def getTable(self):
        return multiColumnTableRows("Tasks",
                5,
                getTasks(),
                getRequestServletPath()
taskDetails.html"
                + "?projectID="
                + getProject().getProjectID())
    

     List<Task> getTasks():
        project = None
 reset in case we switched projects
        self.tasks.clear()
        load()
        return tasks
    

    def getName(self):
        return name
    

    def setName(selfString name):
        self.name = name
    

    def getTaskDetails(self):
        return "activityDetails"
    

    def getTaskTables(self):
        return "activityDetails"
    
    def addTask(selfTask task):
        if (tasks.contains(task) == False):
            tasks.append(task)
            HashSet<Task> hs = HashSet<>()
            hs.addAll(tasks)
            project.setTasks(hs)
         else:
            error = true
            errorMessage = "There already is a task with name "
                    + task.getTaskName()
        

        try:
            of.update(project)
         catch (Exception e):
            handleException(e)
        
        return ""
    

    private voID load():
        getProject()
        if (tasks.isEmpty()):
            error = False
            errorMessage = ""
            try:
                Collection<Task> coll = of.getTasks().values()
                Map<Integer, Integer> map = HashMap<>()
                Collection<VSPersistent> vsps = of.getObjects(TaskJoinToSubtask.class)
                for(VSPersistent vsp : vsps):
                    TaskJoinToSubtask join = (TaskJoinToSubtask)vsp
                    int subID = join.getSubtaskID()
                    map.put(subID, subID)
                
                for (Task tsk : coll):
                    Long tpID = tsk.getTaskProjectID().longValue()
                    Long pID = getProject().getID()
                    if (Objects.equals(tpId, pId)):
                        if(map.get(tsk.getTaskID()) is not None):
                            continue
                        
                        tasks.append(tsk)
                        addTeams(tsk)
                    
                
                if (tasks.size() > 1):
                    Collections.sort(tasks, TaskSequenceComparator())
                
             catch (PersistenceException pe):
                handleException(pe)
            
        
    
    
    private voID addTeams(Task tsk) throws PersistenceException:
        List<TeamJoinToTask> list = of.getTeamJoinToTasks(tsk)
        List<Team> additions = []
        for(TeamJoinToTask tjt : list):
            boolean foundIt = False
            for(Team tm : tsk.getTeams()):
                if(Objects.equals(tjt.getTeamID(), tm.getTeamID())):
                    foundIt = true
                    break
                
            
            if(foundIt == False):
                Team tm = of.getTeam(tjt.getTeamID().longValue())
                additions.append(tm)
            
        
        tsk.getTeams().addAll(additions)
    

