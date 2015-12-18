from geopy.geocoders import Nominatim
from geopy.distance import great_circle

def get_distance(from_addr, to_addr):
    def geocode(address):
        geolocator = Nominatim()
        loc = geolocator.geocode(address)
        return (loc.latitude, loc.longitude)
    from_loc = geocode(from_addr)
    to_loc = geocode(to_addr)
    distance = great_circle(from_loc, to_loc).kilometers
    return distance
