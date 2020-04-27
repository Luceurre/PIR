import csv
import datetime

from timetable2.Timetable import date
from timetable2.Timetable import Timetable, Label, Meeting
from timetable2.tools import RED, GREEN, BLUE

# File formating
DATA_FILE = 'data/data_4.csv'
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
DATE_BEGIN_KEY = 'deb_H'
DATE_END_KEY = 'fin_H'
# On définit les couleurs au passage
labels = {'Home': Label('Home', RED), 'Second': Label('Second', GREEN), 'Other': Label('Other', BLUE)}

SELECTED_DEVICES = ['Device 64']
SELECT_ALL = True
SELECTED_DATE_FROM = date(2018, 1, 22)
SELECTED_DATE_TO = date(2018, 1, 30)
SELECT_ALL_DATE = True

header = None

timetables = {}

try:
    data_file = open('data/data_4.csv', newline='')
except:
    print("File not found!")
    exit()
else:
    data = csv.DictReader(data_file)
    dates = []

    header = data.fieldnames

    for raw in data:
        device = raw['device']
        # Plus lent comme ça mais permet de comparer plusieurs device facilement
        if device in SELECTED_DEVICES or SELECT_ALL:
            if device not in timetables.keys():
                timetables[device] = Timetable(device)
            date_begin_unparsed = raw['deb_H']
            date_end_unparsed = raw['fin_H']

            date_begin = datetime.datetime.strptime(date_begin_unparsed, DATE_FORMAT)
            date_end = datetime.datetime.strptime(date_end_unparsed, DATE_FORMAT)

            meeting = Meeting(date_begin, date_end, labels=[labels[raw['motif']]], loc_id=raw['ID_sejour_1km'])
            timetables[device].add_meeting(meeting)

    for device in timetables.keys():
        if SELECT_ALL_DATE:
            SELECTED_DATE_FROM = timetables[device].get_earliest_meeting_date()
            SELECTED_DATE_TO = timetables[device].get_latest_meeting_date()

        # timetables[device].print_range(SELECTED_DATE_FROM, SELECTED_DATE_TO)
        timetables[device].display_range(SELECTED_DATE_FROM, SELECTED_DATE_TO)

    data_file.close()
