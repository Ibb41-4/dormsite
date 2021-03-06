from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from balance.views import DinnersView, DrinksView, ExpensesView, BillsView


from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'residents.views.index', name='home'),
    url(r'^schedule/', include('schedule.urls')),
    url(r'^user/', include('residents.urls')),
    url(r'^balance/', include('balance.urls')),

    url(r'^expenses/', ExpensesView.as_view(), name='expenses'),
    url(r'^dinners/', DinnersView.as_view(), name='dinners'),
    url(r'^bills/', BillsView.as_view(), name='bills'),
    url(r'^drinks/', DrinksView.as_view(), name='drinks'),


    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()
