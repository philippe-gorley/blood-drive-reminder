class HemaQuebec:

    URL_EN = 'http://www.hema-quebec.qc.ca/index.en.html'

    POST_VALUES = {
        'postalCode' : 'CODE POSTAL',
        'method:searchBloodDrives' : '',
        'selectedWeekIndex' : '0',
        'pcLatitude' : '0',
        'pcLongitude' : '0',
        'idViewToDisplay' : 'map-list',
        'cleanSessionFromBloodDrives' : 'true'
    }

    BLOOD_DRIVES_TABLES_XPATH = '//table[@class="don-table"]'
    DATE_XPATH = 'thead'
    ROW_XPATH = 'tbody/tr'
    CITY_XPATH = 'td[@class="address"]/div/p[1]'
    HOURS_XPATH = 'td/p[@class="hours-detail"]'
    ADDRESS_XPATH = 'td[@class="address"]/div/p[2]'
    CALENDAR_LINK_XPATH = 'td/p[@class="calendar"]/a'
    MAP_LINK_XPATH = 'td[@class="address"]/div/a'

    DATE_EN_FORMAT = '%A, %B %d' 
    TIME_EN_FORMAT = '%I:%M %p'
    DATE_EN_REGEXP = '\w+, (?P<month>\w+) (?P<day>[0-9]{1,2})'
    HOURS_EN_REGEXP = '[0-9]{1,2}:[0-9]{2}\s[AP]M'

    WEEK_COUNT = 3
