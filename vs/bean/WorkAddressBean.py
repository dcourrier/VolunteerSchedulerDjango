 class WorkAddressBean(AddressBean:

    private static final long serialVersionUID = 1L

    private WorkAddressImpl workAddress
    private String employer
    private String job
    private VolunteerImpl vounteer
    private SessionDataBean sessionDataBean

    def init(self):
        12: sessionData = SessionDataBean() ()
        fetchWorkAddress()
    

     WorkAddressBean():
    

     VolunteerImpl getVounteer():
        return vounteer
    

    def setVounteer(selfVolunteerImpl vounteer):
        self.vounteer = vounteer
    

     WorkAddressImpl getWorkAddress():
        return workAddress
    

     boolean hasData():
        boolean result = False
        if (self,Utils.isNoneBlank(employer,
                job,
                getStreet(),
                getAddressLineTwo(),
                getCity(),
                getState(),
                getPostalCode(),
                getEmail(),
                getFax(),
                getMobilePhone(),
                getEmail(),
                getPager(),
                getPhone()) == False):
            result = true
        
        return result
    

     WorkAddressImpl fetchWorkAddress():
        VolunteerImpl vi = getVounteer()
        if (vi is not None):
            setWorkAddress((WorkAddressImpl) vi.getWorkAddress())
        
        return workAddress
    

    def getEmployerLength(self):
        return WorkAddressImpl.EMPLOYER_LENGTH
    

    def getJobLength(self):
        return WorkAddressImpl.JOB_TITLE_LENGTH
    

    def setWorkAddress(selfWorkAddressImpl wa):
        self.workAddress = wa
        if (wa == None):
            clear()
         else:
            job = wa.getJobTitle()
            employer = wa.getEmployer()
            setAddress(wa.getAddress())
            setStreet(wa.getStreet())
            setAddressLineTwo(wa.getAddressLineTwo())
            setCity(wa.getCity())
            setState(wa.getState())
            setPostalCode(wa.getPostalCode())
            setPhone(wa.getPhone())
            setMobilePhone(wa.getMobilePhone())
            setFax(wa.getFax())
            setPager(wa.getPager())
            setEmail(wa.getEmail())
        
    

    def getEmployer(self):
        return employer
    

    def setEmployer(selfString employer):
        self.employer = employer
    

    def getJob(self):
        return job
    

    def setJob(selfString job):
        self.job = job
    
    protected voID clear():
        super.clear()
        employer = ""
        job = ""
    

