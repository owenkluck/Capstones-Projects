from datetime import date
from sys import stderr

from sqlalchemy.exc import SQLAlchemyError
from datetime import timedelta
from database import Database, City, Airport, Venue, Condition, Itinerary, Review


def add_starter_data(session):
    day = Itinerary(airport='Omaha Airport', city='Omaha', date=date(2022, 4, 29))
    session.add(day)
    session.commit()
    san_fran = City(city_name='San Francisco', latitude=37.8, longitude=-122.4, encompassing_geographic_entity='California')
    denver = City(city_name='Denver', latitude=39.7, longitude=-105.0, encompassing_geographic_entity='Colorado')
    session.add(denver)
    session.add(san_fran)
    session.commit()

    mile_high_conditions = Condition(min_temperature=0, max_temperature=105, min_humidity=0, max_humidity=100,
                                     max_wind_speed=40)
    red_rocks_conditions = Condition(open_weather_code=201)
    clear_skies = Condition(open_weather_code=800)
    cloudy = Condition(open_weather_code=801)
    foggy = Condition(open_weather_code=741)
    heavy_snow = Condition(open_weather_code=602)
    rain = Condition(open_weather_code=501)
    drizzle = Condition(open_weather_code=301)
    chase_conditions = Condition()
    alamo_conditions = Condition()
    melting_pot_conditions = Condition()
    casa_bonita_conditions = Condition()
    session.add(mile_high_conditions)
    session.add(red_rocks_conditions)
    session.add(clear_skies)
    session.add(cloudy)
    session.add(foggy)
    session.add(heavy_snow)
    session.add(rain)
    session.add(drizzle)
    session.add(chase_conditions)
    session.add(alamo_conditions)
    session.add(melting_pot_conditions)
    session.add(casa_bonita_conditions)
    session.commit()

    chase = Venue(venue_name='Chase Center', venue_type='Indoor Sports Arena', city_id=1, condition=[chase_conditions])
    alamo = Venue(venue_name='Alamo Drafthouse Cinema', venue_type='Indoor Theater', city_id=1, condition=[alamo_conditions])
    melting_pot = Venue(venue_name='The Melting Pot', venue_type='Indoor Restaurant', city_id=1, condition=[melting_pot_conditions])
    mile_high = Venue(venue_name='Mile High Stadium', venue_type='Outdoor Sports Arena', city_id=2, condition=[mile_high_conditions])
    red_rocks = Venue(venue_name='Red Rocks Amphitheatre', venue_type='Outdoor Theater', city_id=2, condition=[red_rocks_conditions])
    casa_bonita = Venue(venue_name="Casa Bonita", venue_type='Indoor Restaurant', city_id=2, condition=[casa_bonita_conditions])
    session.add(chase)
    session.add(alamo)
    session.add(melting_pot)
    session.add(mile_high)
    session.add(red_rocks)
    session.add(casa_bonita)
    session.commit()

    chase_review_1 = Review(score=4, venue=chase)
    chase_review_2 = Review(score=3, venue=chase)
    alamo_review_1 = Review(score=4, venue=alamo)
    alamo_review_2 = Review(score=1, venue=alamo)
    melting_pot_review_1 = Review(score=2, venue=melting_pot)
    melting_pot_review_2 = Review(score=4, venue=melting_pot)
    mile_high_review_1 = Review(score=4, venue=mile_high)
    mile_high_review_2 = Review(score=3, venue=mile_high)
    session.add(chase_review_1)
    session.add(chase_review_2)
    session.add(alamo_review_1)
    session.add(alamo_review_2)
    session.add(melting_pot_review_1)
    session.add(melting_pot_review_2)
    session.add(mile_high_review_1)
    session.add(mile_high_review_2)
    session.commit()

    first_denver_airport_forecast = Condition(date=date(2002, 9, 21), max_temperature=90, max_humidity=20, max_wind_speed=13, rain=0, visibility=100)
    second_denver_airport_forecast = Condition(date=date(2003, 10, 21), max_temperature=40, max_humidity=40, max_wind_speed=40, rain=10, visibility=85)
    first_omaha_airport_forecast = Condition(date=date(2022, 4, 29), max_temperature=65, max_humidity=0, max_wind_speed=60, rain=0, visibility=100)
    second_omaha_airport_forecast = Condition(date=date(2022, 5, 4), max_temperature=72, max_humidity=10, max_wind_speed=8, rain=5, visibility=92)
    lincoln = City(city_name='Lincoln', encompassing_geographic_entity='Nebraska', latitude=92.01, longitude=95.2)
    omaha = City(city_name='Omaha', encompassing_geographic_entity='Nebraska', latitude=91, longitude=93.4, conditions=[first_omaha_airport_forecast])
    omaha_airport = Airport(name='Omaha Airport', code='SEAL', latitude=90, longitude=90, cities=[lincoln, omaha], conditions=[first_omaha_airport_forecast, second_omaha_airport_forecast])
    denver_airport = Airport(name='Denver Airport', code='ABCD', latitude=120, longitude=57.4, cities=[omaha], conditions=[first_denver_airport_forecast, second_denver_airport_forecast])
    session.add(lincoln)
    session.add(omaha)
    session.add(omaha_airport)
    session.add(denver_airport)
    session.add(first_denver_airport_forecast)
    session.add(second_denver_airport_forecast)
    session.add(first_omaha_airport_forecast)
    session.add(second_omaha_airport_forecast)

    current_airport = Airport(name='Pacific Airport', latitude=90, longitude=90, code='AAAA')
    go_to_airport = Airport(name='Center Airport', latitude=88, longitude=91, code='BBBB')
    other_airport = Airport(name='Dodge Airport', latitude=86, longitude=94, code='CCCC')
    current_city = City(city_name='Blondo', latitude=90, longitude=90.02, airports=[current_airport], encompassing_geographic_entity='US')
    go_to_city = City(city_name='Maple', latitude=88, longitude=91.02, airports=[go_to_airport], encompassing_geographic_entity='US')
    other_city = City(city_name='Fort', latitude=86, longitude=94.02, airports=[other_airport], encompassing_geographic_entity='US')
    # 'Indoor Restaurant', 'Outdoor Restaurant', 'Indoor Theater', 'Outdoor Theater', 'Indoor Sports Arena', 'Outdoor Sports Arena'
    blondo_venue = Venue(venue_name='Mcdonalds', venue_type='Outdoor Restaurant', city=current_city)
    maple_venue_1 = Venue(venue_name='Burger King', venue_type='Outdoor Restaurant', city=go_to_city)
    maple_venue_2 = Venue(venue_name='Baxter Arena', venue_type='Outdoor Sports Arena', city=go_to_city)
    fort_venue_1 = Venue(venue_name='The Rose', venue_type='Outdoor Theater', city=other_city)
    fort_venue_2 = Venue(venue_name='Freddies', venue_type='Outdoor Restaurant', city=other_city)
    session.add(current_airport)
    session.add(go_to_airport)
    session.add(other_airport)
    session.add(current_city)
    session.add(go_to_city)
    session.add(other_city)
    session.add(blondo_venue)
    session.add(maple_venue_2)
    session.add(maple_venue_1)
    session.add(fort_venue_2)
    session.add(fort_venue_1)
    session.commit()


def main():
    try:
        #url = Database.construct_mysql_url('cse.unl.edu', 3306, 'kandrews', 'kandrews', 'qUc:6M')
        url = Database.construct_mysql_url('localhost', 33060, 'airports', 'root', 'cse1208')
        database = Database(url)
        database.ensure_tables_exist()
        session = database.create_session()
        add_starter_data(session)
        session.commit()
        print('Tables and records created.')
    except SQLAlchemyError as exception:
        print('Database setup failed!', file=stderr)
        print(f'Cause: {exception}', file=stderr)
        exit(1)


if __name__ == '__main__':
    main()
