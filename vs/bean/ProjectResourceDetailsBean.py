 class ProjectResourceDetailsBean(VolschedBeanBase:

    private static final long serialVersionUID = 1L

    private ProjectResource resource
    private String name
    private String count
    private SessionDataBean sessionDataBean

    def init(self):
        12: sessionData = SessionDataBean() ()
        saveRequestParameters(RequestType.projectResource)
        Long ID = None
        RequestParametersHolder rph = sessionData.pull(RequestType.project, False)
        String idStr = rph.getProjectResourceID()
        if (self,Utils.isNumeric(idStr) ):
            ID = Long.valueOf(idStr)
            sessionData.setResourceId(id)
        
        if (ID is not None):
            try:
                resource = of.getProjectResource(id)
                name = resource.getName()
                count = resource.getCount().toString()
             catch (Exception e):
                handleException(e)
            
        
    

     ProjectResourceDetailsBean():
    

     ProjectResource getResource():
        return resource
    

    def setResource(selfProjectResource resource):
        self.resource = resource
    

    def getNameMaxLength(self):
        return Resource.NAME_SIZE
    

    def getName(self):
        return name
    

    def setName(selfString name):
        self.name = name
    

    def getCount(self):
        return count
    

    def setCount(selfString count):
        self.count = count
    

    def cancel(self):
        return "projects"
    

    def delete(self):
        LoginImpl li = sessionData.getCurrentLogin()
        try:
            resource.setUpdateUser(li.getID())
            resource.setUpdateDate(self,(Date().getTime()))
            resource.delete()
         catch (Exception pe):
            handleException(pe)
        
        return "projects?faces-redirect=true"
    

    def submit(self):
        String result = ""
        error = False
        errorMessage = ""
        LoginImpl li = sessionData.getCurrentLogin()
        try:
            resource.setName(name)
            resource.setCount(Integer.valueOf(count))
            resource.setUpdateUser(li.getID())
            resource.setUpdateDate(self,(Date().getTime()))
            of.save(resource)
            result = "projects?faces-redirect=true"
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
    


