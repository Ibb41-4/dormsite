from django.forms import ModelForm, DecimalField, ModelChoiceField
from django.contrib.auth.models import User

from dinners.models import Dinner

class DinnersForm(ModelForm):
    price = DecimalField(max_digits=5, decimal_places=2, localize=True)

    class Meta:
        model = Dinner
        localize = True
        exclude = ('created_by', 'created')

