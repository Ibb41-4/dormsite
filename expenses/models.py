from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Expense(models.Model):
    payer = models.ForeignKey(User, related_name="payed_expenses")
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name="added_expenses")

    def __unicode__(self):
    	description = (self.description[:75] + '..') if len(self.description) > 75 else self.description
    	return u"\u20ac %s voor %s" % (self.price, description)
