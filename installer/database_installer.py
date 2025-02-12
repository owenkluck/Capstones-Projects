from datetime import date
from sys import stderr
import json
from sqlalchemy.exc import SQLAlchemyError
from database import Database, City, Airport, Venue, Condition, Review


def add_starter_data(session):
    worms = City(city_name='Worms', latitude=41.1, longitude=-98.3, encompassing_geographic_entity='United States')
    denver = City(city_name='Denver', latitude=39.7, longitude=-105.0, encompassing_geographic_entity='United States')
    session.add(worms)
    session.add(denver)
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

    chase = Venue(venue_name='Chase Center', venue_type='Indoor Sports Arena', cities=[worms],
                  condition=[chase_conditions])
    alamo = Venue(venue_name='Alamo Drafthouse Cinema', venue_type='Indoor Theater', cities=[worms],
                  condition=[alamo_conditions])
    melting_pot = Venue(venue_name='The Melting Pot', venue_type='Indoor Restaurant', cities=[worms],
                        condition=[melting_pot_conditions])
    mile_high = Venue(venue_name='Mile High Stadium', venue_type='Outdoor Sports Arena', cities=[denver],
                      condition=[mile_high_conditions])
    red_rocks = Venue(venue_name='Red Rocks Amphitheatre', venue_type='Outdoor Theater', cities=[denver],
                      condition=[red_rocks_conditions])
    casa_bonita = Venue(venue_name="Casa Bonita", venue_type='Indoor Restaurant', cities=[denver],
                        condition=[casa_bonita_conditions])
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

    first_denver_airport_forecast = Condition(date=date(2002, 9, 21), max_temperature=90, max_humidity=20,
                                              max_wind_speed=13, rain=0, visibility=100)
    second_denver_airport_forecast = Condition(date=date(2003, 10, 21), max_temperature=40, max_humidity=40,
                                               max_wind_speed=40, rain=10, visibility=85)
    first_omaha_airport_forecast = Condition(date=date(2022, 4, 29), max_temperature=65, max_humidity=0,
                                             max_wind_speed=60, rain=0, visibility=100)
    second_omaha_airport_forecast = Condition(date=date(2022, 5, 4), max_temperature=72, max_humidity=10,
                                              max_wind_speed=8, rain=5, visibility=92)
    session.add(first_denver_airport_forecast)
    session.add(second_denver_airport_forecast)
    session.add(first_omaha_airport_forecast)
    session.add(second_omaha_airport_forecast)

    blondo_venue = Venue(venue_name='McDonalds', venue_type='Outdoor Restaurant')
    maple_venue_1 = Venue(venue_name='Burger King', venue_type='Outdoor Restaurant')
    maple_venue_2 = Venue(venue_name='Baxter Arena', venue_type='Outdoor Sports Arena')
    fort_venue_1 = Venue(venue_name='The Rose', venue_type='Outdoor Theater')
    fort_venue_2 = Venue(venue_name='Freddies', venue_type='Outdoor Restaurant')
    session.add(blondo_venue)
    session.add(maple_venue_2)
    session.add(maple_venue_1)
    session.add(fort_venue_2)
    session.add(fort_venue_1)
    session.commit()

    b1 = City(city_name='Lagos', encompassing_geographic_entity='Nigeria', latitude=6.45, longitude=3.4,
              venues=[blondo_venue, fort_venue_1])
    b2 = City(city_name='Cotonou', encompassing_geographic_entity='Benin', latitude=6.402, longitude=2.518,
              venues=[fort_venue_2, maple_venue_2])
    b3 = City(city_name='Abomey', encompassing_geographic_entity='Benin', latitude=7.1853, longitude=1.9914,
              venues=[blondo_venue, fort_venue_1])
    session.add(b1)
    session.add(b2)
    session.add(b3)
    a1 = Airport(name='Cadjehoun Airport', latitude=6.35723, longitude=2.38435, code='DBBB', cities=[b1, b2, b3])
    session.add(a1)
    b1 = City(city_name='Ouagadougou', encompassing_geographic_entity='Burkina Faso', latitude=12.3686,
              longitude=-1.5275, venues=[blondo_venue, fort_venue_1])
    b2 = City(city_name='Reo', encompassing_geographic_entity='Burkina Faso', latitude=12.3167, longitude=-2.4667,
              venues=[blondo_venue, fort_venue_1])
    b3 = City(city_name='Yako', encompassing_geographic_entity='Burkina Faso', latitude=12.9667, longitude=-2.2667,
              venues=[fort_venue_2, maple_venue_2])
    session.add(b1)
    session.add(b2)
    session.add(b3)
    a1 = Airport(name='Ouagadougou Airport', latitude=12.3532, longitude=-1.51242, code='DFFD', cities=[b1, b2, b3])
    session.add(a1)
    b1 = City(city_name='Bobo-Dioulasso', encompassing_geographic_entity='Burkina Faso', latitude=11.1833,
              longitude=-4.2833, venues=[blondo_venue, fort_venue_1])
    b2 = City(city_name='Gaoua', encompassing_geographic_entity='Burkina Faso', latitude=10.3167, longitude=-3.1667,
              venues=[fort_venue_2, maple_venue_2])
    b3 = City(city_name='Salanso', encompassing_geographic_entity='Burkina Faso', latitude=12.1833, longitude=-4.0833,
              venues=[blondo_venue, fort_venue_1])
    session.add(b1)
    session.add(b2)
    session.add(b3)
    a1 = Airport(name='Bobo Dioulasso Airport', latitude=11.1601, longitude=-4.33097, code='DFOO', cities=[b1, b2, b3])
    session.add(a1)
    b1 = City(city_name='Accra', encompassing_geographic_entity='Ghana', latitude=5.6037, longitude=-0.187,
              venues=[blondo_venue, fort_venue_1])
    b2 = City(city_name='Tema', encompassing_geographic_entity='Ghana', latitude=5.6667, longitude=-0.0167,
              venues=[blondo_venue, fort_venue_1])
    b3 = City(city_name='Winneba', encompassing_geographic_entity='Ghana', latitude=5.35, longitude=-0.6333,
              venues=[fort_venue_2, maple_venue_2])
    session.add(b1)
    session.add(b2)
    session.add(b3)
    a1 = Airport(name='Kotoka International Airport', latitude='5.60519', longitude='-0.166786', code='DGAA',
                 cities=[b1, b2, b3])
    session.add(a1)
    b1 = City(city_name='Tamale', encompassing_geographic_entity='Ghana', latitude=9.4075, longitude=-0.8533,
              venues=[fort_venue_2, maple_venue_2])
    b2 = City(city_name='Nalerigu', encompassing_geographic_entity='Ghana', latitude=10.5273, longitude=-0.3698,
              venues=[blondo_venue, fort_venue_1])
    b3 = City(city_name='Po', encompassing_geographic_entity='Burkina Faso', latitude=11.1667, longitude=-1.15,
              venues=[blondo_venue, fort_venue_1])
    session.add(b1)
    session.add(b2)
    session.add(b3)
    a1 = Airport(name='Tamale Airport', latitude='9.55719', longitude='-0.863214', code='DGLE', cities=[b1, b2, b3])
    session.add(a1)
    b1 = City(city_name='Wa', encompassing_geographic_entity='Ghana', latitude=10.0667, longitude=-2.5,
              venues=[fort_venue_2, maple_venue_2])
    b2 = City(city_name='Damongo', encompassing_geographic_entity='Ghana', latitude=9.083, longitude=-1.8188,
              venues=[blondo_venue, fort_venue_1])
    b3 = City(city_name='Diebougou', encompassing_geographic_entity='Burkina Faso', latitude=10.9667, longitude=-3.25,
              venues=[fort_venue_2, maple_venue_2])
    session.add(b1)
    session.add(b2)
    session.add(b3)
    a1 = Airport(name='Wa Airport', latitude='10.0827', longitude='-2.50769', code='DGLW', cities=[b1, b2, b3])
    session.add(a1)
    b1 = City(city_name='Kumasi', encompassing_geographic_entity='Ghana', latitude=6.6833, longitude=-1.6167,
              venues=[fort_venue_2, maple_venue_2])
    b2 = City(city_name='Abengourou', encompassing_geographic_entity='Côte d\'Ivoire', latitude=6.7297,
              longitude=-3.4964, venues=[blondo_venue, fort_venue_1])
    b3 = City(city_name='Bondoukou', encompassing_geographic_entity='Côte d\'Ivoire', latitude=8.0304, longitude=-2.8,
              venues=[fort_venue_2, maple_venue_2])
    session.add(b1)
    session.add(b2)
    session.add(b3)
    a1 = Airport(name='Sunyani Airport', latitude='7.36183', longitude='-2.32876', code='DGSN', cities=[b1, b2, b3])
    session.add(a1)
    b1 = City(city_name='Aboisso', encompassing_geographic_entity='Côte d\'Ivoire', latitude=5.4667, longitude=-3.2,
              venues=[blondo_venue, fort_venue_1])
    b2 = City(city_name='Cape Coast', encompassing_geographic_entity='Ghana', latitude=5.1, longitude=-1.25,
              venues=[fort_venue_2, maple_venue_2])
    b3 = City(city_name='Obuase', encompassing_geographic_entity='Ghana', latitude=6.2, longitude=-1.6833,
              venues=[fort_venue_2, maple_venue_2])
    session.add(b1)
    session.add(b2)
    session.add(b3)
    a1 = Airport(name='Takoradi Airport', latitude='4.89606', longitude='-1.77476', code='DGTK', cities=[b1, b2, b3])
    session.add(a1)
    b1 = City(city_name='Abidjan', encompassing_geographic_entity='Côte d\'Ivoire', latitude=5.3364, longitude=-4.0267,
              venues=[blondo_venue, fort_venue_1])
    b2 = City(city_name='Divo', encompassing_geographic_entity='Côte d\'Ivoire', latitude=5.8372, longitude=-5.3572,
              venues=[fort_venue_2, maple_venue_2])
    b3 = City(city_name='Dabou', encompassing_geographic_entity='Côte d\'Ivoire', latitude=5.3256, longitude=-4.3767,
              venues=[blondo_venue, fort_venue_1])
    session.add(b1)
    session.add(b2)
    session.add(b3)
    a1 = Airport(name='Port Bouet Airport', latitude='5.26139', longitude='-3.92629', code='DIAP', cities=[b1, b2, b3])
    session.add(a1)
    b1 = City(city_name='Bissau', encompassing_geographic_entity='Guinea-Bissau', latitude=11.8592, longitude=-15.5956,
              venues=[blondo_venue, fort_venue_1])
    b2 = City(city_name='Ziguinchor', encompassing_geographic_entity='Senegal', latitude=12.5833, longitude=-16.2667,
              venues=[fort_venue_2, maple_venue_2])
    b3 = City(city_name='Kolda', encompassing_geographic_entity='Senegal', latitude=12.8958, longitude=-14.9408,
              venues=[fort_venue_2, maple_venue_2])
    session.add(b1)
    session.add(b2)
    session.add(b3)
    a1 = Airport(name='Kolda North Airport', latitude='12.8985', longitude='-14.9681', code='GODK', cities=[b1, b2, b3])
    session.add(a1)
    b1 = City(city_name='Bauchi', encompassing_geographic_entity='Nigeria', latitude=10.3158, longitude=9.8442,
              venues=[fort_venue_2, maple_venue_2])
    b2 = City(city_name='Bauchi', encompassing_geographic_entity='Nigeria', latitude=10.3158, longitude=9.8442,
              venues=[blondo_venue, fort_venue_1])
    b3 = City(city_name='Wukari', encompassing_geographic_entity='Nigeria', latitude=7.8704, longitude=9.78,
              venues=[fort_venue_2, maple_venue_2])
    session.add(b1)
    session.add(b2)
    session.add(b3)
    a1 = Airport(name='Jalingo Airport', latitude='38.90059', longitude='40.2795', code='DNJA', cities=[b1, b2, b3])
    session.add(a1)
    b1 = City(city_name='Sumbawanga', encompassing_geographic_entity='Tanzania', latitude=-7.9667, longitude=31.6167,
              venues=[blondo_venue, fort_venue_1])
    b2 = City(city_name='Karonga', encompassing_geographic_entity='Malawi', latitude=-9.9329, longitude=33.9333,
              venues=[fort_venue_2, maple_venue_2])
    b3 = City(city_name='Tukuyu', encompassing_geographic_entity='Tanzania', latitude=-9.2583, longitude=33.6417,
              venues=[blondo_venue, fort_venue_1])
    session.add(b1)
    session.add(b2)
    session.add(b3)
    a1 = Airport(name='Songwe Airport', latitude='-8.91994', longitude='33.274', code='HTGW', cities=[b1, b2, b3])
    session.add(a1)
    b1 = City(city_name='Kigali', encompassing_geographic_entity='Rwanda', latitude=-1.9536, longitude=30.0606,
              venues=[blondo_venue, fort_venue_1])
    b2 = City(city_name='Gitega', encompassing_geographic_entity='Burundi', latitude=-3.4283, longitude=29.925,
              venues=[fort_venue_2, maple_venue_2])
    b3 = City(city_name='Bujumbura', encompassing_geographic_entity='Burundi', latitude=-3.3825, longitude=29.3611,
              venues=[blondo_venue, fort_venue_1])
    session.add(b1)
    session.add(b2)
    session.add(b3)
    a1 = Airport(name='Gitega Airport', latitude='-3.41721', longitude='29.9113', code='HBBE', cities=[b1, b2, b3])
    session.add(a1)
    b1 = City(city_name='Mwanza', encompassing_geographic_entity='Tanzania', latitude=-2.5167, longitude=32.9,
              venues=[blondo_venue, fort_venue_1])
    b2 = City(city_name='Shinyanga', encompassing_geographic_entity='Tanzania', latitude=-3.6619, longitude=33.4231,
              venues=[fort_venue_2, maple_venue_2])
    b3 = City(city_name='Kakonko', encompassing_geographic_entity='Tanzania', latitude=-3.2796, longitude=30.96,
              venues=[blondo_venue, fort_venue_1])
    session.add(b1)
    session.add(b2)
    session.add(b3)
    a1 = Airport(name='Mchauru Airport', latitude='-2.81367', longitude='32.1725', code='HTRU', cities=[b1, b2, b3])
    session.add(a1)
    b1 = City(city_name='Juba', encompassing_geographic_entity='South Sudan', latitude=4.85, longitude=31.6,
              venues=[blondo_venue, fort_venue_1])
    b2 = City(city_name='Gulu', encompassing_geographic_entity='Uganda', latitude=2.7667, longitude=32.3056,
              venues=[fort_venue_2, maple_venue_2])
    b3 = City(city_name='Yei', encompassing_geographic_entity='South Sudan', latitude=4.0904, longitude=30.68,
              venues=[fort_venue_2, maple_venue_2])
    session.add(b1)
    session.add(b2)
    session.add(b3)
    a1 = Airport(name='Yei Airport', latitude='4.13028', longitude='30.7281', code='HSYE', cities=[b1, b2, b3])
    session.add(a1)
    b1 = City(city_name='Ndola', encompassing_geographic_entity='Zambia', latitude=-12.9683, longitude=28.6337,
              venues=[blondo_venue, fort_venue_1])
    b2 = City(city_name='Mufulira', encompassing_geographic_entity='Zambia', latitude=-12.5546, longitude=28.2604,
              venues=[fort_venue_2, maple_venue_2])
    b3 = City(city_name='Chingola', encompassing_geographic_entity='Zambia', latitude=-12.5447, longitude=27.8708,
              venues=[fort_venue_2, maple_venue_2])
    session.add(b1)
    session.add(b2)
    session.add(b3)
    a1 = Airport(name='Simon Mwansa Kapwepwe International Airport', latitude='-12.9981', longitude='28.6649',
                 code='FLND', cities=[b1, b2, b3])
    session.add(a1)
    b1 = City(city_name='Luanshya', encompassing_geographic_entity='Zambia', latitude=-33.1333, longitude=28.4,
              venues=[blondo_venue, fort_venue_1])
    b2 = City(city_name='Kipushi', encompassing_geographic_entity='Congo (Kinshasa)', latitude=-31.76, longitude=27.25,
              venues=[fort_venue_2, maple_venue_2])
    b3 = City(city_name='Chililabombwe', encompassing_geographic_entity='Zambia', latitude=-30.3667, longitude=27.8333,
              venues=[fort_venue_2, maple_venue_2])
    session.add(b1)
    session.add(b2)
    session.add(b3)
    a1 = Airport(name='Southdowns Airport', latitude='-32.9005', longitude='28.1499', code='FLSO')
    session.add(a1)
    a1 = Airport(name='Diego Garcia Naval Support Facility', latitude='-7.31327', longitude='72.4111', code='FJDG')
    session.add(a1)
    b1 = City(city_name='Antsiranana', encompassing_geographic_entity='Madagascar', latitude=-12.2765,
              longitude=49.3115, venues=[blondo_venue, fort_venue_1])
    b2 = City(city_name='Sambava', encompassing_geographic_entity='Madagascar', latitude=-14.2662, longitude=50.1666,
              venues=[fort_venue_2, maple_venue_2])
    b3 = City(city_name='Ambanja', encompassing_geographic_entity='Madagascar', latitude=-13.6786, longitude=48.4522,
              venues=[fort_venue_2, maple_venue_2])
    session.add(b1)
    session.add(b2)
    session.add(b3)
    a1 = Airport(name='Ambilobe Airport', latitude='-13.1884', longitude='48.988', code='FMNE', cities=[b1, b2, b3])
    session.add(a1)
    b1 = City(city_name='Un\'goofaaru', encompassing_geographic_entity='Maldives', latitude=5.6681, longitude=73.0302,
              venues=[blondo_venue, fort_venue_1])
    b2 = City(city_name='Naifaru', encompassing_geographic_entity='Maldives', latitude=5.4442, longitude=73.3662,
              venues=[fort_venue_2, maple_venue_2])
    b3 = City(city_name='Funadhoo', encompassing_geographic_entity='Maldives', latitude=6.1509, longitude=73.2901,
              venues=[fort_venue_2, maple_venue_2])
    session.add(b1)
    session.add(b2)
    session.add(b3)
    a1 = Airport(name='Ifuru Airport', latitude='5.7083', longitude='73.025', code='VREI', cities=[b1, b2, b3])
    session.add(a1)
    b1 = City(city_name='Kudahuvadhoo', encompassing_geographic_entity='Maldives', latitude=2.6717, longitude=72.8936,
              venues=[blondo_venue, fort_venue_1])
    b2 = City(city_name='Thinadhoo', encompassing_geographic_entity='Maldives', latitude=0.5303, longitude=72.9967,
              venues=[fort_venue_2, maple_venue_2])
    b3 = City(city_name='Veymandoo', encompassing_geographic_entity='Maldives', latitude=2.1878, longitude=73.095,
              venues=[fort_venue_2, maple_venue_2])
    session.add(b1)
    session.add(b2)
    session.add(b3)
    a1 = Airport(name='Thimarafushi Airport', latitude='2.211', longitude='73.1533', code='VRNT', cities=[b1, b2, b3])
    session.add(a1)
    b1 = City(city_name='Viligili', encompassing_geographic_entity='Maldives', latitude=0.7539, longitude=73.4353,
              venues=[fort_venue_2, maple_venue_2])
    b2 = City(city_name='Foammulah', encompassing_geographic_entity='Maldives', latitude=-0.3, longitude=73.4256,
              venues=[blondo_venue, fort_venue_1])
    b3 = City(city_name='Fonadhoo', encompassing_geographic_entity='Maldives', latitude=1.8342, longitude=73.5031,
              venues=[fort_venue_2, maple_venue_2])
    session.add(b1)
    session.add(b2)
    session.add(b3)
    a1 = Airport(name='Kooddoo Airport', latitude='30.7324', longitude='73.4336', code='VRMO', cities=[b1, b2, b3])
    session.add(a1)
    b1 = City(city_name='Ta`izz', encompassing_geographic_entity='Yemen', latitude=13.5789, longitude=44.0219,
              venues=[blondo_venue, fort_venue_1])
    b2 = City(city_name='Aden', encompassing_geographic_entity='Yemen', latitude=12.8, longitude=45.0333,
              venues=[fort_venue_2, maple_venue_2])
    b3 = City(city_name='Ibb', encompassing_geographic_entity='Yemen', latitude=13.9667, longitude=44.1667,
              venues=[blondo_venue, fort_venue_1])
    session.add(b1)
    session.add(b2)
    session.add(b3)
    a1 = Airport(name='Aden International Airport', latitude='30.8295', longitude='45.0288', code='OYAA',
                 cities=[b1, b2, b3])
    session.add(a1)
    b1 = City(city_name='Colombo', encompassing_geographic_entity='Sri Lanka', latitude=6.9167, longitude=79.8333,
              venues=[fort_venue_2, maple_venue_2])
    b2 = City(city_name='Sri Jayewardenepura Kotte', encompassing_geographic_entity='Sri Lanka', latitude=6.9,
              longitude=79.9164, venues=[blondo_venue, fort_venue_1])
    b3 = City(city_name='Moratuwa', encompassing_geographic_entity='Sri Lanka', latitude=6.7804, longitude=79.88,
              venues=[blondo_venue, fort_venue_1])
    session.add(b1)
    session.add(b2)
    session.add(b3)
    a1 = Airport(name='Bandaranaike International Colombo Airport', latitude='7.18076', longitude='79.8841',
                 code='VCBI', cities=[b1, b2, b3])
    session.add(a1)
    b1 = City(city_name='Negombo', encompassing_geographic_entity='Sri Lanka', latitude=7.2111, longitude=79.8386,
              venues=[fort_venue_2, maple_venue_2])
    b2 = City(city_name='Kandy', encompassing_geographic_entity='Sri Lanka', latitude=7.297, longitude=80.6385,
              venues=[blondo_venue, fort_venue_1])
    b3 = City(city_name='Galle', encompassing_geographic_entity='Sri Lanka', latitude=6.0395, longitude=80.2194,
              venues=[fort_venue_2, maple_venue_2])
    session.add(b1)
    session.add(b2)
    session.add(b3)
    a1 = Airport(name='Colombo Ratmalana Airport', latitude='6.82199', longitude='79.8862', code='VCCC',
                 cities=[b1, b2, b3])
    session.add(a1)
    b1 = City(city_name='Semey', encompassing_geographic_entity='Kazakhstan', latitude=50.4111, longitude=80.2275,
              venues=[blondo_venue, fort_venue_1])
    b2 = City(city_name='Gornyak', encompassing_geographic_entity='Russia', latitude=51.0, longitude=81.4667,
              venues=[fort_venue_2, maple_venue_2])
    b3 = City(city_name='Shar', encompassing_geographic_entity='Kazakhstan', latitude=49.6003, longitude=81.0549,
              venues=[blondo_venue, fort_venue_1])
    session.add(b1)
    session.add(b2)
    session.add(b3)
    a1 = Airport(name='Semipalatinsk Airport', latitude='50.3513', longitude='80.2344', code='UASS',
                 cities=[b1, b2, b3])
    session.add(a1)
    b1 = City(city_name='Shache', encompassing_geographic_entity='China', latitude=38.4261, longitude=77.25,
              venues=[fort_venue_2, maple_venue_2])
    b2 = City(city_name='Kashgar', encompassing_geographic_entity='China', latitude=39.45, longitude=75.9833,
              venues=[blondo_venue, fort_venue_1])
    b3 = City(city_name='Kargilik', encompassing_geographic_entity='China', latitude=37.8822, longitude=77.4162,
              venues=[fort_venue_2, maple_venue_2])
    session.add(b1)
    session.add(b2)
    session.add(b3)
    a1 = Airport(name='Yeerqiang Airport', latitude='38.2811', longitude='77.0752', code='ZWSC', cities=[b1, b2, b3])
    session.add(a1)
    b1 = City(city_name='Gabasumdo', encompassing_geographic_entity='China', latitude=35.2554, longitude=100.569,
              venues=[blondo_venue, fort_venue_1])
    b2 = City(city_name='Lajia', encompassing_geographic_entity='China', latitude=34.6818, longitude=100.639,
              venues=[fort_venue_2, maple_venue_2])
    b3 = City(city_name='Zequ', encompassing_geographic_entity='China', latitude=35.0376, longitude=101.461,
              venues=[fort_venue_2, maple_venue_2])
    session.add(b1)
    session.add(b2)
    session.add(b3)
    a1 = Airport(name='Golog Maqin Airport', latitude='34.4181', longitude='100.301', code='ZLGL', cities=[b1, b2, b3])
    session.add(a1)
    b1 = City(city_name='Wuwei', encompassing_geographic_entity='China', latitude=37.9278, longitude=102.633,
              venues=[fort_venue_2, maple_venue_2])
    b2 = City(city_name='Jinchang', encompassing_geographic_entity='China', latitude=38.5168, longitude=102.187,
              venues=[blondo_venue, fort_venue_1])
    b3 = City(city_name='Qingquan', encompassing_geographic_entity='China', latitude=38.7823, longitude=101.083,
              venues=[fort_venue_2, maple_venue_2])
    session.add(b1)
    session.add(b2)
    session.add(b3)
    a1 = Airport(name='Alxa Right Banner Badanjilin Airport', latitude='39.225', longitude='101.546', code='ZBAR',
                 cities=[b1, b2, b3])
    session.add(a1)
    b1 = City(city_name='Jiaojiazhuang', encompassing_geographic_entity='China', latitude=38.2636, longitude=101.833,
              venues=[blondo_venue, fort_venue_1])
    b2 = City(city_name='Jinta', encompassing_geographic_entity='China', latitude=37.8573, longitude=102.577,
              venues=[fort_venue_2, maple_venue_2])
    b3 = City(city_name='Liuba', encompassing_geographic_entity='China', latitude=38.1634, longitude=102.149,
              venues=[fort_venue_2, maple_venue_2])
    session.add(b1)
    session.add(b2)
    session.add(b3)
    a1 = Airport(name='Jinchuan Airport', latitude='38.5422', longitude='102.348', code='ZLJC', cities=[b1, b2, b3])
    session.add(a1)
    b1 = City(city_name='Beijing', encompassing_geographic_entity='China', latitude=39.904, longitude=116.408,
              venues=[blondo_venue, fort_venue_1])
    b2 = City(city_name='Baoding', encompassing_geographic_entity='China', latitude=38.8671, longitude=115.484,
              venues=[fort_venue_2, maple_venue_2])
    b3 = City(city_name='Tianjin', encompassing_geographic_entity='China', latitude=39.1467, longitude=117.206,
              venues=[fort_venue_2, maple_venue_2])
    session.add(b1)
    session.add(b2)
    session.add(b3)
    a1 = Airport(name='Beijing Xijiao Airport', latitude='39.9608', longitude='116.257', code='ZBBB',
                 cities=[b1, b2, b3])
    session.add(a1)
    b1 = City(city_name='Changchun', encompassing_geographic_entity='China', latitude=43.9, longitude=125.2,
              venues=[fort_venue_2, maple_venue_2])
    b2 = City(city_name='Gongzhuling', encompassing_geographic_entity='China', latitude=43.5036, longitude=124.809,
              venues=[blondo_venue, fort_venue_1])
    b3 = City(city_name='Dehui', encompassing_geographic_entity='China', latitude=44.5323, longitude=125.697,
              venues=[fort_venue_2, maple_venue_2])
    session.add(b1)
    session.add(b2)
    session.add(b3)
    a1 = Airport(name='Songyuan Chaganhu Airport', latitude='44.9381', longitude='124.55', code='ZYSQ',
                 cities=[b1, b2, b3])
    session.add(a1)
    b1 = City(city_name='Hohhot', encompassing_geographic_entity='China', latitude=40.8151, longitude=111.663,
              venues=[fort_venue_2, maple_venue_2])
    b2 = City(city_name='Xiping', encompassing_geographic_entity='China', latitude=40.082, longitude=113.298,
              venues=[fort_venue_2, maple_venue_2])
    b3 = City(city_name='Beichengqu', encompassing_geographic_entity='China', latitude=40.4348, longitude=113.157,
              venues=[blondo_venue, fort_venue_1])
    session.add(b1)
    session.add(b2)
    session.add(b3)
    a1 = Airport(name='Ulanqab Jining Airport', latitude='41.1297', longitude='113.108', code='ZBUC',
                 cities=[b1, b2, b3])
    session.add(a1)
    b1 = City(city_name='Hiroshima', encompassing_geographic_entity='Japan', latitude=34.4, longitude=132.45,
              venues=[fort_venue_2, maple_venue_2])
    b2 = City(city_name='Kitakyushu', encompassing_geographic_entity='Japan', latitude=33.8833, longitude=130.883,
              venues=[blondo_venue, fort_venue_1])
    b3 = City(city_name='Fukuyama', encompassing_geographic_entity='Japan', latitude=34.4858, longitude=133.363,
              venues=[fort_venue_2, maple_venue_2])
    session.add(b1)
    session.add(b2)
    session.add(b3)
    a1 = Airport(name='Iwakuni Marine Corps Air Station', latitude='34.1439', longitude='132.236', code='RJOI',
                 cities=[b1, b2, b3])
    session.add(a1)
    b1 = City(city_name='Kushiro', encompassing_geographic_entity='Japan', latitude=42.9833, longitude=144.383,
              venues=[blondo_venue, fort_venue_1])
    b2 = City(city_name='Koencho', encompassing_geographic_entity='Japan', latitude=43.8081, longitude=143.894,
              venues=[fort_venue_2, maple_venue_2])
    b3 = City(city_name='Abashiri', encompassing_geographic_entity='Japan', latitude=44.0206, longitude=144.274,
              venues=[fort_venue_2, maple_venue_2])
    session.add(b1)
    session.add(b2)
    session.add(b3)
    a1 = Airport(name='Kenebetsu JASDF Airfield', latitude='43.4252', longitude='144.741', code='RJCS',
                 cities=[b1, b2, b3])
    session.add(a1)
    a1 = Airport(name='Nikolayevsk-na-Amure Airport', latitude='53.155', longitude='140.65', code='UHNN',
                 cities=[b1, b2, b3])
    session.add(a1)
    b1 = City(city_name='Nikolayevsk-na-Amure', encompassing_geographic_entity='Russia', latitude=53.15,
              longitude=140.733, venues=[blondo_venue, fort_venue_1])
    session.add(b1)
    a1 = Airport(name='Akeno Airport', latitude='34.5333', longitude='136.672', code='RJOE', cities=[b1])
    session.add(a1)
    b1 = City(city_name='Nagoya', encompassing_geographic_entity='Japan', latitude=35.1167, longitude=136.933,
              venues=[blondo_venue, fort_venue_1])
    b2 = City(city_name='Toyohashi', encompassing_geographic_entity='Japan', latitude=34.7692, longitude=137.392,
              venues=[fort_venue_2, maple_venue_2])
    b3 = City(city_name='Takatsuki', encompassing_geographic_entity='Japan', latitude=34.85, longitude=135.617,
              venues=[blondo_venue, fort_venue_1])
    session.add(b1)
    session.add(b2)
    session.add(b3)
    a1 = Airport(name='Yelizovo Airport', latitude='53.1679', longitude='158.454', code='UHPP', cities=[b1, b2, b3])
    session.add(a1)
    b1 = City(city_name='Tokyo', encompassing_geographic_entity='Japan', latitude=35.6839, longitude=139.774,
              venues=[fort_venue_2, maple_venue_2])
    b2 = City(city_name='Yokohama', encompassing_geographic_entity='Japan', latitude=35.4333, longitude=139.633,
              venues=[blondo_venue, fort_venue_1])
    b3 = City(city_name='Saitama', encompassing_geographic_entity='Japan', latitude=35.8617, longitude=139.645,
              venues=[fort_venue_2, maple_venue_2])
    session.add(b1)
    session.add(b2)
    session.add(b3)
    a1 = Airport(name='Tokyo Haneda International Airport', latitude='35.5523', longitude='139.78', code='RJTT',
                 cities=[b1, b2, b3])
    session.add(a1)
    b1 = City(city_name='Sapporo', encompassing_geographic_entity='Japan', latitude=43.0621, longitude=141.354,
              venues=[fort_venue_2, maple_venue_2])
    b2 = City(city_name='Asahikawa', encompassing_geographic_entity='Japan', latitude=43.7706, longitude=142.365,
              venues=[blondo_venue, fort_venue_1])
    b3 = City(city_name='Hakodate', encompassing_geographic_entity='Japan', latitude=41.7686, longitude=140.729,
              venues=[fort_venue_2, maple_venue_2])
    session.add(b1)
    session.add(b2)
    session.add(b3)
    a1 = Airport(name='New Chitose Airport', latitude='42.7752', longitude='141.692', code='RJCC', cities=[b1, b2, b3])
    session.add(a1)
    a1 = Airport(name='Eareckson Air Station', latitude='52.7123', longitude='174.114', code='PASY', cities=[b3])
    session.add(a1)
    a1 = Airport(name='Nikolskoye Airport', latitude='55.1783', longitude='166.048', code='UHPX', cities=[b1])
    session.add(a1)
    a1 = Airport(name='Región de Murcia International Airport', latitude='37.803', longitude='-1.125', code='LEMI',
                 cities=[b2])
    session.add(a1)
    b1 = City(city_name='Valencia', encompassing_geographic_entity='Spain', latitude=39.47, longitude=-0.3764,
              venues=[blondo_venue, fort_venue_1])
    b2 = City(city_name='Murcia', encompassing_geographic_entity='Spain', latitude=37.9861, longitude=-1.1303,
              venues=[blondo_venue, fort_venue_1])
    b3 = City(city_name='Alicante', encompassing_geographic_entity='Spain', latitude=38.3453, longitude=-0.4831,
              venues=[fort_venue_2, maple_venue_2])
    session.add(b1)
    session.add(b2)
    session.add(b3)
    a1 = Airport(name='RAF Mona', latitude='53.2586', longitude='-4.37355', code='EGOQ', cities=[b1, b2, b3])
    session.add(a1)
    b1 = City(city_name='Douglas', encompassing_geographic_entity='Isle Of Man', latitude=54.15, longitude=-4.4819,
              venues=[fort_venue_2, maple_venue_2])
    b2 = City(city_name='Liverpool', encompassing_geographic_entity='United Kingdom', latitude=53.4075,
              longitude=-2.9919, venues=[blondo_venue, fort_venue_1])
    b3 = City(city_name='Abertawe', encompassing_geographic_entity='United Kingdom', latitude=51.6167, longitude=-3.95,
              venues=[fort_venue_2, maple_venue_2])
    session.add(b1)
    session.add(b2)
    session.add(b3)
    a1 = Airport(name='Sandtoft Airfield', latitude='53.5597', longitude='-0.858333', code='EGCF', cities=[b1, b2, b3])
    session.add(a1)
    b1 = City(city_name='Agadir', encompassing_geographic_entity='Morocco', latitude=30.4167, longitude=-9.5833,
              venues=[blondo_venue, fort_venue_1])
    b2 = City(city_name='Safi', encompassing_geographic_entity='Morocco', latitude=32.2833, longitude=-9.2333,
              venues=[fort_venue_2, maple_venue_2])
    b3 = City(city_name='Ait Melloul', encompassing_geographic_entity='Morocco', latitude=30.3342, longitude=-9.4972,
              venues=[fort_venue_2, maple_venue_2])
    session.add(b1)
    session.add(b2)
    session.add(b3)
    a1 = Airport(name='Mogador Airport', latitude='31.3975', longitude='-9.68167', code='GMMI', cities=[b1, b2, b3])
    session.add(a1)
    b1 = City(city_name='Peterhead', encompassing_geographic_entity='United Kingdom', latitude=57.5091,
              longitude=-1.7832, venues=[blondo_venue, fort_venue_1])
    b2 = City(city_name='Fraserburgh', encompassing_geographic_entity='United Kingdom', latitude=57.693,
              longitude=-2.005)
    b3 = City(city_name='Forres', encompassing_geographic_entity='United Kingdom', latitude=57.608, longitude=-3.62,
              venues=[blondo_venue, fort_venue_1])
    session.add(b1)
    session.add(b2)
    session.add(b3)
    a1 = Airport(name='Eday Airport', latitude='59.1906', longitude='-2.77222', code='EGED', cities=[b1, b2, b3])
    session.add(a1)
    a1 = Airport(name='Postville Airport', latitude='54.9105', longitude='-59.7851', code='CCD4', cities=[b2])
    session.add(a1)
    a1 = Airport(name='Charlottetown Airport', latitude='52.765', longitude='-56.1156', code='CCH4', cities=[b1])
    session.add(a1)
    b1 = City(city_name='St. John\'s', encompassing_geographic_entity='Canada', latitude=47.4817, longitude=-52.7971,
              venues=[blondo_venue, fort_venue_1])
    b3 = City(city_name='Mount Pearl Park', encompassing_geographic_entity='Canada', latitude=47.5189,
              longitude=-52.8058, venues=[blondo_venue, fort_venue_1])
    session.add(b1)
    session.add(b3)
    a1 = Airport(name='St. John\'s International Airport', latitude='47.6186', longitude='-52.7519', code='CYYT',
                 cities=[b1, b3])
    session.add(a1)
    a1 = Airport(name='Cartwright Airport', latitude='53.6828', longitude='-57.0419', code='CYCA', cities=[b3])
    session.add(a1)
    b1 = City(city_name='Lexington', encompassing_geographic_entity='United States', latitude=38.0423,
              longitude=-84.4587, venues=[blondo_venue, fort_venue_1])
    b2 = City(city_name='Huntington', encompassing_geographic_entity='United States', latitude=38.4109,
              longitude=-82.4344, venues=[blondo_venue, fort_venue_1])
    b3 = City(city_name='Charleston', encompassing_geographic_entity='United States', latitude=38.3484,
              longitude=-81.6323, venues=[fort_venue_2, maple_venue_2])
    session.add(b1)
    session.add(b2)
    session.add(b3)
    a1 = Airport(name='Julian Carroll Airport', latitude='37.5939', longitude='-83.3173', code='KJKL',
                 cities=[b1, b2, b3])
    session.add(a1)
    b1 = City(city_name='Clarksville', encompassing_geographic_entity='United States', latitude=36.5695,
              longitude=-87.342, venues=[blondo_venue, fort_venue_1])
    b2 = City(city_name='Murfreesboro', encompassing_geographic_entity='United States', latitude=35.8492,
              longitude=-86.4119, venues=[fort_venue_2, maple_venue_2])
    b3 = City(city_name='Bowling Green', encompassing_geographic_entity='United States', latitude=36.9719,
              longitude=-86.4373, venues=[fort_venue_2, maple_venue_2])
    session.add(b1)
    session.add(b2)
    session.add(b3)
    a1 = Airport(name='John C Tune Airport', latitude='36.1824', longitude='-86.8867', code='KJWN', cities=[b1, b2, b3])
    session.add(a1)
    b1 = City(city_name='Detroit', encompassing_geographic_entity='United States', latitude=42.3834, longitude=-83.1024,
              venues=[fort_venue_2, maple_venue_2])
    b2 = City(city_name='Cleveland', encompassing_geographic_entity='United States', latitude=41.4767,
              longitude=-81.6804, venues=[blondo_venue, fort_venue_1])
    b3 = City(city_name='Akron', encompassing_geographic_entity='United States', latitude=41.0798, longitude=-81.5219,
              venues=[fort_venue_2, maple_venue_2])
    session.add(b1)
    session.add(b2)
    session.add(b3)
    a1 = Airport(name='Pelee Island Airport', latitude='41.7804', longitude='-82.678', code='CYPT', cities=[b1, b2, b3])
    session.add(a1)
    b1 = City(city_name='Memphis', encompassing_geographic_entity='United States', latitude=35.1046, longitude=-89.9773,
              venues=[fort_venue_2, maple_venue_2])
    b2 = City(city_name='Bartlett', encompassing_geographic_entity='United States', latitude=35.2337,
              longitude=-89.8195, venues=[fort_venue_2, maple_venue_2])
    b3 = City(city_name='Southaven', encompassing_geographic_entity='United States', latitude=34.9514,
              longitude=-89.9787, venues=[blondo_venue, fort_venue_1])
    session.add(b1)
    session.add(b2)
    session.add(b3)
    a1 = Airport(name='University Oxford Airport', latitude='34.3843', longitude='-89.5368', code='KUOX',
                 cities=[b1, b2, b3])
    session.add(a1)
    b1 = City(city_name='Cape Breton', encompassing_geographic_entity='Canada', latitude=46.1389, longitude=-60.1931,
              venues=[blondo_venue, fort_venue_1])
    b2 = City(city_name='Inverness', encompassing_geographic_entity='Canada', latitude=46.2, longitude=-61.1,
              venues=[fort_venue_2, maple_venue_2])
    b3 = City(city_name='Les Iles-de-la-Madeleine', encompassing_geographic_entity='Canada', latitude=47.3833,
              longitude=-61.8667, venues=[fort_venue_2, maple_venue_2])
    session.add(b1)
    session.add(b2)
    session.add(b3)
    a1 = Airport(name='Port Hawkesbury Airport', latitude='45.6567', longitude='-61.3681', code='CYPD',
                 cities=[b1, b2, b3])
    session.add(a1)
    b1 = City(city_name='Los Angeles', encompassing_geographic_entity='United States', latitude=34.1139,
              longitude=-118.407, venues=[blondo_venue, fort_venue_1])
    b2 = City(city_name='San Diego', encompassing_geographic_entity='United States', latitude=32.8312,
              longitude=-117.122, venues=[fort_venue_2, maple_venue_2])
    b3 = City(city_name='Riverside', encompassing_geographic_entity='United States', latitude=33.9381,
              longitude=-117.395, venues=[fort_venue_2, maple_venue_2])
    session.add(b1)
    session.add(b2)
    session.add(b3)
    a1 = Airport(name='San Diego International Airport', latitude='32.7336', longitude='-117.19', code='KSAN',
                 cities=[b1, b2, b3])
    session.add(a1)
    b1 = City(city_name='Wichita', encompassing_geographic_entity='United States', latitude=37.6896, longitude=-97.3442,
              venues=[blondo_venue, fort_venue_1])
    b2 = City(city_name='Topeka', encompassing_geographic_entity='United States', latitude=39.0346, longitude=-95.6955,
              venues=[fort_venue_2, maple_venue_2])
    b3 = City(city_name='Manhattan', encompassing_geographic_entity='United States', latitude=39.1886,
              longitude=-96.6046, venues=[fort_venue_2, maple_venue_2])
    session.add(b1)
    session.add(b2)
    session.add(b3)
    a1 = Airport(name='Wichita Eisenhower National Airport', latitude='37.6499', longitude='-97.4331', code='KICT',
                 cities=[b1, b2, b3])
    session.add(a1)
    b1 = City(city_name='The Pas', encompassing_geographic_entity='Canada', latitude=53.825, longitude=-101.253,
              venues=[blondo_venue, fort_venue_1])
    session.add(b1)
    a1 = Airport(name='Hudson Bay Airport', latitude='52.8167', longitude='-102.311', code='CYHB', cities=[b1])
    session.add(a1)
    b1 = City(city_name='Yorkton', encompassing_geographic_entity='Canada', latitude=51.2139, longitude=-102.463,
              venues=[fort_venue_2, maple_venue_2])
    b2 = City(city_name='Dauphin', encompassing_geographic_entity='Canada', latitude=51.1992, longitude=-100.063,
              venues=[blondo_venue, fort_venue_1])
    session.add(b1)
    session.add(b2)
    a1 = Airport(name='Swan River Airport', latitude='52.1206', longitude='-101.236', code='CZJN', cities=[b1, b2])
    session.add(a1)
    b1 = City(city_name='Iowa City', encompassing_geographic_entity='United States', latitude=41.6559,
              longitude=-91.5303, venues=[blondo_venue, fort_venue_1])
    b2 = City(city_name='Waterloo', encompassing_geographic_entity='United States', latitude=42.492, longitude=-92.3522,
              venues=[fort_venue_2, maple_venue_2])
    b3 = City(city_name='Independence', encompassing_geographic_entity='United States', latitude=42.4622,
              longitude=-91.9027, venues=[fort_venue_2, maple_venue_2])
    session.add(b1)
    session.add(b2)
    session.add(b3)
    a1 = Airport(name='Iowa City Municipal Airport', latitude='41.6392', longitude='-91.5465', code='KIOW',
                 cities=[b1, b2, b3])
    session.add(a1)
    b1 = City(city_name='Council Bluffs', encompassing_geographic_entity='United States', latitude=41.2369,
              longitude=-95.8517, venues=[blondo_venue, fort_venue_1])
    b2 = City(city_name='Bellevue', encompassing_geographic_entity='United States', latitude=41.1535,
              longitude=-95.9357, venues=[fort_venue_2, maple_venue_2])
    b3 = City(city_name='Papillion', encompassing_geographic_entity='United States', latitude=41.1516,
              longitude=-96.0679, venues=[fort_venue_2, maple_venue_2])
    session.add(b1)
    session.add(b2)
    session.add(b3)
    a1 = Airport(name='Council Bluffs Municipal Airport', latitude='41.2592', longitude='-95.7606', code='KCBF',
                 cities=[b1, b2, b3])
    session.add(a1)
    b1 = City(city_name='Omaha', encompassing_geographic_entity='United States', latitude=41.2627, longitude=-96.0522,
              venues=[blondo_venue, fort_venue_1])
    b2 = City(city_name='Lincoln', encompassing_geographic_entity='United States', latitude=40.809, longitude=-96.6788,
              venues=[fort_venue_2, maple_venue_2])
    b3 = City(city_name='Sioux City', encompassing_geographic_entity='United States', latitude=42.4959,
              longitude=-96.3901, venues=[blondo_venue, fort_venue_1])
    session.add(b1)
    session.add(b2)
    session.add(b3)
    a1 = Airport(name='Lincoln Airport', latitude='40.851', longitude='-96.7592', code='KLNK', cities=[b1, b2, b3])
    session.add(a1)
    b1 = City(city_name='San Francisco', encompassing_geographic_entity='California', latitude=37.8, longitude=-122.4,
              venues=[fort_venue_2, maple_venue_2])
    b2 = City(city_name='Concord', encompassing_geographic_entity='United States', latitude=37.9722, longitude=-122.002,
              venues=[blondo_venue, fort_venue_1])
    b3 = City(city_name='Santa Rosa', encompassing_geographic_entity='United States', latitude=38.4458,
              longitude=-122.707, venues=[fort_venue_2, maple_venue_2])
    session.add(b1)
    session.add(b2)
    session.add(b3)
    a1 = Airport(name='Ukiah Municipal Airport', latitude='39.126', longitude='-123.201', code='KUKI',
                 cities=[b1, b2, b3])
    session.add(a1)
    a1 = Airport(name='Santa Ynez Airport', latitude='34.6068', longitude='-120.076', code='KIZA', cities=[b1, b2, b3])
    session.add(a1)
    b1 = City(city_name='Seattle', encompassing_geographic_entity='United States', latitude=47.6211, longitude=-122.324,
              venues=[blondo_venue, fort_venue_1])
    b2 = City(city_name='Portland', encompassing_geographic_entity='United States', latitude=45.5372, longitude=-122.65,
              venues=[fort_venue_2, maple_venue_2])
    b3 = City(city_name='Victoria', encompassing_geographic_entity='Canada', latitude=48.4283, longitude=-123.365,
              venues=[blondo_venue, fort_venue_1])
    session.add(b1)
    session.add(b2)
    session.add(b3)
    a1 = Airport(name='Tacoma Narrows Airport', latitude='47.2679', longitude='-122.578', code='KTIW',
                 cities=[b1, b2, b3])
    session.add(a1)
    b1 = City(city_name='Vancouver', encompassing_geographic_entity='Canada', latitude=49.25, longitude=-123.1,
              venues=[fort_venue_2, maple_venue_2])
    b2 = City(city_name='Bremerton', encompassing_geographic_entity='United States', latitude=47.5436,
              longitude=-122.712, venues=[blondo_venue, fort_venue_1])
    b3 = City(city_name='Richmond', encompassing_geographic_entity='Canada', latitude=49.1667, longitude=-123.133,
              venues=[fort_venue_2, maple_venue_2])
    session.add(b1)
    session.add(b2)
    session.add(b3)
    a1 = Airport(name='Orcas Island Airport', latitude='48.7082', longitude='-122.91', code='KORS', cities=[b1, b2, b3])
    session.add(a1)
    b1 = City(city_name='Medford', encompassing_geographic_entity='United States', latitude=42.3372, longitude=-122.854,
              venues=[fort_venue_2, maple_venue_2])
    b2 = City(city_name='White City', encompassing_geographic_entity='United States', latitude=42.4316,
              longitude=-122.832, venues=[fort_venue_2, maple_venue_2])
    b3 = City(city_name='Grants Pass', encompassing_geographic_entity='United States', latitude=42.4333,
              longitude=-123.332, venues=[blondo_venue, fort_venue_1])
    session.add(b1)
    session.add(b2)
    session.add(b3)
    a1 = Airport(name='California Redwood Coast-Humboldt County Airport', latitude='40.9781', longitude='-124.109',
                 code='KACV', cities=[b1, b2, b3])
    session.add(a1)
    b1 = City(city_name='Coquitlam', encompassing_geographic_entity='Canada', latitude=49.2839, longitude=-122.792,
              venues=[blondo_venue, fort_venue_1])
    b2 = City(city_name='Langley', encompassing_geographic_entity='Canada', latitude=49.1044, longitude=-122.583,
              venues=[fort_venue_2, maple_venue_2])
    b3 = City(city_name='Delta', encompassing_geographic_entity='Canada', latitude=49.0847, longitude=-123.059,
              venues=[fort_venue_2, maple_venue_2])
    session.add(b1)
    session.add(b2)
    session.add(b3)
    a1 = Airport(name='Powell River Airport', latitude='49.8342', longitude='-124.5', code='CYPW', cities=[b1, b2, b3])
    session.add(a1)
    b1 = City(city_name='Juneau', encompassing_geographic_entity='United States', latitude=58.4546, longitude=-134.174,
              venues=[blondo_venue, fort_venue_1])
    session.add(b1)
    a1 = Airport(name='Petersburg James A Johnson Airport', latitude='56.8017', longitude='-132.945', code='PAPG',
                 cities=[b1])
    session.add(a1)
    session.add(b3)
    a1 = Airport(name='Nelson Lagoon Airport', latitude='56.0075', longitude='-161.16', code='PAOU', cities=[b3])
    session.add(a1)
    session.add(b2)
    a1 = Airport(name='Clarks Point Airport', latitude='58.8337', longitude='-158.529', code='PFCL', cities=[b2])
    session.add(a1)
    b1 = City(city_name='Kodiak', encompassing_geographic_entity='United States', latitude=57.7934, longitude=-152.406,
              venues=[blondo_venue, fort_venue_1])
    b2 = City(city_name='Kalifornsky', encompassing_geographic_entity='United States', latitude=60.4417,
              longitude=-151.197, venues=[fort_venue_2, maple_venue_2])
    b3 = City(city_name='Homer', encompassing_geographic_entity='United States', latitude=59.653, longitude=-151.525,
              venues=[blondo_venue, fort_venue_1])
    session.add(b1)
    session.add(b2)
    session.add(b3)
    a1 = Airport(name='Seldovia Airport', latitude='59.4424', longitude='-151.704', code='PASO', cities=[b1, b2, b3])
    session.add(a1)
    a1 = Airport(name='King Cove Airport', latitude='55.1163', longitude='-162.266', code='PAVC', cities=[b1, b3])
    session.add(a1)
    a1 = Airport(name='St George Airport', latitude='56.5783', longitude='-169.662', code='PAPB', cities=[b1, b2, b3])
    session.add(a1)
    a1 = Airport(name='Dillingham Airport', latitude='59.0447', longitude='-158.505', code='PADL', cities=[b2, b3])
    session.add(a1)
    session.commit()
    a1 = Airport(name='New Airport', latitude=45.0, longitude=-35.0, code='ZZUY', cities=[b1])
    session.add(a1)
    a1 = Airport(name='Old Airport', latitude=45.0, longitude=-25.0, code='ZZOY', cities=[b2])
    session.add(a1)
    a1 = Airport(name='Some Airport', latitude=45.0, longitude=15.0, code='ZZOO', cities=[b3])
    session.add(a1)
    a1 = Airport(name='Same Old Airport', latitude=45.0, longitude=35.0, code='ZZOL', cities=[b1])
    session.add(a1)
    a1 = Airport(name='Dog Airport', latitude=45.0, longitude=55.0, code='ZFOY', cities=[b2])
    session.add(a1)
    a1 = Airport(name='Cat Airport', latitude=45.0, longitude=85.0, code='ZIOY', cities=[b3])
    session.add(a1)
    a1 = Airport(name='Mouse Airport', latitude=45.0, longitude=115.0, code='ZIRY', cities=[b1])
    session.add(a1)
    a1 = Airport(name='Mountain Airport', latitude=45.0, longitude=125.0, code='ZIRP', cities=[b2])
    session.add(a1)
    a1 = Airport(name='Gorilla Airport', latitude=45.0, longitude=135.0, code='ZIRY', cities=[b3])
    session.add(a1)
    a1 = Airport(name='Monkey Airport', latitude=45.0, longitude=145.0, code='ZIRY', cities=[b1])
    session.add(a1)
    a1 = Airport(name='Luffy Airport', latitude=45.0, longitude=155.0, code='ZIRY', cities=[b2])
    session.add(a1)
    a1 = Airport(name='Man Airport', latitude=45.0, longitude=165.0, code='ZIRY', cities=[b3])
    session.add(a1)
    a1 = Airport(name='Mildren Airport', latitude=45.0, longitude=175.0, code='ZIRY', cities=[b1])
    session.add(a1)
    a1 = Airport(name='Cucumber Airport', latitude=45.0, longitude=-175.0, code='ZIRY', cities=[b2])
    session.add(a1)
    a1 = Airport(name='Tomahat Airport', latitude=45.0, longitude=-165.0, code='ZIRY', cities=[b3])
    session.add(a1)
    a1 = Airport(name='Quill Airport', latitude=45.0, longitude=-155.0, code='ZIRY', cities=[b1])
    session.add(a1)
    a1 = Airport(name='Mr. Airport', latitude=45.0, longitude=-145.0, code='ZIRY', cities=[b2])
    session.add(a1)
    a1 = Airport(name='Dude Airport', latitude=45.0, longitude=-135.0, code='ZIRY', cities=[b3])
    session.add(a1)
    a1 = Airport(name='Duke Airport', latitude=45.0, longitude=-125.0, code='ZIRY', cities=[b2])
    session.add(a1)
    a1 = Airport(name='Green Airport', latitude=45.0, longitude=-115.0, code='ZIRY', cities=[b3])
    session.add(a1)
    a1 = Airport(name='Red Airport', latitude=45.0, longitude=-105.0, code='ZIRY', cities=[b2])
    session.add(a1)
    a1 = Airport(name='Orange Airport', latitude=45.0, longitude=-95.0, code='ZIRY', cities=[b1])
    session.add(a1)


def main():
    try:
        database_credentials = open('database_credentials.json')
        data = json.load(database_credentials)
        url = Database.construct_mysql_url(data['authority'], data['port'],
                                           data['database'], data['username'],
                                           data['password'])
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
