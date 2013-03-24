from django import forms

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm as UserChangeFormOriginal
from django.contrib.auth.forms import UserCreationForm as UserCreationFormOriginal

from django.forms.formsets import formset_factory
from django.forms.formsets import BaseFormSet

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, HTML, Div, Field
from crispy_forms.bootstrap import FormActions, AppendedText, StrictButton

from .models import User, Room, RoomAssignment


class UserForm(forms.ModelForm):

    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'email', 'birthdate', 'phonenumber', 'emergency_phonenumber')


class UserChangeForm(UserChangeFormOriginal):
    class Meta:
        model = get_user_model()


class UserCreationForm(UserCreationFormOriginal):

    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"]
        try:
            get_user_model().objects.get(username=username)
        except get_user_model().DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])

    class Meta(UserCreationFormOriginal.Meta):
        model = get_user_model()


class UserMoveForm(forms.ModelForm):
    date = forms.DateField(input_formats=['%d-%m-%Y', '%d-%m-%y', '%d%m%Y', '%d%m%y'], label='Datum', help_text='De datum waarop de nieuwe huisgenoot officieel hier komt wonen')
    goer = forms.ModelChoiceField(queryset=User.residents.all(), empty_label=None, label='Vertrekkende huisgenoot')

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.html5_required = True
        self.helper.form_class = ''
        self.helper.layout = Layout(
            Fieldset(
                'Nieuwe huisgenoot',
                'username',
                'date',
                'goer',
            ),
            Fieldset(
                'Doorverhuizers',
                HTML('''
                    {% load crispy_forms_tags %}
                    <span class="help-block">
                        Verwissel de koffertjes zodat iederen in de goede kamer komt.
                        Selecteer daarna de huisgenoot die vertrekt.
                        Dit is dan ook gelijk de kamer waar de nieuwe huisgenoot komt wonen.
                    </span>
                    {{ room_formset.management_form }}
                    {{non_form_errors}}
                    {% for form in room_formset.forms %}
                        {% crispy form %}
                    {% endfor %}
                '''),
            ),
            FormActions(
                StrictButton('Opslaan', type='submit', css_class='btn btn-primary')
            )
        )
        super(UserMoveForm, self).__init__(*args, **kwargs)

    class Meta:
        model = get_user_model()
        fields = ('username', )


class RoomAssignmentForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.residents.all(), empty_label=None, label='Bewoner')
    room = forms.ModelChoiceField(queryset=Room.objects.all(), empty_label=None, required=False)

    def __init__(self, room, *args, **kwargs):
        self.room = room
        self.helper = FormHelper()
        self.helper.html5_required = True
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Div(
                Div(
                    HTML('{0} ({1})'.format(self.room, self.room.current_user())),
                    css_class="span6"
                ),
                Div(
                    css_class="move_user span6 label-info"
                ),
                'user',
                css_class="move_room well row-fluid"
            ),
        )

        super(RoomAssignmentForm, self).__init__(*args, **kwargs)

    class Meta:
        model = RoomAssignment
        exclude = ('room', 'start_date')


class BaseRoomAssignmentsFormSet(BaseFormSet):
    def clean(self):
        if any(self.errors):
            # Don't bother validating the formset unless each form is valid on its own
            return

        if self.total_form_count() != self.initial_form_count():
            raise forms.ValidationError("Er is een kamer bijgekomen, dat kan niet")

        users_present = User.residents.all()
        users = []
        for form in self.forms:
            user = form.cleaned_data['user']

            if user in users:
                raise forms.ValidationError("Elke persoon mag maar een kamer hebben")
            if not user in users_present:
                raise forms.ValidationError("Een persoon woont hier niet")
            users.append(user)

    def _construct_forms(self):  # this one is merely taken from django's BaseFormSet
            # except the additional room parameter for the Form-constructor
            self.forms = []
            for i, room in enumerate(Room.objects.all()):
                self.forms.append(self._construct_form(i, room=room))

RoomAssignmentsFormSet = formset_factory(RoomAssignmentForm, extra=0, formset=BaseRoomAssignmentsFormSet, max_num=Room.objects.all().count())


class AbdicateForm(forms.Form):
    new_elder = forms.ModelChoiceField(queryset=User.residents.all(), empty_label=None, label='De nieuwe huisoudste')

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.html5_required = True
        self.helper.layout = Layout(
            'new_elder',
            FormActions(
                StrictButton('Submit', type='submit', css_class='btn btn-primary')
            )
        )
        super(AbdicateForm, self).__init__(*args, **kwargs)
