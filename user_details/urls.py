from django.conf.urls import patterns, include, url

from django.views.generic.edit import UpdateView

from .views import UserView
from .models import User


urlpatterns = patterns('user_details.views',
    # Examples:
    # url(r'^$', 'dormsite.views.home', name='home'),
    # url(r'^dormsite/', include('dormsite.foo.urls')),
    
    url(r'^$', 'index'),
    url(r'^edit/$', UserView.as_view(), name='edit'),

)
