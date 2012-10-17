from django.conf.urls import patterns, include, url

from expenses.views import ExpensesView


urlpatterns = patterns('expenses.views',
    # Examples:
    # url(r'^$', 'dormsite.views.home', name='home'),
    # url(r'^dormsite/', include('dormsite.foo.urls')),
    
    url(r'^$', ExpensesView.as_view()),
    url(r'^add/$', ExpensesView.as_view()),


)
