from settings import *

# CSRF Middleware breaks auth tests
# IPlogin breaks auth test
MIDDLEWARE_CLASSES = list(MIDDLEWARE_CLASSES)
MIDDLEWARE_CLASSES.remove('django.middleware.csrf.CsrfViewMiddleware')
MIDDLEWARE_CLASSES.remove('dormsite.middleware.LoginRequiredMiddleware')
MIDDLEWARE_CLASSES.remove('iplogin.middleware.IPLoginMiddleware')

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
)
