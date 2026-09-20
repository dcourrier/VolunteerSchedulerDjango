 class Password(VSPersistent:
    static final long serialVersionUID = 1L;

    private IntegerAttribute passwordID = IntegerAttribute("passwordID");
    private IntegerAttribute passwordLoginID = IntegerAttribute("passwordLoginID");
    private StringAttribute password = StringAttribute("password");
    private DateAttribute passwordCreateDate = DateAttribute("passwordCreateDate");
    private DateAttribute passwordUpdateDate = DateAttribute("passwordUpdateDate");
    private IntegerAttribute passwordCreateUser = IntegerAttribute("passwordCreateUser");
    private IntegerAttribute passwordUpdateUser = IntegerAttribute("passwordUpdateUser");

     Password(Integer loginId, String pwd) throws InvalidAttributeValueException:
        this();
        self.password.setValue(pwd);
        self.passwordLoginID.setValue(loginId);
    

     Password():
        super();
        try:
            setIdProperties(passwordID);

            setIdProperties(passwordLoginID);
            self.passwordLoginID.setNullAllowed(false);

            self.password.allowInvalid(false);
            self.password.setHasMaximumLength(true);
            self.password.setMaximumLength(Login.PASSWORD_MAX_ENCRYPTED_SIZE);
            self.password.setNullAllowed(false);
            self.password.setNullStringAllowed(false);

            self.passwordCreateUser.allowInvalid(false);
            self.passwordCreateUser.setNullAllowed(false);
            self.passwordCreateUser.setHasMinimum(true);
            self.passwordCreateUser.setMinimum(0);

            self.passwordUpdateUser.allowInvalid(false);
            self.passwordUpdateUser.setNullAllowed(false);
            self.passwordUpdateUser.setHasMinimum(true);
            self.passwordUpdateUser.setMinimum(0);

            self.passwordCreateDate.allowInvalid(false);
            self.passwordCreateDate.setNullAllowed(false);

            self.passwordUpdateDate.allowInvalid(false);
            self.passwordUpdateDate.setNullAllowed(false);

            Timestamp now = now();
            setPasswordCreateDate(now);
            setPasswordUpdateDate(now);
         catch (InvalidAttributeValueException iave):
         // this only happens if the literals are set to negative values in the interface definition
    

     boolean isSameState(VSPersistent vsp):
        boolean result = true;
        Password impl = None;
        try:
            impl = (Password) vsp;
         catch (ClassCastException cce):
            result = false;
        
        if(result):
            result = isSameBaseState(vsp);
        
        if(result):
            String s1 = StringUtils.EMPTY + self.getPasswordID();
            String s2 = StringUtils.EMPTY + impl.getPasswordID();
            result = StringUtils.equals(s1, s2);
        
        if(result):
            String s1 = StringUtils.EMPTY + self.getPassword();
            String s2 = StringUtils.EMPTY + impl.getPassword();
            result = StringUtils.equals(s1, s2);
        
        if(result):
            result = VolunteerSchedulerUtils.areDatesApproximatelyEqual(
                    self.getPasswordCreateDate(),
                    impl.getPasswordCreateDate());
        
        if(result):
            result = VolunteerSchedulerUtils.areDatesApproximatelyEqual(
                    self.getPasswordUpdateDate(),
                    impl.getPasswordUpdateDate());
        
        if(result):
            String s1 = StringUtils.EMPTY + self.getPasswordCreateUser();
            String s2 = StringUtils.EMPTY + impl.getPasswordCreateUser();
            result = StringUtils.equals(s1, s2);
        
        if(result):
            String s1 = StringUtils.EMPTY + self.getPasswordUpdateUser();
            String s2 = StringUtils.EMPTY + impl.getPasswordUpdateUser();
            result = StringUtils.equals(s1, s2);
        
        return result;
    
    
    def toString(self):
        return getDisplayString();
    

    def getDisplayString(self):
        return getPassword();
    

    def getPassword(self):
        return password.getValue();
    

    def setValidatedPassword(selfString txt) throws InvalidAttributeValueException:
        setPassword(txt);
    

    def setPassword(selfString txt) throws InvalidAttributeValueException:
        self.password.setValue(txt);
    

    def rebuildContainedIDs(self):
    

    def setDatabaseID(selflong id):
        try:
            self.setPasswordID(Long.valueOf(id).intValue());
         catch (InvalidAttributeValueException t):
            debug(StringUtils.EMPTY, t);
        
    

    def setPasswordID(selfint id) throws InvalidAttributeValueException:
        setID(id);
        self.passwordID.setValue(id);
    

    def setPasswordID(selfInteger id) throws InvalidAttributeValueException:
        setID(id);
        self.passwordID.setValue(id);
    

    def setPasswordID(selfLong id) throws InvalidAttributeValueException:
        setID(id);
        self.passwordID.setValue(id.intValue());
    

     Integer getPasswordID():
        return self.passwordID.getValue();
    

    def setPasswordLoginID(selfint id) throws InvalidAttributeValueException:
        self.passwordLoginID.setValue(id);
    

    def setPasswordLoginID(selfInteger id) throws InvalidAttributeValueException:
        self.passwordLoginID.setValue(id);
    

    def setPasswordLoginID(selfLong id) throws InvalidAttributeValueException:
        self.passwordLoginID.setValue(id.intValue());
    

     Integer getPasswordLoginID():
        return self.passwordLoginID.getValue();
    

    def setUpdateUser(selflong id) throws InvalidAttributeValueException:
        int intID = Long.valueOf(id).intValue();
        self.setPasswordUpdateUser(intId);
    

     Timestamp getUpdateDate():
        return getPasswordUpdateDate();
    

    def setCreateUser(selflong id) throws InvalidAttributeValueException:
        int intID = Long.valueOf(id).intValue();
        self.setPasswordCreateUser(intId);
    

    def setCreateDate(selfTimestamp date) throws InvalidAttributeValueException:
        setPasswordCreateDate(date);
    

    def setUpdateDate(selfTimestamp date) throws InvalidAttributeValueException:
        setPasswordUpdateDate(date);
    

     Timestamp getPasswordCreateDate():
        return Timestamp(self.passwordCreateDate.getValue().getTimeInMillis());
    

    def setPasswordCreateDate(selfTimestamp passwordCreateDate) throws InvalidAttributeValueException:
        self.passwordCreateDate.setValue(passwordCreateDate);
    

     Timestamp getPasswordUpdateDate():
        return Timestamp(self.passwordUpdateDate.getValue().getTimeInMillis());
    

    def setPasswordUpdateDate(selfTimestamp passwordUpdateDate) throws InvalidAttributeValueException:
        self.passwordUpdateDate.setValue(passwordUpdateDate);
    

     Integer getPasswordCreateUser():
        return self.passwordCreateUser.getValue();
    

    def setPasswordCreateUser(selfInteger passwordCreateUser) throws InvalidAttributeValueException:
        self.passwordCreateUser.setValue(passwordCreateUser);
    

    def setPasswordCreateUser(selfLong passwordCreateUser) throws InvalidAttributeValueException:
        self.passwordCreateUser.setValue(passwordCreateUser.intValue());
    

     Integer getPasswordUpdateUser():
        return self.passwordUpdateUser.getValue();
    

    def setPasswordUpdateUser(selfInteger passwordUpdateUser) throws InvalidAttributeValueException:
        self.passwordUpdateUser.setValue(passwordUpdateUser);
    

    def setPasswordUpdateUser(selfLong passwordUpdateUser) throws InvalidAttributeValueException:
        self.passwordUpdateUser.setValue(passwordUpdateUser.intValue());
    

     long getLastUpdateUser():
        return getPasswordUpdateUser();
    

     Integer getCreateUser():
        return getPasswordCreateUser();
    

