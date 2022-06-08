from django.db import models

class Book(models.Model):
	name = models.CharField(max_length=250)
	author = models.CharField(max_length=250)
	isbn = models.CharField(max_length=30)
	publisher = models.CharField(max_length=250)

	def __str__(self):
		return self.name