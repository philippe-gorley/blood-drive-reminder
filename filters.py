import json
from distance_calc import get_distance

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

	def filter(self, *blood_drives):
		filtered_drives = []
		for blood_drive in blood_drives:
			if get_distance(self.from_addr, blood_drive.address) <= self.distance:
				filtered_drives.append(blood_drive)
		return filtered_drives

def get_filters(json_file):
	filters = []
	with open(json_file) as config_file:
		config = json.load(config_file)
	if 'filter_by' in config:
		config = config['filter_by']

	if 'city' in config and len(config['city'] > 0):
		for city in config['city']:
			filters.append(CityFilter(city))

	if 'distance' in config and 'address' in config:
		distance = abs(int(config['distance']))
		home_address = config['address']
		filters.append(DistanceFilter(distance, home_address))

	return filters
