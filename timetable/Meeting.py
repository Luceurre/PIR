from datetime import datetime
from timetable.Location import Location


class Meeting:
    DATE_AND_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
    DATE_AND_TIME_BEGIN_KEY = 'deb_H'
    DATE_AND_TIME_END_KEY = 'fin_H'

    def __init__(self, date_and_time_begin: datetime, date_and_time_end, location: Location):
        self.date_and_time_begin = date_and_time_begin
        self.date_and_time_end = date_and_time_end

        self.location = location

    @staticmethod
    def get_meeting_from_raw(raw: dict, location: Location):
        date_begin_unparsed = raw[Meeting.DATE_AND_TIME_BEGIN_KEY]
        date_end_unparsed = raw[Meeting.DATE_AND_TIME_END_KEY]

        date_begin = datetime.strptime(date_begin_unparsed, Meeting.DATE_AND_TIME_FORMAT)
        date_end = datetime.strptime(date_end_unparsed, Meeting.DATE_AND_TIME_FORMAT)

        return Meeting(date_begin, date_end, location)