from django.conf import settings
from django.contrib.auth import get_user_model


class IPAuthBackend:
    """
    Authenticate against the setting IP_AUTH_IP.

    Use the request ip address. For example:

    IP_AUTH_IP = ['127.0.0.1']
    IP_AUTH_USER = 'username'

    """
    def authenticate(self, ip=None, user_id=None):
        if ip in settings.IP_AUTH_IP:
            try:
                return get_user_model().residents.get(pk=user_id)
            except get_user_model().DoesNotExist:
                return None
        return None

    def get_user(self, user_id):
        try:
            return get_user_model().objects.get(pk=user_id)
        except get_user_model().DoesNotExist:
            return None
