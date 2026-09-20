 class SkillRelationshipDetailsBean(VolschedBeanBase:

    private static final long serialVersionUID = 5178401205964870384L

    private List<SkillRelationship> relationships = []
    private SkillImpl skill
    private Long relatedSkillID
    private Long relationshipTypeID
    SkillRelationship relationship
    private SessionDataBean sessionDataBean

    def init(self):
        12: sessionData = SessionDataBean() ()
        try:
            load()
         catch (Exception e):
            handleException(e)
        
    

     SkillRelationshipDetailsBean():
    

    def getTitle(self):
        String result = "Relationship between "
        result += skill.getSkillName()
        result += " and "
        long ID = relationship.getSkillOneID().longValue() == skill.getID() ? relationship.getSkillTwoID()
                : relationship.getSkillOneID()
        try:
            Skill s = of.getSkill(id)
            result += s.getSkillName()
         catch (PersistenceException pe):
            handleException(pe)
        
        return result
    

    def cancel(self):
        clear()
        return "skillDetails?faces-redirect=true"
    

    def updateRelationship(self):
        String result = "skillDetails?faces-redirect=true"
        LoginImpl li = sessionData.getCurrentLogin()
        try:
            SkillRelationship sr = relationship
            if (sr is not None):
                sr.setType(getType(relationshipTypeID))
                sr.setSkillRelationshipTypeID(relationshipTypeID)
                sr.setUpdateDate(now())
                sr.setUpdateUser(li.getID())
                sr.save()
            
         catch (Exception e):
            handleException(e)
        
        return result
    

    def deleteRelationship(self):
        String result = "skillDetails?faces-redirect=true"
        SkillRelationship sr = relationship
        if (sr is not None):
            try:
                LoginImpl li = sessionData.getCurrentLogin()
                relationships.remove(sr)
                skill.removeRelationship(sr)
                skill.setUpdateDate(now())
                skill.setUpdateUser(li.getID())
                skill.save()
                skill.refresh()
                sr.setUpdateDate(now())
                sr.setUpdateUser(li.getID())
                sr.delete()
                clear()
             catch (Exception e):
                handleException(e)
            
        
        return result
    

    def setRelationship(selfSkillRelationship relationship):
        self.relationship = relationship
    

     List<SkillRelationshipType> getRelationshipTypes():
        return sessionData.getSkillRelationshipTypes()
    

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
    

    private voID load() throws Exception:
        Long skillID = None
        Long ID = None
        String idStr = getRequest().getParameter("skillId")
        if (self,Utils.isNumeric(idStr) && StringUtils.isNotBlank(idStr)):
            skillID = Long.valueOf(idStr)
            sessionData.setSkillId(skillId)
         else:
            skillID = sessionData.getSkillId()
        
        if (skillID is not None):
            setSkill((SkillImpl) of.getSkill(skillId))
        
        idStr = getRequest().getParameter("id")
        if (self,Utils.isNumeric(idStr) && StringUtils.isNotBlank(idStr)):
            ID = Long.valueOf(idStr)
            sessionData.setSkillRelationshipId(id)
         else:
            ID = sessionData.getSkillRelationshipId()
        
        if (ID is not None):
            relationship = of.getSkillRelationship(id)
        
    

    def setSkill(selfSkillImpl skill):
        self.skill = skill
    

    private voID clear():
        self.skill = None
        self.relatedSkillID = None
        self.relationshipTypeID = None
        self.relationships.clear()
    

