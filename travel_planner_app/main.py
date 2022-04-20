from kivy.app import App
from kivy.modules import inspector
from kivy.core.window import Window
from travel_planner_app.rest import RESTConnection
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from api_key import API_KEY

Persisted = declarative_base()


class TravelPlannerApp(App):
    def __init__(self, authority='localhost', port=33060, database='codeblue', username='root', password='cse1208',
                 port_api=443, api_key=API_KEY, **kwargs):
        super(TravelPlannerApp, self).__init__(**kwargs)
        url = construct_mysql_url(authority, port, database, username, password)
        self.database = TravelPlannerDatabase(url)
        self.session = self.database.create_session()
        self.connection = RESTConnection('api.openweathermap.org', port_api, '/data/2.5')
        self.api_key = api_key

    def build(self):
        inspector.create_inspector(Window, self)


def construct_mysql_url(authority, port, database, username, password):
    return f'mysql+mysqlconnector://{username}:{password}@{authority}:{port}/{database}'


def construct_in_memory_url():
    return 'sqlite:///'


# This is just a temporary class to help me test code, I'll use the remote database later.
class TravelPlannerDatabase:
    def __init__(self, url):
        self.engine = create_engine(url)
        self.Session = sessionmaker()
        self.Session.configure(bind=self.engine)

    def ensure_tables_exist(self):
        Persisted.metadata.create_all(self.engine)

    def create_session(self):
        return self.Session()
# End Temporary Code.


def main():
    app = TravelPlannerApp()
    app.run()


if __name__ == '__main__':
    main()
