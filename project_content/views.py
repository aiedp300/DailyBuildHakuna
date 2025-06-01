from django.views.generic import ListView
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
import googlemaps
from django.conf import settings
from .forms import *
from datetime import datetime
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from .forms import UserRegistrationForm , UserProfileForm
from .models import UserProfile
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from .forms import BookingForm
from .models import UnavailableDate
from django.contrib.auth import authenticate
from django.contrib.auth import authenticate, login
from django.utils import timezone
from .models import Product, Purchase, ServicePurchase
from .forms import ServicePurchaseForm
from django.contrib import messages

###############  concept ###################################
@login_required
def buy_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    today = timezone.now().date()
    
    # Check if the user has already bought this product today
    if Purchase.objects.filter(user=request.user, product=product, date=today).exists():
        messages.error(request, "You can only buy this product once a day.")
        return redirect('product_detail', product_id=product_id)

    # Otherwise, create a new purchase
    Purchase.objects.create(user=request.user, product=product)
    messages.success(request, "Product bought successfully.")
    return redirect('product_detail', product_id=product_id)

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})

# @login_required
# def buy_service(request):
#     if request.method == 'POST':
#         form = ServicePurchaseForm(request.POST)
#         if form.is_valid():
#             product = form.cleaned_data['product']
#             start_date = form.cleaned_data['start_date']
#             end_date = form.cleaned_data['end_date']
            
#             # Check for overlapping dates
#             overlapping_purchases = ServicePurchase.objects.filter(
#                 product=product,
#                 user=request.user,
#                 start_date__lt=end_date,
#                 end_date__gt=start_date
#             )
            
#             if overlapping_purchases.exists():
#                 messages.error(request, "You already have this product booked for overlapping dates.")
#             else:
#                 purchase = form.save(commit=False)
#                 purchase.user = request.user
#                 purchase.save()
#                 messages.success(request, "Service purchased successfully.")
#                 return redirect('service_purchases')
#     else:
#         form = ServicePurchaseForm()
    
#     return render(request, 'buy_service.html', {'form': form})
@login_required
def buy_service(request):
    purchases = ServicePurchase.objects.filter(user=request.user)
    if request.method == 'POST':
        form = ServicePurchaseForm(request.POST)
        if form.is_valid():
            product = form.cleaned_data['product']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            
            # Check for overlapping dates
            overlapping_purchases = ServicePurchase.objects.filter(
                product=product,
                user=request.user,
                start_date__lt=end_date,
                end_date__gt=start_date
            )
            
            if overlapping_purchases.exists():
                messages.error(request, "You already have this product booked for overlapping dates.")
            else:
                purchase = form.save(commit=False)
                purchase.user = request.user
                purchase.save()
                messages.success(request, "Service purchased successfully.")
                return redirect('service_purchases')
    else:
        form = ServicePurchaseForm()
    
    return render(request, 'buy_service.html', {'form': form, 'purchases': purchases})

@login_required
def service_purchases(request):
    purchases = ServicePurchase.objects.filter(user=request.user)
    return render(request, 'service_purchases.html', {'purchases': purchases})
############################## end conv=cept ##########################################
# def booking_create_view(request):
#     # Retrieve the username from the session
#     username = request.session.get('username')
#     return render(request, 'booking/booking_create.html', {'username': username})

# Create your views here.
def home(request):
    #return HttpResponse("hello world!")
    return render(request,"home.html")
#added to ensure only logins that exist may make a booking - and use their session id for user id

def booking_create_view(request,unit_affected):

    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
          
            check_unit_affected = get_object_or_404(UnavailableDate, unitAffected = unit_affected)
            # Check if any unavailable dates overlap with the booking
            #unavailable_dates = UnavailableDate.objects.filter(start_date__range =[start_date, end_date],unitAffected=check_unit_affected ).exists()
            #cannot unpack non-iterable Unit object
            #unavailable_unit = UnavailableDate.objects.filter(unit_affected)
            #also test for the unit number on the same dates 
            #####################################################  worked but only for dates and not unit also
            if UnavailableDate.objects.filter(start_date__range =[start_date, end_date],unitAffected=check_unit_affected ).exists():
                return render(request, 'booking/error.html', {'message': 'Selected dates are unavailable.'})
            else:
                form.save()
                return redirect('booking_success')
            
            
            # if unavailable_doubleBooking.exists():
            #     return render(request, 'booking/error.html', {'message': 'Selected dates are unavailable.'})
            # else:
            #     form.save()
            #     return redirect('booking_success')
    else:
        form = BookingForm()
    return render(request, 'booking/booking_create.html', {'form': form})

def booking_success_view(request):
    return render(request, 'booking/booking_success.html')
#from .forms import BookingForm
#from .models import UnavailableDate
#from .models import Booking
# def booking_create_view(request):
#     if request.method == 'POST':
#         form = BookingForm(request.POST)
#         if form.is_valid():
#             start_date = form.cleaned_data['start_date']
#             end_Date = form.cleaned_data['end_Date']
#             # Check if any unavailable dates overlap with the booking
#             unavailable_dates = UnavailableDate.objects.filter(date__range=[start_date, end_Date])
#             if unavailable_dates.exists():
#                 return render(request, 'bookings/error.html', {'message': 'Selected dates are unavailable.'})
#             else:
#                 form.save()
#                 return redirect('booking_success')
#     else:
#         form = BookingForm()
#     return render(request, 'bookings/booking_create.html', {'form': form})

# def booking_success_view(request):
#     return render(request, 'bookings/booking_success.html')

