# -*- coding: utf-8 -*-
import random
from datetime import date

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import permission_required
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.contrib.sites.models import Site

from schedule.models import Week, Task, Shift


def toggle(request, pk, toggle):
    shift = Shift.objects.get(pk=pk)

    #only when weeks are in future, or we are still in the first days of the next week
    if not shift.week.deadline_passed or request.user.is_elder():
        shift.done = True if toggle == 'on' else False
        shift.save()
        return HttpResponse('Ok')
    else:
        return HttpResponseForbidden('Not possible')


@permission_required('schedule.view_shifts')
def schedule(request):
    start_week = Week.get_current_week().previous_week(7)

    weeks = start_week.get_weeks(42)
    weeks = weeks[:35]  # don't show the last 7, this way we generate them but don't show them.
                        # This helps preventing that switching changes the overall structure

    for week in weeks:
        assign_weeks(week)

    return render(request, 'schedule/schedule.html', {'data': weeks, 'tasks': Task.objects.all().order_by('description')})


@permission_required('schedule.view_shifts')
def print_schedule(request):
    current_week = Week.get_current_week()
    weeks = current_week.get_weeks(21)
    return render(request, 'schedule/print_schedule.html', {'data': weeks, 'tasks': Task.objects.all().order_by('description')})


@permission_required('schedule.view_shifts')
def switch_shifts(request, id1, id2):
    shift1 = Shift.objects.get(pk=id1)
    shift2 = Shift.objects.get(pk=id2)

    shift1_user = shift1.room.current_user(shift1.week.startdate)
    shift2_user = shift2.room.current_user(shift2.week.startdate)

    #only modify your own shifts, unless you have rights
    if not request.user == shift1_user and not request.user == shift2_user:
        if not request.user.has_perm('schedule.can_switch_others'):
            return HttpResponseForbidden("Je kan alleen je eigen dienst ruilen, vraag de huisoudste als je andere diensten wilt ruilen")

    #only modify shifts so that the right person is doing the right tasks
    if not shift1.task in shift2.room.tasks.all() or not shift2.task in shift1.room.tasks.all():
        return HttpResponseForbidden("De taak is voor één van de kamers niet beschikbaar")

    #only modify current or future shifts
    if (shift1.week.type == Week.PAST or shift2.week.type == Week.PAST) \
            and not request.user.has_perm('schedule.can_switch_others'):
        return HttpResponseForbidden("Je kan geen taken in het verleden wisselen.")

    #only modify from different weeks
    if shift1.week == shift2.week\
            and not request.user.has_perm('schedule.can_switch_others'):
        return HttpResponseForbidden("Je kan niet binnen de zelfde week wisselen.")

    #only modify if two different rooms
    if shift1.room == shift2.room:
        return HttpResponseForbidden("Je wisselt met dezelfde kamer, dat heeft natuurlijk geen zin.")

    #everything is fine, proceed
    shift1.room, shift2.room = shift2.room, shift1.room
    shift1.save()
    shift2.save()

    email_switch_shift(shift1, shift2, shift1_user, shift2_user)

    return HttpResponse('De taken van {0} en {1} zijn omgewisseld'.format(shift1_user, shift2_user))


def email_switch_shift(shift1, shift2, shift1_user, shift2_user):
    plaintext = get_template('schedule/email_switch_shift.txt')
    html = get_template('schedule/email_switch_shift.html')
    subject = get_template('schedule/email_switch_shift_subject.txt')

    current_site = Site.objects.get_current()
    domain = current_site.domain

    d = Context({'shift1': shift1, 'shift2': shift2, 'shift1_user': shift1_user, 'shift2_user': shift2_user, 'domain': domain})

    to = [shift1_user.email, shift2_user.email]
    subject_content = subject.render(d)
    text_content = plaintext.render(d)
    html_content = html.render(d)
    msg = EmailMultiAlternatives(subject=subject_content, body=text_content, to=to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()

'''
Template matrix to do assignment, nrs 1-5 represent kortegang task, nrs 6-14 langegangtask
n weeks and 4 tasks, in proper order (position 4 is kortegang etc)
Every n weeks this template is used with the numbers representing rooms, but each time the rooms shift by one
Also adjust create_kortegang and  create_langegang
'''

matrix = [
    [14, 7 , 6 , 1],
    [13, 8 , 9 , 4],
    [5 , 12, 11, 2],
    [10, 6 , 13, 3],
    [4 , 14, 12, 5],
    [2 , 7 , 8 , 1],
    [11, 9 , 10, 3],
]


def assign_weeks(startingweek):
    for i in range(0, len(matrix)-1):
        if startingweek.next_week(i).is_filled:
            return

    if startingweek.previous_week().is_filled:
        kortegang = create_kortegang(startingweek)
        langegang = create_langegang(startingweek)
    else:  # only needed the first time
        kortegang = list(Task.objects.get(pk=4).rooms.all())  # korte gang
        langegang = list(Task.objects.get(pk=3).rooms.all())  # lange gang
        random.shuffle(kortegang)
        random.shuffle(langegang)

    current_week = startingweek

    # make sure they dont get the same order as last set
    kortegang = shift(kortegang, 1)
    langegang = shift(langegang, 1)

    assign_matrix(current_week, kortegang + langegang)


def shift(seq, n):
    n = n % len(seq)
    return seq[-n:] + seq[:-n]


def create_kortegang(startingweek):
    """recreate the last used order of rooms for the kortegang task (see the matrix)"""
    return [
        startingweek.previous_week(2).shifts.all().get(task__id=4).room,  # 1
        startingweek.previous_week(2).shifts.all().get(task__id=1).room,  # 2
        startingweek.previous_week(1).shifts.all().get(task__id=4).room,  # 3
        startingweek.previous_week(3).shifts.all().get(task__id=1).room,  # 4
        startingweek.previous_week(3).shifts.all().get(task__id=4).room   # 5
    ]


def create_langegang(startingweek):
    """recreate the last used order of rooms for the langegang task (see the matrix)"""
    return [
        startingweek.previous_week(4).shifts.all().get(task__id=2).room,  # 6
        startingweek.previous_week(2).shifts.all().get(task__id=2).room,  # 7
        startingweek.previous_week(2).shifts.all().get(task__id=3).room,  # 8
        startingweek.previous_week(1).shifts.all().get(task__id=2).room,  # 9
        startingweek.previous_week(1).shifts.all().get(task__id=3).room,  # 10
        startingweek.previous_week(1).shifts.all().get(task__id=1).room,  # 11
        startingweek.previous_week(3).shifts.all().get(task__id=3).room,  # 12
        startingweek.previous_week(4).shifts.all().get(task__id=3).room,  # 13
        startingweek.previous_week(3).shifts.all().get(task__id=2).room   # 14
    ]


def assign_matrix(startingweek, rooms):
    current_week = startingweek
    for week in matrix:
        for task in Task.objects.all():
            room = rooms[week[task.id - 1] - 1]
            shift = Shift(task=task, week=current_week, room=room)
            shift.save()
        current_week = current_week.next_week()


def cron(request):
    from .tasks import notify_last_week, notify_next_week

    if date.today().isoweekday() % 7 == 1:
        notify_last_week()

    if date.today().isoweekday() % 7 == 3:
        notify_next_week()

    return HttpResponse('')
