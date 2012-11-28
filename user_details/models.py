from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.signals import post_save

class User(AbstractUser):
    #first_name = models.CharField(max_length=50)
    #last_name = models.CharField(max_length=100)  
    phonenumber = models.CharField(max_length=20, null=True)
    emergency_phonenumber = models.CharField(max_length=20, null=True, blank=True)
    birthdate = models.DateField(null=True,)
    startdate = models.DateField(null=True,)
    enddate = models.DateField(null=True, blank=True)

    REQUIRED_FIELDS = ['first_name', 'last_name', 'email', 'phonenumber', 'birthdate', 'startdate']

    def get_full_name(self):
        return str(self.first_name, self.last_name)

    def get_short_name(self):
        return self.first_name

    def __unicode__(self):
        return self.get_short_name()

    class Meta:
        ordering = ['first_name', 'last_name']