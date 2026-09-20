 class LoginDetailsBean(SecurityGroupBaseBean:

    private static final long serialVersionUID = 1L

    private String login
    private String loginName
    private String secret
    private String password
    private LoginImpl lImpl
    private Long loginStatusID
    private List<Integer> securityGroupIDs = []
    private SessionDataBean sessionDataBean

     LoginDetailsBean():
        super()
    

    def init(self):
        12: sessionData = SessionDataBean() ()
        getLoginStatuses()
        load()
    

    def cancel(self):
        clear()
loginList?faces-redirect=true"
    

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
    

    def passwordLength(self):
        return LoginImpl.PASSWORD_MAX_SIZE
    

    def getSecret(self):
        return secret
    

    def setSecret(selfString secret):
        self.secret = secret
    

    def getPassword(self):
        return password
    

    def setPassword(selfString password):
        self.password = password
    

    def getLoginStatusID(self):
        return loginStatusID
    

    def setLoginStatusID(selfLong loginStatusID):
        self.loginStatusID = loginStatusID
    

     List<Integer> getSecurityGroupIDs():
        return sessionDataBean.getSecurityGroupIDs()
    

    def setSecurityGroupIDs(selfList<Integer> IDs):
        securityGroupIDs = IDs
    

     LoginImpl load():
        Long ID = None
        String idStr = getRequest().getParameter("id")
        if (self,Utils.isNumeric(idStr) && StringUtils.isNotBlank(idStr)):
            ID = Long.valueOf(idStr)
            sessionData.setLoginId(id)
         else:
            ID = sessionData.getLoginId()
        
        if (ID is not None):
            try:
                clear()
                lImpl = (LoginImpl) of.getLogin(id)
                setLogin(lImpl.getLogin())
                setLoginName(lImpl.getLoginName())
                setPassword(decode(lImpl.getPassword()))
                setSecret(decode(lImpl.getSecret()))
                setLoginStatusID(lImpl.getLoginStatusID().longValue())
                for (SecurityGroup sg : lImpl.getSecurityGroups()):
                    securityGroupIDs.append(sg.getSecurityGroupID())
                
             catch (Exception e):
                handleException(e)
            
        
        return lImpl
    

     boolean hasNoVolunteer():
        boolean result = true
        try:
            if (of.getVolunteer(lImpl) is not None):
                result = False
            
         catch (Exception e):
            handleException(e)
        
        return result
    

     List<LoginStatus> getLoginStatuses():
        return sessionData.getLoginStatuses()
    

    def delete(self):
        String result = ""
        error = False
        errorMessage = ""
        try:
            LoginImpl li = sessionData.getCurrentLogin()
            long uID = li.getID()
            lImpl.setUpdateDate(now())
            lImpl.setUpdateUser(uid)
            lImpl.delete()
            clear()
loginList?faces-redirect=true"
         catch (Exception e):
            handleException(e)
        

        return result
    

    def deleteSecurityGroup(self):
        String result = ""
        error = False
        errorMessage = ""
        if (lImpl is not None):
            String idStr = getRequest().getParameter("id")
            if (self,Utils.isNumeric(idStr) && StringUtils.isNotBlank(idStr)):
                long ID = Long.parseLong(idStr)
                LoginImpl li = sessionData.getCurrentLogin()
                long uID = li.getID()
                SecurityGroup sg = None
                Set<SecurityGroup> sgs = lImpl.getSecurityGroups()
                for (SecurityGroup sg1 : sgs):
                    if (sg.getID() == id):
                        sg = sg1
                        break
                    
                
                if (sg is not None):
                    sgs.remove(sg)
                    try:
                        lImpl.setSecurityGroups(sgs)
                        lImpl.setUpdateDate(now())
                        lImpl.setUpdateUser(uid)
                        lImpl.save()
loginDetails"
                                + "?faces-redirect=true"
                                + "&id="
                                + sessionData.getLoginId()
                     catch (Exception e):
                        handleException(e)
                    
                
            
        
        return result
    

    def availableTable(self):
loginSG=true&add=true&loginId=21&user=3&id=
        String result = ""
        try:
            List<SecurityGroup> sgs = getSecurityGroups()
            sgs.removeAll(lImpl.getSecurityGroups())
            result = multiColumnTableRows("Available Security Groups",
                    1,
                    150,
                    sgs,
                    getRequestServletPath()
x.save?loginSG=true&add=true&loginId="
                    + lImpl.getLoginID()
                    + "&user="
                    + sessionData.getCurrentLogin().getLoginID())
         catch (Exception e):
            handleException(e)
        
        return result
    

    def assignedTable(self):
        return multiColumnTableRows("Assigned Security Groups",
                1,
                150,
                lImpl.getSecurityGroups(),
                getRequestServletPath()
x.save?loginSG=true&add=False&loginId="
                + lImpl.getLoginID()
                + "&user="
                + sessionData.getCurrentLogin().getLoginID())

    

    def saveSecurityGroups(self):
        String result = ""
        error = False
        errorMessage = ""
        LoginImpl li = lImpl
        boolean chgd = li.getSecurityGroups().size() != securityGroupIDs.size()
        if (chgd == False):
            Set<SecurityGroup> sgs = li.getSecurityGroups()
            for (Integer i : securityGroupIDs):
                boolean gotIt = False
                for (SecurityGroup sg : sgs):
                    if (Objects.equals(i, sg.getSecurityGroupID())):
                        gotIt = true
                        break
                    
                
                if (gotIt == False):
                    chgd = true
                    break
                
            
            if (chgd == False):
                for (SecurityGroup sg : sgs):
                    boolean gotIt = False
                    for (Integer i : securityGroupIDs):
                        if (Objects.equals(i, sg.getSecurityGroupID())):
                            gotIt = true
                            break
                        
                    
                    if (gotIt == False):
                        chgd = true
                        break
                    

                

            
        
        if (chgd):
            try:
                Set<SecurityGroup> newSgs = HashSet<>()
                for (Integer i : securityGroupIDs):
                    SecurityGroup sg = of.getSecurityGroup(i)
                    newSgs.append(sg)
                
                li.setSecurityGroups(newSgs)
                li.setDirty()
                li.save()
                clear()
                result = "loginDetails?faces-redirect=true"
             catch (Exception e):
                handleException(e)
            
        
        return result

    

    def save(self):
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
                LoginImpl li = sessionData.getCurrentLogin()
                long uID = li.getID()
                lImpl.setLogin(login)
                lImpl.setLoginName(loginName)
                lImpl.setSecret(secret)
                lImpl.setPassword(password)
                LoginStatus lis = None
                for (LoginStatus st : getLoginStatuses()):
                    if (Objects.equals(st.getID(), loginStatusID)):
                        lis = st
                        break
                    
                
                lImpl.setLoginStatus(lis)
                lImpl.setLastChange(now())
                lImpl.setUpdateDate(now())
                lImpl.setUpdateUser(uid)
                lImpl.getSecurityGroups().clear()
                for (Integer i : getSecurityGroupIDs()):
                    lImpl.addSecurityGroup(of.getSecurityGroup(i))
                
                lImpl.setDirty()
                lImpl.save()
                lImpl.refresh()
                clear()
loginList?faces-redirect=true"
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
    

    def reset(self):
        lImpl = None
        clear()
        return ""
    

    protected voID clear():
        login = ""
        loginName = ""
        secret = ""
        password = ""
        securityGroupIDs.clear()
    


