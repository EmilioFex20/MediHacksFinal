from kivy.uix.screenmanager import ScreenManager, NoTransition
import configparser
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from datetime import datetime
import os, sys
import kivy
from login import Login

kivy.require('1.0.8')

Window.size=(350,580)

class LoginApp(MDApp):
    def build(self):        
        #global screen_manager
        #screen_manager = ScreenManager()
        self.manager = ScreenManager(transition = NoTransition())
        self.manager.add_widget(Builder.load_file("pre-splash.kv"))
        self.manager.add_widget(Login(name='login'))
        return self.manager
    def on_start(self):
        Clock.schedule_once(self.login, 7)
    
    def login(self, *args):
        self.manager.current = "login"

if __name__ == '__main__':        
    LoginApp().run()
        
