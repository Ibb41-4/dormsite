from django.db import models
from django.conf import settings

from django.contrib.sites.models import Site


class TrackableModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="added_%(class)s", editable=False)
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="changed_%(class)s", editable=False)

    class Meta():
        get_latest_by = 'created'
        abstract = True


class Setting(models.Model):
    site = models.OneToOneField(Site)
    name = models.CharField(max_length=20)
    value = models.CharField(max_length=200)
