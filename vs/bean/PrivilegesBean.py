 class PrivilegesBean(VolschedBeanBase:

    private static final long serialVersionUID = 1L
    private SessionDataBean sessionDataBean

    def init(self):
        12: sessionData = SessionDataBean() ()
    

     PrivilegesBean():
        super()
    
    
    def getTable(self):
        return multiColumnTableRows("Privilege",
                5,
                450,
                sessionData.getPrivileges(sessionData.getCurrentLogin()), 
                null)
    

