import django_tables2 as tables
from django_tables2 import A

from django.utils.safestring import mark_safe
from django.utils.html import escape

from django.contrib.auth import get_user_model


class PhoneNumberColumn(tables.Column):
    def render(self, value):
        return mark_safe('<a src="tel:{0}" />{0}</a>'.format(escape(value)))


class EmailColumn(tables.EmailColumn):
    def render(self, value, record):
        return self.render_link("mailto:%s %s <%s>" % (record.first_name, record.last_name, value), text=value)


class UsersTable(tables.Table):
    first_name = tables.Column(empty_values=[])
    email = EmailColumn(verbose_name="E-mailadres")
    room = tables.Column(verbose_name="Kamer", accessor="current_room.number")
    startdate = tables.DateColumn(verbose_name="Startdatum", accessor="startdate", orderable=False)

    def render_first_name(self, record):
        '''
        Show at least the username when Firstname is empty
        Also show elders
        '''
        elder_string = '<i class="icon-star"></i> ' if record.is_elder() else ''
        return mark_safe(elder_string + record.get_short_name())

    class Meta:
        model = get_user_model()
        exclude = ('password', 'username', 'is_active', 'is_staff', 'last_login', 'date_joined', 'is_superuser', 'id')
        # add class="paleblue" to <table> tag
        attrs = {"class": "tables2"}
        #sequence = ("...", 'emergency_phonenumber')
