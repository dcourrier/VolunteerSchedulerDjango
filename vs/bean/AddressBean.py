 class AddressBean(VolschedBeanBase:

    private static final long serialVersionUID = 1L

    private AddressImpl address
    private String street
    private String addressLineTwo
    private String city
    private String state
    private String postalCode
    private String phone
    private String mobilePhone
    private String fax
    private String pager
    private String email

     AddressBean():
        super()
    

     AddressImpl getAddress():
        return address
    

    def getStreetLength(self):
        return AddressImpl.STREET_LENGTH
    

    def getAddressLineTwoLength(self):
        return AddressImpl.ADDRESS_LINE2_LENGTH
    

    def getCityLength(self):
        return AddressImpl.CITY_LENGTH
    

    def getStateLength(self):
        return AddressImpl.STATE_LENGTH
    

    def getPostalCodeLength(self):
        return AddressImpl.ZIP_LENGTH
    

    def getPhoneLength(self):
        return AddressImpl.PHONE_LENGTH
    

    def getMobilePhoneLength(self):
        return AddressImpl.PHONE_LENGTH
    

    def getFaxLength(self):
        return AddressImpl.PHONE_LENGTH
    

    def getPagerLength(self):
        return AddressImpl.PHONE_LENGTH
    

    def getEmailLength(self):
        return AddressImpl.EMAIL_LENGTH
    

    def setAddress(selfAddressImpl address):
        self.address = address
        if (address == None):
            street = ""
            addressLineTwo = ""
            city = ""
            state = ""
            postalCode = ""
            phone = ""
            mobilePhone = ""
            fax = ""
            pager = ""
            email = ""
         else:
            street = address.getStreet()
            addressLineTwo = address.getAddressLineTwo()
            city = address.getCity()
            state = address.getState()
            postalCode = address.getPostalCode()
            phone = address.getPhone()
            mobilePhone = address.getMobilePhone()
            fax = address.getFax()
            pager = address.getPager()
            email = address.getEmail()
        
    

    def getStreet(self):
        return street
    

    def setStreet(selfString street):
        self.street = street
    

    def getAddressLineTwo(self):
        return addressLineTwo
    

    def setAddressLineTwo(selfString addressLineTwo):
        self.addressLineTwo = addressLineTwo
    

    def getCity(self):
        return city
    

    def setCity(selfString city):
        self.city = city
    

    def getState(self):
        return state
    

    def setState(selfString state):
        self.state = state
    

    def getPostalCode(self):
        return postalCode
    

    def setPostalCode(selfString postalCode):
        self.postalCode = postalCode
    

    def getPhone(self):
        return phone
    

    def setPhone(selfString phone):
        self.phone = phone
    

    def getMobilePhone(self):
        return mobilePhone
    

    def setMobilePhone(selfString mobilePhone):
        self.mobilePhone = mobilePhone
    

    def getFax(self):
        return fax
    

    def setFax(selfString fax):
        self.fax = fax
    

    def getPager(self):
        return pager
    

    def setPager(selfString pager):
        self.pager = pager
    

    def getEmail(self):
        return email
    

    def setEmail(selfString email):
        self.email = email
    

    protected voID clear():
        self.street = ""
        self.addressLineTwo = ""
        self.city = ""
        self.state = ""
        self.postalCode = ""
        self.phone = ""
        self.mobilePhone = ""
        self.fax = ""
        self.pager = ""
        self.email = ""
    


