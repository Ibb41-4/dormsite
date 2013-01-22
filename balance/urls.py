from django.conf.urls import patterns, url

from .views import BalanceView


urlpatterns = patterns('balance.views',
    # Examples:
    # url(r'^$', 'dormsite.views.home', name='home'),
    # url(r'^dormsite/', include('dormsite.foo.urls')),

    url(r'^$', BalanceView.as_view(), name="balance"),
    url(r'^(?P<pk>\d+)/$', BalanceView.as_view(), name="balance"),
    url(r'^make/$', 'make_balance', name='make_balance'),
)
