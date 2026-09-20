 class EventResourceBean(VolschedBeanBase:

    private static final long serialVersionUID = 1L

    private List<Resource> resources = []
    private ScheduleEventImpl event
    private Resource resource
    private Long resourceId
    private Long resourceUsage
    private Long numJobs
    private SessionDataBean sessionDataBean

    def init(self):
        12: sessionData = SessionDataBean() ()
        saveRequestParameters(RequestType.projectResource)
        getEvent()
        try:
            getResourceAvailabilty()
         catch (Exception e):
            handleException(e)
        
    

     EventResourceBean():
    

    def getNumJobs(self):
        return numJobs
    

    def setNumJobs(selfLong numJobs):
        self.numJobs = numJobs
    

     List<SkillCount> getSkillCounts():
        List<SkillCount> result = []
        if (self.resource is not None):
            for (int i = 1 i <= resource.getCount() i++):
                result.append(SkillCount(i))
            
        
        return result
    

    def getResourceUsage(self):
        return resourceUsage
    

    def setResourceUsage(selfLong resourceUsage):
        self.resourceUsage = resourceUsage
    

    def getResourceId(self):
        return resourceId
    

    def setResourceId(selfLong resourceId):
        self.resourceID = resourceId
    

     Resource getResource():
        if (resource == None):
            Long ID = None
            String idStr = getRequest().getParameter("id")
            if (self,Utils.isNumeric(idStr) && StringUtils.isNotBlank(idStr)):
                ID = Long.valueOf(idStr)
                try:
                    resource = of.getResource(id)
                 catch (PersistenceException pe):
                    handleException(pe)
                
            
        
        return resource
    

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
    

     ScheduleEventImpl getEvent():
        if (event == None):
            RequestParametersHolder rph = sessionData.pull(RequestType.projectResource, False)
            String s = rph.getEventID()
            try:
                long ID = Long.parseLong(s)
                event = (ScheduleEventImpl) of.getEvent(id)
             catch (Exception e):
                handleException(e)
            
        
        return event
    

    def cancel(self):
        reset()
        RequestParametersHolder rph = sessionData.pull(RequestType.projectResource, true)
        return "event?faces-redirect=true&id=" + rph.getEventID()
    

    def update(self):
        String result = ""
        error = False
        errorMessage = ""
        ScheduleEventImpl sei = getEvent()
        if (sei is not None):
            try:
                Resource res = getResource()
                LoginImpl li = sessionData.getCurrentLogin()
                if (res is not None):
                    EventJoinToResource ejr = None
                    for (EventJoinToResource ejr1 : sei.getResourceJoins()):
                        if (ejr1.getResourceID().longValue() == res.getID()):
                            ejr = ejr1
                            break
                        
                    
                    if (ejr is not None):
                        ejr.setCount(resourceUsage)
                        ejr.setUpdateUser(li.getID())
                        ejr.setUpdateDate(now())
                        ejr.save()
                        ejr.refresh()
                     else:
                        sei.addResource(res)
                        sei.setUpdateUser(li.getID())
                        sei.setUpdateDate(now())
                        ejr = of.getNewEventResource(sei, res)
                        ejr.setCreateUser(li.getID())
                        ejr.setUpdateUser(li.getID())
                        ejr.setCreateDate(now())
                        ejr.setUpdateDate(now())
                        ejr.setCount(resourceUsage)
                        ejr.save()
                        ejr.refresh()
                        sei.save()
                    
                
                RequestParametersHolder rph = sessionData.pull(RequestType.projectResource, true)
                result = "event?faces-redirect=true&id=" + rph.getEventID()
                clear()
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
            try:
                if (resource is not None):
                    sei.removeResource(resource)
                    EventJoinToResource ejr = None
                    for (EventJoinToResource ejr1 : sei.getResourceJoins()):
                        if (ejr1.getResourceID().longValue() == resource.getID()):
                            ejr = ejr1
                            break
                        
                    
                    if (ejr is not None):
                        ejr.setUpdateUser(li.getID())
                        ejr.setUpdateDate(now())
                        ejr.delete()
                        sei.removeResource(ejr)
                        sei.setUpdateUser(li.getID())
                        sei.setUpdateDate(now())
                        sei.save()
                        sei.refresh()
                    
                    RequestParametersHolder rph = sessionData.pull(RequestType.resource, true)
                    result = "event?faces-redirect=true&id=" + rph.getEventID()
                    clear()
                
             catch (Exception pe):
                handleException(pe)
            
        
        return result
    

    def title(self):
        getEvent()
        try:
            getResourceAvailabilty()
         catch (Exception e):
            handleException(e)
        
        String result = "Usage of "
        if (self.resource is not None):
            result += self.resource.getDisplayString()
        
        return result
    

    def reset(self):
        clear()
        resourceID = None
        return ""
    

    private voID clear():
        error = False
        errorMessage = ""
        resources.clear()
        self.event = None
        resourceUsage = None
        numJobs = None
    

     List<ResourceAvailability> getResourceAvailabilities():
        List<ResourceAvailability> result = []
        try:
            result.addAll(ResourceAvailabilityManager(getOrganization()).getResourceAvailabilities(getEvent(), getResources()))
         catch (Exception pe):
            handleException(pe)
        
        return result
    

    private ResourceAvailability getResourceAvailabilty() throws Exception:
        ResourceAvailability result = None
        RequestParametersHolder rph = sessionData.pull(RequestType.projectResource, False)
        String idStr = rph.getProjectResourceID()
        Resource r = None
        if (self,Utils.isNumeric(idStr) && StringUtils.isNotBlank(idStr)):
            long ID = Long.parseLong(idStr)
            r = of.getResource(id)
            resource = r
         else:
            r = resource
        
        if (r is not None):
            self.resourceID = r.getID()
            result = ResourceAvailability(r, r.getCount())
            ScheduleEventImpl sei = getEvent()
            if (sei is not None):
                EventJoinToResource ejr = None
                for (EventJoinToResource ejr1 : sei.getResourceJoins()):
                    if (ejr1.getResourceID().longValue() == r.getID()):
                        ejr = ejr1
                        break
                    
                
                if (ejr is not None):
                    result.setCount(r.getCount() - ejr.getCount())
                    self.resourceUsage = ejr.getCount().longValue()
                
            
        
        return result
    

     List<ResourceAvailability> getResourceAvailabilitiesPlus():
        List<ResourceAvailability> result = []
        try:
            List<ResourceAvailability> ras = ResourceAvailabilityManager(getOrganization()).getResourceAvailabilities(getEvent(), getResources())
            ResourceAvailability ra = getResourceAvailabilty()
            if (ra is not None):
                ResourceAvailability foundIt = None
                for (ResourceAvailability r : ras):
                    if (r.getResource().getID().intValue() == ra.getResource().getID()):
                        foundIt = r
                        break
                    
                
                if (foundIt == None):
                    result.append(ra)
                 else:
                    foundIt.setCount(foundIt.getCount() + ra.getCount())
                
            
            result.addAll(ras)
         catch (Exception pe):
            handleException(pe)
        
        return result
    

