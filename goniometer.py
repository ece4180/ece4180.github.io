import cherrypy
import re
import mysql.connector as mariadb
import time
from jinja2 import Environment, FileSystemLoader

from .recordadc import stable_reading, dynamic_reading
from .utils import get_angle, save_plot

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
            reading = stable_reading()
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
        
        time, readings = dynamic_reading()
        save_plot(time, readings)
        temp = env.get_template('dynamic.html')
        return temp.render(Name=Name, max_angle=max(readings))

    @staticmethod
    def get_angle(x):
        return 90.2 - (8.71*x) + (0.428 * (x ** 2)) - (0.0118 * (x ** 3))
