from random import shuffle

from django_tables2 import A
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import permission_required
from django.forms.models import model_to_dict
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context


from schedule.models import Week, Room, Task, Shift
from schedule.tables import WeeksTable

from dormsite.decorators import class_view_decorator


def toggle(request, pk, toggle):
    shift = Shift.objects.get(pk=pk)
    shift.done = True if toggle == 'on' else False
    shift.save()
    return HttpResponse('')

@permission_required('schedule.view_shifts')
def schedule(request):
    start_week = Week.get_current_week().previous_week(7)

    weeks = start_week.get_weeks(35)
    
    for week in weeks:
        assign_weeks(week)

    return render(request, 'schedule/schedule.html', {'data': weeks, 'tasks': Task.objects.all()})

@permission_required('schedule.view_shifts')
def print_schedule(request):
    current_week = Week.get_current_week()
    weeks = current_week.get_weeks(21)
    return render(request, 'schedule/print_schedule.html', {'data': weeks, 'tasks': Task.objects.all()})

@permission_required('schedule.view_shifts')
def switch_shifts(request, id1, id2):
    shift1 = Shift.objects.get(pk=id1)
    shift2 = Shift.objects.get(pk=id2)

    #only modify your own shifts, unless you have rights
    if not request.user == shift1.room.user and not request.user == shift2.room.user:
        if not request.user.has_perm('shift.can_switch_others'):
            return HttpResponseForbidden("own")

    #only modify shifts so that the right person is doing the right tasks
    if not shift1.task in shift2.room.tasks.all() or not shift2.task in shift1.room.tasks.all():
        return HttpResponseForbidden("tasks")

    #only modify current or future shifts
    if shift1.week.type == Week.PAST or shift2.week.type == Week.PAST:
        return HttpResponseForbidden("past")

    #only modify from different weeks
    if shift1.week == shift2.week:
        return HttpResponseForbidden("week")


    #only modify if two different rooms
    if shift1.room == shift2.room:
        return HttpResponseForbidden("same")

    #everything is fine, proceed
    shift1.room, shift2.room = shift2.room, shift1.room
    shift1.save()
    shift2.save()

    email_switch_shift(shift1, shift2)

    return HttpResponse('true')


def email_switch_shift(shift1, shift2):
    plaintext = get_template('schedule/email_switch_shift.html')
    html      = get_template('schedule/email_switch_shift.html')
    subject   = get_template('schedule/email_switch_shift_subject.txt')

    d = Context({ 'shift1': shift1, 'shift2': shift2 })

    from_email, to = 'no-reply@huissite.hmvp.nl', [shift1.room.user.email, shift2.room.user.email]
    subject_content = subject.render(d)
    text_content = plaintext.render(d)
    html_content = html.render(d)
    msg = EmailMultiAlternatives(subject_content, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()

'''
Matrix to do assignment, nrs 1-5 represent kortegang task, nrs 6-14 langegangtask
7 weeks and 4 tasks, in proper order (position 4 is kortegang etc)
'''

matrix = [[4,9,6,1],[5,10,7,2],[13,14,8,4],[12,11,9,3],[6,13,10,5],[7,14,11,1],[8,3,12,2]]

def assign_weeks(startingweek):
    if startingweek.is_filled:
        return

    if startingweek.previous_week().is_filled:
        kortegang = create_kortegang(startingweek)
        langegang = create_langegang(startingweek)
    else:
        kortegang = list(Task.objects.get(pk=4).rooms.all()) #korte gang
        langegang = list(Task.objects.get(pk=3).rooms.all()) #lange gang
    
    current_week = startingweek


    # make sure they dont get the same order as last set
    kortegang = shift(kortegang, 2) 
    langegang = shift(langegang, 2) 

    assign_matrix(current_week, kortegang + langegang)    


def shift(seq, n):
    n = n % len(seq)
    return seq[-n:] + seq[:-n]

def create_kortegang(startingweek):
    """recreate the last used order of rooms for the kortegang task (see the matrix)"""
    x = startingweek.previous_week(3).shifts.all()
    return [
        startingweek.previous_week(2).shifts.all().get(task__id=4).room,
        startingweek.previous_week(1).shifts.all().get(task__id=4).room,
        startingweek.previous_week(1).shifts.all().get(task__id=2).room,
        startingweek.previous_week(5).shifts.all().get(task__id=4).room,
        startingweek.previous_week(3).shifts.all().get(task__id=4).room
    ]

def create_langegang(startingweek):
    """recreate the last used order of rooms for the langegang task (see the matrix)"""
    return [
        startingweek.previous_week(3).shifts.all().get(task__id=1).room,
        startingweek.previous_week(2).shifts.all().get(task__id=1).room,
        startingweek.previous_week(1).shifts.all().get(task__id=1).room,
        startingweek.previous_week(4).shifts.all().get(task__id=3).room,
        startingweek.previous_week(3).shifts.all().get(task__id=3).room,
        startingweek.previous_week(2).shifts.all().get(task__id=3).room,
        startingweek.previous_week(1).shifts.all().get(task__id=3).room,
        startingweek.previous_week(3).shifts.all().get(task__id=2).room,
        startingweek.previous_week(2).shifts.all().get(task__id=2).room
    ]

def assign_matrix(startingweek, rooms):
    current_week = startingweek
    for week in matrix:
        for task in Task.objects.all():
            room = rooms[week[task.id-1]-1]
            shift = Shift(task=task, week=current_week, room=room)
            shift.save()
        current_week = current_week.next_week()


