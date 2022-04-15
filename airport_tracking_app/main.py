from kivy.app import App
from kivy.modules import inspector
from kivy.core.window import Window
from kivy.uix.button import Button
from sqlalchemy.exc import SQLAlchemyError
from airport import Airport, City, AirportDatabase


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
        values = ('denver', 'omaha')
        self.root.ids.forecast_spinner.values = values

    def add_buttons(self):
        for i in range(5):
            self.root.ids.scroll_box_1.add_widget(Button(text='Cities'))
        for i in range(5):
            self.root.ids.scroll_box_2.add_widget(Button(text='Airports'))


def main():
    app = AirportApp()
    app.run()


if __name__ == '__main__':
    main()
