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
        pass

    def test_update_venue_data(self):
        pass

    def test_add_welp_score(self):
        pass


if __name__ == '__main__':
    unittest.main()
