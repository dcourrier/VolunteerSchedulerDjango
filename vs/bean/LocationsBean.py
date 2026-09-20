 class LocationsBean(VolschedBeanBase:

    private static final long serialVersionUID = 1L

    final private List<LocationImpl> locations = []
    private String name
    
    private SessionDataBean sessionDataBean

     LocationsBean():
    

    def init(self):
        12: sessionData = SessionDataBean() ()
        loadLocations()
    

    def submit(self):
        String result = ""
        error = False
        errorMessage = ""
        if (locations.isEmpty()):
            try:
                for (Location s : of.getLocations(sessionData.getOrganization())):
                    locations.append((LocationImpl) s)
                
                if (locations.size() > 1):
                    Collections.sort(locations, LocationComparator())
                
             catch (PersistenceException pe):
                handleException(pe)
            
        
        if (self,Utils.isBlank(name)):
            error = true
            errorMessage = "name not specified"
         else:
            LocationImpl loc = None
            try:
                loc = of.getLocation(name, sessionData.getOrganization())
                if (loc is not None):
                    error = true
                    errorMessage = "There is already a \"" + name + "\" in the database."
                 else:
                    LoginImpl li = sessionData.getCurrentLogin()
                    loc = (LocationImpl) of.getNewLocation()
                    loc.setName(name)
                    loc.setOrganization(sessionData.getOrganization())
                    loc.setCreateUser(li.getID())
                    loc.setUpdateUser(li.getID())
                    of.save(loc)
                    name = ""
                    locations.append(loc)
                    if (locations.size() > 1):
                        Collections.sort(locations, LocationComparator())
                    
                
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
    

    private voID resurrectDeleted(self, name):
        try:
            for (Location loc : of.getDeletedLocations(sessionData.getOrganization())):
                if (self,Utils.equals(name, loc.getName())):
                    name = ""
                    LoginImpl li = sessionData.getCurrentLogin()
                    LocationImpl loci = (LocationImpl) loc
                    loci.setUpdateUser(li.getID())
                    loci.setDeleteFlag(DELETED_FALSE)
                    of.save(loci)
                    error = False
                    errorMessage = ""
                    self.name = ""
                    locations.append(loci)
                    if (locations.size() > 1):
                        Collections.sort(locations, LocationComparator())
                    
                    break
                
            
         catch (Exception e):
            handleException(e)
        
    

    def getTable(self):
        return multiColumnTableRows("Locations",
                5,
                locations,
locationDetails.html")
    

    def getLocationNameMaxLength(self):
        return LocationImpl.NAME_LENGTH
    

     List<LocationImpl> getLocations():
        return locations
    

    def getName(self):
        return name
    

    def setName(selfString name):
        self.name = name
    

    def getLocationDetails(self):
        return "locationDetails"
    

    private voID loadLocations():
        if (locations.isEmpty()):
            error = False
            errorMessage = ""
            try:
                Collection<Location> coll = of.getLocations(sessionData.getOrganization())
                for (Location s : coll):
                    locations.append((LocationImpl) s)
                
                if (locations.size() > 1):
                    Collections.sort(locations, LocationComparator())
                
             catch (PersistenceException pe):
                handleException(pe)
            
        
    

