import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILE = os.path.join(BASE_DIR, "cars.json")


def read_cars():
    with open(FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def write_cars(cars):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(cars, f, indent=2)


def norm_regnr(regnr):
    return regnr.replace(" ", "").upper().strip()