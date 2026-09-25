from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404,render,redirect
from django.contrib import messages
from django.urls import reverse
from django.views import generic,View
from loguru import logger
from django.utils import timezone
from vs.models import *
from vscode.base.business_objects import *
from vscode.utils.utils import ValuesHolder,Utils
from vs.bean.beans import *
from vscode.loader.loaders import LoaderManager

def dashboard_view(request):
    return render(request, "dashboard.html")

def initial(request):
    if len(DbStateCode.objects.all()) == 0:
        LoaderManager().load()
    return render(request, "vs/login.html")

def logout(request):
        ValuesHolder.setCurrentLogin(None)
        SessionData().currentLogin = None
        SessionData().currentLoginPrivileges = []
        return render(request, "vs/login.html")
        
class DummyView(View):
        
    def post(self,request, *args, **kwargs):
        pass
    
    def get(self, request, *args, **kwargs):
        self.post(request, *args, **kwargs)

class HelpView(View):
        
    def post(self,request, *args, **kwargs):
        bean = HelpBean(request)
        return render(request,bean.getURL())
    
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

class LoginView(View):
    def post(self,request, *args, **kwargs):
        loginName = request.POST.get('login')
        pwd = request.POST.get('password')
        try:
            target = LoginBean(request).attempt(loginName,pwd)
            #print(target)
            return render(request, target)
        except InvalidPasswordException:
            msg = 'The password is invalid'
            messages.info(request, msg)
            logger.opt(exception=True).debug(msg)
        except AccountLockedException:
            msg = 'Your account is locked. Contact the administrator at ext 9900'
            messages.info(request, msg)
            logger.opt(exception=True).debug(msg)
        except AccountExpiredException:
            msg = 'Your pasword has expired. You must change it'
            messages.info(request, msg)
            logger.opt(exception=True).debug(msg)
        except:
            msg = 'A system error occurred. Contact the administrator at ext 9900'
            messages.error(request, msg)
            logger.opt(exception=True).error(msg)
            return redirect(request, "vs/login.html")
        else:
            logger.opt(exception=True).error('login failed')
            msg = 'No such login is defined'
            messages.error(request, msg)
        return redirect(request, "vs/login.html")
    
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
         
class Home(View):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
    
    def post(self,request, *args, **kwargs):
        bean = HomeBean(request)
        if bean.isVolunteerUser():
            return render(request, 'vs/volunteerHome.html')
        context = HomeBean.setup(request)
        return render(request, "vs/home.html", context)