import unittest

from sqlalchemy.exc import SQLAlchemyError

from database import *
from datetime import date

from travel_planner_app.main import TravelPlannerApp, construct_mysql_url

PRIME_MERIDIAN = [0, 0]
OPPOSITE_PRIME_MERIDIAN = [0, 180]
app = TravelPlannerApp()


class TravelPlannerAppTests(unittest.TestCase):
    connection = None

    def test_open_weather_connection(self):
        test_app = TravelPlannerApp()
        test_app.connect_to_open_weather(port_api=443)
        test = test_app.weather_connection is not None
        self.assertEqual(test, True)

    def test_one_call_returns_values(self):
        test_app = TravelPlannerApp()
        test_app.connect_to_database(authority='localhost', port=33060, database='airports', username='root', password='cse1208')
        airport = test_app.session.query(Airport).filter(Airport.name == 'Pacific Airport').one()
        test_app.request_onecall_for_place(airport.latitude, airport.longitude, date(2022, 4, 30), None, airport, 'create')
        total = len(airport.conditions)
        self.assertEqual(total, 8)

    def test_get_places_to_validate(self):
        test_app = TravelPlannerApp()
        test_app.connect_to_database(authority='localhost', port=33060, database='airports', username='root', password='cse1208')
        airports, cities = test_app.get_places_to_validate()
        print(airports)
        self.assertEqual(len(airports), 5)
        self.assertEqual(len(cities), 7)

    def test_get_venues_to_validate(self):
        test_app = TravelPlannerApp()
        test_app.connect_to_database(authority='localhost', port=33060, database='airports', username='root', password='cse1208')
        venues = test_app.get_venues_to_validate()
        print(venues)
        self.assertEqual(len(venues), 4)

    def test_validate_city(self):
        pass

    def test_validate_airport(self):
        pass

    def test_update_rating(self):
        pass

    def test_get_new_rating(self):
        pass

    def test_get_average_rating(self):
        pass



if __name__ == '__main__':
    unittest.main()
