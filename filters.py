import json
from distance_calc import Geocoder

class CityFilter:

    def __init__(self, city_name):
        self.city = city_name

    def filter(self, *blood_drives):
        filtered_drives = []
        for blood_drive in blood_drives:
            if blood_drive.city == self.city:
                filtered_drives.append(blood_drive)
        return filtered_drives

class DistanceFilter:

    def __init__(self, max_distance, from_addr):
        self.distance = max_distance
        self.from_addr = from_addr
        self.geocoder = Geocoder()

    def filter(self, *blood_drives):
        filtered_drives = []
        for blood_drive in blood_drives:
            dist = self.geocoder.get_distance(self.from_addr, blood_drive.address)
            if dist <= self.distance:
                filtered_drives.append(blood_drive)
        self.geocoder.save_cache()
        return filtered_drives

def get_filters(json_file):
    filters = []
    with open(json_file) as config_file:
        config = json.load(config_file)
        
    if 'filter_by' in config:
        filter_by = config['filter_by']

        if 'city' in filter_by and len(filter_by['city']) > 0:
            for city in filter_by['city']:
                filters.append(CityFilter(city))

        if 'distance' in filter_by and 'address' in config:
            distance = abs(int(filter_by['distance']))
            home_address = config['address']
            filters.append(DistanceFilter(distance, home_address))
    
    return filters

def apply_filters(filters, blood_drives):
    filtered_drives = {}
    for f in filters:
        for drive in f.filter(*blood_drives):
            filtered_drives[drive.event_id] = drive
    print('There are {} drives left'.format(len(filtered_drives)))
    return filtered_drives.values()
