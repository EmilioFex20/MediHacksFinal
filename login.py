import configparser
import datetime
from kivy.app import App
from kivy.lang import Builder
from kivy .uix.screenmanager import Screen, SlideTransition
from kivymd.toast import toast
import mysql.connector

class Login(Screen):
    pass
    def connect(self):
        app = App.get_running_app()
        input_email = app.manager.get_screen('login').ids['input_email'].text
        input_password = app.manager.get_screen('login').ids['input_password'].text
        config = configparser.ConfigParser()
        config.read('config.ini')

        host = config['mysql']['host']
        user = config['mysql']['user']
        password = config['mysql']['password']
        dbname = config['mysql']['db']

        db = mysql.connect.connect(host = str(host),user = str(user), password=str(password),database = str(dbname))
        cursor = db.cursor()
        
        query = "SELECT count(*) FROM users where email='" + str(input_email)+"' and password = '"+str(input_password)+"'"
        cursor.execute(query)
        data = cursor.fetchone()
        count = data[0]

        if count == 0:
            toast ('Invalid Password')
        else:
            toast('Succesful Login')
            now = datetime.now()
            query = "update users set last_login='" + str(input_email)+"' and password = '"+str(input_password)+"'"
            cursor.execute(query)
            db.commit()
        db.close()
        pass