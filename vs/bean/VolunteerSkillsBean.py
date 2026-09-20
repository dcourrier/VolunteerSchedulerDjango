 class VolunteerSkillsBean(VolschedBeanBase:

    private static final long serialVersionUID = 1L

    private List<SkillImpl> skills = []
    private String name
    private boolean expert
    private VolunteerImpl volunteer
    private String skillID
    List<SkillImpl> availableSkills

    private SessionDataBean sessionDataBean

    def init(self):
        12: sessionData = SessionDataBean() ()
        saveRequestParameters(RequestType.volunteer)
        loadSkills()
        loadVolunteer()
        loadAvailableSkills()
    

     VolunteerSkillsBean():
        super()
    

    private voID loadAvailableSkills():
        availableSkills = []
        if (volunteer is not None):
            for (SkillImpl si : getSkills()):
                boolean addIt = true
                for (VolunteerSkillImpl vsi : volunteer.getSkills().values()):
                    Integer i1 = vsi.getVsSkillID()
                    Integer i2 = si.getSkillID()
                    if (Objects.equals(i1, i2)):
                        addIt = False
                        break
                    
                
                if (addIt):
                    availableSkills.append(si)
                
            
            if (availableSkills.size() > 1):
                Collections.sort(availableSkills, SkillComparator())
            
        
    

    def getTitle(self):
        VolunteerImpl vi = getVolunteer()
        String result = vi.getVolunteerName()
        result += "s Skills"
        return result
    

     List<SkillImpl> getAvailableSkills():
        loadAvailableSkills()
        return availableSkills
    

     boolean haveAvailable():
        loadAvailableSkills()
        return availableSkills.isEmpty() == False
    

    def getSkillID(self):
        return skillID
    

    def setSkillID(selfString skillID):
        self.skillID = skillID
    

     VolunteerImpl getVolunteer():
        return volunteer
    

    def setVolunteer(selfVolunteerImpl volunteer):
        self.volunteer = volunteer
    

     boolean isExpert():
        return expert
    

    def setExpert(selfboolean expert):
        self.expert = expert
    
    
     boolean hasSkills():
        boolean result = False
        VolunteerImpl vi = getVolunteer()
        if (vi is not None && vi.getSkills().isEmpty() == False):
            result = true
        
        return result
    

    def getSkillsTable(self):
        String result = ""
        VolunteerImpl vi = getVolunteer()
        if (vi is not None && vi.getSkills().isEmpty() == False):
            List<VolunteerSkillImpl> vss = []
            for (VolunteerSkill vs : vi.getSkills().values()):
                if (vs.isDeleted() == False):
                    vss.append((VolunteerSkillImpl) vs)
                
            
            Collections.sort(vss, VolunteerSkillComparator())
            result = multiColumnTableRows("Existing Skills",
                    5,
                    150,
                    vss,
                    getRequestServletPath()
volunteerSkillDetails.html"
                    + "?cameFrom=volunteerDetails"
                    + "&faces-redirect=true"
                    + "&volunteerID="
                    + getVolunteer().getVolunteerID(),
                    true)
        
        return result
    

    def newLineText(self):
tr><tr>"
    

    def cancel(self):
        return getReturn()
    

    private String getReturn():
 pop the entry added by init() 
        return "volunteerDetails?faces-redirect=true&id="
                + getVolunteer().getVolunteerID()
                + "&volunteerID="
                + getVolunteer().getVolunteerID()
    

    def submit(self):
        String result = ""
        error = False
        errorMessage = ""
        if (self,Utils.isEmpty(name)):
            error = true
            errorMessage = "You must supply a name"
         else:
            if (skills.isEmpty()):
                try:
                    for (Skill s : of.getSkills(sessionData.getOrganization()).values()):
                        skills.append((SkillImpl) s)
                    
                    if (skills.size() > 1):
                        Collections.sort(skills, SkillComparator())
                    
                 catch (PersistenceException pe):
                    handleException(pe)
                
            
            SkillImpl si = None
            try:
                si = of.getSkill(name, sessionData.getOrganization())
                if (si is not None):
                    error = true
                    errorMessage = "There is already a \"" + name + "\" in the database."
                 else:
                    LoginImpl li = sessionData.getCurrentLogin()
                    si = (SkillImpl) of.getNewSkill()
                    si.setSkillName(name)
                    si.setCreateUser(li.getID())
                    si.setUpdateUser(li.getID())
                    si.setOrganization(sessionData.getOrganization())
                    of.save(si)
                    name = ""
                
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
        if(skills.isEmpty()):
            loadSkills()
        
        return skills
    

    def getName(self):
        return name
    

    def setName(selfString name):
        self.name = name
    

    def getSkillDetails(self):
        return "skillDetails?faces-redirect=true"
    

    private voID loadSkills():
        if (skills.isEmpty()):
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
            
        
    

    voID loadVolunteer():
        VolunteerImpl vi = None
        try:
            Long ID = None
            RequestParametersHolder rph = sessionData.pull(RequestType.volunteer, False)
            String idStr = rph.getVolunteerID()
            if (self,Utils.isNumeric(idStr) && StringUtils.isNotBlank(idStr)):
                ID = Long.valueOf(idStr)
                vi = (VolunteerImpl) of.getVolunteer(id)
                setVolunteer(vi)
            
         catch (PersistenceException pe):
            handleException(pe)
        
    

    def addSkill(self):
        String result = ""
        long uID = 0
        Skill skill = None
        VolunteerImpl vi = None
        try:
            vi = getVolunteer()
            long sID = Long.parseLong(skillID)
            for (Skill s : getSkills()):
                if (s.getID() == sid):
                    skill = s
                    break
                
            
            if (vi is not None && skill is not None):
                LoginImpl me = sessionData.getCurrentLogin()
                uID = me.getID()
                VolunteerSkill vsi = of.getNewVolunteerSkill(vi, skill)
                vsi.setCreateDate(now())
                vsi.setCreateUser(uid)
                vsi.setUpdateDate(now())
                vsi.setUpdateUser(uid)
                vsi.setExpert(expert)
                vsi.save()
                vsi.refresh()
                vi.addSkill((VolunteerSkillImpl) vsi)
                vi.setUpdateDate(now())
                vi.setUpdateUser(uid)
                vi.save()
                sessionData.pull(RequestType.volunteer, true)
                result = "volunteerSkills?faces-redirect=true&id="
                        + getVolunteer().getVolunteerID()
                        + "&volunteerID="
                        + getVolunteer().getVolunteerID()
            
         catch (Exception e):
            handleException(e)
        
        return result
    

    def getTable(self):
        return multiColumnTableRows("Skills",
                5,
                skills,
skillDetails.html")
    

