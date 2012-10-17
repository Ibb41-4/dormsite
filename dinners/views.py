from django.shortcuts import render
from django.views.generic.edit import FormView
from django.views.generic import ListView
from django.http import HttpResponse
from django.utils import simplejson


from dinners.forms import DinnersForm
from dinners.models import Dinner

class DinnersView(ListView, FormView):
    template_name = 'dinners/index.html'
    model = Dinner
    form_class = DinnersForm

    def get_initial(self):
        return {'payer': self.request.user}

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        if not 'object_list' in kwargs:
            kwargs['object_list'] = []

        context = super(DinnersView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['form'] = self.get_form(self.get_form_class())
        return context

    def form_valid(self, form):
        if self.request.user.is_authenticated():
            dinner = form.save(commit=False)
            dinner.created_by = self.request.user
            dinner.save()
            form.save_m2m() # needed because we used commit=False
            data = {'payer': unicode(dinner.payer), 'description': ', '.join(map(unicode, dinner.eaters.all())), 'price': float(dinner.price)}
            json = simplejson.dumps(data)
            return HttpResponse(json, 'text/json')

    def form_invalid(self, form):
        return HttpResponse(form.errors, 'text/html')

