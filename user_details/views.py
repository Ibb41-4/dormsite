from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from user_details.models import UserProfile
from user_details.tables import UsersTable

@login_required
def index(request):
    
    table = UsersTable(UserProfile.objects.all())
    return render(request, 'user_details/index.html', {'table': table})# Create your views here.
