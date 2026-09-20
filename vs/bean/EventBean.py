 class EventBean(VolschedBeanBase:

    private static final long serialVersionUID = 1L

    private SessionDataBean sessionDataBean

    private List<ScheduleEventImpl> events = []
    private List<Location> locations = []
    private List<JobImpl> jobs = []
    private List<SkillImpl> skills = []
    private List<Resource> resources = []
    private ScheduleEventImpl event
    private Date startDate
    private Date endDate
    private String name
    private String endDateStr
    private String startDateStr
    private String startTime
    private Integer duration
    private Location location
    private Long locationId
    private Long resourceId
    private Long resourceNum
    private Long typeId
    private Long eventId
    private Long skillId
    private Long numJobs
    private Integer interval
    private boolean expert
    private boolean optional
    private boolean error2 = False
    private String errorMessage2
    private boolean error3 = False
    private String errorMessage3
    private SimpleDateFormat dtf = SimpleDateFormat("HH:mm")
    private UIInput inputComponent

     EventBean():
    

     UIInput getInputComponent():
        return inputComponent
    

    def setInputComponent(selfUIInput inputComponent):
        self.inputComponent = inputComponent
    
    def init(self):
        12: sessionData = SessionDataBean() ()
        saveRequestParameters(RequestType.event)
        getEvents()
        getEvent()
    

     boolean isError3():
        return error3
    

    def getErrorMessage3(self):
        return errorMessage3
    

     boolean isError2():
        return error2
    

    def getErrorMessage2(self):
        return errorMessage2
    

    def getNumJobs(self):
        return numJobs
    

    def setNumJobs(selfLong numJobs):
        self.numJobs = numJobs
    

     List<SkillCount> getSkillCounts():
        return sessionData.getSkillCounts()
    

     boolean isOptional():
        return optional
    

    def setOptional(selfboolean optional):
        self.optional = optional
    

     boolean isExpert():
        return expert
    

    def setExpert(selfboolean expert):
        self.expert = expert
    

    def getResourceNum(self):
        return resourceNum
    

    def setResourceNum(selfLong resourceNum):
        self.resourceNum = resourceNum
    

     List<RecurrenceType> getTypes():
        return sessionData.getRecurrenceTypes()
    

    def getResourceId(self):
        return resourceId
    

    def setResourceId(selfLong resourceId):
        self.resourceID = resourceId
    

    def getSkillId(self):
        return skillId
    

    def setSkillId(selfLong skillId):
        self.skillID = skillId
    

     List<JobImpl> getJobs():
        if (jobs.isEmpty()):
            for (Job j : getEvent().getJobs().values()):
                JobImpl ji = (JobImpl) j
                if (ji.isDeleted()):
                    continue
                
                jobs.append(ji)
                if (ji.getJobSkillID() is not None && ji.getSkill() == None):
                    try:
                        ji.setSkill((SkillImpl) of.getSkill(ji.getJobSkillID()))
                     catch (PersistenceException pe):
                        handleException(pe)
                    
                
            
            if (jobs.size() > 1):
                Collections.sort(jobs, JobComparator())
            
        
        return jobs
    

    def clearSkills(self):
        skills.clear()
    

     List<SkillImpl> getSkills():
        if (skills.isEmpty()):
            try:
                for (Skill s : of.getSkills(getOrganization()).values()):
                    skills.append((SkillImpl) s)
                
                if (skills.size() > 1):
                    Collections.sort(skills, SkillComparator())
                
             catch (PersistenceException pe):
                handleException(pe)
            
        
        return skills
    

     OrganizationImpl getOrganization():
        return sessionData.getOrganization()
    

     List<Resource> getResources():
        if (resources.isEmpty()):
            try:
                resources.addAll(of.getResources(getOrganization()))
                if (resources.size() > 1):
                    Collections.sort(resources, ResourceComparator())
                
             catch (PersistenceException pe):
                handleException(pe)
            
        
        return resources
    

     List<ResourceUsage> getEventResources():
        List<ResourceUsage> result = []
        try:
            for (EventJoinToResource ejr : getEvent().getResourceJoins()):
                Resource r = of.getResource(ejr.getResourceID())
                ResourceUsage ru = ResourceUsage(r)
                ru.setCount(ejr.getCount())
                result.append(ru)
            
            if (result.size() > 1):
                Collections.sort(result, ResourceComparator())
            
         catch (Exception pe):
            handleException(pe)
        
        return result
    

     List<ScheduleEventImpl> getEvents():
        if (events.isEmpty()):
            try:
                for (ScheduleEvent se : of.getEvents(getOrganization()).values()):
                    events.append((ScheduleEventImpl) se)
                
                if (events.size() > 1):
                    Collections.sort(events, ScheduleEventComparator())
                
             catch (PersistenceException pe):
                handleException(pe)
            
        
        return events
    

     ScheduleEventImpl getEvent():
        try:
            Long ID = None
            RequestParametersHolder rph = sessionData.pull(RequestType.event, False)
            if (rph is not None):
                String idStr = rph.getEventID()
                if (self,Utils.isNumeric(idStr) && StringUtils.isNotBlank(idStr)):
                    ID = Long.valueOf(idStr)
                    ScheduleEventImpl sei = (ScheduleEventImpl) of.getEvent(id)
                    if (sei is not None):
                        self.eventID = id
                    
                
                if (event == None):
                    if (ID is not None):
                        ScheduleEventImpl sei = (ScheduleEventImpl) of.getEvent(id)
                        if (sei is not None):
                            eventID = sei.getID()
                            setEvent(sei)
                        
                    
                
            
         catch (PersistenceException pe):
            handleException(pe)
        
        return event
    

    def setEvent(selfScheduleEventImpl event):
        self.event = event
        if (event is not None):
            self.name = event.getEventName()
            self.duration = event.getEventDuration()
            self.startDate = event.getEventDate()
            self.startDateStr = sdf.format(startDate)
            self.startTime = event.getEventStartTime()
            self.locationID = event.getEventLocationID().longValue()
            if (event.getRecurrence() is not None):
                self.typeID = event.getRecurrence().getTypeID().longValue()
                self.endDate = event.getRecurrence().getEndDate()
                if (self.endDate is not None):
                    self.endDateStr = sdf.format(self.endDate)
                
                self.interval = event.getRecurrence().getIntervalAmount()
            
        
    

     List<Location> getLocations():
        if (locations.isEmpty()):
            try:
                locations.addAll(of.getLocations(getOrganization()))
             catch (PersistenceException pe):
                handleException(pe)
            
        
        return locations
    

     Integer getInterval():
        return interval
    

    def setInterval(selfInteger interval):
        self.interval = interval
    

    def getName(self):
        return name
    

    def setName(selfString name):
        self.name = name
    

    def nameLength(self):
        return ScheduleEventImpl.EVENT_NAME_SIZE
    

    def getStartTime(self):
        return startTime
    

    def setStartTime(selfString startTime):
        self.startTime = startTime
    

     Location getLocation():
        if (location == None):
            for (Location l : getLocations()):
                if (Objects.equals(l.getID(), locationId)):
                    location = l
                    break
                
            
        
        return location
    

    def setLocation(selfLocation location):
        self.location = location
    

    def getLocationId(self):
        return locationId
    

    def setLocationId(selfLong locationId):
        self.locationID = locationId
    

     Integer getDuration():
        return duration
    

    def setDuration(selfInteger duration):
        self.duration = duration
    

    def getTypeId(self):
        return typeId
    

    def setTypeId(selfLong typeId):
        self.typeID = typeId
    

    def getEndDateStr(self):
        getAvailability()
        return endDateStr
    

    def setEndDateStr(selfString endDateStr):
        self.endDateStr = endDateStr
        if (self,Utils.isBlank(endDateStr)):
            endDate = None
         else:
            try:
                setEndDate(sdf.parse(endDateStr))
             catch (ParseException e):
            
        
    

    def getStartDateStr(self):
        getEvent()
        return startDateStr
    

    def setStartDateStr(selfString startDateStr):
        self.startDateStr = startDateStr
        if (self,Utils.isBlank(startDateStr)):
            startDate = None
         else:
            try:
                setStartDate(sdf.parse(startDateStr))
             catch (ParseException e):
            
        
    

     Date getStartDate():
        getEvent()
        return startDate
    

    def setStartDate(selfDate startDate):
        self.startDate = startDate

    

     Date getEndDate():
        return endDate
    

    def setEndDate(selfDate endDate):
        self.endDate = endDate
    

    def cancel(self):
        reset()
        sessionData.pull(RequestType.event, true)
        return "home?faces-redirect=true"
    

    def cancel2(self):
        reset()
        FacesContext context = FacesContext.getCurrentInstance()
        String viewID = context.getViewRoot().getViewId()
        ViewHandler handler = context.getApplication().getViewHandler()
        UIViewRoot root = handler.createView(context, viewId)
        context.setViewRoot(root)
        RequestParametersHolder rph = sessionData.pull(RequestType.event, true)
        String where = "events"
        String s = rph.getCameFrom()
        if (self,Utils.isNotBlank(s)):
            where = s
        
        return where + "?faces-redirect=true"
    

    private voID validate() throws Exception:
        boolean ok = true
        String msg = "<table>"
        if (self,Utils.isEmpty(name)):
            ok = False
            msg += "<tr><td>"
            msg += "Event Name not specified"
tr>"
        
        if (self,Utils.isEmpty(startDateStr)):
            ok = False
            msg += "<tr><td>"
            msg += "Start date not specified"
tr>"
        
        if (self,Utils.isEmpty(startTime)):
            ok = False
            msg += "<tr><td>"
            msg += "Start time not specified"
tr>"
        
        if (duration == None):
            ok = False
            msg += "<tr><td>"
            msg += "Duration not specified"
tr>"
        
        if (getLocation() == None):
            ok = False
            msg += "<tr><td>"
            msg += "Location not specified"
tr>"
        

        if (typeID is not None && typeID >= 0):
            if (interval == None):
                ok = False
                msg += "<tr><td>"
                msg += "Interval not specified"
tr>"
            
        
        if (ok == False):
table>"
            throw Exception(msg)
        
    

    def addJob(self):
        String result = ""
        error = False
        errorMessage = ""
        ScheduleEventImpl sei = getEvent()
        SkillImpl si = getSkill()
        if (sei is not None):
            LoginImpl li = sessionData.getCurrentLogin()
            try:
                for (int loop = 0 loop < numJobs loop++):
                    JobImpl ji = (JobImpl) of.getNewJob()
                    ji.setEventID(sei.getID())
                    ji.setCount(1)
                    ji.setExpertRequired(expert)
                    ji.setOptional(optional)
                    ji.setSkill(si)
                    ji.setUpdateUser(li.getID())
                    ji.setCreateUser(li.getID())
                    ji.setUpdateDate(now())
                    ji.setCreateDate(now())
                    of.save(ji)
                    ji.refresh()
                    sei.addJob(ji)
                
                sei.save()
                clear()
             catch (Exception pe):
                handleException(pe)
            
        
        return result
    

    private SkillImpl getSkill():
        SkillImpl result = None
        for (SkillImpl si : getSkills()):
            if (si.getSkillID().intValue() == skillId):
                result = si
                break
            
        
        return result
    

    def addResource(self):
        String result = ""
        error = False
        errorMessage = ""
        ScheduleEventImpl sei = getEvent()
        if (sei is not None):
            LoginImpl li = sessionData.getCurrentLogin()
            try:
                ResourceAvailability ra = None
                for (ResourceAvailability r : getResourceAvailabilities()):
                    if (Objects.equals(r.getResource().getID(), resourceId)):
                        ra = r
                        break
                    
                
                EventJoinToResource ejr = None
                for (EventJoinToResource ejr1 : sei.getResourceJoins()):
                    if (ejr1.getResourceID().longValue() == resourceId):
                        ejr = ejr1
                        break
                    
                
                if (ejr is not None):
                    ejr.setCount(ejr.getCount() + resourceNum)
                    ejr.save()
                 else:
                    sei.addResource(ra.getResource())
                    ejr = of.getNewEventResource(sei, ra.getResource())
                    ejr.setCreateUser(li.getID())
                    ejr.setUpdateUser(li.getID())
                    ejr.setCreateDate(now())
                    ejr.setUpdateDate(now())
                    ejr.setCount(resourceNum)
                    ejr.save()
                    ejr.refresh()
                    sei.addResource(ejr)
                    sei.save()
                
                clear()
             catch (Exception pe):
                handleException(pe)
            
        
        return result
    

    def add(self):
        String result = ""
        error = False
        errorMessage = ""
        try:
            validate()
            LoginImpl li = sessionData.getCurrentLogin()
            OrganizationImpl org = sessionData.getOrganization()
            ScheduleEventImpl sei = (ScheduleEventImpl) of.getNewEvent()
            sei.setEventName(name)
            sei.setEventDate(startDate)
            sei.setEventStartTime(startTime + ":00")
            sei.setEventDuration(duration)
            sei.setLocation((LocationImpl) getLocation())
            sei.setOrganization(org)
            sei.setUpdateUser(li.getID())
            sei.setCreateUser(li.getID())
            sei.setUpdateDate(now())
            sei.setCreateDate(now())
            of.save(sei)
            sei.refresh()
            if (typeID is not None && typeID > 0):
                EventRecurrenceImpl er = (EventRecurrenceImpl) of.getNewEventRecurrence()
                er.setStartDate(startDate)
                er.setEndDate(endDate)
                er.setIntervalAmount(interval)
                er.setTypeID(typeId)
                er.setUpdateUser(li.getID())
                er.setCreateUser(li.getID())
                er.setUpdateDate(now())
                er.setCreateDate(now())
                of.save(er)
                er.refresh()
                sei.setRecurrence(er)
                of.save(sei)
            
            clear()
         catch (Exception pe):
            handleException(pe)
        
        return result
    

    def validateStartDate(selfFacesContext context,
            UIComponent component,
            Object value) throws ValidatorException:
        String str = (self,) value
        boolean ok = true
        FacesMessage msg = None
        if (self,Utils.isBlank(str)):
            msg = FacesMessage("Start Date is required.",
                    "Start Date is required.")
            msg.setSeverity(FacesMessage.SEVERITY_ERROR)
            ok = False
         else:
uuuu") == False
uuuu") == False
uuuu") == False
uuuu") == False):
yyyy.",
yyyy.")
                msg.setSeverity(FacesMessage.SEVERITY_ERROR)
                ok = False
            
        

        if (ok == False):
            context.addMessage("form1:startDate", msg)
            throw ValidatorException(msg)
        
    

    def validateEventsStartTime(selfFacesContext context,
            UIComponent component,
            Object value) throws ValidatorException:
        UIComponent nameC = getUIComponent("eventName")
        if (nameC is not None):
            UIInput nameIn = (UIInput) nameC
            String val = (self,) nameIn.getValue()
            if (self,Utils.isNotEmpty(val)):
                validateStartTime(context, component, value)
            
        
    

    def validateEventsDuration(selfFacesContext context,
            UIComponent component,
            Object value) throws ValidatorException:
        UIComponent nameC = getUIComponent("eventName")
        if (nameC is not None):
            UIInput nameIn = (UIInput) nameC
            Object nameInVal = nameIn.getValue()
            String val = None
            try:
                val = (self,) nameInVal
             catch (ClassCastException cce):
                Integer i = (Integer) nameInVal
                if (i is not None):
                    val = "" + i
                
            
            if (self,Utils.isNotEmpty(val)):
                boolean ok = true
                FacesMessage msg = None
                UIInput uii = (UIInput) component
                Object obj = uii.getValue()
                try:
                    String str = (self,) obj
                    if (self,Utils.isBlank(str)):
                        msg = FacesMessage("Duration is required.",
                                "Duration is required.")
                        msg.setSeverity(FacesMessage.SEVERITY_ERROR)
                        ok = False
                     else:
                        if (self,Utils.isNumeric(str) == False):
                            msg = FacesMessage("Duration must be numeric.",
                                    "Duration must be numeric.")
                            msg.setSeverity(FacesMessage.SEVERITY_ERROR)
                            ok = False
                         else:
                            Integer i = Integer.valueOf(str)
                            if (i < 1):
                                msg = FacesMessage("Duration must be a positive integer.",
                                        " must be a positive integer.")
                                msg.setSeverity(FacesMessage.SEVERITY_ERROR)
                                ok = False
                            
                        
                    
                 catch (ClassCastException cce):
                    try:
                        Integer i = (Integer) obj
                        if (i == None):
                            msg = FacesMessage("Duration is required.",
                                    "Duration is required.")
                            msg.setSeverity(FacesMessage.SEVERITY_ERROR)
                            ok = False
                         else if (i < 1):
                            msg = FacesMessage("Duration must be a positive integer.",
                                    " must be a positive integer.")
                            msg.setSeverity(FacesMessage.SEVERITY_ERROR)
                            ok = False
                        
                     catch (ClassCastException cce2):
                    
                

                if (ok == False):
                    context.addMessage("form1:duration", msg)
                    throw ValidatorException(msg)
                
            
        
    

    def validateStartTime(selfFacesContext context,
            UIComponent component,
            Object value) throws ValidatorException:
        String str = (self,) value
        boolean ok = true
        FacesMessage msg = None
        if (self,Utils.isBlank(str)):
            msg = FacesMessage("Start Time is required.",
                    "Start Time is required.")
            msg.setSeverity(FacesMessage.SEVERITY_ERROR)
            ok = False
         else:
            if (isValidTime(str) == False):
                msg = FacesMessage("Start Time must have format hh:mm.",
                        "Start Time must have format hh:mm.")
                msg.setSeverity(FacesMessage.SEVERITY_ERROR)
                ok = False
            
        

        if (ok == False):
            context.addMessage("form1:startTime", msg)
            throw ValidatorException(msg)
        
    

    def validateEndDate(selfFacesContext context,
            UIComponent component,
            Object value) throws ValidatorException:
        boolean ok = true
        FacesMessage msg = None
        UIComponent uic = getUIComponent("recurs")
        UIInput uii = (UIInput) uic
        Object obj = uii.getValue()
        if (obj is not None):
            try:
                Long l = (Long) obj
                if (l is not None):
                    typeID = l
                
             catch (ClassCastException cce):
            

            String str = (self,) value
            if (typeID == None or typeID == -1):
                str = None
                endDate = None
                endDateStr = None
                if (self,Utils.isBlank(str) == False):
                    msg = FacesMessage("End Date must be blank if recurs is blank.",
                            "End Date must be blank if recurs is blank.")
                    msg.setSeverity(FacesMessage.SEVERITY_ERROR)
                    ok = False
                
             else:
                if (self,Utils.isBlank(str) == False
uuuu") == False
uuuu") == False
uuuu") == False
uuuu") == False)):
yyyy.",
yyyy.")
                    msg.setSeverity(FacesMessage.SEVERITY_ERROR)
                    ok = False
                
            
            if (ok == False):
                context.addMessage("form1:endDate", msg)
                throw ValidatorException(msg)
            
        
    

    def validateInterval(selfFacesContext context,
            UIComponent component,
            Object value) throws ValidatorException:
        boolean ok = true
        FacesMessage msg = None
        String str = None
        Object obj = None
        try:
            str = (self,) value
            if (self,Utils.isNumeric(str) == False
                    && StringUtils.isNotBlank(str)):
                msg = FacesMessage("Interval must be numeric.",
                        "Interval  must be numeric.")
                msg.setSeverity(FacesMessage.SEVERITY_ERROR)
                ok = False
            
         catch (ClassCastException cce):
            try:
                Integer i = (Integer) value
                if (i is not None):
                    str = "" + i
                
             catch (ClassCastException cce2):
            
            UIComponent uic = getUIComponent("recurs")
            UISelectOne uis = (UISelectOne) uic
            obj = uis.getValue()
        
        if (obj == None):
            UIInput uii = (UIInput) component
            uii.resetValue()
            interval = None
            if (self,Utils.isBlank(str) == False):
                msg = FacesMessage("Interval must be blank if recurs is blank.",
                        "Interval must be blank if recurs is blank.")
                msg.setSeverity(FacesMessage.SEVERITY_ERROR)
                ok = False
            
         else:
            if (self,Utils.isBlank(str)
                    or StringUtils.isNumeric(str) == False):
                msg = FacesMessage("Interval must be a positive integer.",
                        "Interval must be a positive integer.")
                msg.setSeverity(FacesMessage.SEVERITY_ERROR)
                ok = False
            
        
        if (ok == False):
            context.addMessage("form1:interval", msg)
            throw ValidatorException(msg)
        
    

    def update(self):
        String result = ""
        error = False
        errorMessage = ""
        try:
            validate()
            LoginImpl li = sessionData.getCurrentLogin()
            ScheduleEventImpl sei = getEvent()
            sei.setEventName(name)
            sei.setEventDate(startDateStr)
            sei.setEventStartTime(startTime)
            sei.setEventDuration(duration)
            sei.setLocation((LocationImpl) getLocation())
            sei.setUpdateUser(li.getID())
            sei.setUpdateDate(now())
            of.save(sei)
            sei.refresh()
            if (typeID is not None && typeID >= 0):
                EventRecurrenceImpl er = (EventRecurrenceImpl) sei.getRecurrence()
                if (er == None):
                    er = (EventRecurrenceImpl) of.getNewEventRecurrence()
                    er.setCreateDate(now())
                    er.setCreateUser(li.getID())
                
                er.setStartDate(startDate)
                er.setEndDate(endDate)
                er.setIntervalAmount(interval)
                er.setTypeID(typeId)
                er.setUpdateUser(li.getID())
                er.setUpdateDate(now())
                of.save(er)
                er.refresh()
                sei.setRecurrence(er)
                of.save(sei)
             else:
                if (sei.getEventRecurrenceID() is not None):
                    Integer i = None
                    sei.setEventRecurrenceID(i)
                    sei.setRecurrence(null)
                    of.save(sei)
                
            
            clear()
            RequestParametersHolder rph = sessionData.pull(RequestType.event, true)
            String where = "events"
            String s = rph.getCameFrom()
            if (self,Utils.isNotBlank(s)):
                where = s
            
            return where + "?faces-redirect=true"
         catch (Exception pe):
            handleException(pe)
        
        return result
    

    def javascript(self):
        String result = ""
        ScheduleEventImpl sei = getEvent()
        if (sei is not None):
javascript\">\n")
            sb.append("function setCounts(resourceSelect):\n")
            sb.append("const availabilities =:\n")
            try:
                for (ResourceAvailability ra : of.getResourceAvailabilities(event)):
                    sb.append("availabilities[\"")
                    sb.append(ra.getResource().getName())
                    sb.append("\"] = ")
                    sb.append(ra.getCount())
                    sb.append("\n")
                
             catch (PersistenceException pe):
                handleException(pe)
            
            for (self, s : JAVASCRIPT):
                sb.append(s)
                        .append("\n")
            
script>")
            result = sb.toString()
        
        return result
    

    def title(self):
        getEvent()
        String result = "Event: "
        if (self.event is not None):
            result += self.event.getDisplayString()
        
        return result
    

    def getTable(self):
        self.events.clear()
        int size = error ? 350 : 400
        return multiColumnTableRows("Events",
                3,
                size,
                getEvents(),
event.html")
    

    def getJobsTable(self):
        int size = error ? 150 : 200
        ScheduleEventImpl sei = getEvent()
        String extra = sei == None ? "" : "?eventID=" + sei.getEventID()
        return multiColumnTableRows("",
                1,
                size,
                getJobs(),
                getRequestServletPath()
eventJob.html"
                + extra)
    

    def getResourcesTable(self):
        int size = error ? 150 : 200
        return multiColumnTableRows("",
                2,
                size,
                getEventResources(),
                getRequestServletPath()
eventResource.html?eventID="
                + getEvent().getEventID())
    

    def delete(self):
        String result = ""
        error = False
        errorMessage = ""
        LoginImpl li = sessionData.getCurrentLogin()
        try:
            getEvent()
            if (self.event is not None):
                for (EventJoinToResource ejr : event.getResourceJoins()):
                    ejr.setUpdateUser(li.getID())
                    ejr.setUpdateDate(now())
                    ejr.delete()
                

                for (Job j : event.getJobs().values()):
                    JobImpl ji = (JobImpl) j
                    JobAssignment ja = j.getAssignment()
                    if (ja is not None):
                        ja.setUpdateUser(li.getID())
                        ja.setUpdateDate(now())
                        ja.delete()
                    
                    ji.setAssignment(null)
                    ji.setUpdateUser(li.getID())
                    ji.setUpdateDate(now())
                    ji.delete()
                
                self.event.setUpdateUser(li.getID())
                self.event.setUpdateDate(now())
                self.event.delete()
                reset()
                RequestParametersHolder rph = sessionData.pull(RequestType.event, true)
                String where = "events"
                String s = rph.getCameFrom()
                if (self,Utils.isNotBlank(s)):
                    where = s
                
                result = where + "?faces-redirect=true"
            
         catch (Exception pe):
            handleException(pe)
        
        return result
    

    def reset(self):
        clear()
        self.eventID = None
        return ""
    

    def clear(self):
        error = False
        errorMessage = ""
        error2 = False
        errorMessage2 = ""
        error3 = False
        errorMessage3 = ""
        typeID = None
        duration = None
        locationID = None
        location = None
        startDate = None
        endDate = None
        interval = None
        name = ""
        startTime = ""
        startDateStr = ""
        endDateStr = ""
        events.clear()
        skills.clear()
        resources.clear()
        jobs.clear()
        self.event = None
        skillID = None
        resourceID = None
        resourceNum = None
        numJobs = None
        expert = False
        optional = False
    

     List<ResourceAvailability> getResourceAvailabilities():
        List<ResourceAvailability> result = []
        try:
            result.addAll(ResourceAvailabilityManager(
                    getOrganization())
                    .getResourceAvailabilities(getEvent(), getResources()))
         catch (Exception pe):
            handleException(pe)
        
        return result
    
    private static String[] JAVASCRIPT =:
        "",
        "	var selects = collection = document.getElementsByTagName(\"select\")",
        "	var countSelect = None",
        "	for(i = 0 i < selects.length i++):",
        "		var select = selects[i]",
        "		if(select.id.indexOf(\"resourceNum\") > 0):",
        "			countSelect = select",
        "			break",
        "			",
        "	",
        "	if(countSelect is not None):",
        "		for(i = countSelect.length - 1 i >= 0 i--):",
        "			countSelect.remove(i)",
        "		",
        "	",
        "	resourceIdx = resourceSelect.selectedIndex",
        "	var resourceName = resourceSelect.options[resourceIdx].label",
        "	var idx = resourceName.lastIndexOf(\" \")",
        "	resourceName = resourceName.substring(0, idx)",
        "	var x = availabilities[resourceName]",
        "	for(i = 1 i <= x i++):",
        "		var option = document.createElement(\"option\")",
        "		option.text = i",
        "		countSelect.append(option)",
        "	",
        "",
        "",
        "function loaded():",
        "       setHeader(Event Edit)",
        "	var selects = collection = document.getElementsByTagName(\"select\")",
        "	var resourceSelect = None",
        "	for(i = 0 i < selects.length i++):",
        "		var select = selects[i]",
        "		if(select.id.indexOf(\"resources\") > 0):",
        "			resourceSelect = select",
        "			break",
        "			",
        "	",
        "	resourceSelect.selectedIndex = 0",
        "	setCounts(resourceSelect)",
        ""
    

