from kivy.app import App
from kivy.modules import inspector  # For inspection.
from kivy.core.window import Window  # For inspection.
from entertainment_installer import *


class EntertainmentTrackerApp(App):
    def __init__(self, **kwargs):
        super(EntertainmentTrackerApp, self).__init__(**kwargs)
        url = EntertainmentDatabase.construct_mysql_url('localhost', 3306, 'entertainment', 'root', 'cse1208')
        self.entertainment_database = EntertainmentDatabase(url)
        self.session = self.entertainment_database.create_session()

    def build(self):
        inspector.create_inspector(Window, self)  # For inspection (press control-e to toggle).

    def on_start(self):
        # Update City List to match preexisting cities
        for city in self.session.query(City):
            self.root.ids.associated_city.values.append(str(city.city_name))
        # Update Venue List to match preexisting venues
        for venue in self.session.query(Venue):
            self.root.ids.venue_edit_selection.values.append(str(venue.venue_name))

    def add_city(self, name, lat, long, entity):
        # Search for cities with the exact same name
        query = self.session.query(City).filter(City.city_name == name)
        # Check for empty fields
        empty_field = False
        if str(name) == '' or str(lat) == '' or str(long) == '' or str(entity) == '':
            empty_field = True
        if empty_field:
            self.root.ids.city_creation_message.text = 'Please fill in all of the data fields.'
        elif not str(lat).strip('-.').replace('.', '', 1).isdecimal() or not str(long).strip('-.').replace('.', '', 1).isdecimal():
            self.root.ids.city_creation_message.text = f'Lat and Long must be a decimal or whole number.'
        elif query.count() > 0:
            self.root.ids.city_creation_message.text = f'A city with the name {name} already exists.'
        else:
            city = City(city_name=name, latitude=lat, longitude=long, ege=entity)
            self.session.add(city)
            self.root.ids.city_creation_message.text = ''
            self.session.commit()
            self.root.ids.associated_city.values.append(name)
            self.session.commit()
            self.root.transition.direction = 'left'
            self.root.current = 'ask_add_venue'

    def duplicate_name_city(self, candidate_name):
        query = self.session.query(City).filter(City.city_name == candidate_name)
        if query.count() > 0:
            return True
        return False

    def duplicate_name_venue(self, original_name, candidate_name, city_selection):
        c_id = self.session.query(City).filter(City.city_name == city_selection).one().city_id
        same_name = self.session.query(Venue).filter(Venue.venue_name == candidate_name, Venue.city_id == c_id).count()
        if same_name > 0 and original_name != candidate_name:
            return True
        return False

    def add_venue(self, name, v_type, city, min_t, max_t, min_h, max_h, max_ws, owc):
        the_id = self.session.query(City).filter(City.city_name == city).one().city_id
        if self.duplicate_name_venue(name, name, city):
            self.root.ids.venue_creation_message.text = f'A venue under the name {name} already exists in the chosen city.'
        else:
            venue = Venue(venue_name=name, venue_type=v_type, city_id=the_id)
            self.session.add(venue)
            self.session.commit()
            self.root.ids.venue_edit_selection.values.append(name)
            self.session.commit()
            self.add_condition(name, min_t, max_t, min_h, max_h, max_ws, owc)
            self.session.commit()

    def add_condition(self, name, min_t, max_t, min_h, max_h, max_ws, owc):
        data = [min_t, min_h, max_t, max_h, max_ws, owc]
        bad_entry = False
        for element in data:
            if not element.strip('-').replace('.', '', 1).isnumeric() and element != '':
                bad_entry = True
        if bad_entry:
            self.root.ids.venue_creation_message.text = 'All weather condition entries must be an integer.'
        else:
            query = self.session.query(Venue).filter(Venue.venue_name == name).one()
            v_id = query.venue_id
            # If the user passed in an empty string, render it as None
            if min_t == '':
                min_t = None
            if max_t == '':
                max_t = None
            if min_h == '':
                min_h = None
            if max_h == '':
                max_h = None
            if max_ws == '':
                max_ws = None
            if owc == '':
                owc = None
            condition = Condition(min_temperature=min_t, max_temperature=max_t,
                                  min_humidity=min_h, max_humidity=max_h, max_wind_speed=max_ws, open_weather_code=owc)
            self.session.add(condition)
            self.session.commit()
            c_id = condition.condition_id
            vc = VenueCondition(venue_id=v_id, condition_id=c_id)
            self.session.add(vc)
            self.session.commit()
            self.root.transition.direction = 'left'
            self.root.current = 'venue_creation_success'

    def update_venue_data(self, name, new_name, city, new_min_t, new_max_t, new_min_h, new_max_h, new_max_w, new_owc):
        if self.duplicate_name_venue(name, new_name, city):
            self.root.ids.venue_edit_message.text = f'A venue under the name {new_name} already exists.'
        else:
            # Check for empty strings
            if new_min_t == '':
                new_min_t = None
            if new_max_t == '':
                new_max_t = None
            if new_min_h == '':
                new_min_h = None
            if new_max_h == '':
                new_max_h = None
            if new_max_w == '':
                new_max_w = None
            if new_owc == '':
                new_owc = None
            # Grab data from tables
            venue_data = self.session.query(Venue).filter(Venue.venue_name == name).one()
            v_id = venue_data.venue_id
            temp = self.session.query(VenueCondition).filter(VenueCondition.venue_id == v_id).one()
            c_id = temp.condition_id
            condition_data = self.session.query(Condition).filter(Condition.condition_id == c_id).one()
            # Change old data to user inputted data
            condition_data.min_temperature = new_min_t
            condition_data.max_temperature = new_max_t
            condition_data.min_humidity = new_min_h
            condition_data.max_humidity = new_max_h
            condition_data.max_wind_speed = new_max_w
            condition_data.owc = new_owc
            venue_data.venue_name = new_name
            # Update Spinner for new venue name
            old_venues = self.root.ids.venue_edit_selection.values
            new_venues = list()
            for venue in old_venues:
                if venue == name:
                    new_venues.append(new_name)
                else:
                    new_venues.append(venue)
            self.root.ids.venue_edit_selection.values = tuple(new_venues)
            self.root.ids.venue_edit_selection.text = new_name
            # Don't forget to save your changes! :)
            self.session.commit()
            self.root.transition.direction = 'left'
            self.root.current = 'venue_edit_success'

    def update_venue_list(self, city):
        self.root.ids.venue_edit_selection.values.clear()
        c_id = self.session.query(City).filter(City.city_name == city).one().city_id
        venue_count = self.session.query(Venue).count()
        for i in range(1, venue_count + 1):
            current_venue = self.session.get(Venue, i)
            if current_venue.city_id == c_id:
                self.root.ids.venue_edit_selection.values.append(current_venue.venue_name)

    def adjust_opacity(self, t_cb, h_cb, w_cb, wwc_cb):
        if not t_cb:
            self.root.ids.temperature_conditions.opacity = 0
        else:
            self.root.ids.temperature_conditions.opacity = 1
        if not h_cb:
            self.root.ids.humidity_conditions.opacity = 0
        else:
            self.root.ids.humidity_conditions.opacity = 1
        if not w_cb:
            self.root.ids.wind_conditions.opacity = 0
        else:
            self.root.ids.wind_conditions.opacity = 1
        if not wwc_cb:
            self.root.ids.open_weather_conditions.opacity = 0
        else:
            self.root.ids.open_weather_conditions.opacity = 1


if __name__ == '__main__':
    app = EntertainmentTrackerApp()
    app.run()