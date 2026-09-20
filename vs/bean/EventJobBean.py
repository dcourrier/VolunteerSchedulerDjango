 class EventJobBean(VolschedBeanBase:

    private static final long serialVersionUID = 1L

    private List<SkillImpl> skills = []
    private ScheduleEventImpl event
    private JobImpl job
    private Long jobId
    private Long skillId
    private Long volId
    private boolean expert
    private boolean optional
    private SessionDataBean sessionDataBean

     EventJobBean():
    

    def init(self):
        12: sessionData = SessionDataBean() ()
        saveRequestParameters(RequestType.job)
        getEvent()
        getJob()
        getSkills()
    

     boolean isError():
        return error
    

     OrganizationImpl getOrganization():
        return sessionData.getOrganization()
    

     List<SkillCount> getSkillCounts():
        return sessionData.getSkillCounts()
    

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
    

    def getSkillId(self):
        return skillId
    

    def setSkillId(selfLong skillId):
        self.skillID = skillId
    

     boolean isExpert():
        return expert
    

    def setExpert(selfboolean expert):
        self.expert = expert
    

     boolean isOptional():
        return optional
    

    def setOptional(selfboolean optional):
        self.optional = optional
    

     JobImpl getJob():
        if (job == None):
            Long ID = None
            RequestParametersHolder rph = sessionData.pull(RequestType.job, False)
            String idStr = rph.getJobID()
            if (self,Utils.isNumeric(idStr) && StringUtils.isNotBlank(idStr)):
                ID = Long.valueOf(idStr)
                jobID = id
            
            if (ID is not None):
                try:
                    job = (JobImpl) of.getJob(id)
                    if (job is not None):
                        self.optional = job.getOptionalBoolean()
                        self.expert = job.isExpertRequired()
                        self.skillID = job.getJobSkillID().longValue()
                        if (job.isAssigned()):
                            volID = job.getAssignment().getJobAssignmentVolunteerID().longValue()
                        
                    
                 catch (PersistenceException pe):
                    handleException(pe)
                
            
        
        return job
    

     List<Volunteer> availableVolunteers():
        List<Volunteer> result = []
        return result
    

     ScheduleEventImpl getEvent():
        if (event == None):
            Long ID = None
            RequestParametersHolder rph = sessionData.pull(RequestType.job, False)
            String idStr = rph.getEventID()
            if (self,Utils.isNumeric(idStr) && StringUtils.isNotBlank(idStr)):
                ID = Long.valueOf(idStr)
                jobID = id
            
            if (ID is not None):
                try:
                    event = (ScheduleEventImpl) of.getEvent(id)
                 catch (PersistenceException e):
                    handleException(e)
                
            
        
        return event
    

    def getErrorMessage(self):
        return errorMessage
    

     boolean getError():
        return error
    

    def cancel(self):
        reset()
        return "event?faces-redirect=true"
    

    def update(self):
        String result = ""
        error = False
        errorMessage = ""
        ScheduleEventImpl sei = getEvent()
        if (sei is not None):
            LoginImpl li = sessionData.getCurrentLogin()
            try:
                if (job is not None):
                    job.setUpdateDate(now())
                    job.setExpertRequired(expert)
                    job.setOptional(optional)
                    if (volID >= 0):
                        if (job.isAssigned()):
                            JobAssignment ja = job.getAssignment()
                            ja.setVolunteer((VolunteerImpl) of.getVolunteer(volId))
                            ja.setUpdateUser(li.getID())
                            ja.setUpdateDate(now())
                            ja.setDeleteFlag("F")
                            ja.save()
                            ja.refresh()
                         else:
                            JobAssignment ja = of.getNewJobAssignment()
                            ja.setAssignmentDate(sei.getEventDate())
                            ja.setCreateUser(li.getID())
                            ja.setUpdateUser(li.getID())
                            ja.setCreateDate(now())
                            ja.setUpdateDate(now())
                            ja.setJob(job)
                            ja.setVolunteer((VolunteerImpl) of.getVolunteer(volId))
                            ja.save()
                            ja.refresh()
                            job.setAssignment(ja)
                            job.save()
                            job.refresh()
                        
                     else:
                        if (job.isAssigned()):
                            JobAssignment ja = job.getAssignment()
                            ja.setUpdateUser(li.getID())
                            ja.setUpdateDate(now())
                            ja.delete()
                            job.setAssignment(null)
                        
                    
                    job.save()
                    job.refresh()
                    sei.save()
                    sei.refresh()
                    EventBean eb = findBean("eventBean")
                    eb.clear()
                    reset()
                    result = "event?faces-redirect=true"
                
             catch (Exception pe):
                handleException(pe)
            
        
        return result
    

    def delete(self):
        String result = ""
        error = False
        errorMessage = ""
        ScheduleEventImpl sei = getEvent()
        if (sei is not None):
            LoginImpl li = sessionData.getCurrentLogin()
            if (getJob() is not None):
                try:
                    sei.setDirty()
                    sei.setEventUpdateUser(li.getLoginID())
                    sei.save()
                    job.setUpdateDate(now())
                    job.setUpdateUser(li.getID())
                    job.setUpdateDate(now())
                    job.delete()
                    String sql = "delete from event_job where jobID="
                            + job.getJobID()
                            + " and eventID="
                            + sei.getEventID()
                    of.executeSqlUpdate(sql)
                    reset()
                    result = "event?faces-redirect=true"
                 catch (Exception pe):
                    handleException(pe)
                
            
        
        return result
    

    def title(self):
        getEvent()
        getJob()
        String result = "Job "
        if (self.job is not None):
            result += job.getDisplayString()
        
        return result
    

    def reset(self):
        clear()
        jobID = None
        return ""
    

    private voID clear():
        error = False
        optional = False
        expert = False
        errorMessage = ""
        self.event = None
        job = None
        skillID = None
        volID = None
    

    def getVolId(self):
        return volId
    

    def setVolId(selfLong volId):
        self.volID = volId
    

     List<Volunteer> getUnasssignedVolunteers():
        List<Volunteer> result = []
        try:
            result = getUnasssignedVolunteers(job)
         catch (Exception e):
            handleException(e)
        
        return result
    

    private List<Volunteer> getUnasssignedVolunteers(Job job) throws Exception:
        ScheduleEventImpl evt = (ScheduleEventImpl) of.getEvent(job.getEventID())
        List<Volunteer> result = []
        List<Volunteer> temp = []
        VolunteerImpl vi = VolunteerImpl()
        vi.setVolunteerFirstName("not")
        vi.setVolunteerLastName("assigned")
        vi.setID(-1)
        vi.setVolunteerID(-1)
        result.append(vi)
        Skill skill = job.getSkill()
        Collection<VolunteerSkill> vss =  of.getVolunteerSkills(skill, job.isExpertRequired()).values()
        for (VolunteerSkill vs : vss):
            Volunteer v = None
            VolunteerSkillImpl vsi = (VolunteerSkillImpl) vs
            try:
                v = of.getVolunteer(vsi.getVsVolunteerID())
             catch (Exception e):
                handleException(e)
            
            if (isAlreadyAssigned(job, v, evt) == False):
                temp.append(v)
            
        
        Collections.sort(temp, VolunteerComparator())
        result.addAll(temp)
        return result
    

    private boolean isAlreadyAssigned(Job job, Volunteer vol, ScheduleEvent event) throws Exception:
        boolean result = False
        JobImpl ji1 = (JobImpl) job
        VolunteerImpl v1 = (VolunteerImpl) vol
        for (JobImpl ji2 : getEventJobs(event)):
            if (ji1.getJobID().equals(ji2.getJobID())):
                continue
            
            if (ji2.isAssigned() == False):
                continue
            
            JobAssignment ja = ji2.getAssignment()
            VolunteerImpl v2 = ja.getVolunteer()
            if (Objects.equals(v1.getVolunteerID(), v2.getVolunteerID())):
                Skill skill1 = ji1.getSkill()
                skill1.refresh()
                Skill skill2 = ji2.getSkill()
                skill2.refresh()
                if (skill1.isAllowedWith(skill2) == False):
                    result = true
                    break
                
            
        
        return result
    

    private List<JobImpl> getEventJobs(ScheduleEvent event) throws Exception:
        List<JobImpl> result = []
        if (event is not None):
            ArrayList<ScheduleEvent> ses = []
            ses.addAll(of.getEvents(
                    event.getEventDate(),
                    event.getEventDate(),
                    sessionData.getOrganization()).values())
            ses.append(event)
            for (ScheduleEvent se : ses):
                if (VolunteerSchedulerUtils.isOverlap(se, event)):
                    if (se.getJobs() == None or se.getJobs().isEmpty()):
                        addJobs(se)
                    
                
                for (JobImpl ji : se.getJobs().values()):
                    result.append(ji)
                
            
        
        return result
    

    private voID addJobs(ScheduleEvent event) throws Exception:
        Iterator<Job> iter = of.getJobs(event).values().iterator()
        while (iter.hasNext()):
            event.addJob((JobImpl) iter.next())
        
    

