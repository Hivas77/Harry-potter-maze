
import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.properties import StringProperty, NumericProperty, BooleanProperty
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.storage.jsonstore import JsonStore
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from random import randint, choice
import json
import os

# Set default window size (used on desktop; mobile will auto-resize)
Window.size = (360, 640)

# Paths
DATA_PATH = "user_data.json"
CHECKPOINTS = [(50, 50), (100, 300), (300, 500)]

# Load or create store
if not os.path.exists(DATA_PATH):
    with open(DATA_PATH, 'w') as f:
        json.dump({}, f)

def load_users():
    with open(DATA_PATH, 'r') as f:
        return json.load(f)

def save_users(users):
    with open(DATA_PATH, 'w') as f:
        json.dump(users, f)

class LoginScreen(Screen):
    def login(self, username, password):
        users = load_users()
        if username in users and users[username]['password'] == password:
            App.get_running_app().username = username
            self.manager.current = 'game'
        else:
            self.ids.status.text = 'Invalid credentials!'

    def register(self, username, password):
        users = load_users()
        if username in users:
            self.ids.status.text = 'User already exists!'
        else:
            users[username] = {
                'password': password,
                'xp': 100,
                'kills': 0,
                'checkpoint': 0,
                'is_admin': username == "Hivas"
            }
            save_users(users)
            self.ids.status.text = 'Registered! You can now log in.'

class GameScreen(Screen):
    xp = NumericProperty(100)
    kills = NumericProperty(0)
    is_admin = BooleanProperty(False)

    def on_enter(self):
        app = App.get_running_app()
        users = load_users()
        user_data = users[app.username]
        self.xp = user_data.get('xp', 100)
        self.kills = user_data.get('kills', 0)
        self.is_admin = user_data.get('is_admin', False)
        self.player_position = CHECKPOINTS[user_data.get('checkpoint', 0)]
        self.ids.info.text = f"XP: {self.xp} | Kills: {self.kills}"
        # Initialize game objects here later

    def cast_spell(self, spell):
        if spell == "avada":
            self.kills += 1
        elif spell == "expelliarmus":
            if self.xp >= 10:
                self.xp -= 10
        elif spell == "patronum":
            self.xp -= 5
        elif spell == "totalus":
            pass
        elif spell == "sprint":
            pass
        elif spell == "shield":
            pass
        self.save_progress()

    def save_progress(self):
        app = App.get_running_app()
        users = load_users()
        users[app.username]['xp'] = self.xp
        users[app.username]['kills'] = self.kills
        users[app.username]['checkpoint'] = 0  # update checkpoint logic here
        save_users(users)
        self.ids.info.text = f"XP: {self.xp} | Kills: {self.kills}"

class GameApp(App):
    username = ""
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(GameScreen(name='game'))
        return sm

if __name__ == '__main__':
    GameApp().run()
