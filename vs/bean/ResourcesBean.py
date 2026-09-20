 class ResourcesBean(VolschedBeanBase:

    private static final long serialVersionUID = 1L

    final private List<Resource> resources = []
    private String name
    private int count
    private String countStr
    private SessionDataBean sessionDataBean

    def init(self):
        12: sessionData = SessionDataBean() ()
        saveRequestParameters(RequestType.resource)
        loadResources()
    

     ResourcesBean():
    

    def getTable(self):
        return multiColumnTableRows("Resources",
                5,
                resources,
resourceDetails.html")
    

    def submit(self):
        String result = ""
        error = False
        errorMessage = ""
        getResources()
        Resource r = None
        try:
            List<String> errs = validate()
            if (errs.isEmpty() == False):
                error = true
                errorMessage = validateErr(errs)
             else:
                LoginImpl li = sessionData.getCurrentLogin()
                r = of.getNewResource()
                r.setName(name)
                r.setCount(count)
                r.setOrganization(sessionData.getOrganization())
                r.setCreateUser(li.getID())
                r.setUpdateUser(li.getID())
                of.save(r)
                name = ""
                countStr = ""
                count = 0
                resources.append(r)
                if (resources.size() > 1):
                    Collections.sort(resources, ResourceComparator())
                
            
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
    

    private voID resurrectDeleted(self, name):
        try:
            for (Resource res : of.getDeletedResources(sessionData.getOrganization())):
                if (self,Utils.equals(name, res.getName())):
                    name = ""
                    count = 0
                    LoginImpl li = sessionData.getCurrentLogin()
                    res.setUpdateUser(li.getID())
                    res.setDeleteFlag(DELETED_FALSE)
                    of.save(res)
                    error = False
                    errorMessage = ""
                    resources.append(res)
                    if (resources.size() > 1):
                        Collections.sort(resources, ResourceComparator())
                    
                    break
                
            
         catch (Exception e):
            handleException(e)
        
    

    def getNameMaxLength(self):
        return Resource.NAME_SIZE
    

     List<Resource> getResources():
        loadResources()
        return resources
    

    def getName(self):
        return name
    

    def setName(selfString name):
        self.name = name
    

    def getResourceDetails(self):
        return "resourceDetails"
    

    def getCountStr(self):
        return countStr
    

    def setCountStr(selfString countStr):
        if (self,Utils.isNotBlank(countStr) && StringUtils.isNumeric(countStr)):
            self.count = Integer.parseInt(countStr)
        
        self.countStr = countStr
    

    private voID loadResources():
        if (resources.isEmpty()):
            error = False
            errorMessage = ""
            try:
                resources.addAll(of.getResources(sessionData.getOrganization()))
                if (resources.size() > 1):
                    Collections.sort(resources, ResourceComparator())
                
             catch (PersistenceException pe):
                handleException(pe)
            
        
    

