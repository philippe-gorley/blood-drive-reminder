import lxml.html
import re
import json
from datetime import datetime
from urllib.parse import urlparse, parse_qs

class BloodDrive:

    START_TIME = 0
    END_TIME = -1

    def __init__(self, date, html):
        hq_json = 'hema_quebec.json'
        with open(hq_json) as f:
            strings = json.load(f)['strings']
        start_hour = self.get_time(html, strings['time'], strings['time_regexp'], BloodDrive.START_TIME)
        end_hour = self.get_time(html, strings['time'], strings['time_regexp'], BloodDrive.END_TIME)
        self.start_time = self.parse_date(date, strings['date_format'], start_hour, strings['time_format'])
        self.end_time = self.parse_date(date, strings['date_format'], end_hour, strings['time_format'])
        self.city = self.get_content(html, strings['city'])
        self.ics_link = self.get_link(html, strings['calendar'])
        self.map_link = self.get_link(html, strings['map'])
        self.by_appointment = self.get_appointment_only(html, strings['by_appointment'])
        self.address = self.get_address()
        self.event_id = self.gen_id()

    def get_address(self):
        # the address given in the html is incomplete, so parse it from the gmaps link
        qs = urlparse(self.map_link).query
        addr = parse_qs(qs)['q'][0]
        return addr

    def get_content(self, html, xpath):
        return html.xpath(xpath)[0].text_content().strip()

    def get_time(self, html, xpath, regexp, i):
        time = html.xpath(xpath)[0].text_content()
        return re.findall(regexp, time)[i].strip()

    def get_link(self, html, xpath):
        return html.xpath(xpath)[0].get('href').strip()

    def get_appointment_only(self, html, xpath):
        return len(html.xpath(xpath)) == 0

    def gen_id(self):
        # google calendar event ids can only contain a to v and 0-9
        start = self.start_time.strftime('%Y%m%d%H')
        city = self.city.lower()
        identifier = start + city
        base32_enforce = '[^a-v0-9]'
        identifier, _ = re.subn(base32_enforce, '', identifier)
        return identifier

    def parse_date(self, date_string, date_format, time_string, time_format):
        dt = datetime.strptime(date_string, date_format)
        today = datetime.now()
        # if it is December, but the event is in January
        if today.month > dt.month:
            dt = dt.replace(year=today.year+1)
        else:
            dt = dt.replace(year=today.year)
        time = datetime.strptime(time_string, time_format)
        dt = dt.replace(hour=time.hour)
        return dt
