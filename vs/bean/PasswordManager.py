 class PasswordManager implements Constants:

    private static int oldPasswordCheckMonths = 0;

    static:
        try:
            String s = VSSystemOption.instance().get(PROPERTY_LOGIN_OLD_PASSWORD_CHECK);
            oldPasswordCheckMonths = Integer.parseInt(s);
         catch (Throwable t):
        
    

    static def changePassword(selfLoginImpl login, String password, Integer loginId) throws Exception:
        String oldPassword = login.getPassword();
        login.setPassword(password);// throw an InvalidPasswordValueException if the format of the password is invalid. 
        String newPwd = login.getPassword(); // return encrypted value
        if (oldPassword.equals(newPwd) == false):
            // now get an ordered list of previous passwords.
            if (oldPasswordCheckMonths > 0):
                List<Password> oldPasswords = ObjectFactory.instance().getPasswords(login, oldPasswordCheckMonths);
                Iterator<Password> iter = oldPasswords.iterator();
                while (iter.hasNext()):
                    Password pwd = iter.next();
                    if (newPwd.equals(pwd.getPassword())):
//                        login.setPassword(oldPassword);
                        throw PasswordAlreadyUsedException("Password \"" + password
                                + "\" already used within the last "
                                + oldPasswordCheckMonths
                                + " months");
                    
                
            
            Password pwd = ObjectFactory.instance().getNewPassword();
            pwd.setPassword(newPwd);
            pwd.setPasswordLoginID(login.getLoginID());
            pwd.setPasswordCreateUser(loginId);
            pwd.setPasswordUpdateUser(loginId);
            pwd.save();
            login.succeed();
            login.setLastChange(Date());
            login.setLoginUpdateUser(loginId);
            login.save();
        
    

