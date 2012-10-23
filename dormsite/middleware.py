from re import compile

from django.http import HttpResponseRedirect
from django.conf import settings
from django.db.models import signals
from django.utils.functional import curry
from django.db.models.fields import FieldDoesNotExist


EXEMPT_URLS = [compile(settings.LOGIN_URL.lstrip('/'))]
if hasattr(settings, 'LOGIN_EXEMPT_URLS'):
    EXEMPT_URLS += [compile(expr) for expr in settings.LOGIN_EXEMPT_URLS]

class LoginRequiredMiddleware:
    """
    Middleware that requires a user to be authenticated to view any page other
    than LOGIN_URL. Exemptions to this requirement can optionally be specified
    in settings via a list of regular expressions in LOGIN_EXEMPT_URLS (which
    you can copy from your urls.py).

    Requires authentication middleware and template context processors to be
    loaded. You'll get an error if they aren't.
    """
    def process_request(self, request):
        assert hasattr(request, 'user'), "The Login Required middleware\
 requires authentication middleware to be installed. Edit your\
 MIDDLEWARE_CLASSES setting to insert\
 'django.contrib.auth.middlware.AuthenticationMiddleware'. If that doesn't\
 work, ensure your TEMPLATE_CONTEXT_PROCESSORS setting includes\
 'django.core.context_processors.auth'."
        if not request.user.is_authenticated():
            path = request.path_info.lstrip('/')
            if not any(m.match(path) for m in EXEMPT_URLS):
                return HttpResponseRedirect(settings.LOGIN_URL)




class WhodidMiddleware:
    """
    Add user created_by and modified_by foreign key refs to any model automatically.
    
    Almost entirely taken from https://github.com/Atomidata/django-audit-log/blob/master/audit_log/middleware.py
    """

    def process_request(self, request):
        if not request.method in ('GET', 'HEAD', 'OPTIONS', 'TRACE'):
            if hasattr(request, 'user') and request.user.is_authenticated():
                user = request.user
            else:
                user = None

            mark_whodid = curry(self.mark_whodid, user)
            signals.pre_save.connect(mark_whodid,  dispatch_uid = (self.__class__, request,), weak = False)

    def process_response(self, request, response):
        signals.pre_save.disconnect(dispatch_uid =  (self.__class__, request,))
        return response

    def mark_whodid(self, user, sender, instance, **kwargs):
        try:
            if sender._meta.get_field('created_by') and not instance.created_by_id:
                instance.created_by = user
        except FieldDoesNotExist:
            pass

        try:
            if sender._meta.get_field('modified_by'):
                instance.modified_by = user
        except FieldDoesNotExist:
            pass