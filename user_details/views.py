from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.views.generic.edit import UpdateView


from user_details.models import User
from user_details.tables import UsersTable

from .forms import UserForm

@login_required
def index(request):
    group = Group.objects.get(name="Huisgenoten")
    users = User.objects.filter(groups=group, is_active=True)
    table = UsersTable(users)
    return render(request, 'user_details/index.html', {'table': table, 'users':users})# Create your views here.

class UserView(UpdateView):
    form_class = UserForm
    success_url = '/user/'
    model = User

    def get_object(self):
    	return self.request.user
