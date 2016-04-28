from django.contrib import admin

from .models import User
# Register your models here.

class UserModelAdmin(admin.ModelAdmin):
	list_display=["name","email","age","gender"]
	class Meta:
		model=User

	list_display_links=["email"]
	list_filter=["age","gender"]
	search_feilds=["name","age","gender"]

admin.site.register(User, UserModelAdmin)
