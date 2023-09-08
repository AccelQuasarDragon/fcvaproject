from kivy.config import Config
Config.set('kivy', 'log_level', 'debug')

# Set the size of the window
Config.set('graphics', 'width', '600')
Config.set('graphics', 'height', '400')

# Make the window non-resizable
Config.set('graphics', 'resizable', '0')

import kivy
import requests
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Rectangle
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window

kivy.require('2.0.0')

Window.clearcolor = (0, 0, 0, 0)

class LoginPopup(Popup):

    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.title = "Login"
        self.size_hint = (0.6, 0.4)
        self.auto_dismiss = False

        layout = BoxLayout(orientation='vertical')
        self.username_input = TextInput(hint_text='Enter your name', multiline=False)
        login_button = Button(text='Login')
        login_button.bind(on_press=self.on_login)

        layout.add_widget(self.username_input)
        layout.add_widget(login_button)

        self.content = layout

    def on_login(self, instance):
        if self.username_input.text:
            self.app.username = self.username_input.text
            self.app.title = "Logged in as {}!".format(self.app.username)
            main_ui = self.app.build_ui()
            self.app.root_window.add_widget(main_ui)
            self.dismiss()


class CounterApp(App):
    username = ''
    
    def build(self):
        login_popup = LoginPopup(self)
        login_popup.open()
        return FloatLayout()  # Empty layout as a placeholder until the user logs in

    def build_ui(self):
        layout = FloatLayout()

        # Setting the background image for the layout
        with layout.canvas.before:
            self.bg = Rectangle(source='bg.png', size=layout.size, pos=layout.pos)
        
        layout.bind(size=self._update_rect, pos=self._update_rect)

        # Wins layout
        self.wins_label = Label(text='0', font_size=24, pos_hint={'x': -0.025, 'y': 0.15}, size_hint=(0.3, 0.1))
        
        # Plus button for Wins
        wins_plus_button = Button(background_normal='plus_image.png', background_down='plus_image_down.png', pos_hint={'x': 0.1, 'y': 0.25}, size_hint=(0.05, 0.05))
        wins_plus_button.bind(on_press=self.add_win)

        # Minus button for Wins
        wins_minus_button = Button(background_normal='minus_image.png', background_down='minus_image_down.png', pos_hint={'x': 0.1, 'y': 0.1}, size_hint=(0.05, 0.05))
        wins_minus_button.bind(on_press=self.subtract_win)

        # Losses layout
        self.losses_label = Label(text='0', font_size=24, pos_hint={'x': 0.075, 'y': 0.15}, size_hint=(0.3, 0.1))

        # Plus button for Losses
        losses_plus_button = Button(background_normal='plus_image.png', background_down='plus_image_down.png', pos_hint={'x': 0.2, 'y': 0.25}, size_hint=(0.05, 0.05))
        losses_plus_button.bind(on_press=self.add_loss)

        # Minus button for Losses
        losses_minus_button = Button(background_normal='minus_image.png', background_down='minus_image_down.png', pos_hint={'x': 0.2, 'y': 0.1}, size_hint=(0.05, 0.05))
        losses_minus_button.bind(on_press=self.subtract_loss)

        # Add widgets to the layout
        layout.add_widget(self.wins_label)
        layout.add_widget(wins_plus_button)
        layout.add_widget(wins_minus_button)
        layout.add_widget(self.losses_label)
        layout.add_widget(losses_plus_button)
        layout.add_widget(losses_minus_button)

        return layout

    def add_win(self, instance):
        current_wins = int(self.wins_label.text)
        self.wins_label.text = f'{current_wins + 1}'
        self.save_to_file()

    def subtract_win(self, instance):
        current_wins = int(self.wins_label.text)
        if current_wins > 0:
            self.wins_label.text = f'{current_wins - 1}'
        self.save_to_file()

    def add_loss(self, instance):
        current_losses = int(self.losses_label.text)
        self.losses_label.text = f'{current_losses + 1}'
        self.save_to_file()

    def subtract_loss(self, instance):
        current_losses = int(self.losses_label.text)
        if current_losses > 0:
            self.losses_label.text = f'{current_losses - 1}'
        self.save_to_file()

    def save_to_file(self):
        with open('counters.txt', 'w') as f:
            f.write(f"Wins: {self.wins_label.text}\n")
            f.write(f"Losses: {self.losses_label.text}")
    
    def _update_rect(self, instance, value):
        self.bg.size = instance.size
        self.bg.pos = instance.pos

    def on_stop(self):
        # Create the message to send
        message = f"User: {self.username}\nWins: {self.wins_label.text}\nLosses: {self.losses_label.text}"

        # Send POST request
        requests.post("https://ntfy.sh/ryzz_test", data=message.encode(encoding='utf-8'))

if __name__ == '__main__':
    CounterApp().run()