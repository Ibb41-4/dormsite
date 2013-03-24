from datetime import date

from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.conf import settings


class ResidentsManager(UserManager):
    def get_query_set(self):
        queryset = super(ResidentsManager, self).get_query_set()

        # hack to filter on is_active, lets hope the total of users stays small enough
        q_ids = [o.id for o in queryset if o.is_resident()]
        return queryset.filter(id__in=q_ids)


class ResidentsWithoutElderManager(ResidentsManager):
    def get_query_set(self):
        return super(ResidentsWithoutElderManager, self).get_query_set().exclude(groups__name=settings.ELDER_GROUP_NAME)


class User(AbstractUser):
    #first_name = models.CharField(max_length=50)
    #last_name = models.CharField(max_length=100)
    phonenumber = models.CharField(max_length=20, null=True, verbose_name=u'Telefoon')
    emergency_phonenumber = models.CharField(max_length=20, null=True, blank=True, verbose_name=u'Noodnummer')
    birthdate = models.DateField(null=True, verbose_name=u'Geboortedatum')

    objects = UserManager()
    residents_without_elder = ResidentsWithoutElderManager()
    residents = ResidentsManager()

    REQUIRED_FIELDS = ['first_name', 'last_name', 'email', 'phonenumber', 'birthdate']
    USERNAME_FIELD = 'username'

    def get_full_name(self):
        return str(self.first_name, self.last_name)

    def get_short_name(self):
        return self.first_name if self.first_name else self.username

    @property
    def startdate(self):
        if not self.roomassignments.exists():
            return None

        return self.roomassignments.order_by('start_date')[0].start_date

    @property
    def enddate(self):
        if self.roomassignments.exists():
            last_used_assignment = self.roomassignments.all().latest()
            last_used_room = last_used_assignment.room
            if last_used_room.current_user() != self:
                return last_used_assignment.next_in_line.start_date

    def last_room(self, check_date=None):
        _date = check_date or date.today()

        if self.roomassignments.exists():
            try:
                rooms = self.roomassignments.all().filter(start_date__lte=_date)
                if rooms.exists():
                    return rooms.latest().room
            except Room.DoesNotExist:
                pass

    def current_room(self, check_date=None):
        last_room = self.last_room(check_date)
        if last_room and last_room.current_user(check_date) == self:
            return last_room

    @property
    def is_active(self):
        '''Override is_active, to use is_resident but let superusers always be active'''
        return self.is_resident() or self.is_superuser

    @is_active.setter
    def is_active(self, ignored):
        pass  # we ignore this

    def is_resident(self, check_date=None):
        return bool(self.current_room(check_date))
    is_resident.boolean = True  # let django admin use boolean icons

    def is_elder(self):
        return self.groups.filter(name=settings.ELDER_GROUP_NAME).exists()
    is_elder.boolean = True  # let django admin use boolean icons

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
            return None  # this should not happen

        try:
            ra = self.roomassignments.all().filter(start_date__lte=_date).order_by('-start_date')
            if ra.exists():
                return ra[0].user
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
