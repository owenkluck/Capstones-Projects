from airport import Airport, City, AirportDatabase, Forecast
from sys import stderr
from datetime import date
from sqlalchemy.exc import SQLAlchemyError


def add_starter_data(session):
    lincoln = City(name='Lincoln', geographic_entity='Nebraska', location='92.01 95.2')
    session.add(lincoln)
    omaha = City(name='Omaha', geographic_entity='Nebraska', location='91 93.4')
    session.add(omaha)
    omaha_airport = Airport(name='Omaha Airport', code='SEAL', location='90 90', cities=[lincoln, omaha])
    session.add(omaha_airport)
    denver_airport = Airport(name='Denver Airport', code='ABCD', location='120 57.4', cities=[omaha])
    session.add(denver_airport)
    first_denver_airport_forecast = Forecast(date=date(2002, 9, 21), temperature=90, humidity=20, wind_speed=13, rain=0, visibility=100, airport=denver_airport)
    session.add(first_denver_airport_forecast)
    second_denver_airport_forecast = Forecast(date=date(2003, 10, 21), temperature=40, humidity=40, wind_speed=40, rain=10, visibility=85, airport=denver_airport)
    session.add(second_denver_airport_forecast)
    first_omaha_airport_forecast = Forecast(date=date(2022, 4, 7), temperature=65, humidity=0, wind_speed=60, rain=0, visibility=100, airport=omaha_airport)
    session.add(first_omaha_airport_forecast)
    second_omaha_airport_forecast = Forecast(date=date(2022, 5, 4), temperature=72, humidity=10, wind_speed=8, rain=5, visibility=92, airport=omaha_airport)
    session.add(second_omaha_airport_forecast)


def main():
    try:
        url = AirportDatabase.construct_mysql_url('localhost', 33060, 'airports', 'root', 'cse1208')
        airport_database = AirportDatabase(url)
        airport_database.ensure_tables_exist()
        print('Tables created.')
        session = airport_database.create_session()
        add_starter_data(session)
        session.commit()
        print('Records created.')
    except SQLAlchemyError as exception:
        print('Database setup failed!', file=stderr)
        print(f'Cause: {exception}', file=stderr)
        exit(1)


if __name__ == '__main__':
    main()
