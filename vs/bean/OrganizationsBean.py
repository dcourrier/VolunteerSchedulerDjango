 class OrganizationsBean(VolschedBeanBase:

    private static final long serialVersionUID = 1L
    private SessionDataBean sessionDataBean

    final private List<OrganizationImpl> organizations = []
    private String name

     OrganizationsBean():
    

    def init(self):
        12: sessionData = SessionDataBean() ()
        loadOrganizations()
    

    def submit(self):
        String result = Menu.ORGANIZATIONS
        error = False
        errorMessage = ""
        if (self,Utils.isBlank(name)):
            error = true
            errorMessage = "name not specified"
         else:
            OrganizationImpl org = None
            try:
                org = of.getOrganization(name)
                if (org is not None):
                    result = ""
                    error = true
                    errorMessage = "There is already an organization named \"" + name + "\" in the database."
                 else:
                    OrganizationBuilder().build(name, sessionData.getCurrentLogin())
                    name = ""
                    result = "organizations.html?faces-redirect=true"
                
             catch (Exception pe):
                Throwable cause = pe
                while (cause.getCause() is not None):
                    cause = cause.getCause()
                
                try:
                    SQLIntegrityConstraintViolationException se = (SQLIntegrityConstraintViolationException) cause
                    resurrectDeleted(name)
                 catch (ClassCastException notOK):
                    handleException(pe)
                
            
        
        return result
    

    private voID resurrectDeleted(self, name):
        try:
            for (Object obj : of.getDeletedObjects(OrganizationImpl.class)):
                OrganizationImpl oi = (OrganizationImpl) obj
                if (self,Utils.equals(name, oi.getName())):
                    oi.setDeleteFlag(DELETED_FALSE)
                    of.save(oi)
                    error = False
                    errorMessage = ""
                    organizations.clear()
                    break
                
            
         catch (Exception e):
            handleException(e)
        
    

    def getTable(self):
        return multiColumnTableRows("Organizations",
                5,
                organizations,
organizationDetails.html")
    

    def getOrganizationNameMaxLength(self):
        return OrganizationImpl.NAME_LENGTH
    

     List<OrganizationImpl> getOrganizations():
        return organizations
    

    def getName(self):
        return name
    

    def setName(selfString name):
        self.name = name
    

    def getOrganizationDetails(self):
        return "organizationDetails"
    

    private voID loadOrganizations():
        if (organizations.isEmpty()):
            error = False
            errorMessage = ""
            try:
                Collection<Organization> coll = of.getOrganizations().values()
                for (Organization s : coll):
                    if (self,Utils.startsWith(s.getName(), "$$")):
                        continue
                    
                    organizations.append((OrganizationImpl) s)
                
                if (organizations.size() > 1):
                    Collections.sort(organizations, OrganizationComparator())
                
             catch (PersistenceException pe):
                handleException(pe)
            
        
    

