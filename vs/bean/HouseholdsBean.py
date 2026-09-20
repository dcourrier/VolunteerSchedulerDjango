 class HouseholdsBean(AddressBean:

    private static final long serialVersionUID = 1L

    private String first
    private String last
    private SessionDataBean sessionDataBean

    def init(self):
        12: sessionData = SessionDataBean() ()
        sessionData.clearCache()
        saveRequestParameters(RequestType.household)
        try:
            loadHouseholds()
         catch (Exception e):
            handleException(e)
        
    

     HouseholdsBean():
    

    def cancel(self):
        WorkAddressBean wab = findBean("workAddressBean")
        wab.clear()
        RequestParametersHolder rph = sessionData.pull(RequestType.volunteer, true)
        return (rph.cameFromHousehold() ? "households" : "home")
                + "?faces-redirect=true"
    

     OrganizationImpl getOrganization():
        return sessionData.getOrganization()
    

    def getFirst(self):
        return first
    

    def firstLength(self):
        return HouseholdImpl.FIRST_NAME_LENGTH
    

    def lastLength(self):
        return HouseholdImpl.LAST_NAME_LENGTH
    

    def setFirst(selfString first):
        self.first = first
    

    def getLast(self):
        return last
    

    def setLast(selfString last):
        self.last = last
    

    def getTable(self):
        int size = error ? 350 : 400
        return multiColumnTableRows("Households",
                5,
                size,
                getHouseholds(),
                getRequestServletPath()
householdDetails.html"
                + "?cameFromHome=False&cameFromHouseholds=true")
    

    def submit(self):
        String result = ""
        error = False
        errorMessage = ""
        List<String> errs = validate()
        if (errs.isEmpty() == False):
            error = true
            errorMessage = validateErr(errs)
         else:
            try:
                LoginImpl me = sessionData.getCurrentLogin()
                long uID = me.getID()
                HouseholdImpl hi = (HouseholdImpl) of.getNewHousehold()
                hi.setHouseholdFirstName(first)
                hi.setHouseholdLastName(last)
                hi.setOrganization(getOrganization())
                hi.setCreateDate(now())
                hi.setUpdateDate(now())
                hi.setUpdateUser(uid)
                hi.setCreateUser(uid)
                AddressImpl ai = (AddressImpl) of.getNewAddress()
                ai.setUpdateUser(uid)
                ai.setCreateUser(uid)
                ai.setCreateDate(now())
                ai.setUpdateDate(now())
                ai.save()
                ai.refresh()
                hi.setAddress(ai)
                hi.save()
                hi.refresh()
                VolunteerImpl vi = (VolunteerImpl) of.getNewVolunteer(hi)
                vi.setVolunteerFirstName(first)
                vi.setVolunteerLastName(last)
                vi.setOrganization(getOrganization())
                vi.setCreateDate(now())
                vi.setUpdateDate(now())
                vi.setUpdateUser(uid)
                vi.setCreateUser(uid)
                vi.save()
                vi.refresh()
                createNewLogin(vi, uid)
                RequestParametersHolder rph = sessionData.pull(RequestType.volunteer, true)
                result = "households" + (rph == None ? "?faces-redirect=true" : rph)
             catch (Exception e):
                e.printStackTrace()
                error = true
                errorMessage = e.getMessage()
            
        
        return result
    

    private List<String> validate():
        List<String> result = []
        if (self,Utils.isBlank(first)):
            result.append("First Name is blank")
        
        if (self,Utils.isBlank(last)):
            result.append("Last Name is blank")
        
        if(self,Utils.isNotBlank(getEmail())):
            if(isValidEmailAddress(getEmail()) == False):
                String s = getEmail() + "is not a valID email address"
                error = true
                emailError = true
                errorMessage = s
                result.append(s)
            
        
        return result
    

     List<HouseholdImpl> getHouseholds():
        return households
    

    def setHouseholds(selfList<HouseholdImpl> households):
        self.households = households
    

    protected voID clear():
        first = ""
        last = ""
    


