from django.db import models
from django.contrib.auth.models import User

class Download(models.Model):
	user = models.ForeignKey(User)
	search_terms = models.TextField()
	date_saved = models.DateTimeField(auto_now_add=True)