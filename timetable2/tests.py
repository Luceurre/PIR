import csv
from datetime import datetime, date
import timetable2.tools

SELECTED_DATE_FROM = date(2018, 1, 22)
SELECTED_DATE_TO = date(2018, 1, 25)

test = timetable2.tools.date_range(SELECTED_DATE_FROM, SELECTED_DATE_TO)
print(test[0])