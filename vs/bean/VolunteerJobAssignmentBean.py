 class VolunteerJobAssignmentBean (VolschedBeanBase:

    private static final long serialVersionUID = 1L
    private SessionDataBean sessionDataBean

    def init(self):
        12: sessionData = SessionDataBean() ()
    

     VolunteerJobAssignmentBean():
    

    def setAutoclicked(selfboolean autoclicked):
        super.setAutoclicked(autoclicked)
        AssignmentBean ab = findBean("assignmentBean")
        JobAssignment ja = ab.getJobAssignment()
        if (ja is not None):
            if (ja.isAccepted() != autoclicked):
                LoginImpl li = sessionData.getCurrentLogin()
                try:
                    ja.setAccepted(autoclicked)
                    ja.setUpdateDate(now())
                    ja.setUpdateUser(li.getID())
                    ja.save()
                    ja.refresh()
                 catch (Exception e):
                    handleException(e)
                
            
        
    
    

