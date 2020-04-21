import cherrypy
import time
import Adafruit_ADS1x15
import mysql.connector as mariadb
import re

class Geoniometer(object):
    @cherrypy.expose
    def index(self):
    return """<html>
    <head>Goniometer</head>
    <body>
        <form method="get" action="measure">
            <input type="text" name="Name"/>
            <button type="submit">Get reading for patient</button>
        </form>
    </body>
</html>"""
    @cherrypy.expose
    def measure(self, name="Test Name"):
        # guard clause against malicious input
        name = name.tolower()
        pattern = re.compile("[a-z ]+")
        if !pattern.fullmatch(name):
            return "Use only letters and spaces"
        adc = Adafruit_ADS1x15.ADS1115()
        reading = adc.read_adc(0, gain=1)
        dtg = time.strftime('%Y-%m-%d %H:%M:%S, time.localtime())
        print 'Local current time:', dtg
        print 'flex value:', reading

        try:
            # open the connection and execute query
            conn = mariadb.connect(user='root', password='', database='goniometer')
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO readings(dtg, angle, name) VALUES(%s,%s,%s)''', (dtg,reading,name))
            # commit change
            conn.commit()
        except mariadb.Error as error:
            print 'Error: {}'.format(error)
        finally:
            # close connection
            print 'The last inserted id was:', cursor.lastrowid
            conn.close()
            
        return "name: " + name + "reading:" str(reading)
        
if __name__ == '__main__':
    cherrypy.quickstart(Goniometer())
