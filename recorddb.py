import cherrypy
import time
import Adafruit_ADS1x15
import mysql.connector as mariadb
import re
import math
import os
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('templates'))

class Goniometer(object):
    @cherrypy.expose
    def index(self):
        temp = env.get_template('index.html')
        return temp.render()

    @cherrypy.expose
    def measure(self, Name="Test Name", type="static"):
        # guard clause against malicious input
        name = Name.lower()
        pattern = re.compile("[a-z ]+")
        if not pattern.fullmatch(name):
            return "Use only letters and spaces"
        if type == "static":
            reading = Goniometer.stable_reading()
            dtg = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            print('Local current time:', dtg)
            print('flex value:', reading)

            try:
                # open the connection and execute query
                conn = mariadb.connect(user='root', password='4180', database='goniometer')
                cursor = conn.cursor()
                cursor.execute('''INSERT INTO readings(dtg, angle, name) VALUES(%s,%s,%s)''', (dtg,reading,name))
                # commit change
                conn.commit()
            except mariadb.Error as error:
                print('Error: {}'.format(error))
            finally:
                # close connection
                print('The last inserted id was:', cursor.lastrowid)
                conn.close()
            temp = env.get_template('static.html')
            return temp.render(Name=Name, reading=reading)
        time, readings = Goniometer.dynamic_reading()
        fig, ax = plt.subplots()
        ax.plot(time, readings)
        ax.set(xlabel='Time (s)', ylabel='Goniometer reading (degrees)')
        ax.grid()
        fig.savefig("public/images/dynamic_reading.png")
        temp = env.get_template('dynamic.html')
        return temp.render(Name=Name, max_angle=max(readings))

    @staticmethod
    def stable_reading():
        adc = Adafruit_ADS1x15.ADS1115()
        readings = list()
        for i in range(100):
            reading = adc.read_adc(0, gain=1)
            readings.append(reading)
            time.sleep(0.0125)
        return Goniometer.get_angle(sum(readings) / len(readings))

    @staticmethod
    def dynamic_reading():
        adc = Adafruit_ADS1x15.ADS1115()
        readings = list()
        # for 6.25 seconds
        t = np.arange(0, 6.25, 0.03125)
        for i in range(200):
            _readings = list()
            for i in range(10):
                reading = adc.read_adc(0, gain=1)
                _readings.append(reading)
            readings.append(Goniometer.get_angle(sum(_readings) / len(_readings)))
            time.sleep(0.03125)

        return t, readings

    @staticmethod
    def get_angle(x):
        return 90.2 - (8.71*x) + (0.428 * (x ** 2)) - (0.0118 * (x ** 3))

class HistoryPage(object):
    @cherrypy.expose
    def index(self):
        temp = env.get_template('history.html');
        try:
            conn = mariadb.connect(user='root', password='4180', database='goniometer')
            cursor = conn.cursor()
            cursor.execute('''SELECT * FROM readings ORDER BY dtg DESC LIMIT 20''')
            return temp.render(entries=cursor)
        except mariadb.Error as error:
            print('Error: {}'.format(error))
        return temp.render()

    @cherrypy.expose
    def find_by_name(self, patient_name):
        temp = env.get_template('history.html');
        try:
            conn = mariadb.connect(user='root', password='4180', database='goniometer')
            cursor = conn.cursor()
            cursor.execute('''SELECT * FROM readings WHERE name=%s ORDER BY dtg DESC''', (patient_name,));
            return temp.render(entries=cursor)
        except mariadb.Error as error:
            print('Error: {}'.format(error))
        return temp.render()


root = Goniometer()
root.history = HistoryPage()

if __name__ == '__main__':
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './public'
        }
    }
    cherrypy.config.update({'server.socket_host': '192.168.1.148'})
    cherrypy.quickstart(root, '/', conf)
