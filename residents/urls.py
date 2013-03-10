from django.conf.urls import patterns, url

from django.views.generic import ListView

from django.contrib.auth import get_user_model

from .views import UserView


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'dormsite.views.home', name='home'),
    # url(r'^dormsite/', include('dormsite.foo.urls')),

    url(r'^$', 'residents.views.index', name='home'),
    url(r'^old$', 'residents.views.old_residents', name='old'),
    url(r'^edit/$', UserView.as_view(), name='edit'),
    url(r'^iplogin/(?P<user_id>\d+)/$', 'iplogin.views.change_user'),
    url(r'^login/$',  'django.contrib.auth.views.login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout'),
    url(r'^password/reset/$', 'django.contrib.auth.views.password_reset',
        {'post_reset_redirect': '/user/password/reset/done/'},
        name="password_reset"),
    url(r'^password/reset/done/$',
        'django.contrib.auth.views.password_reset_done'),
    url(r'^password/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
        'django.contrib.auth.views.password_reset_confirm',
        {'post_reset_redirect': '/user/password/done/'}),
    url(r'^password/done/$',
        'django.contrib.auth.views.password_reset_complete'),
)
