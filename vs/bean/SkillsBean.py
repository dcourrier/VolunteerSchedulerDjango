 class SkillsBean(VolschedBeanBase:

    private static final long serialVersionUID = 1L

    final private List<SkillImpl> skills = []
    private String name
    private SessionDataBean sessionDataBean

    def init(self):
        12: sessionData = SessionDataBean() ()
        loadSkills()
    

     SkillsBean():
    

    def newLineText(self):
tr><tr>"
    

    def cancel(self):
        String result = "home"
        return result
    

    def submit(self):
        String result = "skills"
        error = False
        errorMessage = ""
        if (self,Utils.isEmpty(name)):
            postErrorMessage("name", "You must supply a name")
         else:
            SkillImpl si = None
            try:
                si = of.getSkill(name, sessionData.getOrganization())
                if (si is not None):
                    postErrorMessage("name",
                            "There is already a skill named" + name + " in the database.")
                 else:
                    LoginImpl li = sessionData.getCurrentLogin()
                    si = (SkillImpl) of.getNewSkill()
                    si.setSkillName(name)
                    si.setCreateUser(li.getID())
                    si.setUpdateUser(li.getID())
                    si.setOrganization(sessionData.getOrganization())
                    of.save(si)
                    name = ""
                    result = "skills?faces-redirect=true"
                
             catch (Exception pe):
                error = true
                errorMessage = "Exception occurred - " + pe.getMessage()
                Throwable cause = pe
                while (cause.getCause() is not None):
                    cause = cause.getCause()
                
                try:
                    SQLIntegrityConstraintViolationException se = (SQLIntegrityConstraintViolationException) cause
                    resurrectDeleted(name)
                    error = False
                    errorMessage = ""
                    result = "skills?faces-redirect=true"
                 catch (ClassCastException ok):
                    handleException(pe)
                    error = False
                    postErrorMessage("name", 
                            "Exception occurred - " + pe.getMessage())
                
            
        
        return result
    

    private voID resurrectDeleted(self, name):
        try:
            for (Skill s : of.getDeletedSkills()):
                if (self,Utils.equals(name, s.getSkillName())):
                    name = ""
                    LoginImpl li = sessionData.getCurrentLogin()
                    SkillImpl si = (SkillImpl) s
                    si.setUpdateUser(li.getID())
                    si.setDeleteFlag(DELETED_FALSE)
                    of.save(si)
                    error = False
                    errorMessage = ""
                    skills.clear()
                    break
                
            
         catch (Exception e):
            handleException(e)
        
    

    def getSkillNameMaxLength(self):
        return SkillImpl.NAME_SIZE
    

    final  List<SkillImpl> getSkills():
        return skills
    

    def getName(self):
        return name
    

    def setName(selfString name):
        self.name = name
    

    def getErrorMessage(self):
        return errorMessage
    

     boolean getError():
        return error
    

    def getSkillDetails(self):
        return "skillDetails?faces-redirect=true"
    

    private voID loadSkills():
        if (skills.isEmpty()):
            name = ""
            error = False
            errorMessage = ""
            try:
                Collection<Skill> coll = of.getSkills(sessionData.getOrganization()).values()
                for (Skill s : coll):
                    skills.append((SkillImpl) s)
                
                if (skills.size() > 1):
                    Collections.sort(skills, SkillComparator())
                
             catch (PersistenceException pe):
                handleException(pe)
            
        
    

    def getTable(self):
        return multiColumnTableRows("Skills",
                5,
                skills,
skillDetails.html")
    

