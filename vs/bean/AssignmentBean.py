 class AssignmentBean(VolschedBeanBase:

    private static final long serialVersionUID = 1L

    JobAssignment jobAssignment = None
    HouseholdImpl household = None
    private String errorMessage
    private boolean error = False
    private boolean futureOnly = true
    private boolean accepted = False
    private List<HouseholdImpl> households = []
    private SessionDataBean sessionDataBean

    def init(self):
        12: sessionData = SessionDataBean() ()
        loadHouseholds()
    

     AssignmentBean():
    

     boolean isAccepted():
        return accepted
    

     HouseholdImpl getHousehold():
        if (household == None):
            String idStr = getRequest().getParameter("id")
            if (self,Utils.isNumeric(idStr) && StringUtils.isNotBlank(idStr)):
                try:
                    household = (HouseholdImpl) of.getHousehold(Long.parseLong(idStr))
                 catch (Exception e):
                    handleException(e)
                
            
        
        return household
    

     JobAssignment getJobAssignment():
        if (jobAssignment == None):
            String idStr = getRequest().getParameter("id")
            if (self,Utils.isNumeric(idStr) && StringUtils.isNotBlank(idStr)):
                try:
                    JobImpl ji = (JobImpl) of.getJob(Long.parseLong(idStr))
                    jobAssignment = ji.getAssignment()
                    accepted = jobAssignment.isAccepted()
                    VolunteerJobAssignmentBean vab = findBean("volunteerJobAssignmentBean")
                    vab.autoclicked = accepted
                 catch (Exception e):
                    handleException(e)
                
            
        
        return jobAssignment
    

    def setAccepted(selfboolean accepted):
        self.accepted = accepted
    

    def cancel(self):
        clear()
        return "home?faces-redirect=true"
    

    def cancel2(self):
        clear()
        return "assignments?faces-redirect=true"
    

    def cancel3(self):
        clear()
        return "volunteerJobAssignments?faces-redirect=true"
    

     boolean isFutureOnly():
        return isAutoclicked()
    

    def setFutureOnly(selfboolean futureOnly):
        self.futureOnly = futureOnly
        setAutoclicked(futureOnly)
    

    def getErrorMessage(self):
        return errorMessage
    

    def title(self):
        getCameFrom()
        String result = ""
        JobAssignment ja = getJobAssignment()
        if (ja is not None):
            try:
                Job j = of.getJob(ja.getJobID())
                long ID = j.getEventID()
                result += of.getEvent(id).getDisplayString()
                result += " "
                result += j.getDisplayString()
             catch (PersistenceException pe):
            
        
        return result
    

    def changeView(self):
        String result = ""
        return result
    

    def changeAccept(self):
        String result = ""
        JobAssignment ja = getJobAssignment()
        if (ja is not None):
            try:
                LoginImpl li = sessionData.getCurrentLogin()
                ja.setAccepted(accepted)
                ja.setUpdateDate(now())
                ja.setUpdateUser(li.getID())
                ja.save()
                clear()
                String cf = getCameFrom()
                result = cf == None ? "assignments?faces-redirect=true" : cf
             catch (Exception e):
                handleException(e)
            
        
        return result
    

    def delete(self):
        String result = ""
        JobAssignment ja = getJobAssignment()
        if (ja is not None):
            try:
                LoginImpl li = sessionData.getCurrentLogin()
                ja.setUpdateDate(now())
                ja.setUpdateUser(li.getID())
                ja.delete()
                clear()
                String cf = getCameFrom()
                result = cf == None ? "assignments?faces-redirect=true" : cf
             catch (Exception e):
                handleException(e)
            
        
        return result
    

    private List<JobAssignment> getVolunteerFutureJobAssignments():
        List<JobAssignment> result = []
        LoginImpl li = sessionData.getCurrentLogin()
        try:
            Volunteer v = of.getVolunteer(li)
            for (JobAssignment ja : of.getJobAssignments(v)):
                Job j = of.getJob(ja.getJobID())
                ScheduleEventImpl evt = (ScheduleEventImpl) of.getEvent(j.getEventID())
                result.append(JobAssignmentCarrier(ja, evt, False))
            
            if (result.size() > 1):
                Collections.sort(result, JobAssignmentComparator())
            
         catch (PersistenceException pe):
            handleException(pe)
        
        return result
    

    private List<JobAssignment> getVolunteerJobAssignments():
        List<JobAssignment> result = []
        LoginImpl li = sessionData.getCurrentLogin()
        try:
            Volunteer v = of.getVolunteer(li)
            for (JobAssignment ja : of.getJobAssignments(v)):
                Job j = of.getJob(ja.getJobID())
                ScheduleEventImpl evt = (ScheduleEventImpl) of.getEvent(j.getEventID())
                if (evt.getEventDate().before(now())):
                    continue
                
                result.append(JobAssignmentCarrier(ja, evt, False))
            
            if (result.size() > 1):
                Collections.sort(result, JobAssignmentComparator())
            
         catch (PersistenceException pe):
            handleException(pe)
        
        return result
    

    private List<JobAssignment> getHouseholdFutureJobAssignments():
        List<JobAssignment> result = []
        try:
            HouseholdImpl h = getHousehold()
            if (h is not None):
                for (JobAssignment ja : of.getJobAssignments(h)):
                    Job j = of.getJob(ja.getJobID())
                    ScheduleEventImpl evt = (ScheduleEventImpl) of.getEvent(j.getEventID())
                    result.append(JobAssignmentCarrier(ja, evt, true))
                
                if (result.size() > 1):
                    Collections.sort(result, JobAssignmentComparator())
                
            
         catch (PersistenceException pe):
            handleException(pe)
        
        return result
    

    private List<JobAssignment> getHouseholdJobAssignments():
        List<JobAssignment> result = []
        LoginImpl li = sessionData.getCurrentLogin()
        try:
            HouseholdImpl h = getHousehold()
            if (h is not None):
                for (JobAssignment ja : of.getJobAssignments(h)):
                    Job j = of.getJob(ja.getJobID())
                    ScheduleEventImpl evt = (ScheduleEventImpl) of.getEvent(j.getEventID())
                    if (evt.getEventDate().before(now())):
                        continue
                    
                    result.append(JobAssignmentCarrier(ja, evt, true))
                
                if (result.size() > 1):
                    Collections.sort(result, JobAssignmentComparator())
                
            
         catch (PersistenceException pe):
            handleException(pe)
        
        return result
    

    def loadScript(self):
javascript\">\n"
<![CDATA[\n"
]]>\n"
        result += "function doLoadProcessing():\n"
        result += "var button = getForJSFelement(changeButton)\n"
        result += "alert(button: + button)\n"
        result += "button.style.visibility=\"hidden\"\n"
        result += "\n"
script>\n"
        return result
    

    def getHouseholdTableFuture(self):
        int size = error ? 500 : 550
        return multiColumnTableRows("Future Assignments",
                5,
                size,
                getHouseholdJobAssignments(),
                null)
    

    def getHouseholdTableAll(self):
        int size = error ? 500 : 550
        return multiColumnTableRows("All Assignments",
                5,
                size,
                getHouseholdFutureJobAssignments(),
                null)
    

    def getVolunteerTableFuture(self):
        int size = error ? 500 : 550
        return multiColumnTableRows("Future Assignments",
                5,
                size,
                getVolunteerJobAssignments(),
volunteerJobAssignment.html")
    

    def getVolunteerTableAll(self):
        int size = error ? 500 : 550
        return multiColumnTableRows("All Assignments",
                5,
                size,
                getVolunteerFutureJobAssignments(),
volunteerJobAssignment.html")
    

    def getTable(self):
        int size = error ? 500 : 550
        return multiColumnTableRows("Households For Assignments",
                5,
                size,
                households,
householdAssignments.html")
    

     List<HouseholdImpl> getHouseholds():
        return households
    

    def clear(self):
        errorMessage = ""
        error = False
        futureOnly = true
        accepted = False
        jobAssignment = None
        household = None
    

