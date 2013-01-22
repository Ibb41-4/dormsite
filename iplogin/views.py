from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.http import HttpResponseRedirect


def change_user(request, user_id, redirect_field_name=REDIRECT_FIELD_NAME):

    redirect_to = request.REQUEST.get(redirect_field_name, '')

    user = authenticate(ip=request.META['REMOTE_ADDR'], user_id=user_id)
    if user is not None:
        auth.login(request, user)
    return HttpResponseRedirect(redirect_to)
