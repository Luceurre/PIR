import string
from timetable.Meeting import Meeting
from timetable.Location import Location
import numpy as np
import matplotlib.pyplot as plt
import csv
import datetime


class Timetable:
    def __init__(self, title: string):
        self.title = title
        # List of meetings
        self.meetings = []
        self.first_meeting_date_and_time = None
        self.last_meeting_date_and_time = None

        self.locations_id = []
        self.locations_id_by_date = {}

    def add_meeting(self, meeting: Meeting):
        # We always update the bound dates of the timetable
        if self.first_meeting_date_and_time is not None:
            if self.first_meeting_date_and_time > meeting.date_and_time_begin:
                self.first_meeting_date_and_time = meeting.date_and_time_begin

            if self.last_meeting_date_and_time < meeting.date_and_time_end:
                self.last_meeting_date_and_time = meeting.date_and_time_end
        else:
            self.first_meeting_date_and_time = meeting.date_and_time_begin
            self.last_meeting_date_and_time = meeting.date_and_time_end

        # On ajoute le compte du nombre de location par jour
        if meeting.location.location_id not in self.locations_id:
            self.locations_id.append(meeting.location.location_id)
        if meeting.date_and_time_end.date() not in self.locations_id_by_date.keys():
            self.locations_id_by_date[meeting.date_and_time_begin.date()] = []
        if meeting.location.location_id not in self.locations_id_by_date[meeting.date_and_time_begin.date()]:
            self.locations_id_by_date[meeting.date_and_time_begin.date()].append(meeting.location.location_id)

        self.meetings.append(meeting)

    def display_location_count_per_day(self):
        day_count = np.arange(0, (self.last_meeting_date_and_time - self.first_meeting_date_and_time).days + 1 % 2)
        location_count = np.zeros(len(day_count))
        location_mean = 0
        day_label = []

        for index, key in enumerate(self.locations_id_by_date):
            location_count[index] = len(self.locations_id_by_date[key])
            location_mean += len(self.locations_id_by_date[key])
            day_label.append(key.strftime('%a'))

        location_mean /= len(day_count)
        fig, ax = plt.subplots()
        ax.plot(day_count, location_count)
        plt.scatter(day_count, np.ones(len(day_count)) * location_mean, color="Orange")
        for i in range(len(day_label)):
            ax.annotate(day_label[i], (i, location_count[i]))
        fig.show()

    @staticmethod
    def timetable_from_csv(file_path: string):
        name = file_path.split('/')[-1].split('.')[0]
        timetable = Timetable(name)

        with open(file_path, newline='') as csv_file:
            reader = csv.DictReader(csv_file)
            for raw in reader:
                location = Location.get_location_from_raw(raw)
                meeting = Meeting.get_meeting_from_raw(raw, location)
                timetable.add_meeting(meeting)

        return timetable
