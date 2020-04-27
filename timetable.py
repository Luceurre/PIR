import csv
import datetime
import random

import cairo
from numpy.matlib import rand

DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
data_file = open('data/data_4.csv', newline='')
data = csv.DictReader(data_file)

def random_color():
    return (random.random(), random.random(), random.random())
def get_data_by_device(data):
    data_by_device = {}
    for raw in data:
        if raw['device'] not in data_by_device.keys():
            data_by_device[raw['device']] = []
        data_by_device[raw['device']].append(raw)
    return data_by_device

def get_data_by_day(data_device):
    data_by_day = {}
    for data in data_device:
        if data['jour'] not in data_by_day.keys():
            data_by_day[data['jour']] = []
        data_by_day[data['jour']].append(data)

    return data_by_day

def draw_date(x, y, w, h, color, ctx):
    if y + h > 0.5:
        print("ay")
    pat = cairo.SolidPattern(*color)
    ctx.rectangle(x, y, w, h)
    ctx.set_source(pat)
    ctx.fill()

def draw_day(day, x, y, w, h, ctx, place_color):
    for meeting in day:
        datetimebegin = datetime.datetime.strptime(meeting['deb_H'], DATE_FORMAT)
        timebegin = datetimebegin.hour + datetimebegin.minute / 60

        reltime = timebegin / 24
        durtime = float(meeting['dur_min']) / 60.
        relduration = durtime / 24

        if meeting['ID_sejour_1km'] not in place_color.keys():
            place_color[meeting['ID_sejour_1km']] = random_color()
        draw_date(x, y + reltime * h, w, h * relduration, place_color[meeting['ID_sejour_1km']], ctx)

data_by_device = get_data_by_device(data)
data_by_day = get_data_by_day(data_by_device['Device 64'])

width = 1920
height = 1080

# Context to draw
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)
ctx.scale(width, height)
place_color = {}

for i in range(7):
    key = list(data_by_day.keys())[i]
    draw_day(data_by_day[key], i / 7, 0, 1, 0.5, ctx, place_color)

# surface.write_to_png("results/" + "timetable1" + ".png")  # Output to PNG

for i in range(7, 14):
    key = list(data_by_day.keys())[i]
    draw_day(data_by_day[key], (i - 7) / 7, 0.5, 1, 0.5, ctx, place_color)

surface.write_to_png("results/" + "timetable" + ".png")  # Output to PNG