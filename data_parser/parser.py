import string
import csv

DEVICE_ID_SPLITTER = ' '
LOCATION_ID_SPLITTER = '_S'


def parse_device_id(device_id: string):
    return device_id.split(' ')[1]


def parse_location_id(location_id: string):
    return location_id.split('_S')[1]


def parse(file_path: string):
    try:
        data_file = open(file_path, newline='')
    except FileNotFoundError:
        print("File not found!")
        exit()
    else:
        data = csv.DictReader(data_file)
        devices = {}
        header = data.fieldnames

        # On sépare les données par device et on parse les ids
        for raw in data:
            raw['device'] = parse_device_id(raw['device'])

            device = raw['device']
            if device not in devices.keys():
                devices[device] = []

            raw['ID_sejour_1km'] = parse_location_id(raw['ID_sejour_1km'])
            raw.pop('device')
            devices[device].append(raw.copy())

        data_file.close()

        header = list(header)
        header.remove('device')
        return header, devices


def write_data(file_path: string, data: list, header: list):
    with open(file_path, 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=header)

        writer.writeheader()
        writer.writerows(data)
