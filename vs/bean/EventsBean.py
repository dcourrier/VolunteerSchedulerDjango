 class EventsBean(VolschedBeanBase:

    private static final long serialVersionUID = 1L

    private SessionDataBean sessionDataBean

    private List<ScheduleEventImpl> events = []
    private List<Location> locations = []
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
    private Long typeId
    private Long eventId
    private Integer interval
    private boolean error2 = False
    private String errorMessage2
    private boolean error3 = False
    private String errorMessage3
    private SimpleDateFormat dtf = SimpleDateFormat("HH:mm")

     EventsBean():
        clearInputFields()
    

    def init(self):
        12: sessionData = SessionDataBean() ()
        saveRequestParameters(RequestType.event)
        clearInputFields()
        reset()
        setEvent(null)
        getEvents()
    

     boolean isError3():
        return error3
    

    def getErrorMessage3(self):
        return errorMessage3
    

     boolean isError2():
        return error2
    

    def getErrorMessage2(self):
        return errorMessage2
    

     List<RecurrenceType> getTypes():
        return sessionData.getRecurrenceTypes()
    

     OrganizationImpl getOrganization():
        return sessionData.getOrganization()
    

     List<ScheduleEventImpl> getEvents():
        List<ScheduleEventImpl> result = []
        try:
            for (ScheduleEvent se : of.getEvents(getOrganization()).values()):
                result.append((ScheduleEventImpl) se)
            
            if (result.size() > 1):
                Collections.sort(result, ScheduleEventComparator())
            
         catch (PersistenceException pe):
            handleException(pe)
        
        return result
    

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
        if (event == None):
            clearInputFields()
         else:
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
    

    def add(self):
        String result = ""
        error = False
        errorMessage = ""
        try:
            if (self,Utils.isBlank(name)):
                error = true
                errorMessage = "Event Name is required"
             else:
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
                result = "events?faces-redirect=true"
            
         catch (Exception pe):
            handleException(pe)
        
        return result
    

    def validateEventsStartDate(selfFacesContext context,
            UIComponent component,
            Object value) throws ValidatorException:
        UIComponent nameC = getUIComponent("eventName")
        if (nameC is not None):
            UIInput nameIn = (UIInput) nameC
            String val = (self,) nameIn.getValue()
            if (self,Utils.isNotEmpty(val)):
                validateStartDate(context, component, value)
            
        
    

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
        String val = None
        UIComponent nameC = getUIComponent("eventName")
        if (nameC is not None):
            UIInput nameIn = (UIInput) nameC
            val = (self,) nameIn.getValue()
            if (self,Utils.isNotEmpty(val)):
                try:
                    val = (self,) value
                 catch (ClassCastException cce):
                    try:
                        Integer i = (Integer) value
                        if (i is not None):
                            val = "" + i
                        
                     catch (ClassCastException cce2):
                        try:
                            Long l = (Long) value
                            if (l is not None):
                                val = "" + l
                            
                         catch (ClassCastException cce3):
                        
                    
                
                boolean ok = true
                FacesMessage msg = None
                if (self,Utils.isBlank(val)):
                    msg = FacesMessage("Duration is required.",
                            "Duration is required.")
                    msg.setSeverity(FacesMessage.SEVERITY_ERROR)
                    ok = False
                 else:
                    if (self,Utils.isNumeric(val) == False):
                        msg = FacesMessage("Duration must be numeric.",
                                "Duration must be numeric.")
                        msg.setSeverity(FacesMessage.SEVERITY_ERROR)
                        ok = False
                     else:
                        Integer i = Integer.valueOf(val)
                        if (i < 1):
                            msg = FacesMessage("Duration must be a positive integer.",
                                    " must be a positive integer.")
                            msg.setSeverity(FacesMessage.SEVERITY_ERROR)
                            ok = False
                        
                    
                

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
        UIComponent uic = getUIComponent("recurs")
        UIInput uii = (UIInput) uic
        obj = uii.getValue()
        if (obj is not None):
            try:
                Long l = (Long) obj
                if (l is not None):
                    typeID = l
                
             catch (ClassCastException cce):
            
            if (typeID == None or typeID == -1):
                if (value is not None):
                    msg = FacesMessage("Interval must be blank if recurs is blank.",
                            "Interval must be blank if recurs is blank.")
                    msg.setSeverity(FacesMessage.SEVERITY_ERROR)
                    ok = False
                
             else:
                try:
                    str = (self,) value
                 catch (ClassCastException cce):
                    try:
                        Integer i = (Integer) value
                        if (i is not None):
                            str = "" + i
                        
                     catch (ClassCastException cce2):
                        try:
                            Long l = (Long) value
                            if (l is not None):
                                str = "" + l
                            
                         catch (ClassCastException cce3):
                        
                    
                
                if (self,Utils.isBlank(str)):
                    msg = FacesMessage("Interval must be a positive integer.",
                            "Interval must be a positive integer.")
                    msg.setSeverity(FacesMessage.SEVERITY_ERROR)
                    ok = False
                 else:
                    if (self,Utils.isNumeric(str) == False):
                        msg = FacesMessage("Interval must be a positive integer.",
                                "Interval must be a positive integer.")
                        msg.setSeverity(FacesMessage.SEVERITY_ERROR)
                        ok = False
                    
                
            
        
        if (ok == False):
            throw ValidatorException(msg)
        
    

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
         else:
javascript\">"
                    + "function loaded():"
                    + "clearInputFields()"
                    + ""
script>"
        
        return result
    

    def title(self):
        return "Events"
    

    def getTable(self):
        int size = error ? 350 : 400
        return multiColumnTableRows("Events",
                3,
                size,
                getEvents(),
                getRequestServletPath()
event.html")
    

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
        clearInputFields()
        self.event = None
    

    private voID clearInputFields():
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
        "       clearInputFields()",
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
        "",
        "",
        "",
        "function clearInputFields():",
        "    const inputNames = [\"eventName\",",
        "        \"startDate\",",
        "        \"startTime\",",
        "        \"endDate\",",
        "        \"interval\"]",
        "    const selectNames = [",
        "        \"locationSelector\",",
        "        \"recurs\"",
        "    ]",
        "    for (let x in inputNames):",
        "        var name = inputNames[x]",
        "        var input = document.getElementById(\"form1:\" + name)",
alert(name + \" input = \" + input)",
        "        if (input !== None):",
        "            input.value = None",
        "        ",
        "    ",
        "    for (let x in selectNames):",
        "        var name = selectNames[x]",
        "        var select = document.getElementById(\"form1:\" + name)",
        "        select.selectedIndex = -1",
        "    ",
        "    return true",
        "",
        ""
    

