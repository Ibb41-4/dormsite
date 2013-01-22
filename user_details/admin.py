from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as UserAdminOriginal
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from .forms import UserChangeForm, UserCreationForm


class UserAdmin(UserAdminOriginal):
    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (
        (None, {'fields': (
            'username', 'password'
        )}),
        (_('Personal info'), {'fields': (
            'first_name', 'last_name', 'email', 'phonenumber', 'emergency_phonenumber',
            'birthdate', 'date_joined', 'enddate'
        )}),
        (_('Permissions'), {'fields': (
            'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'
        )}),
        (_('Important dates'), {'fields': (
            'last_login',
        )}),
    )


admin.site.register(get_user_model(), UserAdmin)
