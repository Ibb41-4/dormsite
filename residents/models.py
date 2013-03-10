from datetime import date

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    #first_name = models.CharField(max_length=50)
    #last_name = models.CharField(max_length=100)
    phonenumber = models.CharField(max_length=20, null=True, verbose_name=u'Telefoon')
    emergency_phonenumber = models.CharField(max_length=20, null=True, blank=True, verbose_name=u'Noodnummer')
    birthdate = models.DateField(null=True, verbose_name=u'Geboortedatum')

    REQUIRED_FIELDS = ['first_name', 'last_name', 'email', 'phonenumber', 'birthdate']
    USERNAME_FIELD = 'username'

    def get_full_name(self):
        return str(self.first_name, self.last_name)

    def get_short_name(self):
        return self.first_name

    @property
    def startdate(self):
        if not self.roomassignments.exists():
            return None

        return self.roomassignments.order_by('start_date')[0].start_date

    @property
    def enddate(self):
        if not self.roomassignments.exists():
            return None

        last_used_assignment = self.roomassignments.all().latest()
        last_used_room = last_used_assignment.room
        if last_used_room.current_user() == self:
            return None
        else:
            return last_used_assignment.next_in_line.start_date

    def last_room(self, check_date=None):
        _date = check_date or date.today()

        if not self.roomassignments.exists():
            return None

        try:
            return self.roomassignments.all().filter(start_date__lte=_date).latest().room
        except Room.DoesNotExist:
            return None

    def current_room(self, check_date=None):
        if self.last_room(check_date) is None:
            return None

        last_room = self.last_room(check_date)
        if last_room.current_user(check_date) == self:
            return last_room

    def is_resident(self, check_date=None):
        return bool(self.current_room(check_date))

    def __unicode__(self):
        return self.get_short_name()

    class Meta:
        ordering = ['first_name', 'last_name']


class Room(models.Model):
    number = models.PositiveIntegerField(unique=True)
    users = models.ManyToManyField(User, through='RoomAssignment', related_name="rooms")
    tasks = models.ManyToManyField('schedule.Task', related_name="rooms")

    def __unicode__(self):
        return 'Kamer %s' % self.number

    def current_user(self, check_date=None):
        _date = check_date or date.today()

        if not self.roomassignments.exists():
            return None

        try:
            return self.roomassignments.all().filter(start_date__lte=_date).order_by('-start_date')[0].user
        except User.DoesNotExist:
            return None

    def add_user(self, user, start_date):
        RoomAssignment.objects.create(room=self, user=user, start_date=start_date)

    class Meta:
        ordering = ['number']


class RoomAssignment(models.Model):
    user = models.ForeignKey(User, related_name='roomassignments')
    room = models.ForeignKey(Room, related_name='roomassignments')
    start_date = models.DateField()

    @property
    def next_in_line(self):
        future_assignments = RoomAssignment.objects.filter(room=self.room, start_date__gt=self.start_date)

        if future_assignments.exists():
            return future_assignments.order_by('start_date')[0]
        else:
            return None

    class Meta:
        ordering = ['start_date']
        get_latest_by = "start_date"
