from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.metrics import dp
from kivy.uix.image import Image
from kivy.uix.screenmanager import SlideTransition

class Connected(Screen):
    def __init__(self, **kwargs):
        super(Connected, self).__init__(**kwargs)
        self.setup_ui()

    def setup_ui(self):
        layout = BoxLayout(orientation='vertical')

        # Add title
        title_label = Label(text="Eye Guard", color=(1, 1, 1, 1), font_size='30sp', size_hint=(1, None), height=dp(100))
        layout.add_widget(title_label)

        # Background image
        background = Image(source='background.jpg', allow_stretch=True, keep_ratio=False)
        layout.add_widget(background)

        # Buttons for different classes
        classes_layout = BoxLayout(orientation='vertical', size_hint=(1, None), spacing=15)
        for class_name in ["Person", "Student", "Professor","Alert", "Surveillance"]:
            button = Button(text=class_name, size_hint=(None, None), size=(dp(500), dp(50)), background_normal='', background_color=(0, 0.5, 0, 1))
            button.bind(on_press=lambda instance, class_name=class_name: self.go_to_class_screen(class_name))
            classes_layout.add_widget(button)

        # Log out button
        logout_button = Button(text="Log Out", size_hint=(None, None), size=(dp(500), dp(50)), background_normal='', background_color=(0.5, 0.5, 1, 1))
        logout_button.bind(on_press=self.logout)

        # Add buttons layout to main layout
        layout.add_widget(classes_layout)
        layout.add_widget(logout_button)

        self.add_widget(layout)

    def go_to_class_screen(self, class_name):
        # Navigate to the corresponding class screen based on the button pressed
        self.manager.transition = SlideTransition(direction="left")
        if class_name == "Person":
            self.manager.current = 'PersonPage'
        elif class_name == "Student":
            self.manager.current = 'StudentPage'
        elif class_name == "Professor":
            self.manager.current = 'ProfessorPage'
        elif class_name == "Surveillance":
            self.manager.current = 'Surveillance'

    def logout(self, instance):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'login'

class PersonPage(Screen):
    pass
class ProfessorPage(Screen):
    pass

class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(Connected(name='connected'))
        sm.add_widget(PersonPage(name='PersonPage'))
        sm.add_widget(PersonPage(name='StudentPage'))
        sm.add_widget(PersonPage(name='ProfessorPage'))
        return sm

if __name__ == '__main__':
    MyApp().run()
