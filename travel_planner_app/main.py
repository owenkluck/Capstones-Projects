import math
from kivy.app import App
from kivy.modules import inspector
from kivy.core.window import Window
from datetime import timedelta, date
from travel_planner_app.database import Database
from travel_planner_app.rest import RESTConnection
from api_key import API_KEY
from database import Airport, City, Venue, Condition
from kivy.logger import Logger
from json import dumps
import csv


class TravelPlannerApp(App):
    def __init__(self, authority='localhost', port=33060, database='airports', username='root', password='cse1208',
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
                    # Change to int to make forgiving comparison
                    if item['Latitude'] == str(latitude) and item['Longitude'] == str(longitude):
                        return True
            return False

    def validate_city(self):
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

    def find_best_entertainment_airport_and_city(self, in_range_airports, destination, current_date):
        best_score = 0
        best_city = None
        best_airport = None
        for airport in in_range_airports:
            city = self.determine_best_city(airport, current_date)
            score = self.get_city_score(city, current_date)
            if score > best_score:
                best_score = score
                best_city = city
                best_airport = airport
        return best_airport, best_city

    def find_closest_airport_to_destination(self, in_range_airports, destination):
        best_option = None
        max_distance = 0
        for airport in in_range_airports:
            if self.find_distance(airport.latitude, airport.longitude, destination.latitude, destination.longitude) > max_distance:
                max_distance = self.find_distance(airport.latitude, airport.longitude, destination.latitude, destination.longitude)
                best_option = airport
        return best_option

    def get_airports_in_range(self, current_airport, current_date):
        airports = self.session.query(Airport).all()
        in_range_airports = []
        for airport in airports:
            # make it, so it returns a list of positive going airports if there are any.
            if self.find_distance(current_airport.latitude, current_airport.longitude, airport.latitude, airport.longitude) <= 3500 and self.is_weather_ok_airport(airport, current_date):
                in_range_airports.append(airport)
        return in_range_airports

    def is_weather_ok_airport(self, airport, current_date):
        # Figure out severe weather
        next_day = current_date + timedelta(days=1)
        for forecast in airport.conditions:
            if next_day == forecast.date:
                if forecast.max_temperature < 45 and forecast.visibility > 5:
                    return True
        return False

    def find_distance(self, current_latitude, current_longitude, next_latitude, next_longitude):
        # need to figure out how to calculate whether you are still going East or West.
        distance = math.acos(math.sin(current_latitude) * math.sin(next_latitude) +
                             math.cos(current_latitude) * math.cos(next_latitude) *
                             math.cos(next_longitude - current_longitude)) * 6371
        return distance

    def determine_best_city(self, airport, current_date):
        best_city = None
        city_score = 0
        for city in airport.cities:
            if self.get_city_score(city, current_date) > city_score:
                city_score = self.get_city_score(city, current_date)
                best_city = city
        return best_city

    def get_city_score(self, city, current_date):
        score = 0
        venues_open = 0
        forecast = self.session.query(Condition).filter(Condition.city_id == city.city_id and Condition.date == current_date).one()
        if self.is_weather_good_city(forecast):
            score += 3
        score += len(self.get_open_venues_list(city, forecast))
        score += venues_open
        return score

    def is_weather_good_city(self, forecast):
        if 32 <= forecast.temperature <= 90 and 0 <= forecast.temperature <= 40 and forecast.wind_speed <= 20:
            return True
        return False

    def does_weather_meet_venues_conditions(self, venue, forecast):
        if venue.min_temperature <= forecast.temperature <= venue.max_temperature and \
                venue.min_humidity <= forecast.temperature <= venue.max_humidity and \
                forecast.wind_speed <= venue.max_wind_speed:
            return True
        return False

    def get_open_venues_list(self, city, forecast):
        venues_to_visit = []
        for venue in city.venues:
            if self.does_weather_meet_venues_conditions(venue, forecast):
                venues_to_visit.append(venue)
        return venues_to_visit

    def create_closest_itinerary_day(self, destination, current_date, current_airport):
        airport = self.find_closest_airport_to_destination(self.get_airports_in_range(current_airport, current_date), destination)
        city = self.determine_best_city(airport, current_date)
        city_forecast = self.session.query(Condition).filter(Condition.date == current_date and Condition.city_id == city.city_id).one()
        venues_to_visit = self.get_open_venues_list(city, city_forecast)

    def create_entertainment_itinerary(self, destination, current_date, current_airport):
        airport, city = self.find_best_entertainment_airport_and_city(self.get_airports_in_range(current_airport, current_date), destination, current_date)
        city_forecast = self.session.query(Condition).filter(Condition.date == current_date and Condition.city_id == city.city_id).one()
        venues_to_visit = self.get_open_venues_list(city, city_forecast)

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
    app.validate_city()
    a, b = app.get_places_to_validate()
    print(a)
    print(b)
    c = app.get_venues_to_validate()
    print(c)
    print(app.validate_airport('AYGA', -6.081689835, 145.3919983))
    d = app.session.query(Airport).all()
    e = app.session.query(City).all()[0]
    f = app.find_closest_airport_to_destination(d, e)
    print(f.name)
    current_date = date(2002, 9, 20)
    print(app.get_airports_in_range(f, current_date)[0].name)
    current_date += timedelta(days=1)
    city = app.session.query(City).filter(City.city_name == 'Omaha').one()
    app.run()


if __name__ == '__main__':
    main()
