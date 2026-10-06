
    
    
class OrganizationsBean(DefaultBean):
    
    def __init__(self,request):
        super().__init__(request)
        
    def setup(self):
        result = {
            'err':False,
            'table' : self.getTable(),
            'nameMaxLength': Skill.NAME_LENGTH
            }
        return result
        
    def submit(self):
        name = self.sessionData.request.POST.get('name')
        if not self.sessionData.context:
            self.sessionData.context = {}
        login = self.sessionData.getCurrentLogin()
        org = self.sessionData.organization
        result = {}
        error = False
        errorMessage = ""
        if Utils.isBlank(name):
            error = True
            errorMessage = "name not specified"
        else:
            skill = None
            try:
                skill = self.of.getSkill(name=name,org=org)
                if skill:
                    result = ""
                    error = True
                    errorMessage = "There is already a skill named \"" + name + "\" in the database."
                else:
                    skill = self.of.getNewSkill(name, login.getLoginID(), org)
                    skill.save()
            except Exception as pe:
                error = True
                errorMessage = str(pe)
        if error:
            result = self.setup()
            result['err'] = True
            result['errMsg'] = errorMessage
            result['target']= Menu.SKILLS
        else:
            result = self.setup()
            result['err'] = False
            result['errMsg'] = errorMessage
            result['target']= Menu.SKILLS_BEAN
        self.sessionData.context = result
        self.sessionData.currentLogin = login
        return result
    
    def getTable(self):
        org = self.sessionData.organization
        skills = self.of.getSkills(org)
        return self.multiColumnTableRows("Skills",
                size=5,
                items=skills,
                style='class=listTable',
                dest="/vs/skillEdit")
    