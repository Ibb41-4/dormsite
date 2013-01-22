from django.contrib.auth import authenticate, login
from django.conf import settings
from django.contrib.auth import get_user_model


class IPLoginMiddleware:
    """
    Middleware that requires a user to be authenticated to view any page other
    than LOGIN_URL. Exemptions to this requirement can optionally be specified
    in settings via a list of regular expressions in LOGIN_EXEMPT_URLS (which
    you can copy from your urls.py).

    Requires authentication middleware and template context processors to be
    loaded. You'll get an error if they aren't.
    """
    def process_request(self, request):
        if request.user.is_authenticated():
            return

        ip = request.META['REMOTE_ADDR']
        user = get_user_model().objects.exclude(groups__name="Huisoudste").filter(groups__name="Huisgenoten", is_active=True)[0]

        if ip in settings.IP_AUTH_IP:
            user = authenticate(ip=ip, user_id=user.id)
            login(request, user)
