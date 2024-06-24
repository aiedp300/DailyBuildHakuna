from django.urls import path
from .views import *
from . import views
#from .views import booking_create_view, booking_success_view

urlpatterns = [
    path("",views.home,name="home"),
    path("home1", HomeView.as_view(), name='my_home_view'), 
    #path("test/<char",views.home_view(),name="mytest"),
    path("geocoding/<int:pk>", GeocodingView.as_view(), name='my_geocoding_view'), 
    path("distance", DistanceView.as_view(), name='my_distance_view'), 
    path("map", MapView.as_view(), name='my_map_view'), 
    path('venue/', views.location_list, name='location_list'),
    path('venue/<int:location_id>/', views.location_detail, name='location_detail'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('welcome/', views.welcome, name='welcome'),
    path('profile/', views.profile, name='profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('logout/', views.logout, name='logout'),
    path('create/', views.booking_create_view, name='booking_create'),
    path('success/', views.booking_success_view, name='booking_success'),
   

]