@login_required
def profile(request):
    return render(request, 'project_content/profile.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            UserProfile.objects.create(user=user)
            return redirect('welcome')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def welcome(request):
    user_profile = UserProfile.objects.get(user=request.user)
    return render(request, 'home.html', {'user_profile': user_profile})



def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('welcome')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

# views.py - In your login view


# def login_view(request):
#     # Your login logic here
#     username = request.POST['username']  # Assuming username is obtained from form
#     user = authenticate(request, username=username, password=request.POST['password'])
#     if user is not None:
#         login(request, user)
#         request.session['username'] = user.username  # Store username in session
#         return redirect('my_home_view')
#     else:
#         # Handle invalid login
#         pass


@login_required
def edit_profile(request):
    user_profile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=user_profile)
    return render(request, 'project_content/edit_profile.html', {'form': form})
def logout(request):
    auth_logout(request)
    return redirect('login')

class HomeView(ListView):
    template_name = "project_content/home1.html"
    context_object_name = 'mydata'
    model = Venue
    success_url = "/"
    
# def some_view(request):
#     # Retrieve the username from the session
#     username = request.session.get('username')
#     return render(request, 'some_template.html', {'username': username})    
    
def home_view(request):
    # Retrieve the username from the session
    username = request.session.get('username')
    return render(request, 'home1.html', {'username': username})




class MapView(View): 
    template_name = "project_content/map.html"

    def get(self,request): 
        key = settings.GOOGLE_API_KEY
        eligable_venue = Venue.objects.filter(place_id__isnull=False)
        venue = []

        for a in eligable_venue: 
            data = {
                'lat': float(a.lat), 
                'lng': float(a.lng), 
                'name': a.name
            }

            venue.append(data)


        context = {
            "key":key, 
            "venue": venue
        }

        return render(request, self.template_name, context)

class DistanceView(View):
    template_name = "project_content/distance.html"

    def get(self, request): 
        form = DistanceForm
        distances = Distances.objects.all()
        context = {
            'form':form,
            'distances':distances
        }

        return render(request, self.template_name, context)

    def post(self, request): 
        form = DistanceForm(request.POST)
        if form.is_valid(): 
            from_location = form.cleaned_data['from_location']
            from_location_info = Venue.objects.get(name=from_location)
            from_adress_string = str(from_location_info.adress)+", "+str(from_location_info.zipcode)+", "+str(from_location_info.city)+", "+str(from_location_info.country)

            to_location = form.cleaned_data['to_location']
            to_location_info = Venue.objects.get(name=to_location)
            to_adress_string = str(to_location_info.adress)+", "+str(to_location_info.zipcode)+", "+str(to_location_info.city)+", "+str(to_location_info.country)

            mode = form.cleaned_data['mode']
            now = datetime.now()

            gmaps = googlemaps.Client(key= settings.GOOGLE_API_KEY)
            calculate = gmaps.distance_matrix(
                    from_adress_string,
                    to_adress_string,
                    mode = mode,
                    departure_time = now
            )


            duration_seconds = calculate['rows'][0]['elements'][0]['duration']['value']
            duration_minutes = duration_seconds/60

            distance_meters = calculate['rows'][0]['elements'][0]['distance']['value']
            distance_kilometers = distance_meters/1000

            if 'duration_in_traffic' in calculate['rows'][0]['elements'][0]: 
                duration_in_traffic_seconds = calculate['rows'][0]['elements'][0]['duration_in_traffic']['value']
                duration_in_traffic_minutes = duration_in_traffic_seconds/60
            else: 
                duration_in_traffic_minutes = None

            
            obj = Distances(
                from_location = Venue.objects.get(name=from_location),
                to_location = Venue.objects.get(name=to_location),
                mode = mode,
                distance_km = distance_kilometers,
                duration_mins = duration_minutes,
                duration_traffic_mins = duration_in_traffic_minutes
            )

            obj.save()

        else: 
            print(form.errors)
        
        return redirect('my_distance_view')


class GeocodingView(View):
    template_name = "project_content/geocoding.html"

    def get(self,request,pk): 
        location = Venue.objects.get(pk=pk)

        if location.lng and location.lat and location.place_id != None: 
            lat = location.lat
            lng = location.lng
            place_id = location.place_id
            label = "from my database"

        elif location.adress and location.country and location.zipcode and location.city != None: 
            adress_string = str(location.adress)+", "+str(location.zipcode)+", "+str(location.city)+", "+str(location.country)

            gmaps = googlemaps.Client(key = settings.GOOGLE_API_KEY)
            result = gmaps.geocode(adress_string)[0]
            
            lat = result.get('geometry', {}).get('location', {}).get('lat', None)
            lng = result.get('geometry', {}).get('location', {}).get('lng', None)
            place_id = result.get('place_id', {})
            label = "from my api call"

            location.lat = lat
            location.lng = lng
            location.place_id = place_id
            location.save()

        else: 
            result = ""
            lat = ""
            lng = ""
            place_id = ""
            label = "no call made"

        context = {
            'location':location,
            'lat':lat, 
            'lng':lng, 
            'place_id':place_id, 
            'label': label
        }
        
        return render(request, self.template_name, context)

#For PlusCode - end lin e162
from .models import Location

def location_detail(request, location_id):
    location = Location.objects.get(pk=location_id)
    return render(request, 'location_detail.html', {'location': location})

def location_list(request):
    venue = Location.objects.all()
    return render(request, 'location_list.html', {'venue': venue})

