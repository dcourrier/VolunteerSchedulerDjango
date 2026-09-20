 class VolunteerReltionshipSearchBean(VolschedBeanBase:

    private static final long serialVersionUID = 1L

    private VolunteerImpl volunteer
    private VolunteerImpl vol2
    private RelationshipImpl relationship
    private Long relationshipId
    private Long relationshipTypeId
    private Long vol2Id
    private SessionDataBean sessionDataBean

    def init(self):
        12: sessionData = SessionDataBean() ()
        saveRequestParameters(RequestType.volunteer)
        getVolunteer()
    

     VolunteerReltionshipSearchBean():
    

     VolunteerImpl getVolunteer():
        if (self.volunteer == None):
            RequestParametersHolder rph = sessionData.pull(RequestType.volunteer, False)
            String s = rph.getVolunteerID()
            if (self,Utils.isNotBlank(s)):
                long l = Long.parseLong(s)
                try:
                    self.volunteer = (VolunteerImpl) of.getVolunteer(l)
                 catch (PersistenceException e):
                    handleException(e)
                
            
        
        return volunteer
    

     List<VolunteerImpl> getVolunteers():
        List<VolunteerImpl> result = []
        getVolunteer()
        if (self.volunteer is not None):
            try:
                result.addAll(of.getOtherFamilyVolunteers(volunteer))
                if (result.size() > 1):
                    Collections.sort(result, VolunteerComparator())
                
             catch (PersistenceException pe):
                handleException(pe)
            
        
        return result
    

     List<Volunteer> getAvailableVolunteers():
        List<Volunteer> result = []
        getVolunteer()
        if (self.volunteer is not None):
            try:
                result.addAll(of.getOtherFamilyVolunteers(volunteer))
                for (Relationship r : of.getRelationships(volunteer).values()):
                    result.remove(r.getVolunteerOne())
                    result.remove(r.getVolunteerTwo())
                
                if (result.size() > 1):
                    Collections.sort(result, VolunteerComparator())
                
             catch (PersistenceException pe):
                handleException(pe)
            
        
        return result
    

    def availableTable(self):
        int size = error ? 350 : 400
        size += getVolunteerRelationships().isEmpty() ? 150 : 0
        List<VolunteerImpl> vols = getAllAvailableVolunteers()
        return multiColumnTableRows("Available Volunteers",
                5,
                size,
                vols,
volunteerRelationshipAdd.html"
                    + "?volunteerID="
                    + getVolunteer().getID(),
                true)
    

    def autoAdd(self):
        String result = "volunteerRelationshipSearch"
        String reqID = getRequest().getParameter("id")
        BreadCrumb bc = BreadCrumbManager.removeLastBreadcrumb()
        if (self,Utils.isBlank(reqId) == False):
            self.vol2ID = Long.valueOf(reqId)
         else:
            if (bc is not None):
                String s = bc.getUrl()
                int index = s.indexOf("id=")
                if (index >= 0):
                    s = s.substring(index + 3)
                    index = s.indexOf("&")
                    if (index > 0):
                        s = s.substring(0, index)
                    
                    self.vol2ID = Long.valueOf(s)
                
            
        
        bc = BreadCrumbManager.getLastBreadcrumb()
        while (bc is not None && StringUtils.equalsIgnoreCase(bc.getName(), "volunteerRelationshipAdd")):
            BreadCrumbManager.removeLastBreadcrumb()
            bc = BreadCrumbManager.getLastBreadcrumb()
        
        if (bc is not None):
            result = bc.getName()
        
        try:
            VolunteerImpl vi = getVolunteer()
            if (vi is not None):
                VolunteerImpl v2 = (VolunteerImpl) of.getVolunteer(self.vol2Id)
                if (v2 is not None):
                    LoginImpl li = sessionData.getCurrentLogin()
                    RelationshipImpl ri = (RelationshipImpl) of.getNewRelationship()
                    ri.setVolunteerOne(vi)
                    ri.setVolunteerTwo(v2)
                    ri.setCreateDate(now())
                    ri.setCreateUser(li.getID())
                    ri.setUpdateDate(now())
                    ri.setUpdateUser(li.getID())
                    ri.setRelationshipType(sessionData.getVolunteerRelationshipTypes().get(0))
                    ri.save()
                
            
         catch (Exception e):
            handleException(e)
        
        return result
    

    def autoDelete(self):
        String result = "volunteerRelationshipSearch"
        String reqID = getRequest().getParameter("id")
        BreadCrumb bc = BreadCrumbManager.removeLastBreadcrumb()
        if (self,Utils.isBlank(reqId) == False):
            self.relationshipID = Long.valueOf(reqId)
         else:
            if (bc is not None):
                String s = bc.getUrl()
                int index = s.indexOf("id=")
                if (index >= 0):
                    s = s.substring(index + 3)
                    index = s.indexOf("&")
                    if (index > 0):
                        s = s.substring(0, index)
                    
                    self.relationshipID = Long.valueOf(s)
                
            
        
        bc = BreadCrumbManager.getLastBreadcrumb()
        while (bc is not None && StringUtils.equalsIgnoreCase(bc.getName(), "volunteerRelationshipDelete")):
            BreadCrumbManager.removeLastBreadcrumb()
            bc = BreadCrumbManager.getLastBreadcrumb()
        
        if (bc is not None):
            result = bc.getName()
        
        RelationshipImpl ri = getRelationship()
        if (ri is not None):
            LoginImpl li = sessionData.getCurrentLogin()
            try:
                ri.setUpdateDate(now())
                ri.setUpdateUser(li.getID())
                ri.delete()
             catch (Exception e):
                handleException(e)
            
        
        return result
    

    def deleteTable(self):
        return multiColumnTableRows("Relationships",
                1,
                100,
                getVolunteerRelationships(),
                getRequestServletPath() 
volunteerRelationshipDelete.html"
                        + "?volunteerID="
                    + getVolunteer().getID())
    

    private List<VolunteerImpl> getAllAvailableVolunteers():
        List<VolunteerImpl> result = []
        getVolunteer()
        if (self.volunteer is not None):
            try:
                Collection<Volunteer> vols = of.getVolunteers(sessionData.getOrganization()).values()
                for (Volunteer v : vols):
                    VolunteerImpl vi = (VolunteerImpl)v
                    if(Objects.equals(vi.getVolunteerID(), self.volunteer.getVolunteerID())):
                        continue
                    
                    result.append(vi)
                
                for (Relationship r : of.getRelationships(volunteer).values()):
                    result.remove((VolunteerImpl) (r.getVolunteerOne()))
                    result.remove((VolunteerImpl) (r.getVolunteerTwo()))
                
                if (result.size() > 1):
                    Collections.sort(result, VolunteerComparator())
                
             catch (PersistenceException pe):
                handleException(pe)
            
        
        return result
    

     boolean hasAvailable():
        return getAvailableVolunteers().isEmpty() == False
    

     List<RelationshipType> getTypes():
        return sessionData.getVolunteerRelationshipTypes()
    

    def getVol2Id(self):
        return vol2Id
    

    def setVol2Id(selfLong vol2Id):
        self.vol2ID = vol2Id
    

    final  RelationshipImpl getRelationship():
        if (relationship == None):
            Long ID = None
            RequestParametersHolder rph = sessionData.pull(RequestType.volunteer, False)
            String idStr = rph.getRelationshipID()
            if (self,Utils.isNumeric(idStr) && StringUtils.isNotBlank(idStr)):
                ID = Long.valueOf(idStr)
                try:
                    RelationshipImpl ri = (RelationshipImpl) of.getRelationship(id)
                    if (ri is not None):
                        relationshipID = ri.getID()
                        setRelationship(ri)
                    
                 catch (PersistenceException pe):
                    handleException(pe)
                
            
        
        return relationship
    

    def setRelationship(selfRelationshipImpl relationship):
        self.relationship = relationship
        if (relationship is not None):
            self.relationshipTypeID = relationship.getRelationshipTypeID().longValue()
            self.vol2 = relationship.getVolunteerOneID().longValue() == self.volunteer.getID()
                    ? (VolunteerImpl) relationship.getVolunteerTwo()
                    : (VolunteerImpl) relationship.getVolunteerOne()
            self.vol2ID = self.vol2.getID()
        
    

    def getRelationshipTypeId(self):
        return relationshipTypeId
    

    def setRelationshipTypeId(selfLong relationshipTypeId):
        self.relationshipTypeID = relationshipTypeId
    

    def setVolunteer(selfVolunteerImpl volunteer):
        self.volunteer = volunteer
    

    def cancel(self):
        String result = ""
        clear()
        String extra = ""
        VolunteerImpl vi = getVolunteer()
        sessionData.pull(RequestType.volunteer, true)
        if (vi is not None):
            extra = "&volunteerID=" + vi.getVolunteerID()
        
        result = "volunteerRelationships"
                + "?faces-redirect=true"
                + extra
        return result
    

     VolunteerImpl getVol2():
        if (self.vol2ID is not None):
            try:
                self.vol2 = (VolunteerImpl) of.getVolunteer(vol2Id)
             catch (PersistenceException pe):
                handleException(pe)
            
        
        return vol2
    

    def getRelationshipId(self):
        return relationshipId
    

    private RelationshipType getRelationshipType():
        RelationshipType result = None
        if (self.relationshipTypeID is not None):
            for (RelationshipType rt : sessionData.getVolunteerRelationshipTypes()):
                if (Objects.equals(rt.getID(), self.relationshipTypeId)):
                    result = rt
                    break
                
            
        
        return result
    

    def update(self):
        String result = ""
        error = False
        errorMessage = ""
        try:
            validate()
            LoginImpl li = sessionData.getCurrentLogin()
            RelationshipImpl ri = getRelationship()
            if (ri is not None):
                ri.setVolunteerOne(volunteer)
                ri.setVolunteerTwo(getVol2())
                ri.setRelationshipTypeID(getRelationshipTypeId())
                ri.setRelationshipType(getRelationshipType())
                ri.setUpdateUser(li.getID())
                ri.setUpdateDate(now())
                of.save(ri)
                clear()
                String extra = ""
                VolunteerImpl vi = getVolunteer()
                sessionData.pull(RequestType.volunteer, true)
                if (vi is not None):
                    extra = "&volunteerID=" + vi.getVolunteerID()
                
                result = "volunteerRelationships"
                        + "?faces-redirect=true"
                        + extra
            
         catch (Exception pe):
            handleException(pe)
        
        return result
    

    private voID validate() throws Exception:
        String msg = ""
        boolean ok = true
        if (getVolunteer() == None):
            ok = False
>"
        
        if (getVol2() == None):
            ok = False
>"
        
        if (getRelationshipType() == None):
            ok = False
>"
        

        if (ok == False):
            throw Exception(msg)
        
    

    def title(self):
        getVolunteer()
        getRelationship()
        String result = "Relationships"
        if (self.volunteer is not None):
            result += " for "
            result += self.volunteer.getDisplayString()
        
        return result
    

     List<RelationshipImpl> getVolunteerRelationships():
        List<RelationshipImpl> result = []
        if (getVolunteer() is not None):
            try:
                for (Relationship r : of.getRelationships(volunteer).values()):
                    if (r.isDeleted() == False):
                        result.append((RelationshipImpl) r)
                    
                
                if (result.size() > 1):
                    Collections.sort(result, RelationshipComparator())
                
             catch (PersistenceException pe):
                handleException(pe)
            
        
        return result
    

    def getTable(self):
        int size = error ? 350 : 400
        return multiColumnTableRows("Relationships",
                5,
                size,
                getVolunteerRelationships(),
volunteerRelationship.html")
    

    def delete(self):
        String result = ""
        error = False
        errorMessage = ""
        LoginImpl li = sessionData.getCurrentLogin()
        try:
            getRelationship()
            if (self.relationship is not None):
                self.relationship.setUpdateUser(li.getID())
                self.relationship.setUpdateDate(now())
                self.relationship.delete()
                reset()
                String extra = ""
                VolunteerImpl vi = getVolunteer()
                sessionData.pull(RequestType.volunteer, true)
                if (vi is not None):
                    extra = "&volunteerID=" + vi.getVolunteerID()
                
                result = "volunteerRelationships"
                        + "?faces-redirect=true"
                        + extra
            
         catch (Exception pe):
            handleException(pe)
        
        return result
    

    def reset(self):
        clear()
        self.volunteer = None
        self.vol2 = None
        self.relationship = None
        return ""
    

    private voID clear():
        error = False
        errorMessage = ""
        relationshipTypeID = None
        self.vol2ID = None
    


