from timetable.Timetable import Timetable

DATA_FILE = "data/172.csv"
timetable = Timetable.timetable_from_csv(DATA_FILE)

timetable.display_location_count_per_day()
