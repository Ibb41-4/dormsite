from datetime import datetime

from django.http import HttpResponseRedirect
from django.views.generic import DetailView
from django.contrib.auth.decorators import permission_required


from core.views import TabledFormView
from residents.models import User

from .models import Balance
from .models import Bill, Dinner, Expense, Drink
from .forms import BillsForm, ExpensesForm, DrinksForm, DinnersForm
from dormsite.decorators import class_view_decorator


@class_view_decorator(permission_required('balance.view_balance'))
class BalanceView(DetailView):
    model = Balance

    def get_object(self):
        if 'pk' in self.kwargs:
            return self.model.objects.get(pk=self.kwargs['pk'])
        else:
            return self.model.get_latest()


@class_view_decorator(permission_required('balance.add_bill'))
class BillsView(TabledFormView):
    model = Bill
    form_class = BillsForm


@class_view_decorator(permission_required('balance.add_drink'))
class DrinksView(TabledFormView):
    model = Drink
    form_class = DrinksForm

    def create_response(self, instance):
        return {'payer': unicode(instance.payer), 'description': instance.number, 'price': float(instance.price)}


@class_view_decorator(permission_required('balance.add_expense'))
class ExpensesView(TabledFormView):
    model = Expense
    form_class = ExpensesForm


@class_view_decorator(permission_required('balance.add_dinner'))
class DinnersView(TabledFormView):
    template_name = 'dinners/index.html'
    model = Dinner
    form_class = DinnersForm

    def get_initial(self):
        initial = super(DinnersView, self).get_initial()
        initial['eaters'] = User.objects.filter(pk=self.request.user.pk)
        return initial

    def create_response(self, instance):
        f = lambda x: unicode(x.user) + ('+' + unicode(x.extra) if x.extra > 0 else '')
        description_array = map(f, instance.eater_set.all())

        return {
            'payer': unicode(instance.payer),
            'description': ', '.join(description_array),
            'price': float(instance.price)
        }


@permission_required('balance.create_balance')
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
