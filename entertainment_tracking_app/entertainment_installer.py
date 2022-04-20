from sys import stderr

from sqlalchemy.exc import SQLAlchemyError

from entertainment import City, Venue, Condition, EntertainmentDatabase, VenueCondition


def add_starter_data(session):
    san_fran = City(city_name='San Francisco', latitude=37.8, longitude=-122.4, ege='California')
    denver = City(city_name='Denver', latitude=39.7, longitude=-105.0, ege='Colorado')
    session.add(san_fran)
    session.add(denver)
    session.commit()

    chase = Venue(venue_name='Chase Center', venue_type='Indoor Sports Arena', city_id=1)
    alamo = Venue(venue_name='Alamo Drafthouse Cinema', venue_type='Indoor Theater', city_id=1)
    melting_pot = Venue(venue_name='The Melting Pot', venue_type='Indoor Restaurant', city_id=1)
    mile_high = Venue(venue_name='Mile High Stadium', venue_type='Outdoor Sports Arena', city_id=2)
    red_rocks = Venue(venue_name='Red Rocks Amphitheatre', venue_type='Outdoor Theater', city_id=2)
    casa_bonita = Venue(venue_name="Casa Bonita", venue_type='Indoor Restaurant', city_id=2)
    session.add(chase)
    session.add(alamo)
    session.add(melting_pot)
    session.add(mile_high)
    session.add(red_rocks)
    session.add(casa_bonita)
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

    mile_high_vc = VenueCondition(venue_id=4, condition_id=1)
    red_rocks_vc = VenueCondition(venue_id=5, condition_id=2)
    chase_vc = VenueCondition(venue_id=1, condition_id=9)
    alamo_vc = VenueCondition(venue_id=2, condition_id=10)
    melting_pot_vc = VenueCondition(venue_id=3, condition_id=11)
    casa_bonita_vc = VenueCondition(venue_id=6, condition_id=12)
    session.add(mile_high_vc)
    session.add(red_rocks_vc)
    session.add(chase_vc)
    session.add(alamo_vc)
    session.add(melting_pot_vc)
    session.add(casa_bonita_vc)
    session.commit()


def main():
    try:
        url = EntertainmentDatabase.construct_mysql_url('localhost', 33060, 'entertainment', 'root', 'cse1208')
        entertainment_database = EntertainmentDatabase(url)
        entertainment_database.ensure_tables_exist()
        print('Tables created.')
        session = entertainment_database.create_session()
        add_starter_data(session)
        session.commit()
        print('Records created.')
    except SQLAlchemyError as exception:
        print('Database setup failed!', file=stderr)
        print(f'Cause: {exception}', file=stderr)
        exit(1)


if __name__ == '__main__':
    main()
