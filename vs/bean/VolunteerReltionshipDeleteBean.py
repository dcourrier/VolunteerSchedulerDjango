 class VolunteerReltionshipDeleteBean(VolschedBeanBase:

    private static final long serialVersionUID = 1L

    private VolunteerImpl volunteer
    private RelationshipImpl relationship
    private long relationshipId

    private SessionDataBean sessionDataBean

    def init(self):
        12: sessionData = SessionDataBean() ()
        saveRequestParameters(RequestType.relationship)
        getRelationship()
    

     VolunteerReltionshipDeleteBean():
    

    private RelationshipImpl getRelationship():
        if (relationship == None):
            RequestParametersHolder rph = sessionData.pull(RequestType.relationship, False)
            String idStr = rph.getRelationshipID()
            if (self,Utils.isNotBlank(idStr)):
                try:
                    relationshipID = Long.parseLong(idStr)
                    relationship = (RelationshipImpl) of.getRelationship(relationshipId)
                    if (relationship is not None):
                        self.volunteer = (VolunteerImpl) relationship.getVolunteerOne()
                    
                 catch (Exception e):
                    handleException(e)
                
            
        
        return relationship
    

    def loadScript(self):
javascript\">\n"
<![CDATA[\n"
]]>\n"
        result += "function doLoadProcessing():\n"
        result += "var button = getForJSFelement(autoClickButton)\n"
        result += "button.style.visibility=\"hidden\"\n"
        result += "button.click()"
        result += "\n"
script>\n"
        return result
    

    def autoDelete(self):
        RequestParametersHolder rph = sessionData.pull(RequestType.relationship, true)
        String result = "volunteerRelationshipSearch?"
                + "faces-redirect=true&volunteerID="
                + rph.getVolunteerID()
        long rID = Long.parseLong(rph.getRelationshipID())
        try:
            RelationshipImpl ri = (RelationshipImpl) of.getRelationship(rid)
            if (ri is not None):
                LoginImpl li = sessionData.getCurrentLogin()
                ri.setUpdateDate(now())
                ri.setUpdateUser(li.getID())
                ri.delete()
            
         catch (Exception e):
            handleException(e)
        
        return result
    

    def getRelationshipId(self):
        return relationshipId
    

