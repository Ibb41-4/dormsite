from django.contrib.auth import authenticate
from django.contrib import auth
from django.conf import settings 
from django.contrib.auth import REDIRECT_FIELD_NAME 
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

 
def login(request, template_name='registration/login.html', redirect_field_name=REDIRECT_FIELD_NAME):
    user = authenticate(ip=request.META['REMOTE_ADDR'])
    redirect_to = request.REQUEST.get(redirect_field_name, '')
    if user is not None:
        auth.login(request, user)
        
        if not redirect_to or '//' in redirect_to or ' ' in redirect_to: 
            redirect_to = settings.LOGIN_REDIRECT_URL
        return HttpResponseRedirect(redirect_to)
    else:
    	return HttpResponseRedirect(reverse('django.contrib.auth.views.login'))

