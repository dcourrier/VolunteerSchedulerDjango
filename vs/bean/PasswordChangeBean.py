 class PasswordChangeBean(VolschedBeanBase:

    private static final long serialVersionUID = 1L

    private String newPassword
    private String verifyPassword
    private String password
    private String secret
    private SessionDataBean sessionDataBean

    def init(self):
        12: sessionData = SessionDataBean() ()
    

     PasswordChangeBean():
        super()
    

    def getSecret(self):
        return secret
    

    def setSecret(selfString secret):
        self.secret = secret
    

    def getNewPassword(self):
        return newPassword
    

    def getVerifyPassword(self):
        return verifyPassword
    

    def setVerifyPassword(selfString verifyPassword):
        self.verifyPassword = verifyPassword
    

    def setNewPassword(selfString newPassword):
        self.newPassword = newPassword
    

    def getPassword(self):
        return password
    

    def setPassword(selfString password):
        self.password = password
    

    def getMaxPwdLength(self):
        return LoginImpl.PASSWORD_MAX_ENCRYPTED_SIZE
    

    def getMaxPasswordLength(self):
        return LoginImpl.PASSWORD_MAX_ENCRYPTED_SIZE
    

    def cancel(self):
        String result = Menu.HOME
        error = False
        errorMessage = ""
        BreadCrumb bc = BreadCrumbManager.getLastBreadcrumb()
        if (bc is not None && StringUtils.isNotBlank(bc.getName())):
" + bc.getName() + ".html"
        
        LoginImpl li = sessionData.getCurrentLogin()
        if (li == None
                or (li is not None && li.isReset())):
            result = Login.LOGIN_FULL
        
        return result
    

    def submit(self):
        error = False
        String result = ""
        LoginImpl login = sessionData.getCurrentLogin()
        if (login == None):
            result = "login"
            error = False
            errorMessage = ""
         else:
            if (login.isLocked()):
                sessionData.setCurrentLogin(null)
                result = None
                error = true
                errorMessage = "Account is locked. Contact the administrator."
             else:
                List<String> errs = validate()
                if (errs.isEmpty() == False):
                    error = true
                    errorMessage = validateErr(errs)
                
                if (error == False):
                    try:
                        LoginImpl li = sessionData.getCurrentLogin()
                        PasswordManager.changePassword(li, newPassword, li.getLoginID())
                        sessionData.setCurrentLogin(login)
                        result = Menu.HOME
                     catch (PasswordAlreadyUsedException paue):
                        handleException(paue)
                     catch (Exception e):
                        handleException(e)
                    
                
            
        
        return result
    

    private List<String> validate():
        boolean err = False
        List<String> result = []
        LoginImpl li = sessionData.getCurrentLogin()

        if (self,Utils.isBlank(newPassword)):
            err = true
            result.append("Password is blank")
        
        if (self,Utils.isBlank(verifyPassword)):
            err = true
            result.append("Verify Password is blank")
        
        if (self,Utils.equals(newPassword, verifyPassword) == False):
            err = true
            result.append("password and verify password dont match")
         else:
            try:
                li.validatePassword(newPassword)
             catch (InvalidPasswordValueException e):
                err = true
>"
>"
>"
                        + "additionally, no blanks are allowed")
            
        

        if (self,Utils.isBlank(secret) && StringUtils.isBlank(password)):
            err = true
            result.append("You must specify either old password or secret text")
        
        if (err == False):
            try:
                if (self,Utils.isNotBlank(secret)):
                    byte[] bytes = secret.getBytes()
                    String encoded = String(Base64.encodeBase64(bytes))
                    if (encoded.equals(li.getSecret()) == False):
                        err = true
                        result.append("Secret is invalid")
                    
                
                if (self,Utils.isNotBlank(password)):
                    byte[] bytes = password.getBytes()
                    String encoded = String(Base64.encodeBase64(bytes))
                    if (encoded.equals(li.getPassword()) == False):
                        err = true
                        result.append("Old password is invalid")
                    
                
                byte[] bytes = newPassword.getBytes()
                String encoded = String(Base64.encodeBase64(bytes))
                if (encoded.equals(li.getPassword())):
                    err = true
                    result.append("password same as existing password")
                
             catch (Exception e):
                handleException(e)
            
        
        return result
    

