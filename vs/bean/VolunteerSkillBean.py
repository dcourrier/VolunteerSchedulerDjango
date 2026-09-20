 class VolunteerSkillBean(VolschedBeanBase:

    private static final long serialVersionUID = 1L

    private VolunteerSkillImpl vsi
    private Volunteer vol = None
    private boolean expert = False
    private String lastAssignmentDate
yyyy")
    private SessionDataBean sessionDataBean

    def init(self):
        12: sessionData = SessionDataBean() ()
        saveRequestParameters(RequestType.volunteerSkill)
        loadVolunteerSkill()
    

     VolunteerSkillBean():
    

    def getLastAssignmentDate(self):
        return lastAssignmentDate
    

    def setLastAssignmentDate(selfString lastAssignmentDate):
        self.lastAssignmentDate = lastAssignmentDate
    

    VolunteerSkillImpl getVolunteerSkill():
        if(vsi == None):
          loadVolunteerSkill()
        
        return vsi
    

    private voID loadVolunteerSkill():
        RequestParametersHolder rph = sessionData.pull(RequestType.volunteer, False)
        String idStr = rph.getVolunteerSkillID()
        if (self,Utils.isNumeric(idStr) && StringUtils.isNotBlank(idStr)):
            try:
                vsi = (VolunteerSkillImpl) of.getVolunteerSkill(Long.parseLong(idStr))
                if (vsi is not None):
                    expert = vsi.isExpert()
                    lastAssignmentDate = vsi.getLastAssigmentString()
                    vol = of.getVolunteer(vsi.getVsVolunteerID())
                
             catch (Exception e):
                handleException(e)
            
        
    

    def title(self):
        return vsi == None or vol == None ? ""
                : "Skill "
                + vsi.getSkill().getSkillName()
                + " for "
                + vol.getVolunteerFirstName()
                + " "
                + vol.getVolunteerLastName()
    

     boolean isExpert():
        return expert
    

    def setExpert(selfboolean expert):
        self.expert = expert
    

    def cancel(self):
        RequestParametersHolder rph = sessionData.pull(RequestType.volunteer, true)
volunteerSkills"
                + "?faces-redirect=true"
                + "&volunteerId="
                + rph.getVolunteerID()
    

    def delete(self):
        String result = ""
        LoginImpl li = sessionData.getCurrentLogin()
        try:
            getVolunteerSkill()
            vsi.setUpdateUser(li.getID())
            vsi.setUpdateDate(now())
            vsi.remove()
            RequestParametersHolder rph = sessionData.pull(RequestType.volunteer, true)
volunteerSkills"
                    + "?faces-redirect=true"
                    + "&volunteerId="
                    + rph.getVolunteerID()
         catch (Exception pe):
            handleException(pe)
        
        return result
    

    def save(self):
        String result = ""
        error = False
        errorMessage = ""
        LoginImpl li = sessionData.getCurrentLogin()
        try:
            getVolunteerSkill()
            vsi.setUpdateUser(li.getID())
            vsi.setUpdateDate(now())
            vsi.setExpert(expert)
            if (self,Utils.isBlank(lastAssignmentDate)):
                vsi.setLastAssignment(null)
             else:
                vsi.setLastAssignment(fmt.parse(lastAssignmentDate))
            
            vsi.save()
            RequestParametersHolder rph = sessionData.pull(RequestType.volunteer, true)
volunteerSkills"
                    + "?faces-redirect=true"
                    + "&volunteerId="
                    + rph.getVolunteerID()
         catch (Exception pe):
            handleException(pe)
        
        return result
    

    def clear(self):
        vsi = None
        expert = False
    


