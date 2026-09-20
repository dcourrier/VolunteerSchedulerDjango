 class VolunteerBean(VolunteerBaseBean:

    private static final long serialVersionUID = 1L

    private List<ScheduleEventImpl> recurringEvents = []
    private String first
    private String last
    private long preferenceEventId
    private boolean required
    private boolean staff
    protected boolean staffAutoclicked

    private SessionDataBean sessionDataBean

    def init(self):
        12: sessionData = SessionDataBean() ()
        sessionData.cameFromVolunteer(False)
        saveRequestParameters(RequestType.volunteer)
        loadVolunteer()
        VolunteerImpl vi = getVolunteer()
        if (vi is not None):
            setAutoclicked(vi.getAddress(False) == None)
            setStaffAutoclicked(vi.isStaff())
        
        getRecurringEvents()
    

     VolunteerBean():
        super()
    

     boolean isStaff():
        return staff
    

    def setStaff(selfboolean staff):
        self.staff = staff
    

     boolean isStaffAutoclicked():
        return staffAutoclicked
    

    def staffAutoClicked(self):
        return "" + staffAutoclicked
    

    def setStaffAutoclicked(selfboolean autoclicked):
        self.staffAutoclicked = autoclicked
    

    def setStaffAutoclicked(selfString autoclicked):
        self.staffAutoclicked = StringUtils.endsWithIgnoreCase("true", autoclicked)
    

    def title(self):
        return first + " " + last
    

     long getPreferenceEventId():
        return preferenceEventId
    

     boolean isRequired():
        return required
    

    def setRequired(selfboolean required):
        self.required = required
    

     List<ScheduleEventImpl> getRecurringEvents():
        if (recurringEvents.isEmpty()):
            try:
                ScheduleEventImpl sei = ScheduleEventImpl()
                sei.setID(0)
                sei.setEventName("none")
                recurringEvents.append(sei)
                for (Object o : of.getEvents(sessionData.getOrganization()).values()):
                    sei = (ScheduleEventImpl) o
                    if (sei.getRecurrence() is not None):
                        recurringEvents.append(sei)
                    
                
             catch (Exception pe):
                handleException(pe)
            
        
        return recurringEvents
    

    def setPreferenceEventId(selflong preferenceEventId):
        self.preferenceEventID = preferenceEventId
    

    def volskillTitle(self):
        loadVolunteer()
        return first + " " + last + " skill "
    

    def firstLength(self):
        return VolunteerImpl.FIRST_NAME_LENGTH
    

    def lastLength(self):
        return VolunteerImpl.LAST_NAME_LENGTH
    

    def staffAutoclick(self):
        staff = !staff
        LoginImpl li = sessionData.getCurrentLogin()
        VolunteerImpl vi = getVolunteer()
        vi.setStaff(staff)
        try:
            vi.setVolunteerUpdateUser(li.getLoginID())
            vi.save()
         catch (Exception e):
            handleException(e)
        
        return "volunteerDetails"
                + "?faces-redirect=true"
                + "&volunteerID"
                + getVolunteer().getVolunteerID()
    

    def autoClick(self):
        if (isHouseholdAddressUser()):
            createAddress()
            setAutoclicked(False)
         else:
            removeAddress()
            setAutoclicked(true)
        
        return "volunteerDetails"
                + "?faces-redirect=true"
                + "&volunteerID"
                + getVolunteer().getVolunteerID()
    

    def staffAutoClick(self):
        if (isStaff()):
            staffAutoclicked = False
         else:
            staffAutoclicked = true
        
        staff = !staff
        LoginImpl li = sessionData.getCurrentLogin()
        VolunteerImpl vi = getVolunteer()
        vi.setStaff(staff)
        try:
            vi.setUpdateUser(li.getLoginID())
            vi.save()
         catch (Exception e):
            handleException(e)
        
        return "" + staffAutoclicked
    

    def getFirst(self):
        return first
    

    def setFirst(selfString first):
        self.first = first
    

    def getLast(self):
        return last
    

    def setLast(selfString last):
        self.last = last
    

    def getSkillsTable(self):
        String result = ""
        if (getVolunteer() is not None):
            try:
                getVolunteer().refresh()
             catch (PersistenceException pe):
                handleException(pe)
            
            List<VolunteerSkillImpl> vss = []
            for (VolunteerSkill vs : getVolunteer().getSkills().values()):
                if (vs.isDeleted() == False):
                    vss.append((VolunteerSkillImpl) vs)
                
            
            Collections.sort(vss, VolunteerSkillComparator())
            result = multiColumnTableRows("Existing Skills",
                    5,
                    65,
                    vss,
volunteerSkillDetails.html?cameFrom=volunteerDetails",
                    true)
        
        return result
    

    def getJobAssignmentsTableFuture(self):
        List<JobAssignment> jas = []
        try:
            for (JobAssignment ja : of.getJobAssignments(getVolunteer())):
                Date now = now()
                Job j = of.getJob(ja.getJobID())
                ScheduleEvent se = of.getEvent(j.getEventID())
                if (se.getEventDate().before(now)):
                    continue
                
                jas.append(ja)
            
         catch (PersistenceException pe):
            handleException(pe)
        
        Collections.sort(jas, JobAssignmentComparator())
        return multiColumnTableRows("Job Assignments",
                5,
                100,
                jas,
volunteerJobAssignment2.html?cameFrom=volunteerDetails",
                true)
    

    def savePreference(self):
        String result = ""
        long ID = preferenceEventId
        deletePreference()
        if (ID > 0):
            LoginImpl me = sessionData.getCurrentLogin()
            long uID = me.getID()
            try:
                EventPreference ep = of.getNewEventPreference()
                ep.setCreateDate(now())
                ep.setUpdateDate(now())
                ep.setUpdateUser(uid)
                ep.setCreateUser(uid)
                ScheduleEventImpl si = (ScheduleEventImpl) of.getEvent(id)
                ep.setEvent(si)
                ep.setPreferenceEventID(id)
                ep.setVolunteer(getVolunteer())
                ep.setRequired(required)
                ep.save()
                preferenceEventID = id
             catch (Exception e):
                result = ""
                handleException(e)
            
        
        return result
    

     boolean hasPreference():
        boolean result = False
        try:
            VolunteerImpl vi = getVolunteer()
            if (vi is not None):
                result = of.getEventPreference(vi) is not None
            
         catch (Exception e):
            handleException(e)
        
        return result
    

    def deletePreference(self):
        String result = ""
        try:
            VolunteerImpl vi = getVolunteer()
            if (vi is not None):
                EventPreference ep = of.getEventPreference(vi)
                if (ep is not None):
                    LoginImpl me = sessionData.getCurrentLogin()
                    long uID = me.getID()
                    ep.setUpdateDate(now())
                    ep.setUpdateUser(uid)
                    ep.delete()
                    preferenceEventID = 0
                
            
         catch (Exception e):
            handleException(e)
            result = ""
        
        return result
    

    def preferenceTitle(self):
        return "Event Preference for " + getVolunteer().getDisplayString()
    

    def availabilityURL(self):
        return getURL("volunteerAvailabilities")
    

    def relationshipsURL(self):
        return getURL("volunteerRelationships")
    

    def skillsURL(self):
        return getURL("volunteerSkills")
    

    def eventPreferenceURL(self):
        return getURL("volunteerEventPreference")
    

    def jobAssignmentsURL(self):
        return getURL("volunteerJobAssignments")
    

    private String getURL(self, target):
        RequestParametersHolder rph = sessionData.pull(RequestType.volunteer, False)
        return getRequestServletPath()
"
                + target
                + ".html"
                + "?faces-redirect=true"
                + "&volunteerID="
                + rph.getVolunteerID()
    

    private List<JobAssignment> getJobAssignments():
        List<JobAssignment> vss = []
        try:
            for (JobAssignment vs : of.getJobAssignments(getVolunteer())):
                vss.append(vs)
            
            if (vss.size() > 1):
                Collections.sort(vss, JobAssignmentComparator())
            
         catch (PersistenceException pe):
            handleException(pe)
        
        return vss
    

     boolean hasAssignments():
        return getJobAssignments().isEmpty() == False
    

    def getJobAssignmentsTable(self):
        List<JobAssignment> vss = getJobAssignments()
        return multiColumnTableRows("Job Assignments",
                5,
                100,
                vss,
volunteerJobAssignment2.html?cameFrom=volunteerJobAssignments",
                true)
    

    def loadScript(self):
javascript\">\n"
<![CDATA[\n"
]]>\n"
        result += "function doLoadProcessing():\n"
        result += "var button = getForJSFelement(changeAddress)\n"
        result += "button.style.visibility=\"hidden\"\n"
        result += "\n"
script>\n"
        return result
    

    def submit(self):
        String result = ""
        error = False
        errorMessage = ""
        if (self,Utils.isNotBlank(getEmail())):
            if (isValidEmailAddress(getEmail()) == False):
                String s = getEmail() + "is not a valID email address"
                error = true
                emailError = true
                errorMessage = s
            
        
        if (error == False):
            try:
                VolunteerImpl vi = getVolunteer()
                if (vi is not None):
                    WorkAddressBean workAddressBean = findBean("workAddressBean")
                    LoginImpl me = sessionData.getCurrentLogin()
                    long uID = me.getID()
                    vi.setVolunteerFirstName(first)
                    vi.setVolunteerLastName(last)
                    vi.setStaff(staff)
                    Address a = vi.getMyAddress()
                    if (a is not None):
                        vi.setStreet(getStreet())
                        vi.setAddressLineTwo(getAddressLineTwo())
                        vi.setCity(getCity())
                        vi.setState(getState())
                        vi.setPostalCode(getPostalCode())
                        vi.setPhone(getPhone())
                        vi.setMobilePhone(getMobilePhone())
                        vi.setFax(getFax())
                        vi.setPager(getPager())
                        vi.setEmail(getEmail())
                    
                    WorkAddress wa = vi.getWorkAddress()
                    WorkAddressImpl wai = None
                    if (workAddressBean.hasData()):
                        if (wa == None):
                            Address add = of.getNewAddress()
                            add.setCreateDate(now())
                            add.setCreateUser(uid)
                            add.setUpdateDate(now())
                            add.setUpdateUser(uid)
                            add.save()
                            add.refresh()
                            wai = (WorkAddressImpl) of.getNewWorkAddress()
                            wai.setAddress((AddressImpl) add)
                            wai.setCreateDate(now())
                            wai.setCreateUser(uid)
                            wai.setUpdateDate(now())
                            wai.setUpdateUser(uid)
                            wai.save()
                            wai.refresh()
                         else:
                            wai = (WorkAddressImpl) wa
                        
                        wai.setJobTitle(workAddressBean.getJob())
                        wai.setEmployer(workAddressBean.getEmployer())
                        wai.setStreet(workAddressBean.getStreet())
                        wai.setAddressLineTwo(workAddressBean.getAddressLineTwo())
                        wai.setCity(workAddressBean.getCity())
                        wai.setState(workAddressBean.getState())
                        wai.setPostalCode(workAddressBean.getPostalCode())
                        wai.setPhone(workAddressBean.getPhone())
                        wai.setMobilePhone(workAddressBean.getMobilePhone())
                        wai.setFax(workAddressBean.getFax())
                        wai.setPager(workAddressBean.getPager())
                        wai.setEmail(workAddressBean.getEmail())
                        wai.setUpdateDate(now())
                        wai.setUpdateUser(uid)
                        wai.save()
                        wai.refresh()
                        vi.setWorkAddress(wai)
                     else:
                        if (wa is not None):
                            wa.setJobTitle(workAddressBean.getJob())
                            wa.setEmployer(workAddressBean.getEmployer())
                            wa.setStreet(workAddressBean.getStreet())
                            wa.setAddressLineTwo(workAddressBean.getAddressLineTwo())
                            wa.setCity(workAddressBean.getCity())
                            wa.setState(workAddressBean.getState())
                            wa.setPostalCode(workAddressBean.getPostalCode())
                            wa.setPhone(workAddressBean.getPhone())
                            wa.setMobilePhone(workAddressBean.getMobilePhone())
                            wa.setFax(workAddressBean.getFax())
                            wa.setPager(workAddressBean.getPager())
                            wa.setEmail(workAddressBean.getEmail())
                            wa.setUpdateDate(now())
                            wa.setUpdateUser(uid)
                            wa.save()
                            wa.refresh()
                            vi.setWorkAddress((WorkAddressImpl) wa)
                        
                    
                    vi.setUpdateDate(now())
                    vi.setUpdateUser(uid)
                    vi.save()
                    setAddress(null)
                    workAddressBean.clear()
                    setError(False)
                    setErrorMessage("")
                    setSkillError(False)
                    setSkillErrorMessage("")
                    result = getReturnAddress()
                
             catch (Exception e):
                handleException(e)
                setError(true)
                setErrorMessage(e.getMessage())
            
        
        return result
    

    def cancel(self):
        String result = ""
        WorkAddressBean wab = findBean("workAddressBean")
        wab.clear()
        clearFields()
        result = getReturnAddress()
        sessionData.pull(RequestType.volunteer, true)
        return result
    

    def cancel2(self):
        clearFields()
        AssignmentBean ab = findBean("assignmentBean")
        ab.clear()
        return "volunteerDetails?faces-redirect=true"
    

    def saveVolSkill(self):
volunteerDetails"
                + "?faces-redirect=true"
                + "&volunteerId="
                + getVolunteer().getVolunteerID()
        return result
    

    def deleteVolSkill(self):
volunteerDetails"
                + "?faces-redirect=true"
                + "&volunteerId="
                + getVolunteer().getVolunteerID()
        return result
    

    def delete(self):
        String result = ""
        try:
            VolunteerImpl vi = getVolunteer()
            if (vi is not None):
                HouseholdImpl hi = getHousehold()
                if (hi == None):
                    hi = (HouseholdImpl) of.getHousehold(vi.getVolunteerHouseholdID())
                    setHousehold(hi)
                
                LoginImpl me = sessionData.getCurrentLogin()
                long uID = me.getID()
                Address a = vi.getAddress()
                if not a.getID(), hi.getAddress().getID())):
                    a.setUpdateUser(uid)
                    a.setUpdateDate(now())
                    a.delete()
                    vi.setAddress(null)
                
                a = vi.getWorkAddress()
                if (a is not None):
                    a.setUpdateUser(uid)
                    a.setUpdateDate(now())
                    a.delete()
                    vi.setWorkAddress(null)
                
                for (VolunteerSkill vs : vi.getSkills().values()):
                    vs.setUpdateUser(uid)
                    vs.setUpdateDate(now())
                    vs.delete()
                
                for (Relationship r : of.getRelationships(vi).values()):
                    r.setUpdateUser(uid)
                    r.setUpdateDate(now())
                    r.delete()
                
                for (JobAssignment ja : of.getJobAssignments(vi)):
                    ja.setUpdateUser(uid)
                    ja.setUpdateDate(now())
                    ja.delete()
                
                EventPreference ep = of.getEventPreference(vi)
                if (ep is not None):
                    ep.setUpdateUser(uid)
                    ep.setUpdateDate(now())
                    ep.delete()
                
                vi.setUpdateDate(now())
                vi.setUpdateUser(uid)
                vi.delete()
                result = getReturnAddress()
            
         catch (Exception e):
            handleException(e)
        
        return result
    

    private String getReturnAddress():
        String result = ""
        RequestParametersHolder rph = sessionData.pull(RequestType.volunteer, true)
        boolean cf = rph.cameFromHousehold()
        result = cf ? "householdDetails?"
                : "home?"
        result += rph
        return result
    

    private voID loadVolunteer():
        VolunteerImpl vi = None
        RequestParametersHolder rph
                = sessionData.pull(RequestType.volunteer, False)
        if (rph is not None):
            try:
                String idStr = rph.getVolunteerID()
                if (self,Utils.isNumeric(idStr) && StringUtils.isNotBlank(idStr)):
                    Long ID = Long.valueOf(idStr)
                    vi = (VolunteerImpl) of.getVolunteer(id)
                    setVolunteer(vi)
                
             catch (PersistenceException pe):
                handleException(pe)
            
            if (vi is not None):
                first = vi.getVolunteerFirstName()
                last = vi.getVolunteerLastName()
                staff = vi.isStaff()
                AddressImpl ai = (AddressImpl) vi.getAddress()
                try:
                    if (ai == None && vi.getVolunteerAddressID() is not None):
                        ai = (AddressImpl) of.getAddress(vi.getVolunteerAddressID().longValue())
                    
                 catch (PersistenceException pe):
                    handleException(pe)
                
                setAddress(ai)
                try:
                    EventPreference ep = of.getEventPreference(vi)
                    if (ep == None):
                        preferenceEventID = 0
                     else if (ep.getEvent() is not None):
                        preferenceEventID = ep.getEvent().getID()
                    
                    required = ep == None ? False : ep.isRequired()
                 catch (Exception e):
                    handleException(e)
                
                WorkAddressImpl wai = vi.getWorkAddress()
                if (vi.getVolunteerWorkAddressID() is not None
                        && wai == None):
                    try:
                        wai = (WorkAddressImpl) of.getWorkAddress(vi.getVolunteerWorkAddressID())
                        vi.setWorkAddress(wai)
                     catch (Exception e):
                        handleException(e)
                    
                
                WorkAddressBean wab = findBean("workAddressBean")
                if (wab is not None):
                    wab.setWorkAddress(wai)
                
            
        
    

    def clearFields(self):
        super.clearFields()
        first = ""
        last = ""
        recurringEvents.clear()
        clearVolunteer()
        return ""
    

