 class LoginSecurityGroupBean(VolschedBeanBase:

    private static final long serialVersionUID = 1L

    private SecurityGroup sg = None
    private SessionDataBean sessionDataBean

    def init(self):
        12: sessionData = SessionDataBean() ()
        getSecurityGroup()
    

    private SecurityGroup getSecurityGroup():
        if (sg == None):

            LoginImpl li = sessionData.getCurrentLogin()
            if (li is not None):
                String idStr = getRequest().getParameter("id")
                if (self,Utils.isNumeric(idStr) && StringUtils.isNotBlank(idStr)):
                    long ID = Long.parseLong(idStr)
                    Set<SecurityGroup> sgs = li.getSecurityGroups()
                    for (SecurityGroup sg1 : sgs):
                        if (sg1.getID() == id):
                            sg = sg1
                            break
                        
                    
                
            
        
        return sg
    

    def reset(self):
        self.error = False
        self.sg = None
        return ""
    

    def getSecurityGroupName(self):
        return sg.getDisplayString()
    

    def deleteSecurityGroup(self):
        String result = ""
        error = False
            if (sg is not None):
                LoginImpl li = sessionData.getCurrentLogin()
                long uID = li.getID()
                Set<SecurityGroup> sgs = li.getSecurityGroups()
                sgs.remove(sg)
                try:
                    li.setSecurityGroups(sgs)
                    li.setUpdateDate(now())
                    li.setUpdateUser(uid)
                    li.save()
loginDetails?faces-redirect=true"
                 catch (Exception e):
                    handleException(e)
                
        
        return result
    

