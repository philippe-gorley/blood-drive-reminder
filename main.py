from blood_drive_decoder import BloodDriveDecoder
from filters import CityFilter

if __name__ == '__main__':
	cf = CityFilter('Hull')
	decoder = BloodDriveDecoder()
	decoder.get_blood_drives()
	drives = cf.filter(*decoder.blood_drives)
	for drive in drives:
		print(drive.to_string())
