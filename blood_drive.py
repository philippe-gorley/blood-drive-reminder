import lxml.html
import re
import json
from datetime import datetime
from urllib.parse import urlparse, parse_qs

class BloodDrive:

    START_TIME = 0
    END_TIME = -1

    def __init__(self, date, data):
        hq_json = 'hema_quebec.json'
        with open(hq_json) as f:
            strings = json.load(f)['strings']
        start_hour = self.get_time(data, strings['time'], strings['time_regexp'], BloodDrive.START_TIME)
        end_hour = self.get_time(data, strings['time'], strings['time_regexp'], BloodDrive.END_TIME)
        self.start_time = self.parse_date(date, strings['date_format'], start_hour, strings['time_format'])
        self.end_time = self.parse_date(date, strings['date_format'], end_hour, strings['time_format'])
        self.city = self.get_content(data, strings['city'])
        self.ics_link = self.get_link(data, strings['calendar'])
        self.map_link = self.get_link(data, strings['map'])
        self.address = self.get_address()
        self.event_id = self.gen_id()

    def get_address(self):
        qs = urlparse(self.map_link).query
        addr = parse_qs(qs)['q'][0]
        return addr

    def get_content(self, xml, xpath):
        return xml.xpath(xpath)[0].text_content().strip()

    def get_time(self, xml, xpath, regexp, i):
        time = xml.xpath(xpath)[0].text_content()
        return re.findall(regexp, time)[i].strip()

    def get_link(self, xml, xpath):
        return xml.xpath(xpath)[0].get('href').strip()

    def gen_id(self):
        start = self.start_time.strftime('%Y%m%d')
        city = self.city.lower()
        identifier = start + city
        base32_enforce = '[^a-v0-9]'
        identifier, _ = re.subn(base32_enforce, '', identifier)
        return identifier

    def parse_date(self, date_string, date_format, time_string, time_format):
        dt = datetime.strptime(date_string, date_format)
        today = datetime.now()
        # if the blood drive is next year
        if today.month > dt.month:
            dt = dt.replace(year=today.year+1)
        else:
            dt = dt.replace(year=today.year)
        time = datetime.strptime(time_string, time_format)
        dt = dt.replace(hour=time.hour)
        return dt

    def to_string(self):
        return self.event_id
