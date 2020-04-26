import cherrypy
import time
import Adafruit_ADS1x15
import mysql.connector as mariadb
import re

class Goniometer(object):
    @cherrypy.expose
    def index(self):
        return """<html>
            <head>
                <h1>Goniometer</h1>
            </head>
            <body>
                <form method="get" action="measure">
                    <div>
                        <input type="radio" id="static" name="type" value="static">
                        <label for="static">Static</label><br>
                        <input type="radio" id="dynamic" name="type" value="dynamic">
                        <label for="dynamic">Dynamic</label><br>
                    </div>
                    <input type="text" name="Name"/>
                    <button type="submit">Get reading for patient</button>
                </form>
            </body>
        </html>"""

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

        return "name: " + name + "reading:" + str(reading)

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
