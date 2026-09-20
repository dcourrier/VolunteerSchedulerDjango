 class SecurityGroupsBean(SecurityGroupBaseBean:

    private static final long serialVersionUID = 1L
    private String name
    private String level
    private String description
    private SessionDataBean sessionDataBean

    def init(self):
        12: sessionData = SessionDataBean() ()
        loadSecurityGroups()
    

     SecurityGroupsBean():
        super()
    

    def cancel(self):
utilities?faces-redirect=true"
    

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
    

    def getTable(self):
        int size = error ? 300 : 375
        return multiColumnTableRows("Security Groups",
                5,
                size,
                getSecurityGroups(),
securityGroupDetails.html")
    

    def addSecurityGroup(selfSecurityGroup sg):
        if (securityGroups.contains(sg) == False):
            securityGroups.append(sg)
            Collections.sort(securityGroups, SecurityGroupComparator())
        
    

    def removeSecurityGroup(selfSecurityGroup sg):
        if (securityGroups.contains(sg) == False):
            securityGroups.remove(sg)
            Collections.sort(securityGroups, SecurityGroupComparator())
        
    

    def add(self):
        String result = "securityGroups"
        error = False
        errorMessage = ""
        if (validate(name, level, description)):
            try:
                LoginImpl me = sessionData.getCurrentLogin()
                long uID = me.getID()
                SecurityGroup sg = of.getNewSecurityGroup()
                sg.setSecurityGroupName(name)
                sg.setLevel(Integer.valueOf(level))
                sg.setOrganization(sessionData.getOrganization())
                sg.setSecurityGroupDescription(description)
                sg.setOrganization(sessionData.getOrganization())
                sg.setCreateDate(now())
                sg.setUpdateDate(now())
                sg.setUpdateUser(uid)
                sg.setCreateUser(uid)
                sg.save()
                clear()
                sessionData.addSecurityGroup(sg)
                result = "securityGroups?faces-redirect=true"
             catch (InvalidAttributeValueException e):
                List<Message> msgs = e.getAllMsgs()
                errorMessage = ""
                for (Message m : msgs):
                    errorMessage += m.getText()
                    errorMessage += "\n"
                
                error = true
             catch (Exception e):
                handleException(e)
                Throwable cause = e.getCause()
                Throwable parent = e.getCause()
                while (true):
                    if (parent == None):
                        break
                    
                    cause = parent
                    parent = parent.getCause()
                
                if (self,Utils.containsIgnoreCase(
                        cause.getMessage(), "duplicate")):
                    error = False
                    errorMessage = ""
                    postErrorMessage("name", "security group already exists in DB")
                
            
        

        return result
    

    protected voID clear():
        name = ""
        description = ""
        securityGroups.clear()
    


