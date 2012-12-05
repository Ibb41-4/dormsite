from random import shuffle

from django_tables2 import A
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import permission_required
from django.forms.models import model_to_dict


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
    current_week = Week.get_current_week()
    weeks = current_week.get_weeks(-7)
    weeks += current_week.get_weeks(27)[1:]
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

	#only modify if two different rooms
	if shift1.room == shift2.room:
		return HttpResponseForbidden("same")

	#everything is fine, proceed
	shift1.room, shift2.room = shift2.room, shift1.room
	shift1.save()
	shift2.save()

	#TODO:Email
	return HttpResponse('true')


def assign_weeks(week):
	weeks = week.get_weeks(7)
	if any(map(lambda week: week.is_filled, weeks)):
		return
	else:
		rooms, excluded_rooms = make_room_list(week)

		split_week_old_rooms = []

		first_of_new_set = True
		split_week2 = False
		for week in weeks:
			split_week = False
			rooms_without_split = []
			#split week, ie we have less rooms then tasks and we need to add some from the next set
			if len(rooms) < len(Task.objects.all()):
				first_of_new_set = True
				split_week = True
				split_week_old_rooms = rooms
				new_rooms, excluded_rooms = make_room_list(week)
				rooms_without_split = [room for room in new_rooms if not room in split_week_old_rooms]
				shuffle(rooms_without_split)
				split_week_new_rooms = rooms_without_split[0:2]
				rooms_without_split = rooms_without_split[2:]
				rooms = split_week_old_rooms + split_week_new_rooms

			rooms = assign_week(week, rooms)
			
			if split_week:
				split_week = False
				split_week2 = True
				rooms = rooms_without_split

			if split_week2:
				split_week2 = False
				rooms = rooms + split_week_old_rooms

			if first_of_new_set:
				first_of_new_set = False
				rooms = rooms + excluded_rooms

def assign_week(week, rooms):
	for task in Task.objects.all():
		room = assign_tasks(task, week, rooms)
		rooms.remove(room)
	return rooms


def make_room_list(week):
	prev_week = week.previous()
	excluded_rooms = list(Room.objects.filter(shifts__week = prev_week))
	rooms = list(Room.objects.all())
	
	for room in excluded_rooms:
		rooms.remove(room)

	return rooms, excluded_rooms


def assign_tasks(task, week, rooms):
	created = False
	shift = None
	shuffle(rooms)
	for room in rooms: #[room for room in rooms if room in task.rooms.all()]:
		if created:
			continue
		shift, created = Shift.objects.get_or_create(task=task, week=week, defaults={'room': room})
	return shift.room