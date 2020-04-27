import string


class Location:
    locations = []
    LABEL_KEY = 'motif'
    LATITUDE_KEY = 'latitude'
    LONGITUDE_KEY = 'longitude'
    LOCATION_ID_KEY = 'ID_sejour_1km'

    def __init__(self, location_id: int, label: string, latitude: float, longitude: float):
        self.location_id = location_id
        self.label = label
        self.latitude = latitude
        self.longitude = longitude

    @staticmethod
    def get_location(location_id: int, label: string, latitude: float, longitude: float):
        for location in Location.locations:
            if location.location_id == location_id:
                return location

        Location.locations.append(Location(location_id, label, latitude, longitude))
        return Location.locations[-1]

    @staticmethod
    def get_location_from_raw(raw: dict):
        location_id = int(raw[Location.LOCATION_ID_KEY])
        location_label = raw[Location.LABEL_KEY]
        location_latitude = float(raw[Location.LATITUDE_KEY])
        location_longitude = float(raw[Location.LONGITUDE_KEY])

        return Location.get_location(location_id, location_label, location_latitude, location_longitude)
