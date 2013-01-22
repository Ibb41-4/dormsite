from django.db import models
from django.conf import settings


class TrackableModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="added_%(class)s", editable=False)
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="changed_%(class)s", editable=False)

    class Meta():
        get_latest_by = 'created'
        abstract = True

"""
class Settings(model.Model):
    site = models.OneToOneField(Site)
    monthly_fee =
    bankaccount =
    email =
    facebook =
    last_fm =
    address =
"""
