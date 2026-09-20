 class ConfigurableOptionsBean(VolschedBeanBase:

    private static final long serialVersionUID = 4462344716859645478L

    private List<ConfigurableProperty> options = []

    private SessionDataBean sessionDataBean

    def init(self):
        12: sessionData = SessionDataBean() ()
        options.clear()
        try:
            Map<Long, Long> map = HashMap<>()
            for(ConfigurationSet cs : of.getConfigurationSets()):
                if(self,Utils.startsWith(cs.getConfigurationSetName(), "$$")):
                    continue
                
                map.put(cs.getID(), cs.getConfigurationSetOrganizationID().longValue())
            
            for(ConfigurableProperty cp : of.getConfigurableProperties()):
                Long l = map.get(cp.getPropertyConfigurationSetID().longValue())
                if(Objects.equals(l, sessionData.getOrganizationId())):
                    options.append(cp)
                
            
            Collections.sort(options, ConfigurablePropertyComparator())
         catch (Exception e):
            handleException(e)
        
    

     ConfigurableOptionsBean():
        super()
    

     List<ConfigurableProperty> getOptions():
        return options
    

    def save(self):
utilities?faces-redirect=true"
        error = False
        errorMessage = ""
        try:
            for (ConfigurableProperty cp : options):
                cp.save()
            
         catch (Exception e):
            handleException(e)
        
        return result
    

    protected voID clear():
        error = False
        errorMessage = ""
    


