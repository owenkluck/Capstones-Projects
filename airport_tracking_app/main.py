from datetime import date
from kivy.app import App
from kivy.modules import inspector
from kivy.core.window import Window
from kivy.uix.button import Button
from sqlalchemy.exc import SQLAlchemyError
from database import Airport, City, Condition, Database


class AirportButtons(Button):
    pass


class CityButtons(Button):
    pass


class AirportApp(App):
    def __init__(self, **kwargs):
        super(AirportApp, self).__init__(**kwargs)
        url = Database.construct_mysql_url('localhost', 33060, 'airports', 'root', 'cse1208')
        self.airport_database = Database(url)
        self.session = self.airport_database.create_session()
        self.airport_database.ensure_tables_exist()
        self.current_airport = None
        self.current_city = None

    def build(self):
        inspector.create_inspector(Window, self)

    def submit_data_airport(self, name, code, latitude, longitude):
        if len(name) > 0 and len(code) > 0 and len(latitude) > 0 and len(longitude) > 0:
            airport = Airport(name=name, code=code, latitude=int(latitude), longitude=int(longitude))
            self.session.add(airport)
            try:
                self.session.commit()
                self.set_current_airport(name)
                self.root.current = 'success_airport'
            except SQLAlchemyError:
                print('Database could not be updated.')
                self.root.ids.create_airport_error.text = 'Database could not be updated.' \
                                                          '\nThe information added may match an airport that' \
                                                          '\nis currently in the database'
        self.root.ids.create_airport_error.text = 'Some information inputs were left blank, \nplease fill out all inputs'

    def submit_data_city(self, name, geographic_entity, latitude, longitude):
        if len(name) > 0 and len(geographic_entity) > 0 and len(latitude) > 0 and len(longitude) > 0:
            city = City(city_name=name, encompassing_geographic_entity=geographic_entity, latitude=int(latitude), longitude=int(longitude))
            self.session.add(city)
            try:
                self.session.commit()
                self.set_current_city(name)
                self.root.current = 'success_city'
            except SQLAlchemyError:
                print('Database could not be updated.')
                self.root.ids.create_city_error.text = 'Database could not be updated.' \
                                                       '\nThe information added may match a city that' \
                                                       '\nis currently in the database.'
        self.root.ids.create_city_error.text = 'Some information inputs were left blank, \nplease fill out all inputs'

    def add_airports_spinner(self):
        values = [airport.name for airport in self.session.query(Airport).all()]
        self.root.ids.forecast_spinner.values = values

    def add_forecast(self, airport_name, date_1):
        airport_id = -1
        try:
            airport_id = self.session.query(Airport).filter(Airport.name == airport_name)[0].airport_id
        except IndexError:
            self.root.current = 'check_forecast'
            self.root.ids.check_forecast_error.text = 'No airport was selected'
        try:
            date_values = date_1.split('/')
            forecasts = self.session.query(Condition).filter(Condition.date == date(int(date_values[2]), int(date_values[1]), int(date_values[0])) and Condition.airport_id == airport_id)
            self.root.ids.forecast.text = f'On {forecasts[0].date}, the weather will be:\n' \
                                          f'temperature: {forecasts[0].max_temperature}\n' \
                                          f'wind_speed: {forecasts[0].wind_speed}\n' \
                                          f'humidity: {forecasts[0].max_humidity}\n' \
                                          f'rain: {forecasts[0].rain}\n' \
                                          f'visibility: {forecasts[0].visibility}'
        except (IndexError, SQLAlchemyError, ValueError):
            self.root.current = 'check_forecast'
            self.root.ids.check_forecast_error.text = 'The date input was incorrect,\n please type date in form DY/MN/YEAR.\n Ex: 1/7/2005'

    def add_buttons(self):
        airports = self.session.query(Airport).all()
        cities = self.session.query(City).all()
        for airport in airports:
            self.root.ids.scroll_box_2.add_widget(AirportButtons(text=airport.name))
        for city in cities:
            self.root.ids.scroll_box_1.add_widget(CityButtons(text=city.city_name))

    def add_city(self, city):
        try:
            self.root.ids.select_city_error.text = ''
            place = self.session.query(City).filter(City.city_name == city)[0]
            if self.current_airport.latitude - 1 <= place.latitude <= self.current_airport.latitude + 1 and \
                    self.current_airport.longitude - 1 <= place.longitude <= self.current_airport.longitude + 1:
                self.current_airport.cities.append(place)
                self.session.add(self.current_airport)
                self.session.commit()
            else:
                self.root.ids.select_city_error.text = 'The city you have chosen is not within range of this airport. Please select a in range city'
        except SQLAlchemyError:
            self.root.ids.select_city_error.text = 'The city you have selected could not be added to the database,' \
                                                   ' there may be multiple of this city or the database may have failed'

    def add_airport(self, airport):
        try:
            self.root.ids.select_airport_error.text = ''
            place = self.session.query(Airport).filter(Airport.name == airport)[0]
            if self.current_city.latitude - 1 <= place.latitude <= self.current_city.latitude + 1 and \
                    self.current_city.longitude - 1 <= place.longitude <= self.current_city.longitude + 1:
                self.current_city.airports.append(place)
                self.session.add(self.current_city)
                self.session.commit()
            else:
                self.root.ids.select_airport_error.text = 'The airport you have chosen is not within range of this city. Please select a in range airport'
        except SQLAlchemyError:
            self.root.ids.select_airport_error.text = 'The airport you have selected could not be added to the database,' \
                                                      ' there may be multiple of this airport or the database may have failed'

    def set_current_city(self, city):
        self.current_city = self.session.query(City).filter(City.city_name == city).one()

    def set_current_airport(self, airport):
        self.current_airport = self.session.query(Airport).filter(Airport.name == airport).one()

    def delete_buttons(self):
        self.root.ids.scroll_box_1.clear_widgets()
        self.root.ids.scroll_box_2.clear_widgets()


def main():
    app = AirportApp()
    app.run()


if __name__ == '__main__':
    main()

# Things to clean up:
    # Re-organize main.py functions.
    # Add range determination to main.py.
    # Make screen take you back after making new city from button.
    # add view itinerary screen
    # make one call work
    # add method to update Condition if it doesn't exist for a day
