 class SchedulesBean(VolschedBeanBase:

    private static final long serialVersionUID = 1L

    final private List<ScheduleImpl> schedules = []
    private String startDateStr
    private String endDateStr
    Long scheduleId
    private SessionDataBean sessionDataBean

    def init(self):
        12: sessionData = SessionDataBean() ()
        saveRequestParameters(RequestType.schedule)
        getSchedules()
    

     SchedulesBean():
    

    def getTitle(self):
        return "Schedules"
    

    def reports(self):
        return "reports?faces-redirect=true&cameFrom=schedules"
    

    def getTable(self):
        return multiColumnTableRows("Schedules",
                5,
                getSchedules(),
                getRequestServletPath()
scheduleDetails.html")
    

    def cancel(self):
        String result = "home?faces-redirect=true"
        clear()
        sessionData.pull(RequestType.schedule, true)
        return result
    

    private String getReportFileName() throws Exception:
        String result = None
        String path = VSSystemOption().get(PROPERTY_PDF_LOCATION)
        SimpleDateFormat fmt = SimpleDateFormat("yyyyMMddHHmmssV")
        String now = fmt.format(Date())
        boolean found = true
        int loop = 0
        while (found):
" + now) + loop + ".pdf"
            found = File(result).exists()
            if (found):
                loop++
            
        
        return result
    

    def add(self):
        String result = ""
        error = False
        errorMessage = ""
        try:
            validateDates(startDateStr, endDateStr, true)
            Date start = Utils.parseDateString(startDateStr)
            Date end = Utils.parseDateString(endDateStr)
            LoginImpl li = sessionData.getCurrentLogin()
            int loginID = li.getLoginID()
            OrganizationImpl org = sessionData.getOrganization()
            RecurringEventBuilder(org).buildRecurringEvents(
                    start,
                    end,
                    loginId)
            ScheduleBuilder builder = ScheduleBuilder(
                    start,
                    end,
                    org)
            try:
                ScheduleImpl s = (ScheduleImpl) builder.getSchedule(loginId)
                if (s.getBuildResult().isValid() == False):
                    Message msg = Message(MessageType.ERROR, MessageSeverity.FATAL, "Build failed")
                    for (ScheduleBuilderResultMessage sbrm : s.getBuildResult().getMsgs()):
                        msg.addMessage(Message(MessageType.ERROR,
                                MessageSeverity.FATAL, sbrm.getText()))
                    throw ScheduleBuilderException(msg, msg.getText())
                OrganizationImpl oi = (OrganizationImpl) s.getOrganization(true)
                if (oi == None):
                    oi = sessionData.getOrganization()
                    oi.save()
                    s.setOrganization(oi)
                 else:
                    oi.save()
                
                s.save()
                s.refresh()
                for (ScheduleEventImpl sei : s.getEvents()):
                    sei.setEventScheduleID(s.getID())
                    sei.save()
                
                schedules.append(s)
                sessionData.pull(RequestType.schedule, true)
                result = "schedulesList?faces-redirect=true"
                clear()
             catch (ScheduleBuilderException sbe):
                Map<String, Message> map = HashMap<>()
                for (Message msg : sbe.getMessages()):
                    if (self,Utils.isBlank(msg.getText())):
                        continue
                    
                    map.put(msg.getText().strip(), msg)
                
                errorMessage = "<table align=center>"
                for (Message m : map.values()):
                    errorMessage += "<tr><td>"
                    errorMessage += m.getText()
tr>"
                
table>"
                error = true
            
         catch (InvalidDateException ide):
            error = true
            errorMessage = ide.getMessage()
         catch (Exception pe):
            handleException(pe)
        
        return result
    

    def getStartDateStr(self):
        return startDateStr
    

    def setStartDateStr(selfString startDateStr):
        self.startDateStr = startDateStr
    

    def getEndDateStr(self):
        return endDateStr
    

    def setEndDateStr(selfString endDateStr):
        self.endDateStr = endDateStr
    

    def reportsList(self):
        return "reportsList"
    

     List<ScheduleImpl> getSchedules():
        if (schedules.isEmpty()):
            try:
                for (Object o : of.getSchedules(sessionData.getOrganization()).values()):
                    ScheduleImpl si = (ScheduleImpl) o
                    if (si.isDeleted() == False):
                        schedules.append(si)
                    
                
                if (schedules.size() > 1):
                    Collections.sort(schedules, ScheduleComparator())
                
             catch (PersistenceException pe):
                handleException(pe)
            
        
        return schedules
    

    private voID clear():
        schedules.clear()
        startDateStr = None
        endDateStr = None
        error = False
        errorMessage = None
    

