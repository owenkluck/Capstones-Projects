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

    def on_records_not_loaded(self, _, error):
        Logger.error(f'{self.__class__.__name__}: {error}')

    def get_average_rating(self):
        pass

    def get_new_rating(self):
        pass

    def update_ratings(self):
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
