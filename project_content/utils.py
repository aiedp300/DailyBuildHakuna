# utils.py

import googlemaps
from django.conf import settings

def geocode_plus_code(plus_code):
    gmaps = googlemaps.Client(key=settings.GOOGLE_API_KEY)
    result = gmaps.geocode(plus_code)

    if result:
        location = result[0]['geometry']['location']
        latitude = location['lat']
        longitude = location['lng']
        return latitude, longitude
    else:
        return None, None
