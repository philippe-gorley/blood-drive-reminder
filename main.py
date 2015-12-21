from blood_drive_decoder import BloodDriveDecoder
import filters as f
from gcalendar import GCalendar

if __name__ == '__main__':
    blood_drives = BloodDriveDecoder().get_blood_drives()
    filters = f.get_filters('./config.json')
    filtered_drives = f.apply_filters(filters, blood_drives)
    #calendar = GCalendar()
    for drive in filtered_drives:
        print(drive.to_string())
    