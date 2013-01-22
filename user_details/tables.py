import django_tables2 as tables

from django.utils.safestring import mark_safe
from django.utils.html import escape

from django.contrib.auth import get_user_model


class PhoneNumberColumn(tables.Column):
    def render(self, value):
        return mark_safe('<a src="tel:{0}" />{0}</a>'.format(escape(value)))


class UsersTable(tables.Table):
    email = tables.EmailColumn(verbose_name="E-mailadres")
    room = tables.Column(verbose_name="Kamer", accessor="room.number")

    class Meta:
        model = get_user_model()
        exclude = ('password', 'username', 'is_active', 'is_staff', 'last_login', 'date_joined', 'is_superuser', 'id', 'startdate', 'enddate')
        # add class="paleblue" to <table> tag
        attrs = {"class": "paleblue"}
        #sequence = ("...", 'emergency_phonenumber')
