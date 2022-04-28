import unittest
from database import *
from datetime import date
from travel_planner_app.main import TravelPlannerApp

PRIME_MERIDIAN = [0, 0]
OPPOSITE_PRIME_MERIDIAN = [0, 180]
app = TravelPlannerApp()


class TravelPlannerAppTests(unittest.TestCase):
    def test_create_closest_itinerary(self):
        airport = app.session.query(Airport).filter(Airport.name == 'Omaha Airport').one()
        app.create_closest_itinerary_day(PRIME_MERIDIAN, app.current_date, airport)
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
