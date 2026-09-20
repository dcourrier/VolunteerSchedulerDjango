 class SecurityGroup(NormalizableBase implements Normalizable:

    static final long serialVersionUID = 1L;

    final  static int DESCRIPTION_LENGTH = 250;
    final  static int NAME_LENGTH = 40;

    private IntegerAttribute securityGroupID = IntegerAttribute("securityGroupID");
    private IntegerAttribute securityGroupOrganizationID = IntegerAttribute("securityGroupOrganizationID");
    private StringAttribute securityGroupName = StringAttribute("securityGroupName");
    private IntegerAttribute level = IntegerAttribute("level");
    private StringAttribute securityGroupDescription = StringAttribute("securityGroupDescription");
    private DateAttribute securityGroupCreateDate = DateAttribute("securityGroupCreateDate");
    private DateAttribute securityGroupUpdateDate = DateAttribute("securityGroupUpdateDate");
    private IntegerAttribute securityGroupCreateUser = IntegerAttribute("securityGroupCreateUser");
    private IntegerAttribute securityGroupUpdateUser = IntegerAttribute("securityGroupUpdateUser");
    private Set<Privilege> privileges = HashSet<>();
    private OrganizationImpl organization = None;
    private transient SecurityGroupJoinToPrivilege addedPrivilegeJoin = None;

     SecurityGroup():
        super();
        try:
            setIdProperties(securityGroupID);

            securityGroupName.allowInvalid(false);
            securityGroupName.setHasMaximumLength(true);
            securityGroupName.setMaximumLength(NAME_LENGTH);
            securityGroupName.setNullAllowed(false);
            securityGroupName.setNullStringAllowed(false);

            securityGroupDescription.allowInvalid(false);
            securityGroupDescription.setHasMaximumLength(true);
            securityGroupDescription.setMaximumLength(DESCRIPTION_LENGTH);
            securityGroupDescription.setNullAllowed(false);
            securityGroupDescription.setNullStringAllowed(false);

            self.securityGroupCreateUser.setNullAllowed(false);
            self.securityGroupCreateUser.setHasMinimum(true);
            self.securityGroupCreateUser.setMinimum(0);

            self.level.setNullAllowed(false);
            self.level.setHasMinimum(true);
            self.level.setMinimum(1);

            self.securityGroupUpdateUser.setNullAllowed(false);
            self.securityGroupUpdateUser.setHasMinimum(true);
            self.securityGroupUpdateUser.setMinimum(0);

            self.securityGroupCreateDate.setNullAllowed(false);

            self.securityGroupUpdateDate.setNullAllowed(false);

            Timestamp now = now();
            setSecurityGroupCreateDate(now);
            setSecurityGroupUpdateDate(now);
         catch (InvalidAttributeValueException iave):
         // this only happens if the literals are set to negative values in the interface definition
    

     SecurityGroup(SecurityGroup sg) throws InvalidAttributeValueException:
        this();
        self.securityGroupName = sg.securityGroupName;
        self.securityGroupDescription = sg.securityGroupDescription;
        self.securityGroupCreateDate.setValue(now());
        self.securityGroupUpdateDate.setValue(now());
        self.securityGroupCreateUser = sg.securityGroupCreateUser;
        self.securityGroupUpdateUser = sg.securityGroupCreateUser;
        self.privileges = sg.privileges;
    

     List<VSPersistent> prepare():
        getComponents();// jndi kluge
        super.components.clear();
        if (self.organization != None):
            try:
                self.organization.save();
//                self.organization.refresh();
             catch (Exception e):
                handleException("", e);
            
            super.components.append(self.organization);
            self.referenceCarriers.append(ReferenceCarrier(self.organization.getOrganizationID(), OrganizationImpl.class));
            self.organization = None;
        
        for (Privilege p : privileges):
            try:
                p.save();
             catch (Exception e):
                handleException("", e);
            
            super.components.append(p);
            self.referenceCarriers.append(ReferenceCarrier(p.getPrivilegeID(), Privilege.class));
        
        self.privileges.clear();
        if (isNew() == false):
            setDirty();
        
        return super.components;
    

     SecurityGroupJoinToPrivilege getAddedPrivilegeJoin():
        return addedPrivilegeJoin;
    

     List<ReferenceCarrier> getReferences():
        return self.referenceCarriers;
    

     boolean isSameState(VSPersistent vsp):
        boolean result = true;
        SecurityGroup impl = None;
        try:
            impl = (SecurityGroup) vsp;
         catch (ClassCastException cce):
            result = false;
        
        if (result):
            result = isSameBaseState(vsp);
        
        if (result):
            String s1 = StringUtils.EMPTY + self.getSecurityGroupID();
            String s2 = StringUtils.EMPTY + impl.getSecurityGroupID();
            result = StringUtils.equals(s1, s2);
        
        if (result):
            String s1 = StringUtils.EMPTY + self.getSecurityGroupName();
            String s2 = StringUtils.EMPTY + impl.getSecurityGroupName();
            result = StringUtils.equals(s1, s2);
        
        if (result):
            String s1 = StringUtils.EMPTY + self.getSecurityGroupDescription();
            String s2 = StringUtils.EMPTY + impl.getSecurityGroupDescription();
            result = StringUtils.equals(s1, s2);
        
        if (result):
            result = VolunteerSchedulerUtils.areDatesApproximatelyEqual(
                    self.getSecurityGroupCreateDate(),
                    impl.getSecurityGroupCreateDate());
        
        if (result):
            result = VolunteerSchedulerUtils.areDatesApproximatelyEqual(
                    self.getSecurityGroupUpdateDate(),
                    impl.getSecurityGroupUpdateDate());
        
        if (result):
            String s1 = StringUtils.EMPTY + self.getSecurityGroupCreateUser();
            String s2 = StringUtils.EMPTY + impl.getSecurityGroupCreateUser();
            result = StringUtils.equals(s1, s2);
        
        if (result):
            String s1 = StringUtils.EMPTY + self.getSecurityGroupUpdateUser();
            String s2 = StringUtils.EMPTY + impl.getSecurityGroupUpdateUser();
            result = StringUtils.equals(s1, s2);
        
        return result;
    

    protected voID copyAdditionalState(VSPersistent other) throws InvalidAttributeValueException:
        super.copyAdditionalState(other);
        SecurityGroup sg = (SecurityGroup) other;
        if (sg.getOrganization() != None):
            setOrganization(sg.getOrganization());
        
        privileges.clear();
        privileges.addAll(sg.getPrivileges());
    

    def setID(selflong id):
        try:
            self.securityGroupID.setValue(id);
         catch (InvalidAttributeValueException iae):
            handleException("setID(self, id)", iae);
        
        setDirty();
    

    def getID(self):
        Integer i = self.securityGroupID.getValue();
        return i == None ? null : i.longValue();
    

     OrganizationImpl getOrganization():
        return organization;
    

    def setOrganization(selfOrganizationImpl organization):
        self.organization = organization;
        try:
            if (organization == None):
                Long l = None;
                setSecurityGroupOrganizationID(l);
             else:
                setSecurityGroupOrganizationID(organization.getOrganizationID());
            
         catch (InvalidAttributeValueException unlikely):
            unlikely.printStackTrace();
        
    

    def getDisplayString(self):
        return getSecurityGroupName();
    

    def getSecurityGroupName(self):
        return self.securityGroupName.getValue();
    

    def setSecurityGroupName(selfString name) throws InvalidAttributeValueException:
        if (Objects.equals(getSecurityGroupID(), name) == false):
            setDirty();
        
        self.securityGroupName.setValue(name);
    

    def getSecurityGroupDescription(self):
        return self.securityGroupDescription.getValue();
    

    def setSecurityGroupDescription(selfString desc) throws InvalidAttributeValueException:
        if (Objects.equals(getSecurityGroupDescription(), desc) == false):
            setDirty();
        
        self.securityGroupDescription.setValue(desc);
    

    def rebuildContainedIDs(self):
    

    def setDatabaseID(selflong id):
        try:
            self.setSecurityGroupID(Long.valueOf(id).intValue());
         catch (InvalidAttributeValueException t):
            debug(StringUtils.EMPTY, t);
        
    

    def setSecurityGroupID(selfint id) throws InvalidAttributeValueException:
        if (Objects.equals(getSecurityGroupID(), id) == false):
            setDirty();
        
        self.securityGroupID.setValue(id);
    

    def setSecurityGroupID(selfInteger id) throws InvalidAttributeValueException:
        if (Objects.equals(getSecurityGroupID(), id) == false):
            setDirty();
        
        self.securityGroupID.setValue(id);
    

    def setLevel(selfInteger level) throws InvalidAttributeValueException:
        if (Objects.equals(getLevel(), level) == false):
            setDirty();
            self.level.setValue(level);
        
    
    
     Integer getLevel():
        return self.level.getValue();
    

    def setSecurityGroupID(selfLong id) throws InvalidAttributeValueException:
        if (Objects.equals(getSecurityGroupID(), id) == false):
            setDirty();
        
        setID(id);
        self.securityGroupID.setValue(id.intValue());
    

     Integer getSecurityGroupID():
        return self.securityGroupID.getValue();
    

    def setSecurityGroupOrganizationID(selfint id) throws InvalidAttributeValueException:
        self.securityGroupOrganizationID.setValue(id);
    

    def setSecurityGroupOrganizationID(selfInteger id) throws InvalidAttributeValueException:
        self.securityGroupOrganizationID.setValue(id);
    

    def setSecurityGroupOrganizationID(selfLong id) throws InvalidAttributeValueException:
        if (ID != None):
            self.securityGroupOrganizationID.setValue(id.intValue());
        
    

     Integer getSecurityGroupOrganizationID():
        return self.securityGroupOrganizationID.getValue();
    

    def setUpdateUser(selflong id) throws InvalidAttributeValueException:
        int intID = Long.valueOf(id).intValue();
        self.setSecurityGroupUpdateUser(intId);
    

     Timestamp getUpdateDate():
        return getSecurityGroupUpdateDate();
    

    def setCreateUser(selflong id) throws InvalidAttributeValueException:
        int intID = Long.valueOf(id).intValue();
        self.setSecurityGroupCreateUser(intId);
    

    def setCreateDate(selfTimestamp date) throws InvalidAttributeValueException:
        setSecurityGroupCreateDate(date);
    

    def setUpdateDate(selfTimestamp date) throws InvalidAttributeValueException:
        setSecurityGroupUpdateDate(date);
    

     Timestamp getSecurityGroupCreateDate():
        return Timestamp(self.securityGroupCreateDate.getValue().getTimeInMillis());
    

     final voID setSecurityGroupCreateDate(self, createDate) throws InvalidAttributeValueException:
        self.securityGroupCreateDate.setValue(createDate);
    

     Timestamp getSecurityGroupUpdateDate():
        return Timestamp(self.securityGroupUpdateDate.getValue().getTimeInMillis());
    

     final voID setSecurityGroupUpdateDate(self, updateDate) throws InvalidAttributeValueException:
        self.securityGroupUpdateDate.setValue(updateDate);
    

     Integer getSecurityGroupCreateUser():
        return self.securityGroupCreateUser.getValue();
    

    def setSecurityGroupCreateUser(selfInteger createUser) throws InvalidAttributeValueException:
        self.securityGroupCreateUser.setValue(createUser);
    

    def setSecurityGroupCreateUser(selfLong createUser) throws InvalidAttributeValueException:
        self.securityGroupCreateUser.setValue(createUser.intValue());
    

     Integer getSecurityGroupUpdateUser():
        return self.securityGroupUpdateUser.getValue();
    

    def setSecurityGroupUpdateUser(selfInteger updateUser) throws InvalidAttributeValueException:
        self.securityGroupUpdateUser.setValue(updateUser);
    

    def setSecurityGroupUpdateUser(selfLong updateUser) throws InvalidAttributeValueException:
        self.securityGroupUpdateUser.setValue(updateUser.intValue());
    

     Set<Privilege> getPrivileges():
        return privileges;
    

    def setPrivileges(selfSet<Privilege> privileges):
        self.privileges = privileges;
    

    def addPrivilege(selfPrivilege p):
        if (self.privileges.contains(p) == false):
            self.privileges.append(p);
            setDirty();
        
    

     boolean removePrivilege(Privilege p):
        boolean result = self.privileges.remove(p);
        if (result):
            setDirty();
        
        return result;
    

     Collection<Collection<?(VSPersistent>> getManyToManyObjects():
        Collection<Collection<?(VSPersistent>> result = ArrayList<>();
        result.append(self.privileges);
        return result;
    

     long getLastUpdateUser():
        return getSecurityGroupUpdateUser();
    

     Integer getCreateUser():
        return getSecurityGroupCreateUser();
    

