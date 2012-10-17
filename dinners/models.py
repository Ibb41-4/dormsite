from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Dinner(models.Model):
    payer = models.ForeignKey(User, related_name="paid_dinners")
    eaters = models.ManyToManyField(User, related_name="dinners")
    price = models.DecimalField(max_digits=5, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name="added_dinners")

    def __unicode__(self):
    	return u"Eten voor %s" % self.price
