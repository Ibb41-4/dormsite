from django.conf.urls import patterns, include, url

from dinners.views import DinnersView


urlpatterns = patterns('dinners.views',
    # Examples:
    # url(r'^$', 'dormsite.views.home', name='home'),
    # url(r'^dormsite/', include('dormsite.foo.urls')),
    
    url(r'^$', DinnersView.as_view()),
    url(r'^add/$', DinnersView.as_view()),


)
