from django.forms import ModelForm, DecimalField, ModelChoiceField
from django.contrib.auth.models import User

from expenses.models import Expense


class ExpensesForm(ModelForm):
    price = DecimalField(max_digits=6, decimal_places=2, localize=True)

    class Meta:
        model = Expense
        localize = True
        exclude = ('created_by', 'created')

