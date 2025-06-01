from django import forms 
from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile
from .models import Booking
from django.contrib.admin.widgets import AdminDateWidget
from .models import ServicePurchase

#################  concept  ######################
class ServicePurchaseForm(forms.ModelForm):
    #start_date = forms.DateField(widget=AdminDateWidget())
    #end_date = forms.DateField(widget=AdminDateWidget())
   
    
    class Meta:
        model = ServicePurchase
        fields = ['product', 'start_date', 'end_date']
        widgets = {
        'start_date': forms.DateInput(attrs={'type': 'date'}),
        'end_date': forms.DateInput(attrs={'type': 'date'}),
    }
##################   end concept #################################
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['start_date', 'end_date','venue','unit','user']

        widgets = {
        'start_date': forms.DateInput(attrs={'type': 'date'}),
        'end_date': forms.DateInput(attrs={'type': 'date'}),
    }


modes = (
    ("driving", "driving"), 
    ("walking", "walking"),
    ("bicycling", "bicycling"),
    ("transit", "transit")
)

class DistanceForm(ModelForm): 
    from_location = forms.ModelChoiceField(label="Location from", required=True, queryset=Venue.objects.all())
    to_location = forms.ModelChoiceField(label="Location to", required=True, queryset=Venue.objects.all())
    mode = forms.ChoiceField(choices=modes, required=True)
    class Meta: 
        model = Distances
        exclude = ['created_at', 'edited_at', 'distance_km','duration_mins','duration_traffic_mins']

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['status', 'profile_picture']