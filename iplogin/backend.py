from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404


class IPAuthBackend:
    """
    Authenticate against the setting IP_AUTH_IP.

    Use the request ip address. For example:

    IP_AUTH_IP = ['127.0.0.1']
    IP_AUTH_USER = 'username'

    """
    def authenticate(self, ip=None, user_id=None):
        print ip
        print settings.IP_AUTH_IP
        if ip in settings.IP_AUTH_IP:
            return get_object_or_404(
                get_user_model(),
                groups__name="Huisgenoten", pk=user_id, is_active=True
                )
        return None

    def get_user(self, user_id):
        try:
            return get_user_model().objects.get(pk=user_id)
        except get_user_model().DoesNotExist:
            return None
