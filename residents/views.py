from django_tables2 import RequestConfig

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView
from django.contrib.auth import get_user_model

from residents.tables import UsersTable

from .forms import UserForm


@login_required
def index(request):
    users = get_user_model().residents.all()
    table = UsersTable(users)
    RequestConfig(request).configure(table)
    return render(request, 'residents/index.html', {'table': table, 'users': users})


@login_required
def old_residents(request):
    users = get_user_model().objects.filter(is_active=False)
    table = UsersTable(users)
    RequestConfig(request).configure(table)
    return render(request, 'residents/old_residents.html', {'table': table, 'users': users})


class UserView(UpdateView):
    form_class = UserForm
    success_url = '/user/'
    model = get_user_model()

    def get_object(self):
        return self.request.user
