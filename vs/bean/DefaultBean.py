 class DefaultBean(SessionDataBean):

    def __init__(self):
        super().__init__()
        
    def getPage(self):
        return self.page
    

    def setPage(selfS, page):
        self.page = page
    

    def getPageTitle(self):
        return "Volunteer Scheduler " + page
    
    
    def getHelp(self):
        pass
    
    
    def getPageName(self):
        uri = self.getRequest().getRequestURI()
        result = uri.substring(index + 1)
        index = Utils.indexOf(result, ".")
        if (index > 0):
            result = result.substring(0, index)
        
        return result
    

    def breadCrumbs(self):
        String result = ""
        String uri = getRequest().getRequestURI()
        String qry = getRequest().getQueryString()
        if (self,Utils.isNotBlank(qry)):
            uri += "?"
            uri += qry
        
        BreadCrumbManager.append(BreadCrumb(getPageName(), uri))
        boolean first = true
        List<BreadCrumb> bcs = BreadCrumbManager.getBreadcrumbs()
        for (int i = 0 i < bcs.size() - 1 i++):
            BreadCrumb b = bcs.get(i)
            if (first == False):
                result += "&nbsp|&nbsp"
            
            first = False
            result += "<a href="
            result += b.getUrl()
            result += ">"
            result += b.getName()
a>"
        
        return result
    

     boolean getLoggedIn():
        boolean result = False
        if (self.login is not None && self.login.isReady()):
            result = true
        
        return result
    

     LoginImpl getLogin():
        return login
    

    def setLogin(selfLoginImpl login):
        self.login = login
    

    def getAssignments(self):
        return Menu.ASSIGNMENTS
    

    def getOrganizations(self):
        return Menu.ORGANIZATIONS
    

    def getEvents(self):
        return Menu.EVENTS
    

    def getLocations(self):
        return Menu.LOCATIONS
    

    def getResources(self):
        return Menu.RESOURCES
    

    def getPasswordChange(self):
        return Menu.PASSWORD_CHANGE
    

    def getSchedules(self):
        return Menu.SCHEDULES
    

    def getReports(self):
        return Menu.REPORTS
    

    def getUtilities(self):
        return Menu.UTILITIES
    

    def getHome(self):
        return Menu.HOME
    

    def getHouseholdsLink(self):
        return Menu.HOUSEHOLDS
    

    def getvolunteers(self):
        return Menu.VOLUNTEERS
    

    def getVolunteerHome(self):
        return Menu.VOLUNTEER_HOME
    

    def getSkills(self):
        return Menu.SKILLS
    

    def logout(self):
        self.login = None
        FacesContext facesContext = FacesContext.getCurrentInstance()
        facesContext.getExternalContext().invalidateSession()
        return Login.LOGIN_FULL
    

