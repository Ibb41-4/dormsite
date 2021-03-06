from django_ical.views import ICalFeed
from markdown import markdown

from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse

from .models import Shift
from residents.models import User


class ShiftFeed(ICalFeed):
    """
    A simple event calender
    """
    product_id = '-//huissite.hmvp.nl//Huistaken//EN'
    timezone = 'CET'
    title = "Huistaken"

    def get_object(self, request, user_pk):
        return get_object_or_404(User, pk=user_pk)

    def items(self, item):
        return Shift.objects.filter(room=item.current_room())

    def item_title(self, item):
        return item.task

    def item_link(self, item):
        return reverse('schedule.views.schedule')

    def item_guid(self, item):
        return reverse('schedule.views.schedule') + str(item.pk)

    def item_description(self, item):
        return item.task.description

    def item_start_datetime(self, item):
        return item.week.startdate

    def item_end_datetime(self, item):
        return item.week.next_week().startdate

    def item_transparency(self, item):
        return 'TRANSPARENT'
