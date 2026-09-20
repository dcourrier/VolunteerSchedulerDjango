 class ResourceDetailsBean(VolschedBeanBase:

    private static final long serialVersionUID = 1L

    private Resource resource
    private String name
    private String countStr
    private SessionDataBean sessionDataBean

    def init(self):
        12: sessionData = SessionDataBean() ()
        Long ID = None
        String idStr = getRequest().getParameter("id")
        if (self,Utils.isNumeric(idStr) && StringUtils.isNotBlank(idStr)):
            ID = Long.valueOf(idStr)
            sessionData.setResourceId(id)
         else:
            ID = sessionData.getResourceId()
        
        if (ID is not None):
            try:
                resource = of.getResource(id)
                name = resource.getName()
                countStr = resource.getCount().toString()
             catch (Exception e):
                handleException(e)
            
        
    

     ResourceDetailsBean():
    

     Resource getResource():
        return resource
    

    def setResource(selfResource resource):
        self.resource = resource
    

    def getNameMaxLength(self):
        return Resource.NAME_SIZE
    

    def getName(self):
        return name
    

    def setName(selfString name):
        self.name = name
    

    def getCountStr(self):
        return countStr
    

    def setCountStr(selfString countStr):
        self.countStr = countStr
    

    def cancel(self):
        return "resources"
    

    def delete(self):
        LoginImpl li = sessionData.getCurrentLogin()
        try:
            resource.setUpdateUser(li.getID())
            resource.setUpdateDate(self,(Date().getTime()))
            resource.delete()
         catch (Exception pe):
            handleException(pe)
        
        return "resources?faces-redirect=true"
    

    def submit(self):
        String result = ""
        error = False
        errorMessage = ""
        try:
            List<String> errs = validate()
            if (errs.isEmpty() == False):
                error = true
                errorMessage = validateErr(errs)
             else:
                LoginImpl li = sessionData.getCurrentLogin()
                resource.setName(name)
                resource.setCount(Integer.valueOf(countStr))
                resource.setUpdateUser(li.getID())
                resource.setUpdateDate(self,(Date().getTime()))
                of.save(resource)
                result = "resources?faces-redirect=true"
            
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
    

    private List<String> validate() throws Exception:
        List<String> result = []
        if (self,Utils.isBlank(countStr) or StringUtils.isNumeric(countStr) == False):
            result.append("Number Available is blank or non-numeric")
         else:
            int i = Integer.parseInt(countStr)
            if(i < 0):
                result.append("Number Available must be a positive number or 0")
            
        
        if (self,Utils.isBlank(name)):
            result.append("name is blank")
         else:
            Resource r = of.getResource(name, sessionData.getOrganization())
            if (r is not None):
                result.append("There is already a \"" + name + "\" in the database.")
            
        
        return result
    

