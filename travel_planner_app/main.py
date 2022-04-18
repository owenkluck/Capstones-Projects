from kivy.app import App
from kivy.modules import inspector
from kivy.core.window import Window


class TravelPlannerApp(App):
    def build(self):
        inspector.create_inspector(Window, self)


def main():
    app = TravelPlannerApp()
    app.run()


if __name__ == '__main__':
    main()
