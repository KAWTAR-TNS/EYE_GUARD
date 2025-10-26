from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.app import App
from connected import Connected  # Import your Connected screen class
from person_page import PersonPage # Import your PersonScreen class

class LoginScreen(Screen):
 pass
class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(Connected(name='connected'))
        sm.add_widget(PersonPage(name='PersonPage'))
        return sm

if __name__ == '__main__':
    MyApp().run()
