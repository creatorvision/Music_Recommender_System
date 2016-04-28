from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render , get_object_or_404, redirect
from django.contrib import messages
from .models import User
from .forms import LoginForm
from django.db import connection, transaction
from collections import namedtuple

def User_signup(request):
	#form=LoginForm()
	#context={
	#	"form":form,
	#}
	#return render(request,"login_home.html",context)

    form=LoginForm(request.POST or None)
    # if form.is_valid():
    #     instance=form.save(commit=False)
    #     instance.save()
    if request.method=='POST' and 'signup' in request.POST:
    	name= request.POST.get('name')
    	age= request.POST.get('age')
    	occupation= request.POST.get('occupation')
    	email= request.POST.get('email')
    	gender= request.POST.get('gender')
    	password= request.POST.get('password')
    	nationality= request.POST.get('nationality')
    	region= request.POST.get('region')
    	instance=User.objects.create(name=name, age=age, occupation=occupation, email=email, gender=gender, password=password, nationality=nationality, region=region)
        #messages.success(request,"sucessfully created")
        return HttpResponseRedirect(instance.get_redirect_after_signup())
    if request.method=="POST" and 'login' in request.POST:
        email= request.POST.get('email')
        password= request.POST.get('password')

        if User.objects.filter(email=email,password=password).exists():
            instance=User.objects.get(email=email)
            return HttpResponseRedirect(instance.get_redirect_after_signup())
        else :
            raise Http404("Username and password Combination did not match")

    context={
        "form":form,
        "buttonvalue":"Create"
    }
    return render(request,"login_home.html",context)

def User_list(request):
    queryset= User.objects.all()
    context={
        "Object_list":queryset,
        "title":"List"
    }
    return render(request,"User_list.html",context)


# def User_create(request):
# 	return HttpResponse("<h1> Welcome to User home Create </h1>")

def User_detail(request, id):
    instance= get_object_or_404(User,id=id)
    form=LoginForm(request.POST or None)
    context={
        "form":form,
        "instance":instance
    }
    if request.method=='POST' and 'reco' in request.POST:
        Songs_list(request)
    else:
        return render(request,"User_detail.html",context)

def User_update(request):
	return HttpResponse("<h1> Welcome to User home Update</h1>")

def User_delete(request, id=None):
	instance =get_object_or_404(User, id=id)
	instance.delete()
	#messages.success(request, "Successfully Deleted")
	return redirect("login:home")

def Songs_list(request):
    c=connection.cursor()
    try:
        c.execute("select * from songs")
        queryset=namedtuplefetchall(c)   
        songname=queryset[0][0]
        #songname=[]
        #i=0
        #for row in c.fetchall():
        #    songname.append(queryset[i].song)
        #    i=i+1
        #print songname
        context={

            "songname":songname
        }
        return render(request,"songs_list.html",context)

    finally:
        c.close()

def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]

