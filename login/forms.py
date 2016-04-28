from django import forms
from .models import User

class LoginForm(forms.ModelForm):
	class Meta:
		model=User
		fields=[

			"name",
			"email",
			"password",
			"age",
			"occupation",
			"nationality",
			"region",
			"gender"
		]