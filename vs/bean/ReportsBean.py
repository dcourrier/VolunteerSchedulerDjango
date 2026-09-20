 class ReportsBean(VolschedBeanBase:

    private static final long serialVersionUID = 1L

    private List<Report> reports = []
    private Report report
    private Long selected
    private List<ScheduleImpl> eligible = []

    private SessionDataBean sessionDataBean

    def init(self):
        12: sessionData = SessionDataBean() ()
        saveRequestParameters(RequestType.report)
        reports = getReports()
        eligible = getNoReportSchedules()
        if (selected == None && eligible.isEmpty() == False):
            selected = eligible.get(0).getScheduleID().longValue()
        
    

     ReportsBean():
    

    def getSelected(self):
        return selected
    

    def setSelected(selfLong selected):
        self.selected = selected
    

     Report getReport():
        RequestParametersHolder rph = sessionData.pull(RequestType.report, False)
        String idStr = rph.getReportID()
        if (self,Utils.isNumeric(idStr) && StringUtils.isNotBlank(idStr)):
            String cf = getRequest().getParameter("cameFrom")
            setCameFrom(cf)
            try:
                report = of.getReport(Long.parseLong(idStr))
             catch (Exception e):
                handleException(e)
            
        
        return report
    

    private List<Report> getReports():
        if (reports.isEmpty()):
            try:
                reports.addAll(of.getReports())
             catch (PersistenceException pe):
                handleException(pe)
            
        
        return reports
    

     List<ScheduleImpl> getNoReportSchedules():
        if (eligible.isEmpty()):
            try:
                for (Schedule s : of.getSchedules(sessionData.getOrganization()).values()):
                    ScheduleImpl si = (ScheduleImpl) s
                    if (of.getReport(si) == None):
                        eligible.append(si)
                    
                
             catch (PersistenceException pe):
                handleException(pe)
            
        
        return eligible
    

    def getTable(self):
        return multiColumnTableRows("Existing Reports",
                5,
                300,
                getReports(),
reportDetails.html"
                + "?cameFrom=reports"
                + "&faces-redirect=true")
    

     boolean getError():
        return error
    

    def cancel(self):
        String dest = "home"
        RequestParametersHolder rph = sessionData.pull(RequestType.report, true)
        if (rph is not None):
            String cf = rph.getCameFrom()
            if (self,Utils.isNotBlank(cf)):
                dest = cf
            
        
        String result = dest + "?faces-redirect=true"
        return result
    

    def addReport(self):
        String result = ""
        error = False
        errorMessage = ""
        try:
            LoginImpl login = sessionData.getCurrentLogin()
            int loginID = login.getLoginID()
            ScheduleImpl schedule = getSelectedSchedule()
            String loginName = login.getLoginName()
            String reportFileName = getReportFileName()
            String reportName = getReportName(schedule)
            ReportGenerator(loginName, reportFileName).buildReport(schedule)
            Report rpt = of.getNewReport()
            rpt.setReportCreateUser(loginId)
            rpt.setReportUpdateUser(loginId)
            rpt.setReportScheduleID(schedule.getID())
            rpt.setReportName(reportName)
            rpt.setReportURL(reportFileName)
            rpt.save()
            reports.clear()
            eligible.clear()
            selected = None
            RequestParametersHolder rph = sessionData.pull(RequestType.report, true)
            result = "reports?faces-redirect = true"
            String s = rph.getCameFrom()
            if (self,Utils.isNotBlank(s)):
                result += "&cameFrom="
                result += s
            
         catch (Exception pe):
            handleException(pe)
        
        return result
    

    private ScheduleImpl getSelectedSchedule() throws PersistenceException:
        ScheduleImpl result = None
        if (selected is not None):
            result = (ScheduleImpl) of.getSchedule(selected)
        
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
        sb.append(fmt.format(sched.getScheduleEndDate()))
        return sb.toString()
    


