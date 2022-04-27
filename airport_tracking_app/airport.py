from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Persisted = declarative_base()


class Airport(Persisted):
    __tablename__ = 'airports'
    airport_id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False)
    code = Column(String(256))
    location = Column(String(256))
    forecasts = relationship('Forecast', uselist=True, back_populates='airport')
    cities = relationship('City', uselist=True, secondary='airport_cities', back_populates='airports')


class City(Persisted):
    __tablename__ = 'cities'
    city_id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False)
    geographic_entity = Column(String(256), nullable=False)
    location = Column(String(256))
    forecasts = relationship('Forecast', uselist=True, back_populates='city')
    airports = relationship('Airport', uselist=True, secondary='airport_cities', back_populates='cities')


class AirportCity(Persisted):
    __tablename__ = 'airport_cities'
    airport_id = Column(Integer, ForeignKey('airports.airport_id', ondelete='CASCADE'), primary_key=True)
    city_id = Column(Integer, ForeignKey('cities.city_id', ondelete='CASCADE'), primary_key=True)


class Forecast(Persisted):
    __tablename__ = 'forecasts'
    forecast_id = Column(Integer, primary_key=True)
    airport_id = Column(Integer, ForeignKey('airports.airport_id'))
    city_id = Column(Integer, ForeignKey('cities.city_id'))
    date = Column(Date)
    temperature = Column(Float)
    humidity = Column(Float)
    wind_speed = Column(Float)
    rain = Column(Float)
    visibility = Column(Float)
    airport = relationship('Airport', back_populates='forecasts')
    city = relationship('City', back_populates='forecasts')


class AirportDatabase(object):
    @staticmethod
    def construct_mysql_url(authority, port, database, username, password):
        return f'mysql+mysqlconnector://{username}:{password}@{authority}:{port}/{database}'

    @staticmethod
    def construct_in_memory_url():
        return 'sqlite:///'

    def __init__(self, url):
        self.engine = create_engine(url)
        self.Session = sessionmaker()
        self.Session.configure(bind=self.engine)

    def ensure_tables_exist(self):
        Persisted.metadata.create_all(self.engine)

    def create_session(self):
        return self.Session()
