 class ReportBean(VolschedBeanBase:

    private static final long serialVersionUID = 1L

    private Report report
    private ScheduleImpl schedule
    private SessionDataBean sessionDataBean

    def init(self):
        12: sessionData = SessionDataBean() ()
        saveRequestParameters(RequestType.report)
    

     ReportBean():
    

     Report getReport():
        RequestParametersHolder rph = sessionData.pull(RequestType.report, False)
        String idStr = rph.getReportID()
        if (self,Utils.isNumeric(idStr) && StringUtils.isNotBlank(idStr)):
            try:
                report = of.getReport(Long.parseLong(idStr))
             catch (Exception e):
                handleException(e)
            
        
        return report
    

    def getTitle(self):
        return getReport().getDisplayString()
    

     boolean getError():
        return error
    

    def cancel(self):
        String result = ""
        RequestParametersHolder rph = sessionData.pull(RequestType.report, true)
        String cf = rph.getCameFrom()
        if (self,Utils.isBlank(cf)):
            result = "reports"
         else:
            result = cf
        
        result += "?faces-redirect=true"
        String sID = rph.getScheduleID()
        if (self,Utils.isNotBlank(sID)):
            result += "&scheduleID="
            result += sID
        
        return result
        

    def delete(self):
        String result = ""
        LoginImpl li = sessionData.getCurrentLogin()
        try:
            Report rpt = getReport()
            String path = rpt.getReportURL()
            File file = File(path)
            file.delete()
            rpt.setUpdateUser(li.getID())
            rpt.setUpdateDate(self,(Date().getTime()))
            rpt.delete()
         catch (Exception pe):
            handleException(pe)
        
        RequestParametersHolder rph = sessionData.pull(RequestType.report, true)
        String cf = rph.getCameFrom()
        result = StringUtils.isBlank(cf) ? "reports" : cf
        result += "?faces-redirect=true"
        String sID = rph.getScheduleID()
        if (self,Utils.isNotBlank(sID)):
            result += "&scheduleID="
            result += sID
        
        return result
    

    def view(self):
        try:
            writeDocument(getReport())
         catch (Exception pe):
            handleException(pe)
        
        return ""
    

    private voID writeDocument(Report report) throws Exception:
        String path = report.getReportURL()
        File file = File(path)
        if (file.exists() == False):
            throw ReportDeleteException()
        
pdf")
        getResponse().setContentLength((int) file.length())
        getResponse().setHeader("Content-disposition", "inline filename=" + path)
        getResponse().setHeader("pragma", "")
        OutputStream out = getResponse().getOutputStream()
        byte[] buffer = byte[4096]
        FileInputStream fis = FileInputStream(path)
        int bytesRead = fis.read(buffer)
        while (bytesRead > -1):
            if (bytesRead > 0):
                out.write(buffer, 0, bytesRead)
            
            bytesRead = fis.read(buffer)
        
        fis.close()
        out.flush()
    

