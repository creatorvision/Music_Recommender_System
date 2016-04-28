from __future__ import unicode_literals

from django.db import models
from django.core.urlresolvers import reverse
# Create your models here.

class User (models.Model):

	name=models.CharField(max_length=255)
	email=models.CharField(max_length=255)
	password=models.CharField(max_length=10)
	nationality=models.CharField(max_length=255)
	region=models.CharField(max_length=255)
	occupation=models.CharField(max_length=255)
	age=models.IntegerField()
	GENDER=(

			("m","male"),
			("f","female")

		)
	gender=models.CharField(max_length=1, choices=GENDER)

	def _unicode_(self):
		return self.email

	def _str_(self):
		return self.email

	def get_redirect_after_signup(self):
		return reverse("login:detail", kwargs={"id":self.id})
