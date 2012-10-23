from django.conf import settings 
from django.contrib.auth.models import User

class IPAuthBackend:
    """
    Authenticate against the setting IP_AUTH_IP.

    Use the request ip address. For example:

    IP_AUTH_IP = ['127.0.0.1']
    IP_AUTH_USER = 'username'

    """
    def authenticate(self, ip=None):
        print ip
        print settings.IP_AUTH_IP
        if ip in settings.IP_AUTH_IP:
            user, created = User.objects.get_or_create(username=settings.IP_AUTH_USER)
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
