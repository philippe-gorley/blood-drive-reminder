import lxml.html
import re
from datetime import datetime
from hema_quebec import HemaQuebec
from urllib.parse import urlparse, parse_qs

class BloodDrive:

    START_TIME = 0
    END_TIME = -1

    def __init__(self, date, data):
        start_hour = self.get_hour(data, BloodDrive.START_TIME)
        end_hour = self.get_hour(data, BloodDrive.END_TIME)
        self.start_time = self.parse_date(date, start_hour)
        self.end_time = self.parse_date(date, end_hour)
        self.city = self.get_city(data)
        self.address = self.get_address(data)
        self.ics_link = self.get_ics_link(data)
        self.map_link = self.get_map_link(data)
        self.address = self.parse_address_from_link()
        self.event_id = self.gen_id()

    def get_city(self, data):
        return data.xpath(HemaQuebec.CITY_XPATH)[0].text_content().strip()

    def get_hour(self, data, i):
        hours = data.xpath(HemaQuebec.HOURS_XPATH)[0].text_content()
        return re.findall(HemaQuebec.HOURS_EN_REGEXP, hours)[i].strip()

    def get_address(self, data):
        return data.xpath(HemaQuebec.ADDRESS_XPATH)[0].text_content().strip()

    def get_ics_link(self, data):
        return data.xpath(HemaQuebec.CALENDAR_LINK_XPATH)[0].get('href').strip()

    def get_map_link(self, data):
        return data.xpath(HemaQuebec.MAP_LINK_XPATH)[0].get('href').strip()

    def gen_id(self):
        date_string = self.start_time.strftime('%Y%m%d')
        identifier = 'bd' + date_string
        place_name = self.address[0:self.address.index(',')]
        identifier += place_name
        identifier = re.sub('\W+', '', identifier)
        return identifier.lower()

    def parse_date(self, date_string, time_string):
        dt = datetime.strptime(date_string, HemaQuebec.DATE_EN_FORMAT)
        today = datetime.now()
        # if the blood drive is next year
        if today.month > dt.month:
            dt = dt.replace(year=today.year+1)
        else:
            dt = dt.replace(year=today.year)
        time = datetime.strptime(time_string, HemaQuebec.TIME_EN_FORMAT)
        dt = dt.replace(hour=time.hour)
        return dt

    def parse_address_from_link(self):
        # https://maps.google.ca/maps?q=9370%2c+boul.+Leduc+suite+30%2cBrossard%2cQu%c3%a9bec%2cJ4Y+0B3&z=15
        qs = urlparse(self.map_link).query
        addr = parse_qs(qs)['q'][0]
        return addr

    def to_string(self):
        s = str(self.start_time) + ' to ' + str(self.end_time) + '\n'
        s += self.city + ' : ' + self.address + '\n'
        #s += self.ics_link + '\n' + self.map_link + '\n'
        return s
