from datetime import date, datetime, timedelta
from math import floor

from django.db import models
from django.conf import settings 


# Create your models here.

class Week(models.Model):
    WEEKS = map(lambda x: (x,'Week %s' % x), range(1,54))
    CURRENT = "current_week"
    FUTURE = "future_week"
    PAST = "past_week"

    number = models.PositiveIntegerField(choices=WEEKS)
    year = models.PositiveIntegerField(default=date.today().year)
    
    @property
    def startdate(self):
        return tofirstdayinisoweek(self.year, self.number)

    @property
    def type(self):
        current_year, current_week_number, ignore = date.today().isocalendar()
        if current_year == self.year and current_week_number == self.number:
            return self.CURRENT
        elif current_year < self.year or (current_year == self.year and current_week_number < self.number):
            return self.FUTURE
        else:
            return self.PAST

    @property
    def tasks(self):
        return list(Task.objects.filter(shifts__week=self))

    @property
    def is_filled(self):
        return len(self.tasks) > 0

    def previous_week(self, number=1):
        number = self.number - number
        year = self.year
        year_length = 53 if is_long_year(self.year) else 52

        if number < 1:
            year -= 1
            number = year_length if number == 0 else number % year_length

        week, created = Week.objects.get_or_create(number=number, year=year)
        return week

    def next_week(self, number=1):
        number = self.number + number
        year = self.year
        year_length = 53 if is_long_year(self.year) else 52

        if number > year_length:
            number = number % year_length
            year += 1

        week, created = Week.objects.get_or_create(number=number, year=year)
        return week

    def get_weeks(self, number):
        weeks = [self]
        if number > 0:
            for i in range(0, number-1):
                weeks.append(weeks[-1].next_week())
        else:
            for i in range(number, 0):
                weeks.insert(0, weeks[0].previous_week())

        return weeks

    @staticmethod
    def get_current_week():
        current_year, current_week_number, ignore = date.today().isocalendar()

        current_week, created = Week.objects.get_or_create(number=current_week_number, year=current_year)
        return current_week


    def __unicode__(self):
        return 'Week {0} beginnend op: {1}'.format(self.number, self.startdate.date().isoformat())

class Task(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()

    def __unicode__(self):
        return self.name
    
class Room(models.Model):
    number = models.PositiveIntegerField()
    user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, blank=True, related_name="room")
    tasks = models.ManyToManyField(Task, related_name="rooms")

    def __unicode__(self):
        if not self.user == None:    
            return unicode(self.user)
        else:
            return 'Kamer %s' % self.number

    class Meta:
        ordering = ['number']
            

class Shift(models.Model):
    week = models.ForeignKey(Week, related_name="shifts")
    room = models.ForeignKey(Room, related_name="shifts")
    task = models.ForeignKey(Task, related_name="shifts")
    done = models.BooleanField()

    def __unicode__(self):
        return '%s %s %s' % (self.week, self.room, self.task)

    class Meta:
        permissions = (
            ("view_shifts", "Can see the schedule"),
            ("can_switch_others", "Can switch other shifts than his own"),
        )
        unique_together = ('week', 'task',)




def tofirstdayinisoweek(year, week):
    ret = datetime.strptime('%04d-%02d-1' % (year, week), '%Y-%W-%w')
    if date(year, 1, 4).isoweekday() > 4:
        ret -= timedelta(days=7)
    return ret

def is_long_year(year):
    '''
    iso years can be 53 weeks long: http://www.staff.science.uu.nl/~gent0113/calendar/isocalendar.htm
    '''
    p = lambda y: y + floor(y/4) - floor(y/100) + floor(y/400)
    return (p(year) % 7 == 4) or (p(year-1) % 7 == 3)