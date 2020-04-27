import timetable2.tools
import cairo
from datetime import datetime, date


class Label:
    def __init__(self, name, color=None):
        self.name = name
        if color is None:
            self.color = timetable2.tools.random_color()
        else:
            self.color = color


class Meeting:
    def __init__(self, date_begin: datetime, date_end: datetime, labels=None, title=""):
        if labels is None:
            labels = []
        self.labels = labels
        self.date_begin = date_begin
        self.date_end = date_end
        self.title = title

    def __str__(self):
        tostr = "("
        for label in self.labels:
            tostr += ' '
            tostr += label.name
        tostr += " ) "
        if self.title != '':
            tostr += self.title + ' '
        tostr += str(self.date_begin.time())
        tostr += ' --> '
        tostr += str(self.date_end.time())

        return tostr

    def get_duration_in_hour(self):
        date_dif = self.date_end - self.date_begin

        return date_dif.total_seconds() / 60 / 60

class Timetable:
    def __init__(self, name):
        self.name = name
        self.meetings = []

    # TODO : vérifier si il y a conflit de meeting
    def add_meeting(self, meeting):
        self.meetings.append(meeting)

    def remove_meeting_by_id(self, id):
        self.meetings.pop(id)

    def get_meeting_at(self, requested_date: date):
        requested_meetings = []
        for meeting in self.meetings:
            if meeting.date_begin.date() == requested_date or meeting.date_end.date() == requested_date:
                requested_meetings.append(meeting)

        return requested_meetings

    def get_meeting_range(self, from_date: date, to_date: date):
        requested_meetings = []
        for meeting in self.meetings:
            if meeting.date_begin.date() >= from_date or meeting.date_end.date() <= to_date:
                requested_meetings.append(meeting)

        return requested_meetings

    def print_day(self, requested_date):
        meetings = self.get_meeting_at(requested_date)
        for meeting in meetings:
            print(meeting)

    def print_range(self, from_date, to_date):
        meetings = self.get_meeting_range(from_date, to_date)
        for meeting in meetings:
            print(meeting)

    # TODO : Choose which color to display when multiple labels
    # TODO : Add meeting label, title, etc..
    def display_meeting(self, meeting, ctx, x, y, w, h, dp_label=False):


        pat = cairo.SolidPattern(*meeting.labels[0].color)
        ctx.rectangle(x, y, w, h)
        ctx.set_source(pat)
        ctx.fill()

        if (dp_label):
            ctx.set_source_rgb(0, 0, 0)
            ctx.set_font_size(0.03)
            ctx.select_font_face("Arial",
                                 cairo.FONT_SLANT_NORMAL,
                                 cairo.FONT_WEIGHT_NORMAL)
            ctx.move_to(x + w * 0.2, y + h * 0.5)
            ctx.show_text(meeting.labels[0].name)

    # TODO : Check for meetings conflict
    # TODO : Add date label
    def display_day(self, requested_date: date, ctx, x, y, w, h, dp_day=True, day_height=0.05):
        if dp_day:
            pat = cairo.SolidPattern(*timetable2.tools.WHITE)
            ctx.rectangle(x, y, w, day_height)
            ctx.set_source(pat)
            ctx.fill()

            day = requested_date.strftime('%a')
            ctx.set_source_rgb(0, 0, 0)
            ctx.set_font_size(0.02)
            ctx.select_font_face("Arial",
                                     cairo.FONT_SLANT_NORMAL,
                                     cairo.FONT_WEIGHT_NORMAL)
            ctx.move_to(x + 0.2 * w, y + 0.5 * day_height)
            ctx.show_text(day)

            return self.display_day(requested_date, ctx, x, y + day_height, w, h - day_height, False)

        meetings = self.get_meeting_at(requested_date)

        nb_meetings = len(meetings)
        if nb_meetings > 0:
            w_meeting = w
            h_meeting = h / nb_meetings

            # TODO : What you did is stupid. Change that.
            for index, meeting in enumerate(meetings):
                date_begin = meeting.date_begin
                begin = meeting.date_begin.hour + meeting.date_begin.minute / 60
                h_meeting = meeting.get_duration_in_hour() / 24

                yloc = y + (begin / 24) * h
                xloc = x

                self.display_meeting(meeting, ctx, xloc, yloc, w_meeting, h * h_meeting)
        else:
            pat = cairo.SolidPattern(*timetable2.tools.BLACK)
            ctx.rectangle(x, y, w, h)
            ctx.set_source(pat)
            ctx.fill()

    # TODO : Add timestamp for the line
    def display_line(self, dates, ctx, x, y, w, h, timestamp=True, timestamp_width=0.1):
        if timestamp:

            pat = cairo.SolidPattern(*timetable2.tools.WHITE)
            ctx.rectangle(x, y, timestamp_width, h)
            ctx.set_source(pat)
            ctx.fill()

            h -= 0.05 # C'est sale Pierre, pas bien
            times = timetable2.tools.time_range()
            nb_times = len(times)
            w_time = timestamp_width
            h_time = h / nb_times
            for index, time in enumerate(times):
                xloc = x
                yloc = y + index * h_time

                ctx.set_source_rgb(0, 0, 0)
                ctx.set_font_size(0.017)
                ctx.select_font_face("Arial",
                                     cairo.FONT_SLANT_NORMAL,
                                     cairo.FONT_WEIGHT_NORMAL)
                ctx.move_to(xloc + 0.2 * w_time, yloc + 0.7 * h_time + 0.05)
                ctx.show_text(time)

            h += 0.05
            return self.display_line(dates, ctx, x + w_time, y, w - w_time, h, False)

        nb_dates = len(dates)
        w_day = w
        if nb_dates > 0:
            w_day = w / nb_dates
        h_day = h

        for index, requested_date in enumerate(dates):
            xloc = x + w_day * index
            yloc = y

            self.display_day(requested_date, ctx, xloc, yloc, w_day, h_day)

    def display_range(self, from_date, to_date, dp_mode='auto', day_per_line=7):
        if dp_mode == 'auto':
            width, height = 1000, 900
        else:
            width, height = dp_mode

        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        ctx = cairo.Context(surface)
        ctx.scale(width, height)

        dates = timetable2.tools.date_range(from_date, to_date)
        nb_dates = len(dates)
        nb_lines = nb_dates // day_per_line
        h_line = 1 / nb_lines
        w_line = 1

        for i in range(nb_lines):
            xloc = 0
            yloc = i * h_line

            self.display_line(dates[i * day_per_line: (i + 1) * day_per_line], ctx, xloc, yloc, w_line, h_line)

        surface.write_to_png("results/" + str(self) + ".png")  # Output to PNG

    def get_earliest_meeting_date(self):
        earliest_date = self.meetings[0].date_begin
        for meeting in self.meetings:
            if meeting.date_begin < earliest_date:
                earliest_date = meeting.date_begin

        return earliest_date.date()

    def get_latest_meeting_date(self):
        latest_date = self.meetings[0].date_begin
        for meeting in self.meetings:
            if meeting.date_begin > latest_date:
                latest_date = meeting.date_begin

        return latest_date.date()

    def __str__(self):
        return self.name + "_timetable"
