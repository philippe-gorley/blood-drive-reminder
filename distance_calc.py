from geopy.geocoders import GoogleV3
from geopy.distance import great_circle
import pickle
import os.path
import time

class Geocoder:

    def __init__(self):
        self._cache_file = 'geocache'
        self._cache = {}
        self.load_cache()
        self.geocoder = GoogleV3()

    def get_distance(self, from_addr, to_addr):
        from_loc = self.geocode(from_addr)
        to_loc = self.geocode(to_addr)
        distance = great_circle(from_loc, to_loc).kilometers
        return distance

    def geocode(self, address):
        if address in self._cache:
            loc = self._cache[address]
        else:
            time.sleep(0.5)  # don't spam the geocoding service
            loc = self.geocoder.geocode(address)
            self._cache[address] = loc
        return (loc.latitude, loc.longitude)

    def save_cache(self):
        with open(self._cache_file, 'wb') as f:
            pickle.dump(self._cache, f)

    def load_cache(self):
        if os.path.isfile(self._cache_file):
            with open(self._cache_file, 'rb') as f:
                self._cache = pickle.load(f)
