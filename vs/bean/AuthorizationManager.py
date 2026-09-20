 class AuthorizationManager implements Constants:

     static boolean isAuthorized(String request, Login login):
        boolean result = false;
        if (StringUtils.isNotBlank(request)):
            Set<SecurityGroup> securityGroups = login.getSecurityGroups();
            Iterator<SecurityGroup> sgIter = securityGroups.iterator();
            while (sgIter.hasNext() && result == false):
                SecurityGroup sg = sgIter.next();
                Iterator<Privilege> privIter = sg.getPrivileges().iterator();
                while (privIter.hasNext() && result == false):
                    Privilege priv = privIter.next();
                    if (request.equals(priv.getPrivilegeName())):
                        result = true;
                    
                
            
        
        return result;
    
    
     static boolean isVolunteerUser(Login login):
        boolean result = false;
        if (login != None):
            Set<SecurityGroup> securityGroups = login.getSecurityGroups();
            if(securityGroups.size() == 1):
                SecurityGroup sg = (SecurityGroup)securityGroups.toArray()[0];
                if(SECURITY_GROUP_VOLUNTEER.equalsIgnoreCase(sg.getSecurityGroupName())):
                    result = true;
                
            
        
        return result;
    

