from django.shortcuts import render
from django.views.generic.edit import FormView
from django.views.generic import ListView
from django.http import HttpResponse
from django.utils import simplejson


from expenses.forms import ExpensesForm
from expenses.models import Expense

class ExpensesView(ListView, FormView):
    template_name = 'expenses/index.html'
    model = Expense
    form_class = ExpensesForm
    object_list = []

    def get_initial(self):
        return {'payer': self.request.user, 'created_by': self.request.user}

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        if not 'object_list' in kwargs:
            kwargs['object_list'] = []

        context = super(ExpensesView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['form'] = self.get_form(self.get_form_class())
        return context

    def form_valid(self, form):
        if self.request.user.is_authenticated():
            expense = form.save(commit=False)
            expense.created_by = self.request.user
            expense.save()
            data = {'payer': unicode(expense.payer), 'description': expense.description, 'price': float(expense.price)}
            json = simplejson.dumps(data)
            return HttpResponse(json, 'text/json')

    def form_invalid(self, form):
        return HttpResponse(form.errors, 'text/html')
