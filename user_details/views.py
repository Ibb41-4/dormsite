from django.shortcuts import render

from user_details.models import UserProfile
from user_details.tables import UsersTable

def index(request):
    
    table = UsersTable(UserProfile.objects.all())
    return render(request, 'user_details/index.html', {'table': table})# Create your views here.
