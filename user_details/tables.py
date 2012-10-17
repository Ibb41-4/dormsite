import django_tables2 as tables
from django_tables2 import A

from user_details.models import UserProfile


class UsersTable(tables.Table):
    naam = tables.Column(verbose_name="Naam", accessor="user.first_name")
    phonenumber = tables.Column(verbose_name="Telefoon")
    emergency_phonenumber = tables.Column(verbose_name="Noodnummer")
    birthdate = tables.DateColumn(verbose_name='Geboorte datum')
    #room = tables.Column(verbose_name="Kamer", accessor="user.room.number")

    class Meta:
        model = UserProfile
        exclude = ('user', 'id' )
        # add class="paleblue" to <table> tag
        attrs = {"class": "paleblue"}
        sequence = ("naam", "...", 'emergency_phonenumber')
        orderable = False

