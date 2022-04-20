from datetime import date

from kivy.app import App
from kivy.modules import inspector
from kivy.core.window import Window
from kivy.uix.button import Button
from sqlalchemy.exc import SQLAlchemyError
from airport import Airport, City, AirportDatabase, Forecast


class AirportApp(App):

    def __init__(self, **kwargs):
        super(AirportApp, self).__init__(**kwargs)
        url = AirportDatabase.construct_mysql_url('localhost', 33060, 'airports', 'root', 'cse1208')
        self.airport_database = AirportDatabase(url)
        self.session = self.airport_database.create_session()
        self.airport_database.ensure_tables_exist()

    def build(self):
        inspector.create_inspector(Window, self)  # For inspection (press control-e to toggle).

    def submit_data_airport(self, name, code, location):
        airport = Airport(name=name, code=code, location=location)
        self.session.add(airport)
        try:
            self.session.commit()
        except SQLAlchemyError:
            print('Database could not be updated.')
            self.root.ids.Error_3.text = 'Database could not be updated.'

    def submit_data_city(self, name, geographic_entity, location):
        city = City(name=name, geographic_entity=geographic_entity, location=location)
        self.session.add(city)
        try:
            self.session.commit()
        except SQLAlchemyError:
            print('Database could not be updated.')
            self.root.ids.Error_2.text = 'Database could not be updated.'

    def add_airports_spinner(self):
        values = [airport.name for airport in self.session.query(Airport).all()]
        self.root.ids.forecast_spinner.values = values

    def add_forecast(self, airport_name, date_1):
        airport_id = self.session.query(Airport).filter(Airport.name == airport_name)[0].airport_id
        try:
            date_values = date_1.split('/')
            forecasts = self.session.query(Forecast).filter(Forecast.date == date(int(date_values[2]), int(date_values[1]), int(date_values[0])) and Forecast.airport_id == airport_id)
            self.root.ids.forecast.text = f'On {forecasts[0].date}, the weather will be:\n' \
                                          f'temperature: {forecasts[0].temperature}\n' \
                                          f'wind_speed: {forecasts[0].wind_speed}\n' \
                                          f'humidity: {forecasts[0].humidity}\n' \
                                          f'rain: {forecasts[0].rain}\n' \
                                          f'visibility: {forecasts[0].visibility}'
        except (IndexError, SQLAlchemyError):
            self.root.current = 'check_forecast'
            self.root.ids.Error_1.text = 'The date input was incorrect,\n please type date in form DY/MN/YEAR.\n Ex: 1/7/2005'

    def add_buttons(self):
        airports = self.session.query(Airport).all()
        cities = self.session.query(City).all()
        for airport in airports:
            self.root.ids.scroll_box_1.add_widget(Button(text=airport.name))
        for city in cities:
            self.root.ids.scroll_box_2.add_widget(Button(text=city.name))

    def delete_buttons(self):
        self.root.ids.scroll_box_1.clear_widgets()
        self.root.ids.scroll_box_2.clear_widgets()


def main():
    app = AirportApp()
    app.run()


if __name__ == '__main__':
    main()
