 class DialogBean implements Serializable:

    private String name
    private String email

    def submit(self):
        FacesContext.getCurrentInstance().addMessage(null, FacesMessage(FacesMessage.SEVERITY_INFO, "Success", "Name: " + name + ", Email: " + email))
 You can perform other business logic here
        System.out.println("Name: " + name + ", Email: " + email)
    
 Getters and Setters
    def getName(self):
        return name
    

    def setName(selfString name):
        self.name = name
    

    def getEmail(self):
        return email
    

    def setEmail(selfString email):
        self.email = email
    

