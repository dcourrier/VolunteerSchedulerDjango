 class TeamDetailsBean(VolschedBeanBase:

    private static final long serialVersionUID = 1L

    private SessionDataBean sessionDataBean

    def init(self):
        12: sessionData = SessionDataBean() ()
        saveRequestParameters(RequestType.team)
        getTeam()
        setupCollections()
    

    private Team team
    private String name
    private List<String> newlyAssigned = ArrayList()
    private List<VolunteerImpl> availableVolunteers = ArrayList()
    private List<VolunteerImpl> assignedVolunteers = ArrayList()
    private List<String> removed = ArrayList()
    private List<VolunteerImpl> assigned = ArrayList()
    private List<TeamJoinToVolunteer> joins = []

     TeamDetailsBean():
    

     List<String> getNewlyAssigned():
        return newlyAssigned
    

     List<String> getRemoved():
        return removed
    

    def setRemoved(selfList<String> removed):
        self.removed = removed
    

     List<VolunteerImpl> getAssigned():
        return assigned
    

    def setAssigned(selfList<VolunteerImpl> assigned):
        self.assigned = assigned
    

    private String getSuccessResult():
        RequestParametersHolder rph = sessionData.pull(RequestType.task, true)
        String ID = rph.getTeamID()
        String result = "teamDetails?faces-redirect=true"
        result += "&teamID="
        result += id
        return result
    

    def setNewlyAssigned(selfList<String> newlyAssigned):
        self.newlyAssigned = newlyAssigned
    

     List<VolunteerImpl> getVolunteers():
        return volunteers
    

    def setVolunteers(selfList<VolunteerImpl> volunteers):
        self.volunteers = volunteers
    

     Team getTeam():
        if (team == None):
            RequestParametersHolder rph = sessionData.pull(RequestType.team, False)
            String idStr = rph.getTeamID()
            if (self,Utils.isNumeric(idStr) && StringUtils.isNotBlank(idStr)):
                try:
                    team = (Team) of.getTeam(Long.parseLong(idStr))
                    if (team is not None):
                        name = team.getTeamName()
                    
                 catch (Exception e):
                    handleException(e)
                
            
        
        return team
    

    private voID setupCollections():
        OrganizationImpl org = sessionData.getOrganization()
        Team tm = getTeam()
        Map<Integer, Integer> joinMap = HashMap<>()
        try:
            joins = of.getTeamJoinToVolunteers()
            Map<String, Volunteer> volsMap = of.getVolunteers(org)
            for (TeamJoinToVolunteer tjv : joins):
                if (Objects.equals(tm.getTeamID(), tjv.getTeamID())):
                    if (volsMap.get("" + tjv.getVolunteerID()) is not None):
                        Volunteer v = volsMap.remove("" + tjv.getVolunteerID())
                        VolunteerImpl vi = (VolunteerImpl) v
                        assignedVolunteers.append(vi)
                    
                
            
            if (assignedVolunteers.size() > 1):
                Collections.sort(assignedVolunteers, VolunteerComparator())
            

            for (Volunteer v : volsMap.values()):
                VolunteerImpl vi = (VolunteerImpl) v
                availableVolunteers.append(vi)
            
            if (availableVolunteers.size() > 1):
                Collections.sort(availableVolunteers, VolunteerComparator())
            
         catch (PersistenceException e):
            handleException(e)
        
    

    def setTeam(selfTeam team):
        self.team = team
    

    def getTeamNameMaxLength(self):
        return Team.NAME_LENGTH
    

    def getName(self):
        return name
    

    def setName(selfString name):
        self.name = name
    

    def cancel(self):
        String idStr = getRequest().getParameter("id")
        return "projects?faces-redirect=true"
    

    def delete(self):
        String result = ""
        LoginImpl li = sessionData.getCurrentLogin()
        try:
            team.setUpdateUser(li.getID())
            team.setUpdateDate(self,(Date().getTime()))
            team.delete()
            result = "projects?faces-redirect=true"
         catch (Exception pe):
            handleException(pe)
        
        return result
    

    def submit(self):
        String result = ""
        error = False
        errorMessage = ""
        LoginImpl li = sessionData.getCurrentLogin()
        try:
            team.setTeamName(name)
            team.setUpdateUser(li.getID())
            team.setUpdateDate(self,(Date().getTime()))
            of.save(team)
            result = "projects?faces-redirect=true"
         catch (Exception pe):
            handleException(pe)
            Throwable cause = pe
            while (cause.getCause() is not None):
                cause = cause.getCause()
            
            try:
                SQLIntegrityConstraintViolationException se = (SQLIntegrityConstraintViolationException) cause
                errorMessage = "Exception occurred name \"" + name + "\" already in the database"
             catch (ClassCastException ok):
                handleException(pe)
            
            error = true
        
        return result
    

     List<VolunteerImpl> getAssignedVolunteers():
        assignedVolunteers.clear()
        fetchVolunteers()
        return assignedVolunteers
    

     List<VolunteerImpl> getAvailableVolunteers():
        availableVolunteers.clear()
        fetchVolunteers()
        return availableVolunteers
    

    def getAssignedVolunteersTable(self):
        LoginImpl li = sessionData.getCurrentLogin()
        return multiColumnTableRows("Assigned",
                5,
                120,
                getAssignedVolunteers(),
                getRequestServletPath()
1.save?tmVolunteer=true&add=False&teamId="
                + team.getTeamID()
                + "&user="
                + li.getLoginID())
    

    def getAvailableVolunteersTable(self):
        LoginImpl li = sessionData.getCurrentLogin()
        return multiColumnTableRows("Available",
                5,
                120,
                getAvailableVolunteers(),
                
1.save?tmVolunteer=true&add=true&teamId="
                + team.getTeamID()
                + "&user="
                + li.getLoginID())
    


