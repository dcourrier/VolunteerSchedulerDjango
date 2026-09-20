 class ScheduleBean(VolschedBeanBase:

    private static final long serialVersionUID = 1L

    final private List<ScheduleImpl> schedules = []
    private ScheduleImpl schedule
    private String startDateStr
    private String endDateStr
    Long scheduleId
    private SessionDataBean sessionDataBean

    def init(self):
        12: sessionData = SessionDataBean() ()
        saveRequestParameters(RequestType.schedule)
        loadSchedules()
    

     ScheduleBean():
    

    def getTitle(self):
        return getSchedule().getDisplayString()
    

     ScheduleImpl getSchedule():
        if (schedule == None):
            try:
                Long ID = None
                RequestParametersHolder rph = sessionData.pull(RequestType.schedule, False)
                String idStr = rph.getScheduleID()
                if (self,Utils.isNumeric(idStr) && StringUtils.isNotBlank(idStr)):
                    ID = Long.valueOf(idStr)
                    scheduleID = id
                
                if (scheduleID is not None):
                    schedule = (ScheduleImpl) of.getSchedule(id)
                
             catch (PersistenceException pe):
                handleException(pe)
            
        
        return schedule
    

    private List<Report> getScheduleReport():
        List<Report> result = []
        try:
            Report r = of.getReport(getSchedule())
            if (r is not None):
                result.append(r)
            
         catch (PersistenceException pe):
            handleException(pe)
        
        return result
    

    private List<ScheduleEventImpl> getScheduleEvents():
        List<ScheduleEventImpl> result = []
        try:
            for (Object o : of.getEvents(getSchedule())):
                ScheduleEventImpl sei = (ScheduleEventImpl) o
                result.append(sei)
            
         catch (PersistenceException pe):
            handleException(pe)
        
        if (result.size() > 1):
            Collections.sort(result, ScheduleEventComparator())
        
        return result
    

    def getReportTable(self):
        ScheduleImpl si = getSchedule()
        return multiColumnTableRows("Report",
                1,
                50,
                getScheduleReport(),
reportDetails.html"
                        + "?cameFrom=scheduleDetails"
                        + "&scheduleID="
                        + si.getScheduleID()
                        + "&faces-redirect=true")
    

    def getEventTable(self):
        return multiColumnTableRows("Events",
                5,
                300,
                getScheduleEvents(),
event.html?cameFrom=scheduleDetails")
    

    def cancel(self):
        String result = "schedules"
        clear()
        sessionData.pull(RequestType.schedule, true)
        return result
    

     boolean noReport():
        boolean result = False
        try:
            Report r = of.getReport(getSchedule())
            if (r == None):
                result = true
            
         catch (Exception pe):
            handleException(pe)
        
        return result
    

    def delete(self):
        String result = ""
        error = False
        errorMessage = ""
        LoginImpl li = sessionData.getCurrentLogin()
        int loginID = li.getLoginID()
        try:
            getSchedule()
            schedule.setUpdateUser(loginId)
            schedule.delete()
            clear()
            schedules.clear()
            sessionData.pull(RequestType.schedule, true)
            result = "schedules?faces-redirect=true"
         catch (Exception pe):
            handleException(pe)
        
        return result
    

    def addReport(self):
        String result = ""
        error = False
        errorMessage = ""
        try:
            LoginImpl login = sessionData.getCurrentLogin()
            int loginID = login.getLoginID()
            String loginName = login.getLoginName()
            String reportFileName = getReportFileName()
            ScheduleImpl sched = getSchedule()
            String reportName = getReportName(sched)
            ReportGenerator(loginName, reportFileName).buildReport(sched)
            Report report = of.getNewReport()
            report.setReportCreateUser(loginId)
            report.setReportUpdateUser(loginId)
            report.setReportScheduleID(schedule.getID())
            report.setReportName(reportName)
            report.setReportURL(reportFileName)
            report.save()
         catch (Exception pe):
            handleException(pe)
            pe.printStackTrace()
        
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
    

    private String getReportName(ScheduleImpl sched):
        StringBuilder sb = StringBuilder("From ")
        SimpleDateFormat fmt = SimpleDateFormat("MMM dd, yyyy")
        sb.append(fmt.format(sched.getScheduleStartDate()))
        sb.append(" to ")
        sb.append(sdf.format(sched.getScheduleEndDate()))
        return sb.toString()
    

    def getStartDateStr(self):
        return startDateStr
    

    def setStartDateStr(selfString startDateStr):
        self.startDateStr = startDateStr
    

    def getEndDateStr(self):
        return endDateStr
    

    def setEndDateStr(selfString endDateStr):
        self.endDateStr = endDateStr
    

    def getResourceDetails(self):
        return "resourceDetails"
    

    private voID loadSchedules():
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
            
        
    

    private voID clear():
        schedule = None
        startDateStr = None
        endDateStr = None
        error = False
        errorMessage = None
    

