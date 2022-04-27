import math
from kivy.app import App
from kivy.modules import inspector
from kivy.core.window import Window
from datetime import timedelta, date
from travel_planner_app.database import Database
from travel_planner_app.rest import RESTConnection
from api_key import API_KEY
from database import Airport, City, Venue, Condition, Itinerary, Review
from kivy.logger import Logger
from json import dumps
import csv
from sqlalchemy.exc import SQLAlchemyError


class TravelPlannerApp(App):
    def __init__(self, authority='localhost', port=33060, database='airports', username='root', password='cse1208',
                 api_key=API_KEY, **kwargs):
        super(TravelPlannerApp, self).__init__(**kwargs)
        self.authority = authority
        self.port = port
        self.database_name = database
        self.username = username
        self.password = password
        self.url = None
        self.database = None
        self.session = None
        self.weather_connection = None
        self.geo_connection = None
        self.api_key = api_key
        self.validate_city_records = None
        self.current_location = None
        self.outdoor_sporting_events = 0
        self.outdoor_plays = 0
        self.outdoor_restaurants = 0
        self.current_date = date
        self.updated_forecast = None

    def build(self):
        inspector.create_inspector(Window, self)

    def connect_to_database(self, authority, port, database, username, password):
        try:
            url = construct_mysql_url(authority, port, database, username, password)
            database = Database(url)
            session = database.create_session()
            self.session = session
            self.database = database
            self.url = url
        except SQLAlchemyError:
            print('could not connect to database')

    def connect_to_open_weather(self, port_api=443):
        self.weather_connection = RESTConnection('api.openweathermap.org', port_api, '/data/2.5')
        self.geo_connection = RESTConnection('api.openweathermap.org', 443, '/geo/1.0')

    def get_places_to_validate(self):
        unvalidated_airports = self.session.query(Airport).filter(Airport.validated is False)
        unvalidated_cities = self.session.query(City).filter(City.validated is False)
        return unvalidated_airports, unvalidated_cities

    def get_venues_to_validate(self):
        venue_ids = set()
        unvalidated_reviews = self.session.query(Review).filter(Review.validated is False)
        for review in unvalidated_reviews:
            venue_ids.add(review.venue_id)
        unvalidated_venues = self.session.query(Venue.venue_id in venue_ids)
        return unvalidated_venues

    def validate_airport(self, airport_name):
        airport = self.session.query(Airport).filter(Airport.name == airport_name).one()
        # May need to update to make comparison forgiving
        with open('airports.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for item in reader:
                if item['ICAO'] == airport.airport_code:
                    # Change to int to make forgiving comparison
                    if item['Latitude'] == str(airport.latitude) and item['Longitude'] == str(airport.longitude):
                        airport.validated = True
                        self.submit_data(airport)
                        return True
            return False

    def validate_city(self, city_name):
        city = self.session.query(City).filter(City.name == city_name).one()
        self.geo_connection.send_request(
            'direct',
            {
                'q': city_name,
                'appid': API_KEY
            },
            None,
            self.on_records_loaded,
            self.on_records_not_loaded,
            self.on_records_not_loaded,
        )
        if self.validate_city_records['lat'] == city.latitude\
                and self.validate_city_records['lon'] == city.longitude\
                and city.name == self.validate_city_records['name']:
            city.validated = True
            self.submit_data(city)
            return True
        else:
            if city.name == self.validate_city_records['name']:
                print('lat and lon incorrect')
            else:
                print('incorrect')
            return False

    def on_records_loaded(self, _, response):
        print(dumps(response, indent=4, sort_keys=True))
        self.validate_city_records = response

    def on_records_not_loaded(self, _, error):
        Logger.error(f'{self.__class__.__name__}: {error}')

    def get_average_rating(self, venue_name):
        return self.session.query(Venue).filter(Venue.name == venue_name).one().average_welp.score

    def get_new_ratings(self):
        new_ratings = self.session.query(Review).filter(Review.validated is False)
        return new_ratings

    def update_rating(self, rating, venue_name, review_id):
        venue = self.session.query(Venue).filter(Venue.name == venue_name).one()
        review = self.session.query(Review).filter(Review.review_id == review_id).one()
        new_average_score = (len(venue.reviews) * venue.average_welp_score + rating) / (len(venue.reviews + 1))
        venue.average_welp_score = new_average_score
        venue.welp_score_needs_update = False
        self.submit_data(venue)
        review.validated = True
        self.submit_data(review)

    def find_best_entertainment_airport_and_city(self, in_range_airports, current_date):
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
            if self.find_distance(airport.latitude, airport.longitude, destination.latitude,
                                  destination.longitude) > max_distance:
                max_distance = self.find_distance(airport.latitude, airport.longitude, destination.latitude,
                                                  destination.longitude)
                best_option = airport
        return best_option

    def get_airports_in_range(self, current_airport, current_date):
        airports = self.session.query(Airport).all()
        in_range_airports = []
        for airport in airports:
            # make it, so it returns a list of positive going airports if there are any.
            if self.find_distance(current_airport.latitude, current_airport.longitude, airport.latitude,
                                  airport.longitude) <= 3500 and self.is_weather_ok_airport(airport, current_date):
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
        forecast = self.session.query(Condition).filter(
            Condition.city_id == city.city_id and Condition.date == current_date).one()
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

    def determine_venues(self, venues_to_visit):
        # 'Indoor Restaurant', 'Outdoor Restaurant', 'Indoor Theater', 'Outdoor Theater', 'Indoor Sports Arena', 'Outdoor Sports Arena'
        venues = []
        event = None
        restaurant = None
        if self.outdoor_plays < self.outdoor_sporting_events:
            event = self.search_for_outdoor_theater(event, venues_to_visit)
            if event is None:
                event = self.search_for_outdoor_sports(event, venues_to_visit)
            if event is None:
                event = self.search_for_indoor_events(event, venues_to_visit)
        else:
            event = self.search_for_outdoor_sports(event, venues_to_visit)
            if event is None:
                event = self.search_for_outdoor_theater(event, venues_to_visit)
            if event is None:
                event = self.search_for_indoor_events(event, venues_to_visit)
        for venue in venues_to_visit:
            if venue.venue_type == 'Outdoor Restaurant':
                restaurant = venue
        if event is None:
            for venue in venues_to_visit:
                if venue.venue_type == 'Indoor Restaurant':
                    restaurant = venue
        if event is not None:
            venues.append(event)
        if restaurant is not None:
            venues.append(restaurant)
        return venues

    def search_for_indoor_events(self, event, venues_to_visit):
        for venue in venues_to_visit:
            if venue.venue_type == 'Indoor Theater' or venue.venue_type == 'Indoor Sports Arena':
                event = venue
        return event

    def search_for_outdoor_sports(self, event, venues_to_visit):
        for venue in venues_to_visit:
            if venue.venue_type == 'Outdoor Sports Arena':
                event = venue
        return event

    def search_for_outdoor_theater(self, event, venues_to_visit):
        for venue in venues_to_visit:
            if venue.venue_type == 'Outdoor Theater':
                event = venue
        return event

    def create_closest_itinerary_day(self, destination, current_date, current_airport):
        airport = self.find_closest_airport_to_destination(self.get_airports_in_range(current_airport, current_date),
                                                           destination)
        city = self.determine_best_city(airport, current_date)
        city_forecast = self.session.query(Condition).filter(
            Condition.date == current_date and Condition.city_id == city.city_id).one()
        venues_to_visit = self.get_open_venues_list(city, city_forecast)

    def create_entertainment_itinerary(self, destination, current_date, current_airport):
        airport, city = self.find_best_entertainment_airport_and_city(
            self.get_airports_in_range(current_airport, current_date), destination, current_date)
        city_forecast = self.session.query(Condition).filter(
            Condition.date == current_date and Condition.city_id == city.city_id).one()
        venues_to_visit = self.get_open_venues_list(city, city_forecast)
        venues = self.determine_venues(venues_to_visit)

    def get_previous_itinerary(self):
        itineraries = self.session.query(Itinerary).filter(Itinerary.date < self.current_date)
        return itineraries

    def get_current_location(self):
        itinerary = self.session.query(Itinerary).filter(Itinerary.date == self.current_date).one()
        airport = self.session.query(Airport).filter(Airport.name == itinerary.airport).one()
        return airport.latitude, airport.longitude

    def prepare_itinerary(self):
        pass

    def update_existing_itinerary(self, itinerary_date):
        itinerary = self.session.query(Itinerary).filter(Itinerary.date == itinerary_date).one()
        airport = self.session.query(Airport).filter(Airport.name == itinerary.airport).one()
        outdated_forecast = self.session.query(Condition).filter(Condition.airport_id == airport.airport_id and
                                                                 Condition.date == itinerary_date).one()
        self.request_onecall_for_place(airport.latitude, airport.longitude, itinerary_date, outdated_forecast)

    def request_onecall_for_place(self, latitude, longitude, itinerary_date, outdated_forecast):
        self.weather_connection.send_request(
            'onecall',
            {
                'lat': latitude,
                'lon': longitude,
                'appid': API_KEY
            },
            None,
            self.update_forecast,
            self.on_records_not_loaded,
            self.on_records_not_loaded,
        )
        forecast = None
        for day in self.updated_forecast['daily']:
            if date.fromtimestamp(int(day['dt'])) == itinerary_date:
                forecast = day
        if forecast is not None:
            outdated_forecast.max_temperature = int(forecast['temp']['max'])
            outdated_forecast.min_temperature = int(forecast['temp']['min'])
            outdated_forecast.humidity = int(forecast['humidity'])
            outdated_forecast.rain = int(forecast['dew_point'])
            outdated_forecast.visibility = 10
            outdated_forecast.wind_speed = int(forecast['wind_speed'])
            new_forecast = outdated_forecast
            self.submit_data(new_forecast)
        else:
            print('No forecast matched the date of the itinerary')
        pass

    def update_forecast(self, _, response):
        print(dumps(response, indent=4, sort_keys=True))
        self.updated_forecast = response

    def submit_data(self, data):
        try:
            self.session.add(data)
            self.session.commit()
        except SQLAlchemyError:
            print('could not submit data')


def construct_mysql_url(authority, port, database, username, password):
    return f'mysql+mysqlconnector://{username}:{password}@{authority}:{port}/{database}'


def construct_in_memory_url():
    return 'sqlite:///'


def main():
    app = TravelPlannerApp()
    # app.validate_city()
    # a, b = app.get_places_to_validate()
    # print(a)
    # print(b)
    # c = app.get_venues_to_validate()
    # print(c)
    # print(app.validate_airport('AYGA', -6.081689835, 145.3919983))
    # d = app.session.query(Airport).all()
    # e = app.session.query(City).all()[0]
    # f = app.find_closest_airport_to_destination(d, e)
    # print(f.name)
    # current_date = date(2002, 9, 20)
    # print(app.get_airports_in_range(f, current_date)[0].name)
    # current_date += timedelta(days=1)
    # city = app.session.query(City).filter(City.city_name == 'Omaha').one()
    app.update_existing_itinerary(date(2002, 1, 1))
    app.run()


if __name__ == '__main__':
    main()
