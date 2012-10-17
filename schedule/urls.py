from django.conf.urls import patterns, include, url

urlpatterns = patterns('schedule.views',
    # Examples:
    # url(r'^$', 'dormsite.views.home', name='home'),
    # url(r'^dormsite/', include('dormsite.foo.urls')),
    
    url(r'^$', 'schedule'),
    url(r'^(?P<pk>\d+)/(?P<toggle>\w+)/', 'toggle'),
    url(r'^(?P<pk>\d+)/(?P<toggle>\w+)/', 'toggle'),

)
