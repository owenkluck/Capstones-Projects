import unittest
from main import *
from database import *


class TestEntertainment(unittest.TestCase):
    def test_commit_city_to_database(self):
        url = Database.construct_in_memory_url()
        database = Database(url)
        database.ensure_tables_exist()
        test_app = EntertainmentTrackerApp()
        test_app.session = database.create_session()
        test_app.commit_city_to_database('example_entity', 45, 50, 'example_city')
        actual = test_app.session.query(City).filter(City.city_name == 'example_city').one()
        self.assertEqual(actual.city_name, 'example_city')
        self.assertEqual(actual.latitude, 45)
        self.assertEqual(actual.longitude, 50)
        self.assertEqual(actual.encompassing_geographic_entity, 'example_entity')

    def test_commit_venue_to_database(self):
        url = Database.construct_in_memory_url()
        database = Database(url)
        database.ensure_tables_exist()
        test_app = EntertainmentTrackerApp()
        test_app.session = database.create_session()
        test_app.commit_city_to_database('example_entity', 45, 50, 'example_city')
        test_app.commit_venue_to_database('example_city', 'example_venue', 'example_venue_type')
        actual = test_app.session.query(Venue).filter(Venue.venue_name == 'example_venue').one()
        self.assertEqual(actual.venue_name, 'example_venue')
        self.assertEqual(actual.city.city_name, 'example_city')
        self.assertEqual(actual.venue_type, 'example_venue_type')

    def test_add_condition(self):
        url = Database.construct_in_memory_url()
        database = Database(url)
        database.ensure_tables_exist()
        test_app = EntertainmentTrackerApp()
        test_app.session = database.create_session()
        test_app.commit_city_to_database('example_entity', '45', '50', 'example_city')
        test_app.commit_venue_to_database('example_city', 'example_venue', 'example_venue_type')
        test_app.add_condition('example_venue', '-10', '100', '0', '85', '30', '')
        actual = test_app.session.query(Condition).filter(Condition.condition_id == 1).one()
        self.assertEqual(actual.condition_id, 1)
        self.assertEqual(actual.min_temperature, -10)
        self.assertEqual(actual.max_temperature, 100)
        self.assertEqual(actual.min_humidity, 0)
        self.assertEqual(actual.max_humidity, 85)
        self.assertEqual(actual.max_wind_speed, 30)
        self.assertEqual(actual.open_weather_code, None)

    def test_update_venue_data(self):
        url = Database.construct_in_memory_url()
        database = Database(url)
        database.ensure_tables_exist()
        test_app = EntertainmentTrackerApp()
        test_app.session = database.create_session()
        test_app.commit_city_to_database('example_entity', '45', '50', 'example_city')
        test_app.commit_venue_to_database('example_city', 'example_venue', 'example_venue_type')
        test_app.add_condition('example_venue', '-10', '100', '0', '85', '30', '')
        test_app._update_venue_data('example_venue', 'new_venue', 'example_city', '-5', '105', '10', '90', '50', '501')
        actual = test_app.session.query(Condition).filter(Condition.condition_id == 1).one()
        self.assertEqual(actual.condition_id, 1)
        self.assertEqual(actual.min_temperature, -5)
        self.assertEqual(actual.max_temperature, 105)
        self.assertEqual(actual.min_humidity, 10)
        self.assertEqual(actual.max_humidity, 90)
        self.assertEqual(actual.max_wind_speed, 50)
        self.assertEqual(actual.open_weather_code, 501)

    def test_add_welp_score(self):
        url = Database.construct_in_memory_url()
        database = Database(url)
        database.ensure_tables_exist()
        test_app = EntertainmentTrackerApp()
        test_app.session = database.create_session()
        test_app.commit_city_to_database('example_entity', '45', '50', 'example_city')
        test_app.commit_venue_to_database('example_city', 'example_venue', 'example_venue_type')
        test_app.add_welp_score(5, 'example_city', 'example_venue')
        actual = test_app.session.query(Review).filter(Review.review_id == 1)
        self.assertEqual(actual.review_id, 1)
        self.assertEqual(actual.review_score, '5')
        self.assertEqual(actual.venue_being_reviewed, 'example_venue')
        self.assertEqual(actual.city, 'example_city')


if __name__ == '__main__':
    unittest.main()
