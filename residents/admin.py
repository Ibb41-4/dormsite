from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as UserAdminOriginal
from django.utils.translation import ugettext_lazy as _

from .forms import UserChangeForm, UserCreationForm

from .models import Room, RoomAssignment, User


class RoomAssignmentAdmin(admin.TabularInline):
    model = RoomAssignment
    extra = 0


class RoomAdmin(admin.ModelAdmin):
    list_display = ['number', 'current_user']
    #list_editable = ['user']
    inlines = [
        RoomAssignmentAdmin,
    ]


class UserAdmin(UserAdminOriginal):
    list_display = UserAdminOriginal.list_display + ('is_active', 'is_resident', 'startdate',)
    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (
        (None, {'fields': (
            'username', 'password'
        )}),
        (_('Personal info'), {'fields': (
            'first_name', 'last_name', 'email', 'phonenumber', 'emergency_phonenumber',
            'birthdate', 'date_joined'
        )}),
        (_('Permissions'), {'fields': (
            'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'
        )}),
        (_('Important dates'), {'fields': (
            'last_login',
        )}),
    )
    inlines = [
        RoomAssignmentAdmin,
    ]

admin.site.register(Room, RoomAdmin)
admin.site.register(User, UserAdmin)
