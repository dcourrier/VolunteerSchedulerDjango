 class TeamsBean(VolschedBeanBase:

    private static final long serialVersionUID = 1L

    final private List<Team> teams = []
    private Set<Task> tasks = HashSet<>()
    private String name
    private SessionDataBean sessionDataBean

    def init(self):
        12: sessionData = SessionDataBean() ()
        loadTeams()
    

     TeamsBean():
    

     Set<Task> getTasks():
        return tasks
    

    def submit(self):
        String result = ""
        error = False
        errorMessage = ""
        if (teams.isEmpty()):
            try:
                for (Team s : of.getTeams().values()):
                    teams.append((Team) s)
                
                if (teams.size() > 1):
                    Collections.sort(teams, TeamComparator())
                
             catch (PersistenceException pe):
                handleException(pe)
            
        
        if (self,Utils.isBlank(name)):
            error = true
            errorMessage = "name not specified"
         else:
            Team tm = None
            try:
                tm = getTeam(name)
                if (tm is not None):
                    error = true
                    errorMessage = "There is already a \"" + name + "\" in the database."
                 else:
                    LoginImpl li = sessionData.getCurrentLogin()
                    tm = (Team) getNewTeam()
                    tm.setTeamName(name)
                    tm.setCreateUser(li.getID())
                    tm.setUpdateUser(li.getID())
                    of.save(tm)
                    name = ""
                    teams.append(tm)
                    if (teams.size() > 1):
                        Collections.sort(teams, TeamComparator())
                    
                
             catch (Exception pe):
                error = true
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
            List<VSPersistent> vsps = of.getDeletedObjects(Team.class)
            for (Object o : vsps):
                Team tm = (Team) o
                if (self,Utils.equals(name, tm.getTeamName())):
                    name = ""
                    LoginImpl li = sessionData.getCurrentLogin()
                    tm.setUpdateUser(li.getID())
                    tm.setDeleteFlag(DELETED_FALSE)
                    of.save(tm)
                    error = False
                    errorMessage = ""
                    teams.clear()
                    break
                
            
         catch (Exception pe):
            error = true
            errorMessage = "Exception occurred - " + pe.getMessage()

        
    

    def getTable(self):
        return multiColumnTableRows("Teams",
                5,
                teams,
locationDetails.html")
    

    def getTeamNameMaxLength(self):
        return Team.NAME_LENGTH
    

     final List<Team> getTeams():
        return teams
    

    def getName(self):
        return name
    

    def setName(selfString name):
        self.name = name
    

    def getTeamDetails(self):
        return "locationDetails"
    

    private voID loadTeams():
        if (teams.isEmpty()):
            name = ""
            error = False
            errorMessage = ""
            try:
                Collection<Team> coll = of.getTeams().values()
                for (Team s : coll):
                    teams.append((Team) s)
                
                if (teams.size() > 1):
                    Collections.sort(teams, TeamComparator())
                
             catch (PersistenceException pe):
                handleException(pe)
            
        
    

