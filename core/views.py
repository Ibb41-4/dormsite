from datetime import date

from django.shortcuts import render
from django.http import HttpResponse
from django.utils import simplejson

from django.views.generic import DetailView
from django.views.generic.edit import FormView
from django.views.generic import ListView

from balance.models import Balance


class DefaultDetailView(DetailView):
    def get_object(self, queryset=None):
        try: 
            return self.model.objects.filter(preview=False).latest()
        except self.model.DoesNotExist:
            return self.model(created=date.today)


class TabledFormView(ListView, FormView):
    object_list = []

    def get_queryset(self):
        return super(TabledFormView, self).get_queryset().filter(created__gt=Balance.get_latest().created)

    def get_initial(self):
        return {'payer': self.request.user, 'created_by': self.request.user}

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        if not 'object_list' in kwargs:
            kwargs['object_list'] = []

        context = super(TabledFormView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['form'] = self.get_form(self.get_form_class())
        return context
    
    def form_valid(self, form):
        if self.request.user.is_authenticated():
            instance = form.save()
            data = self.create_response(instance)
            json = simplejson.dumps(data)
            return HttpResponse(json, 'text/json')

    def create_response(self, instance):
        return {'payer': unicode(instance.payer), 'description': instance.description, 'price': float(instance.price)}

    def form_invalid(self, form):
        return HttpResponse(form.errors, 'text/html')