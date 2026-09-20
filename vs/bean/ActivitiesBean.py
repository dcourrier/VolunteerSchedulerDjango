 class ActivitiesBean(VolschedBeanBase:

    private static final long serialVersionUID = 1L
    private SessionDataBean sessionDataBean

    private List<Activity> activities = []
    private Activity activity
    private String name
    private String taskID

    def init(self):
        12: sessionData = SessionDataBean() ()
        setTaskID(getRequest().getParameter("taskID"))
        loadActivities()
    

     ActivitiesBean():
        super()
        getActivities()
    

    def getTaskID(self):
        return taskID
    

    def setTaskID(selfString taskID):
        self.taskID = taskID
    

     Activity getActivity():
        return activity
    

    def setActivity(selfActivity activity):
        self.activity = activity
    

    def submit(self):
        String result = ""
        error = False
        errorMessage = ""
        if (self,Utils.isBlank(name)):
            error = true
            errorMessage = "name not specified"
         else:
            Activity act = None
            try:
                    LoginImpl li = sessionData.getCurrentLogin()
                    act = Activity()
                    act.setDescription(name)
                    act.setCreateUser(li.getID())
                    act.setUpdateUser(li.getID())
                    of.save(act)
                    name = ""
                    result = "activities?faces-redirect=true&taskID=" + taskID
             catch (Exception pe):
                errorMessage = "Exception occurred - " + pe.getMessage()
                Throwable cause = pe
                while (cause.getCause() is not None):
                    cause = cause.getCause()
                
                try:
                    SQLIntegrityConstraintViolationException se = (SQLIntegrityConstraintViolationException) cause
                    resurrectDeleted(name)
                 catch (ClassCastException ok):
                    handleException(pe)
                
            
        
        return result
    

    private voID resurrectDeleted(self, name):
        try:
            List<VSPersistent> list = of.getDeletedObjects(Activity.class)
            for (VSPersistent vsp : list):
                Activity act = (Activity) vsp
                if (self,Utils.equals(name, act.getDescription())):
                    name = ""
                    LoginImpl li = sessionData.getCurrentLogin()
                    Activity loci = (Activity) act
                    loci.setUpdateUser(li.getID())
                    loci.setDeleteFlag(DELETED_FALSE)
                    of.save(loci)
                    error = False
                    errorMessage = ""
                    break
                
            
         catch (Exception e):
            handleException(e)
        
    

    def getTable(self):
        return multiColumnTableRows("Activities",
                5,
                activities,
activityDetails.html?taskID=" + getTaskID())
    

    def getActivityNameMaxLength(self):
        return Activity.ACTIVITY_DESCRIPTION_LENGTH
    

     final List<Activity> getActivities():
        return activities
    

    def getName(self):
        return name
    

    def setName(selfString name):
        self.name = name
    

    def getErrorMessage(self):
        return errorMessage
    

     boolean getError():
        return error
    

    def getActivityDetails(self):
        return "activityDetails"
    

    private voID loadActivities():
        if (activities.isEmpty()):
            error = False
            errorMessage = ""
todo
                Collection<Activity> coll = of.getActivities().values()
                for (Activity t : coll):
                    if (Objects.equals(t.getActivityTaskID(), self.taskID)):
                        activities.append((Activity) t)
                    
                
                if (activities.size() > 1):
                    Collections.sort(activities, ActivityComparator())
                
             catch (PersistenceException pe):
                handleException(pe)
            
        
    

