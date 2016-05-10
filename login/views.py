from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render , get_object_or_404, redirect, render_to_response
from django.contrib import messages
from .models import User
from .forms import LoginForm
from django.db import connection, transaction
from collections import namedtuple
from django.utils.encoding import iri_to_uri, uri_to_iri
from django.utils.deprecation import RemovedInDjango20Warning
from django.utils.encoding import force_text
from django.utils.safestring import SafeBytes
from math import sqrt
import unicodedata


def User_signup(request):
    #form=LoginForm()
    #context={
    #   "form":form,
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
#   return HttpResponse("<h1> Welcome to User home Create </h1>")

def User_detail(request, id):
    instance= get_object_or_404(User,id=id)
    form=LoginForm(request.POST or None)
    context={
        "form":form,
        "instance":instance
    }
    if request.method=='POST' and 'reco' in request.POST:
        freq =0
        c=connection.cursor()
        c.execute("select sum(frequency) from rating where UserId=%s",[id])
        freq = c.fetchone()
        print "freq = "
        print freq[0]>=20

        if freq[0]>=20:
            #Songs_list(request)
            
            songs = {}
            try:
                c.execute("select UserId from genreliking ")
                query = c.fetchall()
                #print query
                for item in query:
                    for Uid in item:
                        songRating = {}
                        c.execute("select SongId,rating from rating where UserId = %s ",[Uid])
                        songList = c.fetchall()
                        #print songList
                        for song in songList:
                            songRating[song[0]] = song[1];
                            #print songRating
                        songs[Uid] = songRating
            finally:
                c.close()
                
            # A dictionary of users and the feature count of a small  set of music items
            '''songs={'dev': {'summer of 69': 3.5, 'numb': 3.5, 'demons': 4.0, 'sugar':4.0, 'main toh jhum':3.5,'in the end': 3.0, 'cloud nine': 3.5, '21 guns':4.0, 'wake me up':4.5, 'broken dreams':3.5, 'kabhi kabhi': 1.5,'aanewala pal': 1.5},
            'swapnil': {'summer of 69': 3.5, 'numb': 4.0, 'mockingbird': 4.0, 'lose yourself': 3.5,'in the end': 3.5, 'cloud nine': 3.5, '21 guns':4.0, 'wake me up':4.5, 'broken dreams':3.5, 'kabhi kabhi': 1.5,'aanewala pal': 2.0},
            'kshitij': {'summer of 69': 2.5, 'numb': 2.5,'in the end': 2.0, 'cloud nine': 2.5, 'kabhi kabhi': 3.5,'aanewala pal': 4.5, 'woh shaam':3.5, 'jeena yahan':4.0, 'kuch toh log':3.5, 'duniya bananewale':3.5},
            'prudhvi': {'summer of 69': 2.5, 'numb': 2.5, 'musaphir': 3.0, 'chalte chalte mere': 3.5,'in the end': 2.0, 'cloud nine': 2.5, 'kabhi kabhi': 3.0,'aanewala pal': 4.0, 'woh shaam':3.5, 'jeena yahan':4.0, 'kuch toh log':3.0, 'duniya bananewale':2.5},
            'rahul': {'party all night': 3.5, 'after party': 4.0,'bandeya': 3.5, 'agar tum saath': 3.5, '21 guns':2.0, 'wake me up':2.5, 'party tonight':3.5, 'kabhi kabhi': 2.5,'aanewala pal': 1.0, 'tu bin bataye': 4.5, 'raabta': 3.5},
            'nishant': {'party all night': 3.5, 'after party': 4.0,'bandeya': 3.5, 'agar tum saath': 3.5, '21 guns':2.0, 'wake me up':2.5, 'party tonight':3.5, 'kabhi kabhi': 2.5,'aanewala pal': 1.0},
            'test': {'jiya ho':3.0}}
            '''

            ID = unicodedata.normalize('NFKD', id).encode('ascii','ignore')
            UIDS = int(ID)
            TEST = getRecommendations(songs,UIDS)
            
            TempTest = []
            c = connection.cursor()
            for SID in TEST:
                temp = list(SID)
                c.execute("select SongName from songs where SongId=%s",[SID[1]])
                songName = c.fetchone()
                name= songName[0]
                name = unicodedata.normalize('NFKD', name).encode('ascii','ignore')
                tempTuple = (SID[0],name)
                TempTest.append(tempTuple)
                
            c=connection.cursor()
            try:
                # query="SELECT * from songs"
                # c.execute(query)
                # querysetSong=c.fetchall()

                # feedback=dict()
                # ratingset=dict()
                ncontext={
                               "SongList":TempTest,
                               # "feedback":feedback,
                               # "ratingset":ratingset,
                               # "querysetSong":querysetSong
                          }
                c.close()
                return render(request,"songs_list.html",ncontext)
            finally:
                 c.close()            
                                    
        else:
            #Select 6 songs with top most frequncies
            print 'else<=20'
            c = connection.cursor()
            c.execute("SELECT age,gender from login_user where id = %s",[id])
            ageGender = c.fetchone()
            age = ageGender[0]
            gender = ageGender[1]
            print gender
            print age
            
            c.execute("SELECT rating.SongId  FROM rating inner join login_user on login_user.id= rating.UserId  where login_user.age>=%s and login_user.age<=%s and login_user.gender=%s ORDER BY frequency DESC LIMIT 6",[age-10,age+10,gender])
            ids = c.fetchall()
            
            print ids
            print len(ids)
            if len(ids)<=0:
                # No user of given gender and age +- 10
                # So suggesting only on the basis of age +- 10
                c.execute("SELECT rating.SongId  FROM rating inner join login_user on login_user.id= rating.UserId  where login_user.age>=%s and login_user.age<=%s ORDER BY frequency DESC LIMIT 6",[age-10,age+10])
                ids = c.fetchall()
                print "after"
                print ids
                if len(ids)<=0:
                    # No user of given gender and age +- 10
                    # So suggesting top 6 songs on frequency basis
                    c.execute("SELECT rating.SongId  FROM rating  ORDER BY frequency DESC LIMIT 6")
                    ids = c.fetchall()

            #print ids[0][0]
            TempTest = []
            counter=0
            for IDS in ids:   
                c.execute("SELECT SongName FROM songs where SongId=%s",[ids[counter][0]])
                NAME = c.fetchone()
                NAME = unicodedata.normalize('NFKD', NAME[0]).encode('ascii','ignore')
                print NAME
                tempTuple = (counter,NAME)
                TempTest.append(tempTuple)
                counter += 1
            
            #print TempTest    
            # query="SELECT * from songs"
            # c.execute(query)
            # querysetSong=c.fetchall()
                
            # feedback=dict()
            # ratingset=dict()
            ncontext={
                        "SongList":TempTest,
                        # "feedback":feedback,
                        # "ratingset":ratingset,
                        # "querysetSong":querysetSong
                     }
            return render(request,"songs_list.html",ncontext)        
    else:
        return render(request,"User_detail.html",context)


