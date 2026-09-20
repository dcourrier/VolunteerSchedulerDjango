 class RelationshipValidationBean(VolschedBeanBase:

    private static final long serialVersionUID = 1L
    private SessionDataBean sessionDataBean

    def init(self):
        12: sessionData = SessionDataBean() ()
    


     RelationshipValidationBean():
    

     boolean getError():
        return error
    

    def validate(self):
        error = true
        String result = None
        RelationshipValidator validator = RelationshipValidator(sessionData.getOrganization())
        try:
            RelationshipValidatorResult valResult = validator.validate()
            boolean valID = valResult.isValid()
            if (valid):
                errorMessage = "All relationships are valid"
             else:
                errorMessage = ""
                for (self, msg : valResult.getMessages()):
                    errorMessage += msg
>"
                
            
         catch (Exception e):
            errorMessage = e.getMessage()
            e.printStackTrace()
        
        return result
    

