import unittest
from main import *
from database import *


class TestAirport(unittest.TestCase):
    def test_submit_data_airport(self):
        url = Database.construct_in_memory_url()
        database = Database(url)
        database.ensure_tables_exist()
        session = database.create_session()
        AirportApp.submit_data_airport(self, 'example', 'AAAA', 45, 50)
        actual = session.query(Airport).filter(Airport.name == 'example').one()
        self.assertEqual(actual.name, 'example')
        self.assertEqual(actual.code, 'AAAA')
        self.assertEqual(actual.latitude, 45)
        self.assertEqual(actual.longitude, 50)

    def test_submit_data_city(self):
        url = Database.construct_in_memory_url()
        database = Database(url)
        database.ensure_tables_exist()
        session = database.create_session()
        AirportApp.submit_data_city(self, 'example_city', 'example_geographic_entity', 45, 50)
        actual = session.query(City).filter(City.name == 'example_city').one()
        self.assertEqual(actual.city_name, 'example_city')
        self.assertEqual(actual.latitude, 45)
        self.assertEqual(actual.longitude, 50)
        self.assertEqual(actual.encompassing_geographic_entity, 'example_geographic_entity')


if __name__ == '__main__':
    unittest.main()
