from django import template
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from vs.bean.beans import SessionData
from vscode.base.business_objects import SecurityUtils

register = template.Library()

@register.simple_block_tag(end_name="VSAuthorizer_end")
def VSAuthorizer(content, _type):
    result = ''
    sd = SessionData()
    #print(sd)
    login = sd.getCurrentLogin()
    if login:
        #print(str(login) + ' : ' + str(_type))
        if SecurityUtils.isAuthorized(login, _type):
            #print('authorized')
            result = mark_safe(content)
    return result
            
        