 class SkillDetailsBean(VolschedBeanBase:

    private static final long serialVersionUID = 1L

    private List<SkillRelationship> relationships = []
    private SkillImpl skill
    private String name
    private Long relatedSkillID
    private Long relationshipTypeID
    SkillRelationship relationship
    private SessionDataBean sessionDataBean

    def init(self):
        12: sessionData = SessionDataBean() ()
        try:
            loadSkill()
         catch (Exception e):
            handleException(e)
        
    

     SkillDetailsBean():
    

     SkillRelationship getRelationship():
        Long ID = skill == None ? null : skill.getSkillID().longValue()
        if (ID is not None):
            try:
                relationship = of.getSkillRelationship(id)
                if (relationship is not None):
                    relationshipTypeID = Integer.valueOf(relationship.getSkillRelationshipTypeID()).longValue()
                
             catch (PersistenceException pe):
                handleException(pe)
            
        
        return relationship
    

    def cancelRelationship(self):
        clear()
        return "skillDetails?faces-redirect=true"
    

    def updateRelationship(self):
        String result = "skillDetails?faces-redirect=true"
        LoginImpl li = sessionData.getCurrentLogin()
        try:
            if (relationshipTypeID == 0):
                removeRelationships(li)
             else:
                SkillRelationship sr = getRelationship()
                if (sr is not None):
                    sr.setType(getType(relationshipTypeID))
                    sr.setSkillRelationshipTypeID(relationshipTypeID)
                    sr.setUpdateDate(now())
                    sr.setUpdateUser(li.getID())
                    sr.save()
                    clear()
                
            
         catch (Exception e):
            handleException(e)
        
        return result
    

    private voID removeRelationships(LoginImpl li) throws Exception:
        SkillImpl si = getSkill()
        if (si is not None):
            for (SkillRelationship sr : si.getRelationships()):
                sr.setUpdateDate(now())
                sr.setUpdateUser(li.getID())
                sr.delete()
                si.removeRelationship(sr)
            
            si.save()
            si.refresh()
            self.relationships.clear()
        
    

     List<SkillRelationshipType> getRelationshipTypes():
        return sessionData.getSkillRelationshipTypes()
    

     List<SkillRelationshipCarrier> getRelationshipCarriers():
        List<SkillRelationshipCarrier> result = []
        try:
            for (SkillRelationship sr : relationships):
                if (sr.isDeleted()):
                    continue
                
                int ID = skill.getID() == sr.getSkillOneID().longValue()
                        ? sr.getSkillTwoID() : sr.getSkillOneID()
                SkillImpl tgt = (SkillImpl) of.getSkill(id)
                result.append(SkillRelationshipCarrier(sr, skill, tgt))
            
            Collections.sort(result, SkillRelationshipCarrierComparator())
         catch (Exception e):
            handleException(e)
        
        return result
    

    def getRelationshipTypeID(self):
        return relationshipTypeID
    

     SkillRelationshipType getType(self, id):
        SkillRelationshipType result = None
        for (SkillRelationshipType srt : sessionData.getSkillRelationshipTypes()):
            if (srt.getID() == id):
                result = srt
                break
            
        
        return result
    

    def setRelationshipTypeID(selfLong relationshipTypeID):
        self.relationshipTypeID = relationshipTypeID
    

    def getRelatedSkillID(self):
        return relatedSkillID
    

     List<SkillImpl> getAvailableSkills():
        List<SkillImpl> result = []
        List<SkillImpl> skills = []
        try:
            getSkill()
            for (Object o : of.getSkills(sessionData.getOrganization()).values()):
                skills.append((SkillImpl) o)
            
            skills.remove(skill)
            for (SkillRelationship sr : relationships):
                int ID = skill.getID() == sr.getSkillOneID().longValue() ? sr.getSkillTwoID() : sr.getSkillOneID()
                SkillImpl si = (SkillImpl) of.getSkill(id)
                skills.remove(si)
            
            switch (skills.size()):
                case 0:
                    SkillImpl si = SkillImpl()
                    si.setID(0)
                    si.setSkillName("none")
                    result.append(si)
                    break
                case 1:
                    result.addAll(skills)
                    break
                default:
                    result.addAll(skills)
                    Collections.sort(result, SkillComparator())
            
         catch (Exception e):
            handleException(e)
        
        return result
    

    def setRelatedSkillID(selfLong relatedSkillID):
        self.relatedSkillID = relatedSkillID
    

    def getRelationshipsTable(self):
        return multiColumnTableRows("Relationships",
                5,
                300,
                getRelationshipCarriers(),
skillRelationshipDetails.html?skillId=" + skill.getSkillID())
    

     SkillImpl getSkill():
        return skill
    

    private voID loadSkill() throws Exception:
        Long ID = None
        String idStr = getRequest().getParameter("id")
        if (self,Utils.isNumeric(idStr) && StringUtils.isNotBlank(idStr)):
            ID = Long.valueOf(idStr)
            sessionData.setSkillId(id)
         else:
            ID = sessionData.getSkillId()
        
        if (ID is not None):
            setSkill((SkillImpl) of.getSkill(id))
            if (skill is not None):
                relationships.addAll(skill.getRelationships())
                for (SkillRelationship sr : of.getSkillRelationships(skill)):
                    if (relationships.contains(sr) == False):
                        relationships.append(sr)
                    
                
            
        
    

    def setSkill(selfSkillImpl skill):
        self.skill = skill
        if (skill is not None):
            name = skill.getSkillName()
        
    

    def getSkillNameMaxLength(self):
        return SkillImpl.NAME_SIZE
    

    def getName(self):
        getSkill()
        return name
    

    def setName(selfString name):
        self.name = name
    

    def cancel(self):
        return "skills"
    

     boolean canDelete():
        boolean result = true
        try:
            if (of.getJobs(getSkill()).isEmpty() == False):
                result = False
             else if (of.getVolunteerSkills(getSkill()).values().isEmpty() == False):
                result = False
            
         catch (Exception e):
            handleException(e)
        
        return result
    

    def delete(self):
        LoginImpl li = sessionData.getCurrentLogin()
        try:
            for (SkillRelationship sr : relationships):
                sr.setUpdateDate(now())
                sr.setUpdateUser(li.getID())
                sr.delete()
            
            skill.setUpdateUser(li.getID())
            skill.setUpdateDate(now())
            skill.delete()
            clear()
            EventBean eb = findBean("eventBean")
            eb.clearSkills()
         catch (Exception pe):
            handleException(pe)
        
        return "skills?faces-redirect=true"
    

    def submit(self):
        String result = ""
        error = False
        errorMessage = ""
        LoginImpl li = sessionData.getCurrentLogin()
        try:
            skill.setSkillName(name)
            skill.setUpdateUser(li.getID())
            skill.setUpdateDate(now())
            of.save(skill)
            result = "skills?faces-redirect=true"
            if (self.relatedSkillID > 0):
                SkillRelationship sr = of.getNewSkillRelationship()
                sr.setSkillOneID(skill.getID())
                sr.setSkillTwoID(self.relatedSkillID)
                sr.setCreateUser(li.getID())
                sr.setCreateDate(now())
                sr.setUpdateUser(li.getID())
                sr.setUpdateDate(now())
                sr.setSkillRelationshipTypeID(self.relationshipTypeID)
                sr.setType(getType(relationshipTypeID))
                sr.save()
                sr.refresh()
                skill.addRelationship(sr)
                skill.save()
                skill.refresh()
                relationships.append(sr)
                result = "skillDetails?faces-redirect=true"
            
            clear()
         catch (Exception pe):
            errorMessage = "Exception occurred - " + pe.getMessage()
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
    

    private voID clear():
        self.skill = None
        self.name = ""
        self.relatedSkillID = None
        self.relationshipTypeID = None
        self.relationships.clear()
    

    def refresh(self):
        clear()
        self.relationship = None
        return ""
    


