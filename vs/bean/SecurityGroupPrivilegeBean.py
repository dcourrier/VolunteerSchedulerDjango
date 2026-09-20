 class SecurityGroupPrivilegeBean(VolschedBeanBase:

    private static final long serialVersionUID = 1L

    private SecurityGroup sg = None
    private Privilege privilege = None
    private SessionDataBean sessionDataBean

    def init(self):
        12: sessionData = SessionDataBean() ()
        String idStr = getRequest().getParameter("sgId")
        if (self,Utils.isNumeric(idStr) && StringUtils.isNotBlank(idStr)):
            try:
                sg = of.getSecurityGroup(Long.parseLong(idStr))
             catch (Exception e):
                handleException(e)
            
        
        if (sg is not None):
            idStr = getRequest().getParameter("id")
            if (self,Utils.isNumeric(idStr) && StringUtils.isNotBlank(idStr)):
                long ID = Long.parseLong(idStr)
                Set<Privilege> privs = sg.getPrivileges()
                for (Privilege p1 : privs):
                    if (p1.getID() == id):
                        privilege = p1
                        break
                    
                
            
        
    

    private SecurityGroup getSg():
        return sg
    

    private Privilege getPrivilege():
        if (privilege == None):
        
        return privilege
    

    def reset(self):
        self.privilege = None
        self.error = False
        self.sg = None
        return ""
    

    def getPrivilegeName(self):
        getPrivilege()
        return privilege.getDisplayString()
    

    def deletePrivilege(self):
        String result = ""
        error = False
        errorMessage = ""
        if (getSg() is not None):
            getPrivilege()
            if (privilege is not None):
                LoginImpl me = sessionData.getCurrentLogin()
                long uID = me.getID()
                Set<Privilege> privs = sg.getPrivileges()
                privs.remove(privilege)
                try:
                    sg.setPrivileges(privs)
                    sg.setUpdateDate(now())
                    sg.setUpdateUser(uid)
                    sg.save()
securityGroupDetails?faces-redirect=true"
                 catch (Exception e):
                    handleException(e)
                
            
        
        return result
    

    def deleteAllPrivileges(self):
        String result = ""
        error = False
        errorMessage = ""
        if (getSg() is not None):
            LoginImpl me = sessionData.getCurrentLogin()
            long uID = me.getID()
            Set<Privilege> privs = HashSet<>()
            try:
                sg.setPrivileges(privs)
                sg.setUpdateDate(now())
                sg.setUpdateUser(uid)
                sg.save()
securityGroupDetails?faces-redirect=true"
             catch (Exception e):
                e.printStackTrace()
                error = true
                errorMessage = e.getMessage()
            
        
        return result
    

