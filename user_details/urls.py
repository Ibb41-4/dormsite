from django.conf.urls import patterns, include, url

urlpatterns = patterns('user_details.views',
    # Examples:
    # url(r'^$', 'dormsite.views.home', name='home'),
    # url(r'^dormsite/', include('dormsite.foo.urls')),
    
    url(r'^$', 'index'),

)
