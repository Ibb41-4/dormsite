from django import forms
from residents.models import User

from .models import Bill
from .models import Expense
from .models import Drink
from .models import Dinner
from .models import Eater


class PriceForm(forms.ModelForm):
    price = forms.DecimalField(max_digits=5, decimal_places=2, localize=True)

    class Meta:
        localize = True


class BillsForm(PriceForm):

    class Meta(PriceForm.Meta):
        model = Bill


class ExpensesForm(PriceForm):

    class Meta(PriceForm.Meta):
        model = Expense


class DrinksForm(PriceForm):
    number = forms.IntegerField(max_value=100, min_value=1)

    class Meta(PriceForm.Meta):
        model = Drink


class DinnersForm(PriceForm):

    class Meta(PriceForm.Meta):
        model = Dinner
        exclude = ['number']

    def save(self, commit=True):
        dinner = super(DinnersForm, self).save(commit=False)  # Save the child so we have an ID for the m2m

        def save_m2m():
            eaters = self.cleaned_data.get('eaters')
            for eater in eaters:
                extra = self.data.get(str(eater.id) + "_extra")
                print dinner
                print eater
                print extra
                print self.cleaned_data
                print str(eater.id) + "_extra"
                print self.data

                Eater.objects.create(dinner=dinner, user=eater, extra=extra)

        if commit:
            # If we are committing, save the instance and the m2m data immediately.
            dinner.save()
            save_m2m()
        else:
            # We're not committing. Add a method to the form to allow deferred
            # saving of m2m data.
            self.save_m2m = save_m2m

        return dinner
