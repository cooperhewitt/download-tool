from django.db import models

class Download(models.Model):
	email = models.CharField(max_length=20)