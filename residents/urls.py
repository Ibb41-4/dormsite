from django.conf.urls import patterns, url
from django.contrib.auth.decorators import permission_required

from .views import UserView, UserMoveView, AbdicateView


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'dormsite.views.home', name='home'),
    # url(r'^dormsite/', include('dormsite.foo.urls')),

    url(r'^$', 'residents.views.index', name='home'),
    url(r'^old/$', 'residents.views.old_residents', name='old'),
    url(r'^edit/$', UserView.as_view(), name='edit'),
    url(r'^move/$', permission_required('add_user')(UserMoveView.as_view()), name='move'),
    url(r'^abdicate/$', AbdicateView.as_view(), name='abdicate'),
    url(r'^iplogin/(?P<user_id>\d+)/$', 'iplogin.views.change_user'),

)

urlpatterns += patterns('django.contrib.auth.views',
    url(r'^login/$',  'login'),
    url(r'^logout/$', 'logout'),
    url(r'^password/reset/$', 'password_reset',
        {'post_reset_redirect': '/user/password/reset/done/'},
        name="password_reset"),
    url(r'^password/reset/done/$', 'password_reset_done'),
    url(r'^password/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'password_reset_confirm',
        {'post_reset_redirect': '/user/password/done/'}),
    url(r'^password/done/$', 'password_reset_complete'),
)
