from django.db import models
from django.contrib.auth.models import User

class TrackableModel(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)
	created_by = models.ForeignKey(User, related_name="added_%(class)s", editable=False)
	modified_by = models.ForeignKey(User, related_name="changed_%(class)s", editable=False)

	class Meta():
		get_latest_by = 'created'
		abstract = True
