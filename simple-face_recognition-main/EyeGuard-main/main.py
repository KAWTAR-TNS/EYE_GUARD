from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager, SlideTransition, Screen
from kivy.uix.label import Label
import os
from connected import Connected

class Login(Screen):
    def do_login(self, loginText, passwordText):
        app = App.get_running_app()

        if loginText == "admin" and passwordText == "PFA":
            app.username = loginText
            app.password = passwordText

            self.manager.transition = SlideTransition(direction="left")
            self.manager.current = 'connected'

            app.config.read(app.get_application_config())
            app.config.write()
        else:
            self.show_warning("Invalid login or password.")

    def show_warning(self, message):
        warning_label = Label(text=message, color=(1, 0, 0, 1), size_hint=(1, None), height=30)
        self.add_widget(warning_label)

    def resetForm(self):
        self.ids['login'].text = "admin"
        self.ids['password'].text = "PFA"

class LoginApp(App):
    username = StringProperty(None)
    password = StringProperty(None)

    def build(self):
        manager = ScreenManager()

        manager.add_widget(Login(name='login'))
        manager.add_widget(Connected(name='connected'))  # Add the Connected screen

        return manager

    def get_application_config(self):
        if not self.username:
            return super(LoginApp, self).get_application_config()

        conf_directory = os.path.join(self.user_data_dir, self.username)

        if not os.path.exists(conf_directory):
            os.makedirs(conf_directory)

        return super(LoginApp, self).get_application_config(os.path.join(conf_directory, 'config.cfg'))

if __name__ == '__main__':
    LoginApp().run()
