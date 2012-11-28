from datetime import date, datetime

from django.conf import settings 
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.utils import simplejson
from django.views.generic import DetailView


from core.views import TabledFormView
from user_details.models import User

from .models import Balance, BalanceRow
from .models import Bill, Dinner, Expense, Drink
from .forms import BillsForm, ExpensesForm, DrinksForm, DinnersForm


class BalanceView(DetailView):
    model = Balance

    def get_object(self):
        if 'pk' in self.kwargs:
            return self.model.objects.get(pk=self.kwargs['pk'])
        else:
            return self.model.get_latest()


class BillsView(TabledFormView):
    model = Bill
    form_class = BillsForm

class DrinksView(TabledFormView):
    model = Drink
    form_class = DrinksForm

    def create_response(self, instance):
        return {'payer': unicode(instance.payer), 'description': instance.number, 'price': float(instance.price)}


class ExpensesView(TabledFormView):
    model = Expense
    form_class = ExpensesForm

class DinnersView(TabledFormView):
    template_name = 'dinners/index.html'
    model = Dinner
    form_class = DinnersForm
    
    def get_initial(self):
        initial = super(DinnersView, self).get_initial()
        initial['eaters']=User.objects.filter(pk=self.request.user.pk)
        return initial


    def create_response(self, instance):
        return {'payer': unicode(instance.payer), 'description': ', '.join(map(lambda x: unicode(x.user)+(u'+'+unicode(x.extra) if x.extra > 0  else u''), instance.eater_set.all())), 'price': float(instance.price)}


def make_balance(request):
    request.user.has_perm('balance.add_balance')
    new_balance = Balance.objects.get(preview=True)
    new_balance.preview = False

    #reset created dates (we don't count previews)
    new_balance.created_by = request.user
    new_balance.created = datetime.now()
    new_balance.save()
  
    preview_balance = Balance(preview=True, created_by=request.user, modified_by=request.user)
    preview_balance.save()

    return HttpResponseRedirect('/balance/')
