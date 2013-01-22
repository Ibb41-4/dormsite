from django.conf import settings
from django.contrib.auth import get_user_model

from django.contrib.auth import BACKEND_SESSION_KEY


def iplogin(request):
    ip = request.META['REMOTE_ADDR']

    if ip in settings.IP_AUTH_IP and request.session[BACKEND_SESSION_KEY] == "iplogin.backend.IPAuthBackend":
        normal_users = get_user_model().objects.exclude(groups__name="Huisoudste").filter(groups__name="Huisgenoten", is_active=True)
        return {'iplogin': True, 'users': normal_users}

    return {}
