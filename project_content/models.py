from django.db import models
from .utils import geocode_plus_code
from django.contrib.auth.models import User
from location_field.models.plain import PlainLocationField
from django.utils import timezone
# import random num generatot like numpy
####################### testing concept  #######################################
class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f'{self.user.username} - {self.product.name} on {self.date}'


class ServicePurchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f'{self.user.username} - {self.product.name} from {self.start_date} to {self.end_date}'
    

    
###########################  end test concept  #######################################



class Venue(models.Model):
    club = models.CharField(max_length=500,blank=True, null=True)
    name = models.CharField(max_length=500,blank=True, null=True)
    zipcode = models.CharField(max_length=200,blank=True, null=True)
    city = models.CharField(max_length=200,blank=True, null=True)
    country = models.CharField(max_length=200,blank=True, null=True)
    adress = models.CharField(max_length=200,blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    edited_at = models.DateTimeField(auto_now=True)

    lat = models.CharField(max_length=200,blank=True, null=True)
    lng = models.CharField(max_length=200,blank=True, null=True)
    place_id = models.CharField(max_length=200,blank=True, null=True)

    def __str__(self):
        return self.name
    
class UnitSite(models.Model):
    #lookup value from other table ( first col aka primary key-ish)
    venue=models.ForeignKey(Venue,on_delete=models.CASCADE)
    UnitSite_Venue  =  models.CharField(max_length=500, blank=True, null=True) 
    local_name = models.CharField(max_length=100)
    TarrifPerPeron_Low_Season = models.FloatField(default=0.0)
    TarrifPerPeron_Mid_Season = models.FloatField(default=0.0)
    TarrifPerPeron_High_Season = models.FloatField(default=0.0)
    
    def save(self, *args, **kwargs):
        # Automatically populate author_name field with the name of the author
        if self.venue:
            self.UnitSite_Venue = self.venue.name
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.UnitSite_Venue +' site  ' + self.local_name
# fk lookup to UnitSite_Venue and stored in column VenueSiteNoBooked
#fk lookup to Unit and stored in colun unitBooked 
class Event(models.Model):
    name = models.CharField(max_length=100)
    FromDate = models.DateField()
    ToDate = models.DateField()
    


# concat VenueSiteNoUnitFromDate
    def __str__(self):
        return self.name  
class Unit(models.Model):
    RegistrationNo = models.CharField(max_length=50 ,  blank=True, null=True)
    YearModel = models.CharField(max_length=100, blank=True, null=True)
    Max_Pax= models.IntegerField()
    #use lookup to populate
    venue=models.ForeignKey(Venue,on_delete=models.CASCADE,max_length=500,blank=True, null=True)
    AvailableVenue = models.CharField(max_length=500 ,  blank=True, null=True)
    def save(self, *args, **kwargs):
        if self.venue:
            self.AvailableVenue = self.venue.name
        super().save(*args, **kwargs)
    def __str__(self):
        return self.RegistrationNo + '  ' + self.YearModel
class UnitImage(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    #must be a collection of pictures as per prescribe policy and quality set out by service
#in subfolder labled registration and an index number of the number of pictures
    image = models.ImageField(upload_to='unit_images/')
    def __str__(self):
        return self.unit.RegistrationNo + '  '
# class UnavailableDate(models.Model):
#     date = models.DateField(blank=True, null=True)

# class Booking(models.Model):
#     start_date = models.DateField(blank=True, null=True)
#     end_date = models.DateField(blank=True, null=True)
class UnavailableDate(models.Model):
    #for which unit are there dates unavailable 
    unitUnavailabe=models.ForeignKey(Unit,on_delete=models.CASCADE,blank=True, null=True)
    unitAffected = models.CharField(max_length=500 ,  blank=True, null=True)
    start_date = models.DateField( blank=True, null=True)   
    end_Date = models.DateField( blank=True, null=True)
    def save(self, *args, **kwargs):
        # Automatically populate author_name field with the name of the author
        if self.unitUnavailabe:
            self.unitAffected = self.unitUnavailabe
        super().save(*args, **kwargs)
        
    def concatenated_string(self):
        return f"{self.unitAffected } - {self.start_date.strftime('%Y-%m-%d')}"
    def __str__(self):
        return   self.concatenated_string() #self.unitUnavailabe #unitAffected #+ '  from  ' #+  self.fromDate.strftime('%Y-%m-%d')
#             # which unit and which unitsite from which venue
class Booking(models.Model):
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)  
    venue=models.ForeignKey(Venue,on_delete=models.CASCADE,max_length=500,blank=True, null=True)
    BookingVenue = models.CharField(max_length=500 ,  blank=True, null=True) 
    unit=models.ForeignKey(Unit,on_delete=models.CASCADE,blank=True, null=True)
    BookingUnit = models.CharField(max_length=500 ,  blank=True, null=True)
    #fk for Venue , unit and UserProfile
    user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True)
    BookingUser= models.CharField(max_length=500 ,  blank=True, null=True)
    def concatenated_string(self):
        return f"{self.user} - {self.start_date.strftime('%Y-%m-%d')}"
    def __str__(self):
        return   self.concatenated_string()
    def save(self, *args, **kwargs):
        # Automatically populate author_name field with the name of the author
        if self.venue:
            self.BookingVenue = self.venue
        if self.user:
            self.BookingUser = self.user
        super().save(*args, **kwargs)  
    
class Distances (models.Model): 
    from_location = models.ForeignKey(Venue, related_name = 'from_location', on_delete=models.CASCADE)
    to_location = models.ForeignKey(Venue, related_name = 'to_location', on_delete=models.CASCADE)
    mode = models.CharField(max_length=200, blank=True, null=True)
    distance_km = models.DecimalField(max_digits=10, decimal_places=2)
    duration_mins = models.DecimalField(max_digits=10, decimal_places=2)
    duration_traffic_mins = models.DecimalField(max_digits=10, decimal_places=2,blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    edited_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id
#Plus Code example model
class Location(models.Model):
    plus_code = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100,blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.latitude or not self.longitude:
            self.latitude, self.longitude = geocode_plus_code(self.plus_code)
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.name
        
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=100, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)
    def __str__(self):
        return self.user.username
    


