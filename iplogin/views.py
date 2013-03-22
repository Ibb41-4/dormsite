from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


def change_user(request, user_id, redirect_field_name=REDIRECT_FIELD_NAME):

    redirect_to = request.REQUEST.get(redirect_field_name, '')
    if redirect_to == reverse('django.contrib.auth.views.login'):
        redirect_to = '/'

    user = authenticate(ip=request.META['REMOTE_ADDR'], user_id=user_id)
    if user is not None:
        auth.login(request, user)
    return HttpResponseRedirect(redirect_to)
