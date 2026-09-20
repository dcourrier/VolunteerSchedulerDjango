 class LoginAdminBean(VolschedBeanBase:

    private static final long serialVersionUID = 1L

    private String name
    private String password

     LoginAdminBean():
    

    def getName(self):
        return name
    

    def setName(selfString name):
        self.name = name
    

    def getPassword(self):
        return password
    

    def setPassword(selfString password):
        self.password = password
    

    def getMaxNameLength(self):
        return LoginImpl.LOGIN_NAME_MAX_SIZE
    

    def getMaxPasswordLength(self):
        return LoginImpl.PASSWORD_MAX_ENCRYPTED_SIZE
    

    def submit(self):
        error = False
        String result = None

        LoginImpl li = None
        return result
    

