from django.conf.urls import url
from django.contrib import admin

from .views import (

    User_signup,
    User_detail,
    User_update,
    User_delete,
    User_list,
    ContactUs,
    About,
)

urlpatterns = [
    url(r'^$',User_signup, name='home'),  # this will be our home page for post application
    url(r'^list/$',User_list ,name='list'),    
    url(r'^(?P<id>\d+)/detail/$',User_detail , name='detail'),
    url(r'^edit/$',User_update, name='update'),
    url(r'^(?P<id>\d+)/delete/$',User_delete ,name='delete'),
    url(r'^about/$',About, name='About'),
    url(r'^contactus/$',ContactUs, name='ContactUs'),
]
