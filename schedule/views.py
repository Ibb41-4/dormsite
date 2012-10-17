from random import shuffle

from django_tables2 import A
from django.shortcuts import render
from django.http import HttpResponse


from schedule.models import Week, Room, Task, Shift
from schedule.tables import WeeksTable

def toggle(request, pk, toggle):
	shift = Shift.objects.get(pk=pk)
	shift.done = True if toggle == 'on' else False
	shift.save()
	return HttpResponse('')

def schedule(request):
    #Week.objects.filter(startdate__gt=zz)
    current_week = Week.get_current_week()
    weeks = current_week.get_weeks(-7)
    weeks += current_week.get_weeks(27)[1:]

    data = []
    current = 'past_week'
    for week in weeks:
    	assign_weeks(week)
    	if current_week is week:
    		current = 'current_week'
    	weekdata = {'Week': week.startdate, 'startdate': week.startdate, 'current': current }

    	if current == 'current_week':
    		current = 'future_week'

    	for task in week.tasks:
    		shift = Shift.objects.get(week=week, task=task)
    		weekdata[task.id] = {
    			'room':shift.room, 
    			'id': shift.id,
    			'done': shift.done,
    		}

    	data.append(weekdata)
  #  d = list(list(s)[0].shifts

   # x = A("shifts.0").resolve(s[1])
   # x()
    table = WeeksTable(data)
    table.paginate(page=request.GET.get('page', 1), per_page=35)
    return render(request, 'schedule/schedule.html', {'data': data, 'tasks': Task.objects.all()})

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
	for room in rooms:
		if created:
			continue
		shift, created = Shift.objects.get_or_create(task=task, week=week, defaults={'room': room})
	return shift.room