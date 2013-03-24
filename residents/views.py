from django_tables2 import RequestConfig

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView, CreateView, FormView
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db import transaction
from django.http import HttpResponseRedirect
from django.conf import settings

from residents.tables import UsersTable

from .forms import UserForm, UserMoveForm, RoomAssignmentsFormSet, AbdicateForm
from .models import Room, User


@login_required
def index(request):
    users = get_user_model().residents.all()
    table = UsersTable(users)
    RequestConfig(request).configure(table)
    return render(request, 'residents/index.html', {'table': table, 'users': users})


@login_required
def old_residents(request):
    users = get_user_model().objects.filter(is_active=False)
    table = UsersTable(users)
    RequestConfig(request).configure(table)
    return render(request, 'residents/old_residents.html', {'table': table, 'users': users})


class UserMoveView(CreateView):
    template_name = 'residents/move_form.html'
    model = User
    form_class = UserMoveForm
    success_url = '/'

    @transaction.commit_on_success
    def form_valid(self, form):
        context = self.get_context_data()
        room_formset = context['room_formset']

        if room_formset.is_valid():
            new = form.save()

            #add new user to group
            group = Group.objects.get(name=settings.RESIDENTS_GROUP_NAME)
            new.groups.add(group)
            new.save()

            #do change residents
            goer = form.cleaned_data['goer']
            if not goer:
                return self.render_to_response(self.get_context_data(form=form, non_form_errors=room_formset.non_form_errors()))

            startdate = form.cleaned_data['date']

            #check for each room the new assignment
            rooms = Room.objects.all()
            for index, room_form in enumerate(room_formset):
                room = rooms[index]
                user = room_form.cleaned_data['user']

                #replace goer with new user
                if user == goer:
                    user = new

                #only save changed rooms
                if not room.current_user() == user:
                    room.roomassignments.create(start_date=startdate, user=user)

            return HttpResponseRedirect(self.success_url)
        else:
            return self.render_to_response(self.get_context_data(form=form, non_form_errors=room_formset.non_form_errors()))

    #def form_invalid(self, form):
    #    return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super(UserMoveView, self).get_context_data(**kwargs)

        if self.request.POST:
            context['room_formset'] = RoomAssignmentsFormSet(self.request.POST)
        else:
            data = {
                'form-TOTAL_FORMS': Room.objects.count(),
                'form-INITIAL_FORMS': Room.objects.count(),
                'form-MAX_NUM_FORMS': Room.objects.count(),
            }
            for index, room in enumerate(Room.objects.all()):
                data['form-{}-room'.format(index)] = room
                data['form-{}-user'.format(index)] = room.current_user()

            context['room_formset'] = RoomAssignmentsFormSet(data)
        return context


class UserView(UpdateView):
    form_class = UserForm
    success_url = '/user/'
    model = get_user_model()

    def get_object(self):
        return self.request.user


class AbdicateView(FormView):
    template_name = 'residents/abdicate_form.html'
    form_class = AbdicateForm
    success_url = '/'

    def form_valid(self, form):
        if self.request.user.is_elder() or self.request.user.is_superuser:
            group = Group.objects.get(name=settings.ELDER_GROUP_NAME)
            old_elder = self.request.user
            if old_elder.is_superuser and not old_elder.is_resident():
                old_elder = group.user_set.all()[0]

            new_elder = form.cleaned_data['new_elder']

            new_elder.groups.add(group)
            old_elder.groups.remove(group)

            new_elder.is_staff = True
            old_elder.is_staff = False

            new_elder.save()
            old_elder.save()

        return HttpResponseRedirect(self.success_url)
