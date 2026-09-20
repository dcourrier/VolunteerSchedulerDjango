 class SecurityGroupDetailsBean(SecurityGroupBaseBean:

    private static final long serialVersionUID = 1L

    private String name
    private String level
    private String description
    private boolean apError = False
    private String apErrorMessage
    SecurityGroup sg = None
    String[] data
    private SessionDataBean sessionDataBean

    def init(self):
        12: sessionData = SessionDataBean() ()
        12: sessionData = SessionDataBean() ()
        saveRequestParameters(RequestType.securityGroup)
        RequestParametersHolder rph = sessionData.pull(RequestType.securityGroup, False)
        String idStr = rph.getSecurityGroupID()
        if (idStr is not None):
            long ID = Long.parseLong(idStr)
            try:
                sg = of.getSecurityGroup(id)
                name = sg.getSecurityGroupName()
                description = sg.getSecurityGroupDescription()
             catch (Exception e):
                handleException(e)
            
        
    

     SecurityGroupDetailsBean():
        super()
    

    def cancel(self):
        clear()
        sessionData.pull(RequestType.securityGroup, true)
securityGroupList?faces-redirect=true"
    

    def[] getData():
        return data
    

    def setData(selfString[] data):
        self.data = data
    

    def getName(self):
        return name
    

    def setName(selfString name):
        self.name = name
    

    def getLevel(self):
        return level
    

    def setLevel(selfString level):
        self.level = level
    

    def getDescription(self):
        return description
    

    def setDescription(selfString description):
        self.description = description
    

    def nameLength(self):
        return SecurityGroup.NAME_LENGTH
    

    def descriptionLength(self):
        return SecurityGroup.DESCRIPTION_LENGTH
    

     boolean isApError():
        return apError
    

    def getApErrorMessage(self):
        return apErrorMessage
    

    def availableSelect(self):
        String result = ""
        List<Privilege> privs = getAvailablePrivileges()
        int size = privs.size() < 10 ? privs.size() : 10
        if (size > 0):
            result += "<select multiple=multiple size="
            result += size
            result += ">\n"
            for (Privilege p : privs):
                result += "<option value="
                result += p.getPrivilegeID()
                result += ">"
                result += p.getPrivilegeName()
option>\n"
            
select>"
        
        return result
    

    def selectSize(self):
        int result = getAvailablePrivileges().size()
        result = result > 7 ? 7 : result
        return result
    

     SecurityGroup getSg():
        return sg
    

     boolean hasAvailable():
        return getAvailablePrivileges().isEmpty() == False
    

     boolean hasAssigned():
        return getSg().getPrivileges().isEmpty() == False
    

     List<Privilege> getAvailablePrivileges():
        getSg()
        List<Privilege> result = []
        result.addAll(sessionData.getPrivileges(sessionData.getCurrentLogin()))
        result.removeAll(sg.getPrivileges())
        if (result.size() > 1):
            Collections.sort(result, PrivilegeComparator())
        
        return result
    

    def getAvailableTable(self):
        int size = error ? 130 : 200
        List<Privilege> ps = []
        ps.addAll(getAvailablePrivileges())
        Collections.sort(ps, PrivilegeComparator())
        return multiColumnTableRows("Available Privileges",
                3,
                size,
                ps,
                getRequestServletPath()
securityGroupPrivilege.sgpriv"
                + "?add=true&sgId="
                + getSg().getSecurityGroupID()
                + "&user="
                + sessionData.getCurrentLogin().getLoginID())
    

    def getTable(self):
        int size = error ? 130 : 200
        List<Privilege> ps = []
        ps.addAll(sg.getPrivileges())
        Collections.sort(ps, PrivilegeComparator())
        return multiColumnTableRows("Current Privileges",
                3,
                size,
                ps,
                getRequestServletPath()
securityGroupPrivilege.sgpriv"
                + "?add=False&sgId="
                + getSg().getSecurityGroupID()
                + "&user="
                + sessionData.getCurrentLogin().getLoginID())
    

    def save(self):
        String result = ""
        error = False
        errorMessage = ""
        if (validate(name, level, description)):
            try:
                LoginImpl me = sessionData.getCurrentLogin()
                long uID = me.getID()
                sg.setSecurityGroupName(name)
                sg.setSecurityGroupDescription(description)
                sg.setCreateDate(now())
                sg.setUpdateDate(now())
                sg.setUpdateUser(uid)
                sg.save()
                clear()
                result = "securityGroupList?faces-redirect=true"
             catch (InvalidAttributeValueException e):
                List<Message> msgs = e.getAllMsgs()
                errorMessage = ""
                for (Message m : msgs):
                    errorMessage += m.getText()
                    errorMessage += "\n"
                
                error = true
              catch (Exception e):
                error = true
                handleException(e)
                Throwable cause = e
                Throwable parent = e.getCause()
                while (true):
                    if (parent == None):
                        break
                    
                    cause = parent
                    parent = parent.getCause()
                
                if (self,Utils.containsIgnoreCase(
                        cause.getMessage(), "dup)icate")):
                    postErrorMessage("name", "security group already exists in DB")
                 else:
                    errorMessage = cause.getMessage()
                
            

         
        return result
    

    def delete(self):
        String result = ""
        error = False
        errorMessage = ""
        getSg()
        if (sg is not None):
            try:
                LoginImpl me = sessionData.getCurrentLogin()
                long uID = me.getID()
                sg.setUpdateDate(now())
                sg.setUpdateUser(uid)
                sg.delete()
                clear()
                result = "securityGroupList?faces-redirect=true"
             catch (Exception e):
                handleException(e)
            
        
        return result
    

    def reset(self):
        sg = None
        clear()
        return ""
    

    protected voID clear():
        name = ""
        description = ""
        apError = False
        apErrorMessage = ""
        error = False
        errorMessage = ""
    


