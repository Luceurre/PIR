from datetime import date, timedelta
import random

# Renvoie une couleur aléatoire compatible avec l'affichage graphique souhaité
from time import time

RED = (255, 255, 0)
GREEN = (0, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

def random_color():
    color = (random.randint(0, 256), random.randint(0, 256), random.randint(0, 256))
    return color


def date_range(start: date, end: date):
    date_generated = [start + timedelta(days=x) for x in range(0, (end - start).days + 1)]

    return date_generated

def time_range():
    times = []
    for i in range(2):
        for j in range(9):
            times.append(str(i) + str(j) + 'h')

    for i in range(4):
        times.append('2' + str(i) + 'h')

    return times
random.seed(time())