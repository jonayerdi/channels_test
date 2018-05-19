from django.db import models

class Text(models.Model):
	id = models.AutoField(primary_key=True)
	text = models.TextField()
