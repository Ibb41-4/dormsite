from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User




# Re-register UserAdmin
#admin.site.unregister(User)
admin.site.register(User)