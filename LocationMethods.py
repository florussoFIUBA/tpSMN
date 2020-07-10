import geocoder

def ReturnActualLocation():
    myLocation = geocoder.ip('me')
    return myLocation.latlng