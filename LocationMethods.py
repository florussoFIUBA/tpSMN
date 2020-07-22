import geocoder
from geopy.geocoders import Nominatim

def ReturnActualLocation():
    myLocation = geocoder.ip('me')
    return myLocation.latlng

def ReturnAddress():
    #RETURNS CURRENT CITY
    latLong = ReturnActualLocation()
    geolocator = Nominatim(user_agent="tp2")
    location = geolocator.reverse(f"{latLong[0]}, {latLong[1]}")
    return location.address.split(',')[4]

