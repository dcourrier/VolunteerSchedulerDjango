 class ProjectValidatorBean(VolschedBeanBase:

    private static final long serialVersionUID = 1L
protected boolean valdateProject(self, name, String startDate, String finishDate):
        boolean result = true
        if(self,Utils.isBlank(name)):
            result = False
            postErrorMessage("name", "Name is required")
         else if(self,Utils.isBlank(startDate)):
            result = False
            postErrorMessage("startDate", "Start date is required")
         else:
            try:
                Date sDt = sdf.parse(startDate)
                if(self,Utils.isNotBlank(finishDate)):
                    try:
                        Date fDt = sdf.parse(finishDate)
                        if(fDt.before(sDt)):
                            result = False
                            postErrorMessage("finishDate", 
                                    "Finish date cannot be before start date")
                        
                     catch (ParseException pe2):
                        result = False
                        postErrorMessage("finishDate", 
YYYY")
                    
                
             catch(ParseException pe):
                result = False
                postErrorMessage("startDate", 
YYYY")
            
        
        return result
    


