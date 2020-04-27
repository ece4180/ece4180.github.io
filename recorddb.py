import cherrypy
import time
import Adafruit_ADS1x15
import mysql.connector as mariadb
import re
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('templates'))

class Goniometer(object):
    @cherrypy.expose
    def index(self):
        return open('index.html');

    @cherrypy.expose
    def measure(self, Name="Test Name", type="static"):
        # guard clause against malicious input
        name = Name.lower()
        pattern = re.compile("[a-z ]+")
        if not pattern.fullmatch(name):
            return "Use only letters and spaces"
        reading = Goniometer.stable_reading() if type == "static" else Goniometer.max_reading()
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

        if (type == 'static'):
            temp = env.get_template('static.html')
            return temp.render(reading=reading)
            
        temp = env.get_template('dynamic.html')
        return temp.render(readings=readings)

    @staticmethod
    def stable_reading():
        adc = Adafruit_ADS1x15.ADS1115()
        readings = list()
        for i in range(10):
            reading = adc.read_adc(0, gain=1)
            readings.append(reading)
            time.sleep(0.125)
        return sum(readings) / len(readings)

    @staticmethod
    def max_reading():
        adc = Adafruit_ADS1x15.ADS1115()
        readings = list()
        # for 6.25 seconds
        for i in range(200):
            reading = adc.read_adc(0, gain=1)
            readings.append(reading)
            time.sleep(0.03125)
        return max(readings)

if __name__ == '__main__':
    cherrypy.config.update({'server.socket_host': '192.168.1.148'})
    cherrypy.quickstart(Goniometer())
