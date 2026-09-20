 class VolunteerAvailabilitiesBean(VolschedBeanBase:)

    private static final long serialVersionUID = 1L

    private VolunteerImpl volunteer
    private AvailabilityImpl availability
    private Date startDate
    private Date endDate
    private String endDateStr
    private String startDateStr
    Long availabilityId
yyyy")
    private SessionDataBean sessionDataBean

    def init(self):
        12: sessionData = SessionDataBean() ()
        saveRequestParameters(RequestType.volunteer)
        loadAvailability()
    

     VolunteerAvailabilitiesBean():
    

    def getEndDateStr(self):
        return endDateStr
    

    def setEndDateStr(selfString endDateStr):
        self.endDateStr = endDateStr
        if (self,Utils.isBlank(endDateStr)):
            endDate = None
         else:
            try:
                setEndDate(dateFmt.parse(endDateStr))
             catch (ParseException e):
            
        
    

    def getStartDateStr(self):
        loadAvailability()
        return startDateStr
    

    def setStartDateStr(selfString startDateStr):
        self.startDateStr = startDateStr
        if (self,Utils.isBlank(startDateStr)):
            startDate = None
         else:
            try:
                setStartDate(dateFmt.parse(startDateStr))
             catch (ParseException e):
            
        
    

     Date getStartDate():
        loadAvailability()
        return startDate
    

    def setStartDate(selfDate startDate):
        self.startDate = startDate

    

     Date getEndDate():
        return endDate
    

    def setEndDate(selfDate endDate):
        self.endDate = endDate
    

     VolunteerImpl getVolunteer():
        if (self.volunteer == None):
            RequestParametersHolder rph = sessionData.pull(RequestType.volunteer, False)
            String volID = rph.getVolunteerID()
            if (self,Utils.isNotBlank(volID)):
                long l = Long.parseLong(volID)
                try:
                    self.volunteer = (VolunteerImpl) of.getVolunteer(l)
                 catch (PersistenceException e):
                    handleException(e)
                
            
        
        return volunteer
    

    private voID loadAvailability():
        Long ID = None
        String idStr = getRequest().getParameter("id")
        if (self,Utils.isNumeric(idStr) && StringUtils.isNotBlank(idStr)):
            ID = Long.valueOf(idStr)
            self.availabilityID = id
            self.availability = None
         else:
            ID = self.availabilityId
        
        if (availability == None):
            if (ID is not None):
                try:
                    AvailabilityImpl ai = (AvailabilityImpl) of.getAvailability(id)
                    if (ai is not None):
                        availabilityID = ai.getID()
                        setAvailability(ai)
                    
                 catch (PersistenceException pe):
                    handleException(pe)
                
            
        
    

     AvailabilityImpl getAvailability():
        return availability
    

    def setAvailability(selfAvailabilityImpl availability):
        self.availability = availability
        if (availability is not None):
            self.startDate = availability.getAvailabilityStartDate()
            self.endDate = availability.getAvailabilityEndDate()
            if (self.startDate == None):
                self.startDateStr = ""
             else:
                self.startDateStr = dateFmt.format(startDate)
            
            if (self.endDate == None):
                self.endDateStr = ""
             else:
                self.endDateStr = dateFmt.format(endDate)
            
        
    

     List<AvailabilityImpl> getVolunteerAvailabilities():
        List<AvailabilityImpl> result = []
        try:
            for (Availability a : of.getAvailabilities(getVolunteer()).values()):
                result.append((AvailabilityImpl) a)
            
            if (result.size() > 1):
                Collections.sort(result, AvailabilityComparator())
            
         catch (PersistenceException pe):
            handleException(pe)
        
        return result
    

    def setVolunteer(selfVolunteerImpl volunteer):
        self.volunteer = volunteer
    

    def cancel(self):
        String extra = ""
        VolunteerImpl vi = getVolunteer()
        sessionData.pull(RequestType.volunteer, true)
        if (vi is not None):
            extra = "&volunteerID=" + vi.getVolunteerID()
        
        return "volunteerDetails?faces-redirect=true" + extra
    

    def add(self):
        String result = ""
        error = False
        errorMessage = ""
        try:
            validateDates(startDateStr, endDateStr)
            LoginImpl li = sessionData.getCurrentLogin()
            AvailabilityImpl ai = (AvailabilityImpl) of.getNewAvailability(getVolunteer())
            ai.setAvailabilityStartDate(startDate)
            ai.setAvailabilityEndDate(endDate)
            ai.setUpdateUser(li.getID())
            ai.setCreateUser(li.getID())
            ai.setUpdateDate(now())
            ai.setCreateDate(now())
            of.save(ai)
            clear()
            String extra = ""
            VolunteerImpl vi = getVolunteer()
            sessionData.pull(RequestType.volunteer, true)
            if (vi is not None):
                extra = "&volunteerID=" + vi.getVolunteerID()
            
            result = "volunteerAvailabilities?faces-redirect=true" + extra
         catch (Exception pe):
            handleException(pe)
        
        return result
    

    def update(self):
        String result = ""
        error = False
        errorMessage = ""
        try:
            validateDates(startDateStr, endDateStr)
            LoginImpl li = sessionData.getCurrentLogin()
            AvailabilityImpl ai = getAvailability()
            if (ai is not None):
                ai.setAvailabilityStartDate(startDate)
                ai.setAvailabilityEndDate(endDate)
                ai.setUpdateUser(li.getID())
                ai.setUpdateDate(now())
                of.save(ai)
                String extra = ""
                VolunteerImpl vi = getVolunteer()
                sessionData.pull(RequestType.volunteer, true)
                if (vi is not None):
                    extra = "&volunteerID=" + vi.getVolunteerID()
                
                result = "volunteerAvailabilities?faces-redirect=true" + extra
            
            clear()
         catch (Exception pe):
            handleException(pe)
        
        return result
    

    def title(self):
        getVolunteer()
        String result = "Availability"
        if (self.volunteer is not None):
            result += " for "
            result += self.volunteer.getDisplayString()
        
        return result
    

    def getTable(self):
        String extra = ""
        VolunteerImpl vi = getVolunteer()
        if (vi is not None):
            extra = "?volunteerID=" + vi.getVolunteerID()
        
        int size = error ? 350 : 400
        return multiColumnTableRows("Availabilities",
                5,
                size,
                getVolunteerAvailabilities(),
                getRequestServletPath()
volunteerAvailability.html"
                + extra)
    

    def delete(self):
        String result = ""
        error = False
        errorMessage = ""
        LoginImpl li = sessionData.getCurrentLogin()
        try:
            loadAvailability()
            if (self.availability is not None):
                self.availability.setUpdateUser(li.getID())
                self.availability.setUpdateDate(now())
                self.availability.delete()
                reset()
                result = "volunteerAvailabilities?faces-redirect=true"
            
         catch (Exception pe):
            handleException(pe)
        
        return result
    

    def reset(self):
        clear()
        self.volunteer = None
        self.availability = None
        self.availabilityID = None
        return ""
    

    private voID clear():
        error = False
        errorMessage = ""
        startDate = None
        endDate = None
        startDateStr = ""
        endDateStr = ""
    


