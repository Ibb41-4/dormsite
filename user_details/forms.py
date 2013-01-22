from django import forms

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm as UserChangeFormOriginal
from django.contrib.auth.forms import UserCreationForm as UserCreationFormOriginal


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
