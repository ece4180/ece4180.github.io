import cherrypy
import mysql.connector as mariadb
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('templates'))

class History(object):
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
