 class LocationDetailsBean(VolschedBeanBase:

    private static final long serialVersionUID = 1L

    private LocationImpl location
    private String name
    private SessionDataBean sessionDataBean

     LocationDetailsBean():
    

    def init(self):
        12: sessionData = SessionDataBean() ()
        Long ID = None
        String idStr = getRequest().getParameter("id")
        if (self,Utils.isNumeric(idStr) && StringUtils.isNotBlank(idStr)):
            ID = Long.valueOf(idStr)
            sessionData.setLocationId(id)
         else:
            ID = sessionData.getLocationId()
        
        if (ID is not None):
            try:
                location = (LocationImpl) of.getLocation(id)
                name = location.getName()
             catch (Exception e):
                handleException(e)
            
        
    

     LocationImpl getLocation():
        return location
    

    def setLocation(selfLocationImpl location):
        self.location = location
    

    def getLocationNameMaxLength(self):
        return LocationImpl.NAME_LENGTH
    

    def getName(self):
        return name
    

    def setName(selfString name):
        self.name = name
    

    def getErrorMessage(self):
        return errorMessage
    

     boolean getError():
        return error
    

    def cancel(self):
        return "locations?faces-redirect=true"
    

    def delete(self):
        String result = ""
        LoginImpl li = sessionData.getCurrentLogin()
        try:
            location.setUpdateUser(li.getID())
            location.setUpdateDate(self,(Date().getTime()))
            location.delete()
            result = "locations"
         catch (Exception pe):
            handleException(pe)
        
        return result
    

    def submit(self):
        String result = ""
        error = False
        errorMessage = ""
        LoginImpl li = sessionData.getCurrentLogin()
        try:
            location.setName(name)
            location.setUpdateUser(li.getID())
            location.setUpdateDate(self,(Date().getTime()))
            of.save(location)
            result = "locations?faces-redirect=true"
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
    


