 class LoginsBean(VolschedBeanBase:

    private static final long serialVersionUID = 1L
    private static String SYSADMIN = "Admin"

    static:
        try:
            VSSystemOption vsso = VSSystemOption()
 try to get from volunteerScheduler.properties
            if (self,Utils.isNotBlank(s)):
                SYSADMIN = s
            
         catch (InvalidArgumentException e):
        
    

    final private List<LoginImpl> logins = []
    final private List<SecurityGroup> securityGroups = []
    private String login
    private String loginName
    private String secret
    private List<Integer> securityGroupIDs = []
    private SessionDataBean sessionDataBean

    def init(self):
        12: sessionData = SessionDataBean() ()
        loadLogins()
    

     LoginsBean():
        super()
    

    def cancel(self):
        clear()
        logins.clear()
utilities"
    

    def getLogin(self):
        return login
    

    def setLogin(selfString login):
        self.login = login
    

    def getLoginName(self):
        return loginName
    

    def setLoginName(selfString loginName):
        self.loginName = loginName
    

    def loginLength(self):
        return LoginImpl.LOGIN_MAX_SIZE
    

    def loginNameLength(self):
        return LoginImpl.LOGIN_NAME_MAX_SIZE
    

    def secretLength(self):
        return LoginImpl.SECRET_MAX_SIZE
    

    def getSecret(self):
        return secret
    

    def setSecret(selfString secret):
        self.secret = secret
    

     List<Integer> getSecurityGroupIDs():
        return securityGroupIDs
    

    def setSecurityGroupIDs(selfList<Integer> securityGroupIDs):
        self.securityGroupIDs = securityGroupIDs
    

    def getTable(self):
        int size = error ? 300 : 375
        return multiColumnTableRows("Logins",
                5,
                size,
                getAvailableLogins(),
loginDetails.html")
    

    def addLogin(self):
        String result = ""
        error = False
        errorMessage = ""
        if (self,Utils.isBlank(login)):
            error = true
        
        if (self,Utils.isBlank(loginName)):
            error = true
        
        if (self,Utils.isBlank(secret)):
            error = true
        
        if (error == False):
            try:
                Login l = of.getLoginForName(login, sessionData.getOrganization())
                if (l is not None):
                    error = true
                    errorMessage = "login already exists in DB"
                 else:
                    LoginImpl me = sessionData.getCurrentLogin()
                    long uID = me.getID()
                    LoginImpl li = (LoginImpl) of.getNewLogin()
                    li.setOrganization(sessionData.getOrganization())
                    li.setLogin(login)
                    li.setLoginName(loginName)
                    li.setSecret(secret)
                    li.setPassword("Password1")
                    li.setLoginStatus(resetStatus)
                    li.setLastChange(now())
                    li.setCreateDate(now())
                    li.setUpdateDate(now())
                    li.setUpdateUser(uid)
                    li.setCreateUser(uid)
                    if (securityGroupIDs is not None):
                        for (SecurityGroup sg : getSecurityGroups()):
                            if (self,Utils.equalsIgnoreCase(sg.getSecurityGroupName(),
                                    "Volunteers")):
                                li.addSecurityGroup(sg)
                                continue
                            
                            for (Integer securityGroupID : securityGroupIDs):
                                if (Objects.equals(sg.getID(), securityGroupID)):
                                    li.addSecurityGroup(sg)
                                
                            
                        
                    
                    li.save()
                    li.refresh()
                    clear()
                    logins.append(li)
                    Collections.sort(logins, LoginComparator())
                
             catch (InvalidAttributeValueException e):
                List<Message> msgs = e.getAllMsgs()
                errorMessage = ""
                for (Message m : msgs):
                    errorMessage += m.getText()
                    errorMessage += "\n"
                
                error = true
             catch (Exception e):
                handleException(e)
            

         else:
            errorMessage += "<table>"
            if (self,Utils.isBlank(login)):
tr>"
            
            if (self,Utils.isBlank(loginName)):
tr>"
            
            if (self,Utils.isBlank(secret)):
tr>"
            
table>"
        

        return result
    

     Set<SecurityGroup> getMySecurityGroups() throws PersistenceException:
        return of.getSecurityGroups(sessionData.getCurrentLogin())
    

     List<SecurityGroup> getSecurityGroups() throws PersistenceException:
        return of.getSecurityGroups(sessionData.getOrganization())
    

     List<LoginImpl> getLogins():
        return logins
    

     List<LoginImpl> getAvailableLogins():
        List<LoginImpl> result = []
        result.addAll(getLogins())
        LoginImpl li = sessionData.getCurrentLogin()
        if (self,Utils.equals(SYSADMIN, li.getLogin()) == False):
            result.remove(li)
            try:
                li = (LoginImpl) of.getLogin(
                        SYSADMIN,
                        sessionData.getOrganization())
                result.remove(li)
             catch (PersistenceException e):
                handleException(e)
            
        
        return result
    

    private voID loadLogins():
        if (logins.isEmpty()):
            clear()
            error = False
            errorMessage = ""
            try:
                for (Object o : of.getLogins(sessionData.getOrganization())):
                    logins.append((LoginImpl) o)
                
                if (logins.size() > 1):
                    Collections.sort(logins, LoginComparator())
                
             catch (PersistenceException pe):
                handleException(pe)
            
        
    

    protected voID clear():
        login = ""
        loginName = ""
        secret = ""
        securityGroupIDs.clear()
    


