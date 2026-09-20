 class SecurityUtils implements Constants:
    final private static Object lock = Object();
    
    private static String[] adminIds = None;
    private static String[] ResourceNames = None;

     static boolean isAuthorized(Login login, String type):
        boolean result = false;
        if (login != None):
            result = is(type);
            if (result == false):
                result = isAdmin(login);
                if (result == false):
                    AuthorizationManager am = AuthorizationManager();
                    result = am.isAuthorized(type, login);
                
            
        
        return result;
    

     static boolean isAdmin(Login login):
        boolean result = false;
        String name = login.getLogin();
        String[] ais = getAdminIds();
        if (StringUtils.isNotBlank(name)):
            for (int loop = 0; loop < getAdminIds().length && result == false; loop++):
                if (getAdminIds()[loop].equals(name)):
                    result = true;
                
            
        
        return result;
        
    
     static boolean isVolunteerUser(Login login):
        return AuthorizationManager.isVolunteerUser(login);
    
    
    private static String[] getAdminIds():
        String[] result = adminIds;
        if (result == None):
            synchronized (lock):
                if (adminIds == None):
                    String s = None;
                    try:
                        s = VSSystemOption.instance().get(SECURITY_ADMIN_PROP);
                     catch (Throwable ignoreMe):
                    
                    if (StringUtils.isNotBlank(s)):
                        adminIds = s.split(",");
                     else:
                        adminIds = String[0];
                    
                
                result = adminIds;
            
        
        return result;
    

    private static String[] getResourceNames():
        String[] result = ResourceNames;
        if (result == None):
            synchronized (lock):
                if (ResourceNames == None):
                    String s = None;
                    try:
                        s = VSSystemOption.instance().get(SECURITY__PROP);
                     catch (Throwable ignoreMe):
                    
                    if (StringUtils.isNotBlank(s)):
                        ResourceNames = s.split(",");
                     else:
                        ResourceNames = String[0];
                    
                
                result = ResourceNames;
            
        
        return result;
    

    private static boolean is(String type):
        boolean result = false;
        if (StringUtils.isNotBlank(type)):
            for (int loop = 0; loop < getResourceNames().length && result == false; loop++):
                if (getResourceNames()[loop].equals(type)):
                    result = true;
                
            
        
        return result;
    