# Returns a distance-based similarity score for person1 and person2
def sim_distance_pearson(prefs,person1,p2):
    # Get the list of mutually rated items
    si={}
    for item in prefs[person1]:
        if item in prefs[p2]: si[item]=1
    # Find the number of elements
    n=len(si)
    # if they are no ratings in common, return 0
    if n==0: return 0
    # Add up all the preferences
    sum1=sum([prefs[person1][it] for it in si])
    sum2=sum([prefs[p2][it] for it in si])
    # Sum up the squares
    sum1Sq=sum([pow(prefs[person1][it],2) for it in si])
    sum2Sq=sum([pow(prefs[p2][it],2) for it in si])
    # Sum up the products
    pSum=sum([prefs[person1][it]*prefs[p2][it] for it in si])
    # Calculate Pearson score
    num=pSum-(sum1*sum2/n)
    den=sqrt((sum1Sq-pow(sum1,2)/n)*(sum2Sq-pow(sum2,2)/n))
    if den==0: return 0
    r=num/den
    return r
    
def getRecommendations(prefs,person,similarity=sim_distance_pearson):
    totals={}
    simSums={}
    for other in prefs:
        # don't compare me to myself
        if other==person: continue
        sim=similarity(prefs,person,other)
        # ignore scores of zero or lower
        if sim<=0: continue
        for item in prefs[other]:
            # only score music items I haven't seen yet
            if item not in prefs[person] or prefs[person][item]==0:
                # Similarity * Score
                totals.setdefault(item,0)
                totals[item]+=prefs[other][item]*sim
                # Sum of similarities
                simSums.setdefault(item,0)
                simSums[item]+=sim
    # Create the normalized list
    rankings=[(total/simSums[item],item) for item,total in totals.items( )]
    # Return the sorted list
    rankings.sort()
    rankings.reverse( )
    return rankings

def User_update(request):
    return HttpResponse("<h1> Welcome to User home Update</h1>")

def User_delete(request, id=None):
    instance =get_object_or_404(User, id=id)
    instance.delete()
    #messages.success(request, "Successfully Deleted")
    return redirect("login:home")

def ContactUs(request):
    return render(request,"contactus.html",)
    
def About(request):
    return render(request,"about.html",)