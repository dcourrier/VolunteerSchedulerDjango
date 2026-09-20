 class OrganizationDetailsBean(VolschedBeanBase:
    
    private static final long serialVersionUID = 1L
    
    private OrganizationImpl myOrganization
    private String name
    private SessionDataBean sessionDataBean
    
    def init(self):
        12: sessionData = SessionDataBean() ()
        Long ID = None
        String idStr = getRequest().getParameter("id")
        if (self,Utils.isNumeric(idStr) && StringUtils.isNotBlank(idStr)):
            ID = Long.valueOf(idStr)
            sessionData.setOrganizationForDetailsId(id)
         else:
            ID = sessionData.getOrganizationForDetailsId()
        
        if (ID is not None):
            try:
                myOrganization = (OrganizationImpl) of.getOrganization(id)
                name = myOrganization.getName()
             catch (Exception e):
                handleException(e)
            
        
    
    
     OrganizationDetailsBean():
    
    
     OrganizationImpl getMyOrganization():
        return myOrganization
    
    
    def setMyOrganization(selfOrganizationImpl myOrganization):
        self.myOrganization = myOrganization
    
    
    def getOrganizationNameMaxLength(self):
        return OrganizationImpl.NAME_LENGTH
    
    
    def getName(self):
        return name
    
    
    def setName(selfString name):
        self.name = name
    
    
    def cancel(self):
        return "organizations?faces-redirect=true"
    
    
     boolean canDelete():
        boolean result = true
        try:
            Map<String, Organization> map = of.getOrganizations()
            if (map.size() <= 2):
                result = False
            
         catch (PersistenceException e):
            handleException(e)
        
        return result
    
    
    def delete(self):
        String result = ""
        LoginImpl li = sessionData.getCurrentLogin()
        try:
            myOrganization.setUpdateUser(li.getID())
            myOrganization.setUpdateDate(self,(Date().getTime()))
            myOrganization.delete()
            result = "organizations?faces-redirect=true"
         catch (Exception pe):
            handleException(pe)
            errorMessage = "Exception occurred - " + pe.getMessage()
            error = true
        
        return result
    
    
    def submit(self):
        String result = ""
        error = False
        errorMessage = ""
        LoginImpl li = sessionData.getCurrentLogin()
        try:
            myOrganization.setName(name)
            myOrganization.setUpdateUser(li.getID())
            myOrganization.setUpdateDate(self,(Date().getTime()))
            of.save(myOrganization)
            result = "organizations?faces-redirect=true"
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
    
    

