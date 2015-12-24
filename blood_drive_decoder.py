import urllib.parse
import urllib.request
import lxml.html
import json
from blood_drive import BloodDrive

class BloodDriveDecoder:

    def __init__(self):
        with open('hema_quebec.json') as f:
            self.data = json.load(f)

    def get_blood_drives(self):
        blood_drives = []
        for post_values in self.data['posts']:
            payload = urllib.parse.urlencode(post_values)
            payload = payload.encode('utf-8')
            req = urllib.request.Request(self.data['url'], payload)
            drives_html = self.get_html_tables(req)
            week = self.extract_blood_drives(drives_html)
            blood_drives = blood_drives + week
        return blood_drives

    def get_html_tables(self, req):
        with urllib.request.urlopen(req) as response:
            page = response.read()
            doc = lxml.html.document_fromstring(page.decode('utf-8', 'ignore'))
            return doc.xpath(self.data['strings']['blood_drive_tables'])

    def extract_blood_drives(self, html_tables):
        blood_drives = []
        for html_table in html_tables:
            date = html_table.xpath(self.data['strings']['date'])
            date = date[0].text_content().strip()
            rows = html_table.xpath(self.data['strings']['row'])
            for row in rows:
                blood_drive = BloodDrive(date, row)
                blood_drives.append(blood_drive)
        return blood_drives
