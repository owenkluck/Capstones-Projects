from datetime import date

from kivy.app import App
from kivy.modules import inspector  # For inspection.
from kivy.core.window import Window  # For inspection.
import json

from kivy.uix.button import Button, Label
from sqlalchemy.exc import MultipleResultsFound

from database import *


class ItineraryButtons(Button):
    pass


class ItineraryLabel(Label):
    pass


def bad_condition_entry(data_list):
    bad_entry = False
    for element in data_list:
        if not element.strip('-').replace('.', '', 1).isnumeric() and element != '':
            bad_entry = True
    return bad_entry


def valid_welp_score(score):
    return str(score).isdigit() and 1 <= eval(score) <= 5


def bad_lat_long(lat, long):
    return not str(lat).strip('-.').replace('.', '', 1).isdecimal() or \
           not str(long).strip('-.').replace('.', '', 1).isdecimal()


class EntertainmentTrackerApp(App):
    def __init__(self, **kwargs):
        super(EntertainmentTrackerApp, self).__init__(**kwargs)
        database_credentials = open('database_credentials.json')
        data = json.load(database_credentials)
        url = Database.construct_mysql_url(data['authority'], data['port'],
                                           data['database'], data['username'],
                                           data['password'])
        self.entertainment_database = Database(url)
        self.session = self.entertainment_database.create_session()
        print('success')

    def build(self):
        inspector.create_inspector(Window, self)  # For inspection (press control-e to toggle).

    def on_start(self):
        # Update City List to match preexisting cities
        i = 0
        city_names = []
        for city in self.session.query(City):
            print(i)
            i += 1
            city_names.append(str(city.city_name))
            #self.root.ids.associated_city.values.append(str(city.city_name))
        self.root.ids.associated_city.values = city_names
        # Update Venue List to match preexisting venues
        venue_names = []
        for venue in self.session.query(Venue):
            print('ran 2')
            venue_names.append(str(venue.venue_name))
            #self.root.ids.venue_edit_selection.values.append(str(venue.venue_name))
        self.root.ids.venue_edit_selection.values = venue_names

    def add_city(self, name, lat, long, entity):
        # Search for cities with the exact same name
        query = self.session.query(City).filter(City.city_name == name)
        empty_field = False
        data = [name, lat, long, entity]
        for element in data:
            if str(element) == '':
                empty_field = True
        if empty_field:
            self.root.ids.city_creation_message.text = 'Please fill in all of the data fields.'
        elif bad_lat_long(lat, long):
            self.root.ids.city_creation_message.text = f'Lat and Long must be a decimal or whole number.'
        elif query.count() > 0:
            self.root.ids.city_creation_message.text = f'A city with the name {name} already exists.'
        else:
            self.commit_city_to_database(entity, lat, long, name)
            self.root.ids.city_creation_message.text = ''
            self.root.ids.associated_city.values.append(name)
            self.root.transition.direction = 'left'
            self.root.current = 'ask_add_venue'

    def commit_city_to_database(self, entity, lat, long, name):
        city = City(city_name=name, latitude=lat, longitude=long, encompassing_geographic_entity=entity)
        self.session.add(city)
        self.session.commit()

    def duplicate_name_city(self, candidate_name):
        query = self.session.query(City).filter(City.city_name == candidate_name)
        return query.count() > 0

    def duplicate_name_venue(self, original_name, candidate_name, city_selection, create_or_edit):
        duplicate_name = False
        city = self.session.query(City).filter(City.city_name == city_selection).one()
        # venues_to_check = self.session.query(Venue).filter(Venue.city_id == c_id)
        venues_to_check = city.venues
        for venue in venues_to_check:
            if create_or_edit == 'CREATE' and venue.venue_name == candidate_name:
                duplicate_name = True
                self.root.ids.venue_name_error.text = f'A venue under the name {candidate_name} already exists in the chosen city.'
            if create_or_edit == 'EDIT' and venue.venue_name == candidate_name and original_name != candidate_name:
                duplicate_name = True
                self.root.ids.venue_edit_message.text = f'A venue under the name {candidate_name} already exists in the chosen city.'
        return duplicate_name

    def check_city_for_venues(self, city, edit_or_review):
        message = 'No venues exist in this city.'
        city = self.session.query(City).filter(City.city_name == city).one()
        # venue_query = self.session.query(Venue).filter(Venue.city_id == c_id)
        venue_query = city.venues
        if len(venue_query) > 0:
            self.update_venue_list(city)
            self.root.transition.direction = 'left'
            if edit_or_review == 'EDIT':
                self.root.current = 'edit_venue'
            else:
                self.root.current = 'choose_venue_new_review'
        else:
            if edit_or_review == 'EDIT':
                self.root.ids.no_venues_message.text = message
            else:
                self.root.ids.no_venues_to_review.text = message

    def add_venue(self, ven_name, ven_type, city_name, min_temp, max_temp, min_humidity, max_humidity, max_wind_speed,
                  weather_condition_code):
        self.root.ids.venue_edit_selection.values.append(ven_name)
        self.commit_venue_to_database(city_name, ven_name, ven_type)
        condition_added = self.add_condition(ven_name, min_temp, max_temp, min_humidity, max_humidity, max_wind_speed,
                                             weather_condition_code)
        if condition_added:
            self.root.transition.direction = 'left'
            self.root.current = 'venue_creation_success'

    def commit_venue_to_database(self, city_name, ven_name, ven_type):
        city_query = self.session.query(City).filter(City.city_name == city_name).one()
        venue = Venue(venue_name=ven_name, venue_type=ven_type, cities=[city_query])
        self.session.add(venue)
        self.session.commit()

    def add_condition(self, venue_name, min_t, max_t, min_h, max_h, max_ws, owc):
        data = [min_t, max_t, min_h, max_h, max_ws, owc]
        if bad_condition_entry(data):
            self.root.ids.venue_condition_error.text = 'All weather condition entries must be an integer.'
            return False
        else:
            query = self.session.query(Venue).filter(Venue.venue_name == venue_name).one()
            v_id = query.venue_id
            # If the user passed in an empty string, render it as None
            for element in data:
                if element == '':
                    data[data.index(element)] = None
            min_t, max_t, min_h, max_h, max_ws, owc = data
            condition = Condition(min_temperature=min_t, max_temperature=max_t,
                                  min_humidity=min_h, max_humidity=max_h, max_wind_speed=max_ws, open_weather_code=owc)
            self.session.add(condition)
            self.session.commit()
            c_id = condition.condition_id
            vc = VenueCondition(venue_id=v_id, condition_id=c_id)
            self.session.add(vc)
            self.session.commit()
            return True

    def update_venue_data(self, name, new_name, city, new_min_t, new_max_t, new_min_h, new_max_h, new_max_w, new_owc):
        venue_updated_successfully = self._update_venue_data(name, new_name, city, new_min_t, new_max_t, new_min_h,
                                                             new_max_h, new_max_w, new_owc)
        if venue_updated_successfully:
            self.update_spinner_names(name, new_name)
            self.root.transition.direction = 'left'
            self.root.current = 'venue_edit_success'

    def _update_venue_data(self, name, new_name, city, new_min_t, new_max_t, new_min_h, new_max_h, new_max_w, new_owc):
        data = [new_min_t, new_max_t, new_min_h, new_max_h, new_max_w, new_owc]
        if new_name == '':
            self.root.ids.venue_edit_message.text = "Venue name can't be an empty string."
            return False
        elif bad_condition_entry(data):
            self.root.ids.venue_edit_message.text = 'Venue conditions must be integers.'
            return False
        elif self.duplicate_name_venue(name, new_name, city, 'EDIT'):
            self.root.ids.venue_edit_message.text = 'A venue under that name already exists.'
            return False
        else:
            # Check for empty strings
            for element in data:
                if element == '':
                    data[data.index(element)] = None
            new_min_t, new_max_t, new_min_h, new_max_h, new_max_w, new_owc = data
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
            condition_data.open_weather_code = new_owc
            venue_data.venue_name = new_name
            # Don't forget to save your changes! :)
            self.session.commit()
            return True

    def update_spinner_names(self, name, new_name):
        old_venues = self.root.ids.venue_edit_selection.values
        new_venues = list()
        for venue in old_venues:
            if venue == name:
                new_venues.append(new_name)
            else:
                new_venues.append(venue)
        self.root.ids.venue_edit_selection.values = tuple(new_venues)
        self.root.ids.venue_edit_selection.text = new_name

    def update_venue_list(self, city):
        self.root.ids.venue_edit_selection.values.clear()
        # city = self.session.query(City).filter(City.city_name == city).one()
        venue_count = self.session.query(Venue).count()
        for i in range(1, venue_count + 1):
            current_venue = self.session.get(Venue, i)
            if current_venue in city.venues:
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

    def add_welp_score(self, review_score, venue_being_reviewed):
        valid_score = self._add_welp_score(review_score, venue_being_reviewed)
        if valid_score:
            self.root.transition.direction = 'left'
            self.root.current = 'review_added_success'
        else:
            self.root.ids.invalid_welp_score.text = 'Welp scores must be an integer 1-5.'

    def _add_welp_score(self, review_score, venue_being_reviewed):
        if valid_welp_score(review_score):
            # city = self.session.query(City).filter(City.city_name == city).one()
            venue = self.session.query(Venue).filter(Venue.venue_name == venue_being_reviewed).one()
            if venue.average_welp_score is None:
                venue.average_welp_score = review_score
            else:
                venue.average_welp_score = (len(venue.reviews) * venue.average_welp_score + int(review_score)) \
                                           / (len(venue.reviews) + 1)
            v_id = venue.venue_id
            review = Review(venue_id=v_id, score=review_score)
            self.session.add(review)
            self.session.commit()
            return True
        return False

    def add_itineraries(self, selected_itinerary_text):
        try:
            self.root.ids.past_itineraries.clear_widgets()
            self.root.ids.proposed_itineraries.clear_widgets()
            selected_itinerary = None
            next_city = 'Undetermined'
            if selected_itinerary_text is not None:
                _, _, city_name = selected_itinerary_text.partition('City: ')
                city_name, _, _ = city_name.partition('\n')
                selected_itinerary = self.session.query(Itinerary).filter(Itinerary.city == city_name).one()
                next_city = city_name
                self.update_select_itinerary(True, selected_itinerary)
            itineraries = self.session.query(Itinerary).order_by(Itinerary.date)
            today_date = date.today()
            day_count = 1
            current_location = None
            for itinerary in itineraries:
                itinerary_text = f'City: {itinerary.city}\nVenues: '
                for venue in itinerary.venues:
                    itinerary_text += f'{venue.venue_name}({venue.venue_type}), '
                if selected_itinerary is not None and itinerary.date == selected_itinerary.date and itinerary != selected_itinerary:
                    self.update_select_itinerary(False, itinerary)
                if itinerary.itinerary_type == 'Past' or itinerary.selected:
                    if itinerary != selected_itinerary:
                        current_location = itinerary.city
                        time_difference = itinerary.date - today_date
                        day_count = str(time_difference)
                        day_count, _, _ = day_count.partition(' day')
                        if len(day_count) > 2:
                            day_count = '0'
                    if itinerary.selected:
                        next_city = itinerary.city
                        self.root.ids.selected_itinerary.text = 'Next ' + itinerary_text
                    self.root.ids.past_itineraries.add_widget(ItineraryLabel(text=f'Day #{day_count}: {itinerary.date}\n' + itinerary_text))
                else:
                    if itinerary.itinerary_type == 'Close':
                        self.root.ids.proposed_itineraries.add_widget(ItineraryLabel(text='Closest\nto Destination'))
                    else:
                        self.root.ids.proposed_itineraries.add_widget(ItineraryLabel(text='Most Venues'))
                    self.root.ids.proposed_itineraries.add_widget(ItineraryButtons(text='Next ' + itinerary_text))
            self.root.ids.current_status.text = f'Day #{day_count}\nCurrent City: {current_location}\nNext City: {next_city}'
        except MultipleResultsFound:
            self.root.ids.itinerary_error_message.text = 'There seems to be multiple of the same values in the database'

    def update_select_itinerary(self, selected, itinerary):
        itinerary.selected = selected
        self.session.add(itinerary)
        self.session.commit()


if __name__ == '__main__':
    app = EntertainmentTrackerApp()
    app.run()
