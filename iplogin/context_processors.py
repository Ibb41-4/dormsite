from django.conf import settings
from django.contrib.auth import get_user_model, BACKEND_SESSION_KEY


def iplogin(request):
    ip = request.META['REMOTE_ADDR']

    backend = request.session[BACKEND_SESSION_KEY] if BACKEND_SESSION_KEY in request.session else ''

    #only respond when iplogin is possible and the backend is enabled
    if ip in settings.IP_AUTH_IP and backend == "iplogin.backend.IPAuthBackend":
        normal_users = get_user_model().residents_without_elder.all()

        return {'iplogin': True, 'iplogin_users': normal_users}

    return {}
