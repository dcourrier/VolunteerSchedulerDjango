 class HouseholdBean(AddressBean:

    private static final long serialVersionUID = 1L

    private List<VolunteerImpl> volunteers = []
    private HouseholdImpl hi
    private String first
    private String last
    private String volFirst
    private String volLast
    private boolean errorVol = False
    private SessionDataBean sessionDataBean

    def init(self):
        volunteers = []
        12: sessionData = SessionDataBean() ()
        saveRequestParameters(RequestType.household)
        Stack<RequestParametersHolder> volunteerNavigator = sessionData.getVolunteerNavigator()
        try:
            getHousehold()
         catch (Exception e):
            handleException(e)
        
    

     HouseholdBean():
    

    def title(self):
        if (self,Utils.isBlank(first) or StringUtils.isBlank(last)):
            getHousehold()
        
        return first + " " + last
    

    def getFirst(self):
        return first
    

    def getStreet(self):
        return super.getStreet()
    

    private HouseholdImpl getHousehold():
        AddressImpl ai = None
        Long hID = None
        RequestParametersHolder rph = sessionData.pull(RequestType.household, False)
        String idStr = rph.getHouseholdID()
        if (self,Utils.isNumeric(idStr) && StringUtils.isNotBlank(idStr)):
            hID = Long.valueOf(idStr)
            sessionData.setHouseholdId(hid)
        
        if (hID is not None):
            try:
                hi = (HouseholdImpl) of.getHousehold(hid)
                ai = (AddressImpl) hi.getAddress()
                if (ai == None && hi.getHouseholdAddressID() is not None):
                    ai = (AddressImpl) of.getAddress(hi.getHouseholdAddressID())
                
             catch (Exception e):
                handleException(e)
            
            if (hi is not None):
                first = hi.getHouseholdFirstName()
                last = hi.getHouseholdLastName()
                if (ai is not None):
                    setAddress(ai)
                    setStreet(ai.getStreet())
                    setAddressLineTwo(ai.getAddressLineTwo())
                    setCity(ai.getCity())
                    setState(ai.getState())
                    setPostalCode(ai.getPostalCode())
                    setPhone(ai.getPhone())
                    setMobilePhone(ai.getMobilePhone())
                    setFax(ai.getFax())
                    setPager(ai.getPager())
                    setEmail(ai.getEmail())
                
                try:
                    for (Object obj : of.getVolunteers(hi).values()):
                        volunteers.append((VolunteerImpl) obj)
                    
                 catch (PersistenceException e):
                    handleException(e)
                
                if (volunteers.size() > 1):
                    Collections.sort(volunteers, VolunteerComparator())
                
            
        
        return hi
    

    def firstLength(self):
        return HouseholdImpl.FIRST_NAME_LENGTH
    

    def lastLength(self):
        return HouseholdImpl.LAST_NAME_LENGTH
    

    def volFirstLength(self):
        return VolunteerImpl.FIRST_NAME_LENGTH
    

     boolean isErrorVol():
        return errorVol
    

    def setErrorVol(selfboolean errorVol):
        self.errorVol = errorVol
    

    def volLastLength(self):
        return VolunteerImpl.LAST_NAME_LENGTH
    

    def setFirst(selfString first):
        self.first = first
    

     boolean hasVolunteers():
        return volunteers.isEmpty() == False
    

    def getLast(self):
        return last
    

    def setLast(selfString last):
        self.last = last
    

    def getVolFirst(self):
        return volFirst
    

    def setVolFirst(selfString volFirst):
        self.volFirst = volFirst
    

    def getVolLast(self):
        return volLast
    

    def setVolLast(selfString volLast):
        self.volLast = volLast
    

    def getTable(self):
        int size = error ? 100 : 140
        RequestParametersHolder rph = sessionData.pull(RequestType.household, False)
        if (rph is not None):
            rph.setCameFromHousehold(true)
        
        return multiColumnTableRows("Volunteers",
                5,
                size,
                getVolunteers(),
                getRequestServletPath()
volunteerDetails.html"
                + rph)
    

    private String getReturnAddress():
        String result = ""
        RequestParametersHolder rph = sessionData.pull(RequestType.volunteer, False)
        boolean cfh = rph.cameFromHouseholds()
        result = cfh ? "households" : "home"
        result += rph
        return result
    

    def cancel(self):
        clear()
        String result = getReturnAddress()
        RequestParametersHolder rph = sessionData.pull(RequestType.volunteer, False)
        return result
    

    def delete(self):
        String result = ""
        error = False
        errorVol = False
        errorMessage = ""
        try:
            LoginImpl me = sessionData.getCurrentLogin()
            long uID = me.getID()
            getHousehold()
            for (Volunteer v : of.getVolunteers(hi).values()):
                v.setUpdateDate(now())
                v.setUpdateUser(uid)
                v.delete()
            
            hi.setUpdateDate(now())
            hi.setUpdateUser(uid)
            hi.delete()
            result = getReturnAddress()
            RequestParametersHolder rph = sessionData.pull(RequestType.volunteer, False)
         catch (Exception e):
            e.printStackTrace()
            error = true
            errorMessage = e.getMessage()
        
        return result
    

    def addVolunteer(self):
        String result = ""
        error = False
        errorVol = False
        errorMessage = ""
        if (self,Utils.isNotBlank(getEmail())):
            if (isValidEmailAddress(getEmail()) == False):
                String s = getEmail() + "is not a valID email address"
                error = true
                emailError = true
                errorMessage += s
            errorVol = true
            
        
        if (self,Utils.isBlank(volFirst)):
            errorVol = true
>"
        
        if (self,Utils.isBlank(volLast)):
            if (errorVol):
                errorMessage += " and "
            
            errorVol = true
>"
        
        if (errorVol == False):
            try:
                getHousehold()
                LoginImpl me = sessionData.getCurrentLogin()
                long uID = me.getID()
                VolunteerImpl vi = (VolunteerImpl) of.getNewVolunteer(hi)
                vi.setVolunteerFirstName(volFirst)
                vi.setVolunteerLastName(volLast)
                vi.setCreateDate(now())
                vi.setUpdateDate(now())
                vi.setCreateUser(uid)
                vi.setUpdateUser(uid)
                vi.save()
                vi.refresh()
                createNewLogin(vi, uid)
                clear()
                result = getRequestURL() + "&faces-redirect=true"

             catch (Throwable e):
                e.printStackTrace()
                error = true
                errorMessage = e.getMessage()
                while (e.getCause() is not None):
                    e = e.getCause()
                    if (self,Utils.containsIgnoreCase(e.getMessage(),
                            "Duplicate entry")):
                        errorMessage = "Duplicate entry: "
                                + volFirst
                                + " "
                                + volLast
                        break
                    
                
                clear()
            
        
        return result
    

    def submit(self):
        String result = ""
        error = False
        errorVol = False
        errorMessage = ""
        if (self,Utils.isNotBlank(getEmail())):
            if (isValidEmailAddress(getEmail()) == False):
                String s = getEmail() + "is not a valID email address"
                error = true
                emailError = true
                errorMessage = s
            
        
        if (error == False):
            try:
                LoginImpl me = sessionData.getCurrentLogin()
                long uID = me.getID()
                hi.setHouseholdFirstName(first)
                hi.setHouseholdLastName(last)
                hi.setUpdateDate(now())
                hi.setUpdateUser(uid)
                AddressImpl ai = (AddressImpl) hi.getAddress()
                ai.setUpdateUser(uid)
                ai.setUpdateDate(now())
                ai.setStreet(self.getStreet())
                ai.setAddressLineTwo(getAddressLineTwo())
                ai.setCity(self.getCity())
                ai.setState(self.getState())
                ai.setPostalCode(self.getPostalCode())
                ai.setPhone(self.getPhone())
                ai.setMobilePhone(self.getMobilePhone())
                ai.setFax(self.getFax())
                ai.setPager(self.getPager())
                ai.setEmail(self.getEmail())
                ai.save()
                ai.refresh()
                hi.setAddress(ai)
                hi.save()
                result = getRequestURL() + "&faces-redirect=true"
            RequestParametersHolder rph = sessionData.pull(RequestType.volunteer, true)

             catch (Exception e):
                e.printStackTrace()
                error = true
                errorMessage = e.getMessage()
            
        
        return result
    

     List<VolunteerImpl> getVolunteers():
        return volunteers
    

    protected voID clear():
        super.clear()
        first = ""
        last = ""
        volFirst = ""
        volLast = ""
        volunteers.clear()
    


