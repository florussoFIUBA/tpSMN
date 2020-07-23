import geocoder
from geopy.geocoders import Nominatim

def RetornarLocalizacionActual():
    myLocation = geocoder.ip('me')
    return myLocation.latlng

def RetornarLocalizacion():
    latLong = RetornarLocalizacionActual()
    geolocator = Nominatim(user_agent="tp2")
    location = geolocator.reverse(f"{latLong[0]}, {latLong[1]}")
    return location.address.split(',')[2]

'''
Recibe un string con la localidad, provincia, pais.
Retorna None si no encuentra la localidad. Para obtener las coordenadas
location.latitude y location.longitude
'''
def obtenerLatLongDeLocalidad(lugar):
    geolocator = Nominatim(user_agent="tp2")
    location = geolocator.geocode(lugar)
    
    return location