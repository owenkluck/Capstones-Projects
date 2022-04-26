from datetime import date
from sys import stderr

from sqlalchemy.exc import SQLAlchemyError

from database import Database, City, Airport, Venue, Condition


def add_starter_data(session):
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

    lincoln = City(city_name='Lincoln', encompassing_geographic_entity='Nebraska', latitude=92.01, longitude=95.2)
    omaha = City(city_name='Omaha', encompassing_geographic_entity='Nebraska', latitude=91, longitude=93.4)
    first_denver_airport_forecast = Condition(date=date(2002, 9, 21), max_temperature=90, max_humidity=20, max_wind_speed=13, rain=0, visibility=100)
    second_denver_airport_forecast = Condition(date=date(2003, 10, 21), max_temperature=40, max_humidity=40, max_wind_speed=40, rain=10, visibility=85)
    first_omaha_airport_forecast = Condition(date=date(2022, 4, 7), max_temperature=65, max_humidity=0, max_wind_speed=60, rain=0, visibility=100)
    second_omaha_airport_forecast = Condition(date=date(2022, 5, 4), max_temperature=72, max_humidity=10, max_wind_speed=8, rain=5, visibility=92)
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


def main():
    try:
        url = Database.construct_mysql_url('cse.unl.edu', 3306, 'kandrews', 'kandrews', 'qUc:6M')
        #url = Database.construct_mysql_url('localhost', 33060, 'test', 'root', 'cse1208')
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
