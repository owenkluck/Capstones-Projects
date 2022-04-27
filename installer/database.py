from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Persisted = declarative_base()


class City(Persisted):
    __tablename__ = 'cities'
    city_id = Column(Integer, primary_key=True, autoincrement=True)
    city_name = Column(String(256), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    encompassing_geographic_entity = Column(String(256), nullable=False)
    validated = Column(Boolean, default=False)
    venues = relationship('Venue', uselist=True, back_populates='city')
    airports = relationship('Airport', uselist=True, secondary='airport_cities', back_populates='cities')


class Venue(Persisted):
    __tablename__ = 'venues'
    venue_id = Column(Integer, primary_key=True, autoincrement=True)
    city_id = Column(Integer, ForeignKey('cities.city_id', ondelete='cascade'))
    itinerary_id = Column(Integer, ForeignKey('itineraries.itinerary_id', ondelete='CASCADE'))
    venue_name = Column(String(256), nullable=False)
    venue_type = Column(String(256), nullable=False)
    average_welp_score = Column(Float)
    welp_score_needs_update = Column(Boolean, default=False)
    condition = relationship('Condition', back_populates='venue', secondary='venue_conditions')
    city = relationship('City', back_populates='venues')
    reviews = relationship('Review', back_populates='venue')
    itinerary = relationship('Itinerary', back_populates='venues')


class Review(Persisted):
    __tablename__ = 'reviews'
    review_id = Column(Integer, primary_key=True, autoincrement=True)
    venue_id = Column(Integer, ForeignKey('venues.venue_id', ondelete='CASCADE'))
    score = Column(Integer, nullable=False)
    validated = Column(Boolean, default=False)
    venue = relationship('Venue', back_populates='reviews')


class Condition(Persisted):
    __tablename__ = 'conditions'
    condition_id = Column(Integer, primary_key=True, autoincrement=True)
    min_temperature = Column(Integer)
    max_temperature = Column(Integer)
    min_humidity = Column(Integer)
    max_humidity = Column(Integer)
    max_wind_speed = Column(Integer)
    rain = Column(Integer)
    visibility = Column(Integer)
    open_weather_code = Column(Integer)
    date = Column(Date)
    venue = relationship('Venue', uselist=True, back_populates='condition', secondary='venue_conditions')
    airport = relationship('Airport', back_populates='conditions')


class VenueCondition(Persisted):
    __tablename__ = 'venue_conditions'
    venue_id = Column(Integer, ForeignKey('venues.venue_id', ondelete='CASCADE'), primary_key=True)
    condition_id = Column(Integer, ForeignKey('conditions.condition_id', ondelete='CASCADE'), primary_key=True)


class Airport(Persisted):
    __tablename__ = 'airports'
    airport_id = Column(Integer, primary_key=True)
    condition_id = Column(Integer, ForeignKey('conditions.condition_id', ondelete='CASCADE'))
    name = Column(String(256), nullable=False)
    code = Column(String(256))
    longitude = Column(Float)
    latitude = Column(Float)
    validated = Column(Boolean, default=False)
    conditions = relationship('Condition', uselist=True, back_populates='airport')
    cities = relationship('City', uselist=True, secondary='airport_cities', back_populates='airports')


class AirportCity(Persisted):
    __tablename__ = 'airport_cities'
    airport_id = Column(Integer, ForeignKey('airports.airport_id', ondelete='CASCADE'), primary_key=True)
    city_id = Column(Integer, ForeignKey('cities.city_id', ondelete='CASCADE'), primary_key=True)


class Itinerary(Persisted):
    __tablename__ = 'itineraries'
    itinerary_id = Column(Integer, primary_key=True, autoincrement=True)
    airport_id = Column(Integer, ForeignKey('airports.airport_id', ondelete='CASCADE'))
    city_id = Column(Integer, ForeignKey('cities.city_id', ondelete='CASCADE'))
    venues = relationship('Venue', uselist=True, back_populates='itinerary')
    date = Column(Date)


class Database(object):
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
