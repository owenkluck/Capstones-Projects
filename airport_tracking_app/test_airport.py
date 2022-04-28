import unittest
from main import *
from database import *


class TestAirport(unittest.TestCase):
    def test_commit_airport(self):
        url = Database.construct_in_memory_url()
        database = Database(url)
        database.ensure_tables_exist()
        test_app = AirportApp()
        test_app.session = database.create_session()
        test_app.commit_airport_to_database('AAAA', 45, 50, 'example')
        actual = test_app.session.query(Airport).filter(Airport.name == 'example').one()
        self.assertEqual(actual.name, 'example')
        self.assertEqual(actual.code, 'AAAA')
        self.assertEqual(actual.latitude, 45)
        self.assertEqual(actual.longitude, 50)

    def test_commit_city(self):
        url = Database.construct_in_memory_url()
        database = Database(url)
        database.ensure_tables_exist()
        test_app = AirportApp()
        test_app.session = database.create_session()
        test_app.commit_city_to_database('example_geographic_entity', '45', '50', 'example_city')
        actual = test_app.session.query(City).filter(City.city_name == 'example_city').one()
        self.assertEqual(actual.city_name, 'example_city')
        self.assertEqual(actual.latitude, 45)
        self.assertEqual(actual.longitude, 50)
        self.assertEqual(actual.encompassing_geographic_entity, 'example_geographic_entity')

    def test_add_city(self):
        url = Database.construct_in_memory_url()
        database = Database(url)
        database.ensure_tables_exist()
        test_app = AirportApp()
        test_app.session = database.create_session()
        test_airport = Airport(name='test_airport', code='ZZZZ', longitude=5, latitude=10)
        test_city = City(city_name='test_city', longitude=5, latitude=10, encompassing_geographic_entity='example_state')
        test_app.session.commit()
        test_app.current_airport = test_airport
        test_app.append_city_to_current_airport(test_city)
        actual = test_app.session.query(Airport).filter(Airport.name == 'test_airport').one()
        self.assertEqual(actual.cities, [test_city])

    def test_add_airport(self):
        url = Database.construct_in_memory_url()
        database = Database(url)
        database.ensure_tables_exist()
        test_app = AirportApp()
        test_app.session = database.create_session()
        test_airport = Airport(name='test_airport', code='ZZZZ', longitude=5, latitude=10)
        test_city = City(city_name='test_city', longitude=5, latitude=10, encompassing_geographic_entity='example_state')
        test_app.session.commit()
        test_app.current_city = test_city
        test_app.append_airport_to_current_city(test_airport)
        actual = test_app.session.query(City).filter(City.city_name == 'test_city').one()
        self.assertEqual(actual.airports, [test_airport])

if __name__ == '__main__':
    unittest.main()
