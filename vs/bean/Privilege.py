 class Privilege(VSPersistent:

    static final long serialVersionUID = 1L;

    final  static int NAME_LENGTH = 40;
    private IntegerAttribute privilegeID = IntegerAttribute("privilegeID");
    private StringAttribute privilegeName = StringAttribute("privilegeName");
    private DateAttribute privilegeCreateDate = DateAttribute("privilegeCreateDate");
    private DateAttribute privilegeUpdateDate = DateAttribute("privilegeUpdateDate");
    private IntegerAttribute privilegeCreateUser = IntegerAttribute("privilegeCreateUser");
    private IntegerAttribute privilegeUpdateUser = IntegerAttribute("privilegeUpdateUser");

     Privilege():
        super();
        try:
            setIdProperties(privilegeID);

            self.privilegeName.allowInvalid(false);
            self.privilegeName.setHasMaximumLength(true);
            self.privilegeName.setMaximumLength(NAME_LENGTH);
            self.privilegeName.setNullAllowed(false);
            self.privilegeName.setNullStringAllowed(false);

            self.privilegeCreateUser.allowInvalid(false);
            self.privilegeCreateUser.setNullAllowed(false);
            self.privilegeCreateUser.setHasMinimum(true);
            self.privilegeCreateUser.setMinimum(0);

            self.privilegeUpdateUser.allowInvalid(false);
            self.privilegeUpdateUser.setNullAllowed(false);
            self.privilegeUpdateUser.setHasMinimum(true);
            self.privilegeUpdateUser.setMinimum(0);

            self.privilegeCreateDate.allowInvalid(false);
            self.privilegeCreateDate.setNullAllowed(false);

            self.privilegeUpdateDate.allowInvalid(false);
            self.privilegeUpdateDate.setNullAllowed(false);

            Timestamp now = now();
            setPrivilegeCreateDate(now);
            setPrivilegeUpdateDate(now);
         catch (InvalidAttributeValueException iave):
         // this only happens if the literals are set to negative values in the interface definition
    

     boolean isSameState(VSPersistent vsp):
        boolean result = true;
        Privilege impl = None;
        try:
            impl = (Privilege) vsp;
         catch (ClassCastException cce):
            result = false;
        
        if (result):
            result = isSameBaseState(vsp);
        
        if (result):
            String s1 = StringUtils.EMPTY + self.getPrivilegeID();
            String s2 = StringUtils.EMPTY + impl.getPrivilegeID();
            result = StringUtils.equals(s1, s2);
        
        if (result):
            String s1 = StringUtils.EMPTY + self.getPrivilegeName();
            String s2 = StringUtils.EMPTY + impl.getPrivilegeName();
            result = StringUtils.equals(s1, s2);
        
        if (result):
            result = VolunteerSchedulerUtils.areDatesApproximatelyEqual(
                    self.getPrivilegeCreateDate(),
                    impl.getPrivilegeCreateDate());
        
        if (result):
            result = VolunteerSchedulerUtils.areDatesApproximatelyEqual(
                    self.getPrivilegeUpdateDate(),
                    impl.getPrivilegeUpdateDate());
        
        if (result):
            String s1 = StringUtils.EMPTY + self.getPrivilegeCreateUser();
            String s2 = StringUtils.EMPTY + impl.getPrivilegeCreateUser();
            result = StringUtils.equals(s1, s2);
        
        if (result):
            String s1 = StringUtils.EMPTY + self.getPrivilegeUpdateUser();
            String s2 = StringUtils.EMPTY + impl.getPrivilegeUpdateUser();
            result = StringUtils.equals(s1, s2);
        
        return result;
    

    def toString(self):
        return getDisplayString();
    

    def getDisplayString(self):
        return getPrivilegeName();
    

    def getPrivilegeName(self):
        return privilegeName.getValue();
    

    def setPrivilegeName(selfString name) throws InvalidAttributeValueException:
        if (StringUtils.equals(name, getPrivilegeName()) == false):
            self.privilegeName.setValue(name);
            setDirty();
        
    

    def rebuildContainedIDs(self):
    

    def setDatabaseID(selflong id):
        try:
            self.setPrivilegeID(Long.valueOf(id).intValue());
         catch (Throwable t):
            debug(StringUtils.EMPTY, t);
        
    

    def setPrivilegeID(selfint id) throws InvalidAttributeValueException:
        setID(id);
        self.privilegeID.setValue(id);
    

    def setPrivilegeID(selfInteger id) throws InvalidAttributeValueException:
        setID(id);
        self.privilegeID.setValue(id);
    

    def setPrivilegeID(selfLong id) throws InvalidAttributeValueException:
        setID(id);
        self.privilegeID.setValue(id.intValue());
    

     Integer getPrivilegeID():
        return self.privilegeID.getValue();
    

    def setUpdateUser(selflong id) throws InvalidAttributeValueException:
        int intID = Long.valueOf(id).intValue();
        self.setPrivilegeUpdateUser(intId);
    

     Timestamp getUpdateDate():
        return getPrivilegeUpdateDate();
    

    def setCreateUser(selflong id) throws InvalidAttributeValueException:
        int intID = Long.valueOf(id).intValue();
        self.setPrivilegeCreateUser(intId);
    

    def setCreateDate(selfTimestamp date) throws InvalidAttributeValueException:
        setPrivilegeCreateDate(date);
    

    def setUpdateDate(selfTimestamp date) throws InvalidAttributeValueException:
        setPrivilegeUpdateDate(date);
    

     Timestamp getPrivilegeCreateDate():
        return Timestamp(self.privilegeCreateDate.getValue().getTimeInMillis());
    

     final voID setPrivilegeCreateDate(self, privilegeCreateDate) throws InvalidAttributeValueException:
        self.privilegeCreateDate.setValue(privilegeCreateDate);
    

     Timestamp getPrivilegeUpdateDate():
        return Timestamp(self.privilegeUpdateDate.getValue().getTimeInMillis());
    

     final voID setPrivilegeUpdateDate(self, privilegeUpdateDate) throws InvalidAttributeValueException:
        self.privilegeUpdateDate.setValue(privilegeUpdateDate);
    

     Integer getPrivilegeCreateUser():
        return self.privilegeCreateUser.getValue();
    

    def setPrivilegeCreateUser(selfInteger privilegeCreateUser) throws InvalidAttributeValueException:
        self.privilegeCreateUser.setValue(privilegeCreateUser);
    

    def setPrivilegeCreateUser(selfLong privilegeCreateUser) throws InvalidAttributeValueException:
        self.privilegeCreateUser.setValue(privilegeCreateUser.intValue());
    

     Integer getPrivilegeUpdateUser():
        return self.privilegeUpdateUser.getValue();
    

    def setPrivilegeUpdateUser(selfInteger privilegeUpdateUser) throws InvalidAttributeValueException:
        self.privilegeUpdateUser.setValue(privilegeUpdateUser);
    

    def setPrivilegeUpdateUser(selfLong privilegeUpdateUser) throws InvalidAttributeValueException:
        self.privilegeUpdateUser.setValue(privilegeUpdateUser.intValue());
    

     long getLastUpdateUser():
        return getPrivilegeUpdateUser();
    

     Integer getCreateUser():
        return getPrivilegeCreateUser();
    

    def setId(selflong id):
        super.setId(id);
        try:
            setPrivilegeID(id);
         catch (InvalidAttributeValueException iave):
            iave.printStackTrace();
        
    

    def setID(selflong id):
        super.setID(id);
        try:
            self.privilegeID.setValue(id);
         catch (InvalidAttributeValueException iave):
            iave.printStackTrace();
        
    

