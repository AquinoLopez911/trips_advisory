from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt
import datetime



# Create your views here.
def login_register(request):
    return render(request, 'login.html')

def register(request):
    if request.POST:
        errors_from_Validator = User.objects.registration_validator(request.POST)
        if len(errors_from_Validator) > 0:
            for key, value in errors_from_Validator.items():
                messages.error(request, value)
            return redirect('/')
        else:
            hash1 = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())

            user = User.objects.create(name=request.POST['name'], alias=request.POST['username'], email=request.POST['email'].lower(), password=hash1.decode() )
            print(f"created user: {user}")

            request.session['id'] = user.id

            user = User.objects.get(id = request.session['id'])

    return redirect('/travels')

def login(request):
    login_errors = User.objects.login_validator(request.POST)
    if len(login_errors) > 0:
        for key, value in login_errors.items():
            messages.error(request, value)
        return redirect('/')   
    request.session['id'] = User.objects.filter(email = request.POST['email'].lower())[0].id
    request.session['name'] = User.objects.filter(email = request.POST['email'].lower())[0].name
    return redirect('/travels')



def show_all_trips(request):
    if 'id' not in request.session:
        return redirect('/')
    else:
        #get todays date
        # today = datetime.datetime.now()

        #get the loggid in user
        user = User.objects.get(id = request.session['id'])

        #get the trips that THIS user has planned
        user_trips = Trip.objects.filter(planner = user.id)

        #get the trips that THIS user has JOINED
        joined_trips = Trip.objects.filter(buddies = user.id)

        #DELETE TRIPS THAT HAVE ALREADY STARTED OR PASSED ?
        # #trips that started before today
        # expired_trips = Trip.objects.filter(start_date = today )

        # print(today)
        # print(expired_trips[0])

        # for trip in expired_trips:
        #     print("today" + today)
        #     print("start date: " + trip.start_date)
        #     if trip.start_date < today:
        #         trip.delete()

        #get all trips where THIS user IS NOT a BUDDY
        all_trips = Trip.objects.exclude(id__in = joined_trips)



        #in the html, when we display all_trips, we will exclude trips he is a planner of 

        context = {


            'logged_in_user' : user,
            'user_trips': user_trips,
            'all_trips' : all_trips,
            'user' : user,
            'joined_trips' : joined_trips
        }
        return render(request, 'travel_advisery.html', context) 

def add_trip(request ):
    if 'id' not in request.session:
        return redirect('/')
    return render(request, 'add_trip.html')


def create_trip(request):
    if 'id' not in request.session:
        return redirect('/')
    else:    
        print(request.POST)
        trip_errors = Trip.objects.trip_registration(request.POST)
        user = User.objects.get(id = request.session['id'])

        if len(trip_errors) > 0:
            for key, value in trip_errors.items():
                messages.error(request, value)
            return redirect('/add_trip')
        else:
            print("trip creaed succesfuly")
            Trip.objects.create(destination=request.POST['destination'], planner=user, start_date=request.POST['start_date'], end_date=request.POST['end_date'], plan=request.POST['plan'])
    
    return redirect("/travels")



def trip_info(request, number):
    if 'id' not in request.session:
        return redirect('/')
    else:    
        this_trip = Trip.objects.get(id=number)
        this_trip_buddies = this_trip.buddies.exclude(id = request.session['id'])

        
        all_trips = Trip.objects.all().order_by('created_at')

        context = {
            'this_trip' : this_trip,
            'this_trip_buddies' : this_trip_buddies,
            'all_trips' : all_trips,

        }
    return render(request, 'trip_info.html', context)





def join_trip(request, number):
    user = User.objects.get(id=request.session['id'])
    this_trip = Trip.objects.get(id=number)

    this_trip.buddies.add(user)

    user_trips = Trip.objects.filter(planner = user.id)
    joined_trips = Trip.objects.filter(buddies = user.id)
    all_trips = Trip.objects.all()

    context = {

            'logged_in_user' : user,
            'user_trips': user_trips,
            'all_trips' : all_trips,
            'user' : user,
            'joined_trips' : joined_trips
        }
    return redirect("/travels") 











def logout(request):
    request.session.clear()
    return redirect('/')