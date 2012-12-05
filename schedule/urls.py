from django.conf.urls import patterns, include, url

from feeds import ShiftFeed

urlpatterns = patterns('schedule.views',
    # Examples:
    # url(r'^$', 'dormsite.views.home', name='home'),
    # url(r'^dormsite/', include('dormsite.foo.urls')),
    
    url(r'^$', 'schedule', name="schedule"),
    url(r'^print/$', 'print_schedule'),
    url(r'^ical/(?P<user_pk>\d+)/$', ShiftFeed(), name="ical_schedule"),
    url(r'^(?P<pk>\d+)/(?P<toggle>\w+)/', 'toggle'),
    url(r'^switch/(?P<id1>\d+)/(?P<id2>\d+)/', 'switch_shifts'),

)
