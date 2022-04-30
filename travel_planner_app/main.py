import math
from kivy.app import App
from kivy.modules import inspector
from kivy.core.window import Window
from datetime import timedelta, date

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView

from database import Database
from rest import RESTConnection
from api_key import API_KEY
from database import Airport, City, Venue, Condition, Itinerary, Review
from kivy.logger import Logger
from json import dumps
from kivy.clock import Clock
import csv
from sqlalchemy.exc import SQLAlchemyError

PRIME_MERIDIAN = [0, 0]
OPPOSITE_PRIME_MERIDIAN = [0, 180]


class ReviewScrollView(ScrollView):
    pass


class ItineraryView(BoxLayout):
    pass


class BlackLineX(BoxLayout):
    pass


class BlackLineY(BoxLayout):
    pass


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
        self.api_key = API_KEY
        self.validate_city_records = None
        self.current_location = None
        self.outdoor_sporting_events = 0
        self.outdoor_plays = 0
        self.outdoor_restaurants = 0
        self.current_date = date.today()
        self.updated_forecast = None
        self.previous_destination = None
        self.destination = None
        self.final_destination = None
        self.ratings_to_update = []
        self.queued_entertainment_itineraries = []
        self.queued_closest_itineraries = []

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
        # for airport in range(len(unvalidated_airports)):
        #     unvalidated_airports[airport] = unvalidated_airports[airport].name
        # for city in range(len(unvalidated_cities)):
        #     unvalidated_airports[city] = unvalidated_airports[city].name
        # self.root.ids.unvalidated_airport.values = unvalidated_airports
        # self.root.ids.unvalidated_city.values = unvalidated_cities
        return unvalidated_airports, unvalidated_cities

    def add_locations_spinner(self):
        spinner_airports = [airport.name for airport in self.session.query(Airport).all(Airport.validated is False)]
        spinner_city = [city.city_name for city in self.session.query(City).all(City.validated is False)]
        self.root.ids.airports_spinner1.values = spinner_airports
        self.root.ids.city_spinner.values = spinner_city

    def get_venues_to_validate(self):
        venue_ids = set()
        unvalidated_reviews = self.session.query(Review).filter(Review.validated is False)
        for review in unvalidated_reviews:
            venue_ids.add(review.venue_id)
        unvalidated_venues = self.session.query(Venue.venue_id in venue_ids)
        return unvalidated_venues

    def validate_airport(self, airport_name):
        airport = self.session.query(Airport).filter(Airport.name == airport_name).one()
        with open('airports.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for item in reader:
                if item['ICAO'] == airport.airport_code:
                    if (int(item['Latitude']) - .009) <= airport.latitude <= (int(item['Latitude']) + .009) and \
                            (int(item['Longitude']) - .009) <= airport.longitude <= (int(item['Longitude']) + .009):
                        airport.validated = True
                        self.submit_data(airport)
                        return True
            return False

    def validate_city(self, city_name):
        city = self.session.query(City).filter(City.city_name == city_name).one()
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
        if (self.validate_city_records['lat'] - .009) <= city.latitude <= (self.validate_city_records['lat'] + .009) \
                and (self.validate_city_records['lon'] - .009) <= city.longitude <= (
                self.validate_city_records['lon'] + .009) \
                and city.city_name == self.validate_city_records['name']:
            city.validated = True
            self.submit_data(city)
            return True
        else:
            if city.city_name == self.validate_city_records['name']:
                print('lat and lon incorrect')
            else:
                print('incorrect')
            return False

    def on_records_loaded(self, _, response):
        print(dumps(response, indent=4, sort_keys=True))
        self.validate_city_records = response[0]

    def on_records_not_loaded(self, _, error):
        Logger.error(f'{self.__class__.__name__}: {error}')

    def populate_ratings_scroll_view(self):
        ratings = self.get_new_ratings()
        venues = []
        for rating in ratings:
            if rating.venue not in venues:
                venues.append(rating.venue)
        for venue in venues:
            view = ReviewScrollView()
            view.children[0].children[1].text = venue.venue_name
            for rating in venue.reviews:
                view.children[0].children[0].children[0].add_widget(CheckBox())
                view.children[0].children[0].children[1].add_widget(Label(text=f'score: {rating.score} id: {rating.review_id}'))
            self.root.ids.venue_and_review_scroll.add_widget(view)

    def check_state_of_checkboxes(self):
        root = self.root.ids.venue_and_review_scroll
        venues = root.children
        for x in range(len(venues)):
            venue = root.children[x].children[0].children[1].text
            checkboxes = root.children[x].children[0].children[0].children[0].children
            labels = root.children[x].children[0].children[0].children[1].children
            for i in range(len(checkboxes)):
                if checkboxes[i].active:
                    text = labels[i].text.split()
                    review_id = text[3]
                    print(venue, review_id)
                    self.update_rating(venue, review_id)

    def get_average_rating(self, venue_name):
        try:
            return self.session.query(Venue).filter(Venue.name == venue_name).one().average_welp.score
        except SQLAlchemyError:
            print('There seems to be two venues with the same name in the database,'
                  ' that or the name in the database doesn\'t exist')

    def get_new_ratings(self):
        new_ratings = self.session.query(Review).filter(Review.validated == False)
        return new_ratings

    def update_rating(self, venue_name, review_id):
        try:
            venue = self.session.query(Venue).filter(Venue.venue_name == venue_name).one()
            review = self.session.query(Review).filter(Review.review_id == review_id).one()
            if venue.average_welp_score is None:
                new_average_score = review.score
            else:
                new_average_score = (len(venue.reviews) * venue.average_welp_score + review.score) / (len(venue.reviews) + 1)
            venue.average_welp_score = new_average_score
            venue.welp_score_needs_update = False
            self.submit_data(venue)
            review.validated = True
            self.submit_data(review)
        except SQLAlchemyError:
            print('it seems the database refuses your request, make a better request.')

    def find_airport_to_cross_meridian(self, current_airport, in_range_airports):
        cross_airports = []
        if current_airport.longitude < 0:
            for airport in in_range_airports:
                if airport.longitude > 0:
                    cross_airports.append(airport)
        if current_airport.longitude > 0:
            for airport in in_range_airports:
                if airport.longitude < 0:
                    cross_airports.append(airport)
        max_airport = None
        for airport in cross_airports:
            if airport > max_airport:
                max_airport = airport
        if max_airport is not None:
            if self.previous_destination != PRIME_MERIDIAN or self.previous_destination != OPPOSITE_PRIME_MERIDIAN:
                if self.destination == PRIME_MERIDIAN:
                    self.destination = OPPOSITE_PRIME_MERIDIAN
                elif self.destination == OPPOSITE_PRIME_MERIDIAN:
                    self.destination = PRIME_MERIDIAN
            else:
                self.destination = self.final_destination
        return max_airport

    def can_meridian_be_passed(self, current_airport, in_range_airports):
        airport = None
        if abs(self.find_distance(current_airport.latitude, current_airport.longitude, self.destination[0],
                                  self.destination[1])) < 3500:
            airport = self.find_airport_to_cross_meridian(current_airport, in_range_airports)
        return airport

    def find_best_entertainment_airport_and_city(self, in_range_airports, current_date, current_airport):
        best_airport = self.can_meridian_be_passed(current_airport, in_range_airports)
        if best_airport is None:
            best_score = 0
            best_airport = in_range_airports[0]
            best_city = in_range_airports[0].cities[0]
            for airport in in_range_airports:
                city = self.determine_best_city(airport, current_date)
                score = self.get_city_score(city, current_date)
                if score > best_score:
                    best_score = score
                    best_city = city
                    best_airport = airport
            print(f'{best_city}, from end of algorithm')
        else:
            best_city = self.determine_best_city(best_airport, current_date)
            print('else in find best entertainment airport/city')
        return best_airport, best_city

    def find_closest_airport_to_destination(self, in_range_airports, destination, current_airport):
        best_option = self.can_meridian_be_passed(current_airport, in_range_airports)
        if best_option is None:
            max_distance = 0
            print(in_range_airports)
            for airport in in_range_airports:
                print(airport)
                print(airport.airport_id)
                print(airport.latitude)
                if self.find_distance(airport.latitude, airport.longitude, destination[0],
                                      destination[1]) > max_distance:
                    max_distance = self.find_distance(airport.latitude, airport.longitude, destination[0],
                                                      destination[1])
                    best_option = airport
        return best_option

    def get_airports_in_range(self, current_airport, current_date):
        airports = self.session.query(Airport).all()
        in_range_airports = []
        for airport in airports:
            # make it, so it returns a list of positive going airports if there are any.
            if self.find_distance(current_airport.latitude, current_airport.longitude, airport.latitude,
                                  airport.longitude) <= 3500 and self.is_weather_ok_airport(airport, current_date):
                if len(airport.cities) != 0:
                    in_range_airports.append(airport)
        if len(in_range_airports) == 0:
            print('No airports in range')
        return in_range_airports

    def is_weather_ok_airport(self, airport, current_date):
        # Figure out severe weather
        next_day = current_date + timedelta(days=1)
        if len(airport.conditions) == 0:
            return True
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
        best_city = airport.cities[0]
        print(best_city)
        city_score = 0
        for city in airport.cities:
            if self.get_city_score(city, current_date) > city_score:
                city_score = self.get_city_score(city, current_date)
                best_city = city
        return best_city

    def get_city_score(self, city, current_date):
        score = 0
        venues_open = 0
        forecasts_at_city = self.session.query(Condition).filter(Condition.city_id == city.city_id).count()
        if forecasts_at_city > 0:
            forecasts = self.session.query(Condition).filter(
                Condition.city_id == city.city_id and Condition.date == current_date)
            forecasts_on_date = []
            for forecast in forecasts:
                if forecast.date == current_date:
                    forecasts_on_date.append(forecast)
            if len(forecasts_on_date) > 1:
                print('multiple conditions found of same date and same city')
                forecast = self.session.query(Condition).filter(
                    Condition.city_id == city.city_id and Condition.date == current_date)
                for x in forecast:
                    print(x.date)
                max_id = self.session.query(Condition).filter(
                    Condition.city_id == city.city_id and Condition.date == current_date)[0].condition_id
                for condition in forecast:
                    if condition.condition_id > max_id:
                        condition_to_delete = self.session.query(Condition).filter(
                            Condition.condition_id == max_id).one()
                        max_id = condition.condition_id
                        self.delete_row(condition_to_delete)
                    elif condition.condition_id < max_id:
                        self.delete_row(condition)
                return self.get_city_score(city, current_date)
            if self.is_weather_good_city(forecasts[0]):
                score += 3
                score += len(self.get_open_venues_list(city, forecasts[0]))
            score += venues_open
            return score
        else:
            self.request_onecall_for_place(city.latitude, city.longitude, current_date, None, None, city, 'create', self.api_key)
            score = self.get_city_score(city, current_date)
            return score

    def is_weather_good_city(self, forecast):
        if 32 <= forecast.max_temperature <= 90 and 0 <= forecast.max_temperature <= 40 and forecast.max_wind_speed <= 20:
            return True
        return False

    def does_weather_meet_venues_conditions(self, venue, forecast):
        if len(venue.condition) != 0:
            condition = venue.condition[0]
            if condition.min_temperature <= forecast.max_temperature <= condition.max_temperature and \
                    condition.min_humidity <= forecast.max_humidity <= condition.max_humidity and \
                    forecast.max_wind_speed <= condition.max_wind_speed:
                return True
            return False
        return True

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
                                                           destination, current_airport)
        city = self.determine_best_city(airport, current_date)
        print(city)
        print('hi')
        city_forecast_length = self.session.query(Condition).filter(
            Condition.date == current_date and Condition.city_id == city.city_id).count()
        print(city_forecast_length)
        if city_forecast_length == 0:
            self.request_onecall_for_place(airport.latitude, airport.longitude, current_date, None, None, city,
                                           'create', self.api_key)
            self.create_closest_itinerary_day(destination, current_date, current_airport)
        elif city_forecast_length > 1:
            print('multiple forecasts on a single date, associated with one city')
        else:
            city_forecast = self.session.query(Condition).filter(Condition.date == current_date
                                                                 and Condition.city_id == city.city_id).one()
            venues_to_visit = self.get_open_venues_list(city, city_forecast)
            venues = self.determine_venues(venues_to_visit)
            itinerary = Itinerary(airport=airport.name, city=city.city_name, venues=venues, date=current_date)
            self.queued_closest_itineraries.append(itinerary)
            print('Success')

    def create_entertainment_itinerary(self, destination, current_date, current_airport):
        airport, city = self.find_best_entertainment_airport_and_city(
            self.get_airports_in_range(current_airport, current_date), current_date, current_airport)
        city_forecast = self.session.query(Condition).filter(
            Condition.date == current_date and Condition.city_id == city.city_id).one()
        venues_to_visit = self.get_open_venues_list(city, city_forecast)
        venues = self.determine_venues(venues_to_visit)
        itinerary = Itinerary(airport=airport.name, city=city.city_name, venues=venues, date=current_date)
        self.queued_entertainment_itineraries.append(itinerary)
        print('Success')

    def get_previous_itinerary(self):
        itineraries = self.session.query(Itinerary).filter(Itinerary.date < self.current_date)
        return itineraries

    def get_current_location(self):
        itinerary = self.session.query(Itinerary).filter(Itinerary.date == self.current_date).one()
        airport = self.session.query(Airport).filter(Airport.name == itinerary.airport).one()
        return airport.latitude, airport.longitude

    def prepare_itinerary(self):
        current_itineraries = self.session.query(Itinerary).filter(Itinerary.date >= self.current_date)
        max_date = self.current_date
        current_airport = None
        for itinerary in current_itineraries:
            self.update_existing_itinerary(itinerary)
            if itinerary.date > max_date:
                max_date = itinerary.date
            if itinerary.date == self.current_date:
                current_airport = self.session.query(Airport).filter(Airport.name == itinerary.airport).one()
        new_itineraries = (7 - (max_date - self.current_date).days)
        for i in range(new_itineraries):
            max_date += timedelta(days=1)
            self.create_closest_itinerary_day(self.destination, max_date, current_airport)
            self.create_entertainment_itinerary(self.destination, max_date, current_airport)
            next_itinerary = self.session.query(Itinerary).filter(Itinerary.date == max_date)
            this_itinerary = None
            for itinerary in next_itinerary:
                if itinerary.date == max_date:
                    this_itinerary = itinerary
            if this_itinerary is None:
                return
            current_airport = self.session.query(Airport).filter(Airport.name == this_itinerary.airport).one()

    def update_existing_itinerary(self, itinerary):
        airport = self.session.query(Airport).filter(Airport.name == itinerary.airport).one()
        future_forecasts = []
        for condition in airport.conditions:
            if condition.date >= self.current_date:
                future_forecasts.append(condition)
        if len(future_forecasts) > 0:
            outdated_forecasts = self.session.query(Condition).filter(Condition.airport_id == airport.airport_id and
                                                                      Condition.date == itinerary.date)
            outdated_forecast = outdated_forecasts[0]
            for forecast in outdated_forecasts:
                if forecast.date == itinerary.date:
                    outdated_forecast = forecast
            self.request_onecall_for_place(airport.latitude, airport.longitude, itinerary.date, outdated_forecast,
                                           airport, None, 'update', self.api_key)
        else:
            self.request_onecall_for_place(airport.latitude, airport.longitude, itinerary.date,
                                           None, airport, None, 'create', self.api_key)

    def populate_itinerary_view(self):
        # itineraries = self.session.query(Itinerary).all()
        # closest_current_itineraries = []
        # entertainment_current_itineraries = []
        # for itinerary in itineraries:
        #     if itinerary.date >= self.current_date and itinerary.itinerary_type == 'Close':
        #         closest_current_itineraries.append(itinerary)
        #     if itinerary.date >= self.current_date and itinerary.itinerary_type == 'Entertain':
        #         entertainment_current_itineraries.append(itinerary)
        self.root.ids.itinerary_scroll.size_hint_min_x = 300 * ((len(self.queued_closest_itineraries) + len(self.queued_entertainment_itineraries)) / 2)
        root_1 = self.root.ids.entertainment_itinerary
        root_2 = self.root.ids.closest_itinerary
        for itinerary in self.queued_entertainment_itineraries:
            itinerary_view = ItineraryView()
            itinerary_view.children[1].children[0].text = f'Entertainment: {1}'
            itinerary_view.children[1].children[1].text = f'Eat at: {1}'
            itinerary_view.children[1].children[2].text = f'Go to: {itinerary.city}'
            itinerary_view.children[1].children[3].text = f'Arrive At: {itinerary.airport}'
            itinerary_view.children[1].children[4].text = f'Airport Leave:'
            itinerary_view.children[1].children[5].text = f'Date {itinerary.date}'
            root_1.add_widget(itinerary_view)
        for itinerary in self.queued_closest_itineraries:
            itinerary_view = ItineraryView()
            itinerary_view.children[1].children[0].text = f'Entertainment: {1}'
            itinerary_view.children[1].children[1].text = f'Eat at: {1}'
            itinerary_view.children[1].children[2].text = f'Go to: {itinerary.city}'
            itinerary_view.children[1].children[3].text = f'Arrive At: {itinerary.airport}'
            itinerary_view.children[1].children[4].text = f'Airport Leave:'
            itinerary_view.children[1].children[5].text = f'Date {itinerary.date}'
            root_2.add_widget(itinerary_view)

    def request_onecall_for_place(self, latitude, longitude, itinerary_date, outdated_forecast, airport, city,
                                  update_or_create, api_key):
        self.weather_connection.send_request(
            'onecall',
            {
                'lat': latitude,
                'lon': longitude,
                'appid': api_key
            },
            None,
            self.update_forecast,
            self.on_records_not_loaded,
            self.on_records_not_loaded,
        )
        if update_or_create == 'update':
            self.update_old_forecast(itinerary_date, outdated_forecast)
        else:
            self.create_new_forecasts(airport, city)

    def update_old_forecast(self, itinerary_date, outdated_forecast):
        forecast = None
        for day in self.updated_forecast['daily']:
            if date.fromtimestamp(int(day['dt'])) == itinerary_date:
                forecast = day
        if forecast is not None:
            outdated_forecast.max_temperature = int(forecast['temp']['max'])
            outdated_forecast.min_temperature = int(forecast['temp']['min'])
            outdated_forecast.humidity = int(forecast['humidity'])
            outdated_forecast.rain = int(forecast['pop'])
            outdated_forecast.visibility = 10
            outdated_forecast.max_wind_speed = int(forecast['wind_speed'])
            new_forecast = outdated_forecast
            self.submit_data(new_forecast)
        else:
            print('No forecast matched the date of the itinerary')

    def update_forecast(self, _, response):
        # print(dumps(response, indent=4, sort_keys=True))
        self.updated_forecast = response

    def create_new_forecasts(self, airport, city):
        for day in self.updated_forecast['daily']:
            max_temperature = int(day['temp']['max'])
            min_temperature = int(day['temp']['min'])
            humidity = int(day['humidity'])
            wind_speed = int(day['wind_speed'])
            visibility = 10
            rain = int(day['pop'])
            if city is None:
                forecast = Condition(date=date.fromtimestamp(int(day['dt'])), max_temperature=max_temperature,
                                     min_temperature=min_temperature, max_humidity=humidity, max_wind_speed=wind_speed,
                                     visibility=visibility, rain=rain, airport=airport)
            else:
                forecast = Condition(date=date.fromtimestamp(int(day['dt'])), max_temperature=max_temperature,
                                     min_temperature=min_temperature, max_humidity=humidity, max_wind_speed=wind_speed,
                                     visibility=visibility, rain=rain, city=city)
            self.submit_data(forecast)

    def submit_data(self, data):
        try:
            if type(data) is list:
                for item in data:
                    self.session.add(item)
            else:
                self.session.add(data)
            self.session.commit()
        except SQLAlchemyError:
            print('could not submit data')

    def delete_row(self, item):
        print(f'{item}, deleted')
        self.session.delete(item)
        self.session.commit()

    def add_airports_spinner(self):
        values = [airport.name for airport in self.session.query(Airport).all()]
        self.root.ids.airport_spinner.values = values

    def add_airports_city_spinner(self):
        values = [airport.name for airport in self.session.query(Airport).all()] and [city.city_name for city in
                                                                                      self.session.query(City).all()]
        self.root.ids.airports_city_spinner1.values = values

    def delete_buttons(self):
        self.root.ids.scroll_box_1.clear_widgets()
        self.root.ids.scroll_box_2.clear_widgets()

    def loading_screen(self, **kwargs):
        super(TravelPlannerApp, self).__init__(**kwargs)
        Clock.schedule_once(self.load, 3)

    def load(self, app):
        self.root.current = 'mainmenu1'


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
    # app.update_existing_itinerary(date(2002, 1, 1))
    # datte = date(2000, 1, 1)
    # datte = timedelta(days=1) + datte
    # print(datte)
    app.connect_to_database('localhost', 33060, 'airports', 'root', 'cse1208')
    app.connect_to_open_weather()
    app.destination = PRIME_MERIDIAN
    # airport = Airport(name='Strawberry Airport', latitude=90, longitude=91, code='EEEE')
    # app.session.add(airport)
    # app.session.commit()
    airport = app.session.query(Airport).filter(Airport.name == 'Omaha Airport').one()
    # app.create_closest_itinerary_day(PRIME_MERIDIAN, app.current_date, airport)
    # app.create_entertainment_itinerary(PRIME_MERIDIAN, app.current_date, airport)
    # itinerary = app.session.query(Itinerary).all()[0]
    # app.update_existing_itinerary(itinerary)
    app.run()


if __name__ == '__main__':
    main()

# Put Error handling around all one() statements
# Make method to create conditions for a place of None exist.
# Start writing unit tests for itinerary functions.
# Make sure algorithm implements all necessary requirements.
# Make sure main is complete and functional.
# change all date query comparisons
