from django.conf.urls import patterns, include, url
from django.views.generic.detail import DetailView

from core.views import DefaultDetailView

from .models import Balance
from .views import BalanceView
from .views import BillsView, DrinksView, ExpensesView, DinnersView


urlpatterns = patterns('balance.views',
    # Examples:
    # url(r'^$', 'dormsite.views.home', name='home'),
    # url(r'^dormsite/', include('dormsite.foo.urls')),
    
    url(r'^$', BalanceView.as_view(), name="balance"),
    url(r'^(?P<pk>\d+)/$', BalanceView.as_view(), name="balance"),
    url(r'^make/$', 'make_balance', name='make_balance'),
)
