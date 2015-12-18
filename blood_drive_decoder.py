import urllib.parse
import urllib.request
import lxml.html
from blood_drive import BloodDrive
from hema_quebec import HemaQuebec

class BloodDriveDecoder:

	def __init__(self):
		self.blood_drives = []

	def get_blood_drives(self):
		post_values = HemaQuebec.POST_VALUES
		for i in range(HemaQuebec.WEEK_COUNT):
			post_values['selectedWeekIndex'] = str(i)
			payload = urllib.parse.urlencode(post_values)
			payload = payload.encode('utf-8')
			req = urllib.request.Request(HemaQuebec.URL_EN, payload)
			self.extract_blood_drives(self.get_html_tables(req))

	def get_html_tables(self, req):
		with urllib.request.urlopen(req) as response:
			page = response.read()
			doc = lxml.html.document_fromstring(page.decode('utf-8', 'ignore'))
			return doc.xpath(HemaQuebec.BLOOD_DRIVES_TABLES_XPATH)

	def extract_blood_drives(self, html_tables):
		for html_table in html_tables:
			date = html_table.xpath(HemaQuebec.DATE_XPATH)[0].text_content().strip()
			rows = html_table.xpath(HemaQuebec.ROW_XPATH)
			for data in rows:
				blood_drive = BloodDrive(date, data)
				self.blood_drives.append(blood_drive)
