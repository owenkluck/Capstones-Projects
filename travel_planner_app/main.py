import math

from kivy.app import App
from kivy.modules import inspector
from kivy.core.window import Window
from travel_planner_app.database import Database
from travel_planner_app.rest import RESTConnection
from api_key import API_KEY
from database import Airport, City, Venue
from kivy.logger import Logger
from json import dumps
import csv


class TravelPlannerApp(App):
    def __init__(self, authority='localhost', port=33060, database='database', username='root', password='cse1208',
                 port_api=443, api_key=API_KEY, **kwargs):
        super(TravelPlannerApp, self).__init__(**kwargs)
        url = construct_mysql_url(authority, port, database, username, password)
        self.database = Database(url)
        self.session = self.database.create_session()
        self.connection = RESTConnection('api.openweathermap.org', port_api, '/data/2.5')
        self.api_key = api_key
        self.validate_city_records = None
        self.current_location = None

    def build(self):
        inspector.create_inspector(Window, self)

    def get_places_to_validate(self):
        unvalidated_airports = self.session.query(Airport).all()
        unvalidated_cities = self.session.query(City).all()
        # for airport in range(len(unvalidated_airports)):
        #     unvalidated_airports[airport] = unvalidated_airports[airport].name
        # for city in range(len(unvalidated_cities)):
        #     unvalidated_airports[city] = unvalidated_airports[city].name
        return unvalidated_airports, unvalidated_cities

    def get_venues_to_validate(self):
        unvalidated_venues = self.session.query(Venue).all()
        return unvalidated_venues

    def validate_airport(self, airport_code, latitude, longitude):
        # May need to update to make comparison forgiving
        with open('airports.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for item in reader:
                if item['ICAO'] == airport_code:
                    if item['Latitude'] == latitude and item['Longitude'] == longitude:
                        return True
            return False

    def validate_city(self, city_name, latitude, longitude):
        geo_connection = RESTConnection('api.openweathermap.org', 443, '/geo/1.0')
        geo_connection.send_request(
            'direct',
            {
                'q': 'London,US',
                'appid': API_KEY
            },
            None,
            self.on_records_loaded,
            self.on_records_not_loaded,
            self.on_records_not_loaded
        )

    def on_records_loaded(self, _, response):
        print(dumps(response, indent=4, sort_keys=True))
        self.validate_city_records = response
        # call method that gets lat/long from GUI and validates location.

    def on_records_not_loaded(self, _, error):
        Logger.error(f'{self.__class__.__name__}: {error}')

    def get_average_rating(self):
        pass

    def get_new_rating(self):
        pass

    def update_ratings(self):
        pass

    def find_closest_airport_to_destination(self, in_range_airports, destination):
        best_option = None
        max_distance = 0
        for airport in in_range_airports:
            if self.find_distance(airport.latitude, airport.longitude, destination.latitude, destination.longitude) > max_distance:
                max_distance = self.find_distance(airport.latitude, airport.longitude, destination.latitude, destination.longitude)
                best_option = airport
        return best_option

    def get_airports_in_range(self, current_airport):
        airports = self.session.query(Airport).all()
        in_range_airports = []
        for airport in airports:
            if self.find_distance(current_airport.latitude, current_airport.longitude, airport.latitude, airport.longitude) <= 3500 and self.is_weather_ok_airport():
                in_range_airports.append(airport)
        return in_range_airports

    def is_weather_ok_airport(self):
        pass

    def find_distance(self, current_latitude, current_longitude, next_latitude, next_longitude):
        # need to figure out how to calculate whether you are still going East or West.
        distance = math.acos(math.sin(current_latitude) * math.sin(next_latitude) +
                             math.cos(current_latitude) * math.cos(next_latitude) *
                             math.cos(next_longitude - current_longitude)) * 6371
        return distance

    def determine_best_city(self, airport):
        best_city = None
        city_score = 0
        for city in airport.cities:
            pass
        return best_city

    def get_city_score(self, city):
        score = 0
        venues_open = 0
        if self.is_weather_good_city():
            score += 3
        for venue in city.venues:
            if self.does_weather_meet_venues_conditions(venue, city.forecast):
                venues_open += 1
        score += venues_open
        return score

    def is_weather_good_city(self):
        pass

    def does_weather_meet_venues_conditions(self, venue, weather):
        return True

    def create_closest_itinerary_day(self, destination):
        airport = self.find_closest_airport_to_destination(self.get_airports_in_range(self.current_location), destination)
        pass

    def create_entertainment_itinerary(self):
        pass

    def get_previous_itinerary(self):
        pass

    def get_current_location(self):
        pass


def construct_mysql_url(authority, port, database, username, password):
    return f'mysql+mysqlconnector://{username}:{password}@{authority}:{port}/{database}'


def construct_in_memory_url():
    return 'sqlite:///'


def main():
    app = TravelPlannerApp()
    app.run()


if __name__ == '__main__':
    main()
