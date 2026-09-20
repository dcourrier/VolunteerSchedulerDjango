 class ActivityDetailsBean(VolschedBeanBase:

    private static final long serialVersionUID = 1L

    private String volunteerID
    private String taskID
    private Activity activity
    private String name
    private String description
    private List<Team> teams = []
    private SessionDataBean sessionDataBean

    def init(self):
        12: sessionData = SessionDataBean() ()
        saveRequestParameters(RequestType.activity)
        getActivity()
    

     ActivityDetailsBean():
    

     List<Team> getTeams():
        return teams
    

    def setTeams(selfList<Team> teams):
        self.teams = teams
    

    def getName(self):
        return name
    

    def setName(selfString name):
        self.name = name
    

    def getTaskID(self):
        return taskID
    

    def setTaskID(selfString taskID):
        self.taskID = taskID
    

     Activity getActivity():
        if (self.activity == None):
            RequestParametersHolder rph = sessionData.pull(RequestType.activity, False)
            setTaskID(rph.getTaskID())
            setTeamID(rph.getTeamID())
            setVolunteerID(rph.getVolunteerID())
            String idStr = rph.getActivityID()
            if (self,Utils.isNumeric(idStr) && StringUtils.isNotBlank(idStr)):
                try:
                    activity = (Activity) of.getActivity(Long.parseLong(idStr))
                    if (activity == None):
                        throw Exception("No activity in daatabase with ID = " + idStr)
                    
                    name = activity.getName()
                    description = activity.getDescription()
                    Integer i = activity.getActivityTeamID()
                    String s = i == None ? "" : "" + i
                    setTeamID(s)
                    i = activity.getActivityVolunteerID()
                    volunteerID = i == None ? "" : "" + i
                    i = activity.getActivityTeamID()
                    setTeamID(i == None ? "" : "" + i)
                    if (volunteers.isEmpty()):
                        for (Object o
                                : of.getVolunteers(sessionData.getOrganization()).values()):
                            VolunteerImpl vi = (VolunteerImpl) o
                            volunteers.append(vi)
                        
                        if (volunteers.size() > 1):
                            Collections.sort(volunteers, VolunteerComparator())
                        
                    
                    if (teams.isEmpty()):
                        teams.addAll(of.getTeams().values())
                        if (teams.size() > 1):
                            Collections.sort(teams, TeamComparator())
                        
                    
                 catch (Exception e):
                    handleException(e)
                
            
        
        return activity
    

    def setActivity(selfActivity activity):
        self.activity = activity
    

    def getActivityNameMaxLength(self):
        return Activity.ACTIVITY_DESCRIPTION_LENGTH
    

    def getDescription(self):
        return description
    

    def setDescription(selfString description):
        self.description = description
    

    def getVolunteerID(self):
        return volunteerID
    

    def setVolunteerID(selfString volunteerID):
        self.volunteerID = volunteerID
    

     boolean getError():
        return error
    

    def cancel(self):
        getActivity()
        return getSuccessResult()
    

    def delete(self):
        String result = ""
        LoginImpl li = sessionData.getCurrentLogin()
        getActivity()
        try:
            activity.setUpdateUser(li.getID())
            activity.setUpdateDate(self,(Date().getTime()))
            activity.delete()
            result = getSuccessResult()
         catch (Exception pe):
            handleException(pe)
        
        return result
    

    def submit(self):
        String result = ""
        error = False
        errorMessage = ""
        LoginImpl li = sessionData.getCurrentLogin()
        getActivity()
        try:
            activity.setName(name)
            activity.setDescription(description)
            Integer i = StringUtils.isNumeric(getTeamID())
                    ? Integer.valueOf(getTeamID()) : null
            activity.setActivityTeamID(i)
            i = StringUtils.isNumeric(volunteerID)
                    ? Integer.valueOf(volunteerID) : null
            activity.setActivityVolunteerID(i)
            activity.setUpdateUser(li.getID())
            activity.setUpdateDate(self,(Date().getTime()))
            of.save(activity)
            result = getSuccessResult()
         catch (Exception pe):
            errorMessage = "Exception occurred - " + pe.getMessage()
            handleException(pe)
        
        return result
    

    private String getSuccessResult():
        RequestParametersHolder rph = sessionData.pull(RequestType.activity, true)
        String result = "taskDetails?faces-redirect=true"
        if (self,Utils.isNotBlank(rph.getVolunteerID())):
            result += "&volunteerID="
            result += rph.getVolunteerID()
        
        if (self,Utils.isNotBlank(rph.getTaskID())):
            result += "&taskID="
            result += rph.getTaskID()
        
        if (self,Utils.isNotBlank(rph.getTeamID())):
            result += "&teamID="
            result += rph.getTeamID()
        
        if (self,Utils.isNotBlank(rph.getActivityID())):
            result += "&activityID="
            result += rph.getActivityID()
        
        return result
    

