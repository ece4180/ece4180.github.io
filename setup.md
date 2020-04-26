# Setup
## Webserver
We recommend running the webserver using the apache2 or nginx. The following set up instructions is for apache2.
```
sudo apt-get update
sudo apt-get upgrade
sudo apt install apache2
```

We can view our ip-address using ```hostname -I```

## ADS 1115
To set up the raspberry pi to use the i2c sensor, we can use the gui to enable the i2c protocol.
First we need to install the i2ctools package.
```
sudo apt-get update
sudo apt-get install i2ctools
```
Afterward we need to check that the **/etc/modules** file contains the following line at the end of file.
```
i2c-dev
```
Next, enable i2c in the boot configuration by uncommenting the line: `dtparam=i2c_arm=on`.
Remember to reboot after enabling the i2c protocol. To ensure it is working.
```
sudo i2cdetect -y 1
```

We need to download the library for our ADS ADC. When using python and pip, make sure to use python3 and pip3
```
sudo apt-get install python-pip
python -m pip install --upgrade pip setuptools wheel
sudo apt-get install git build-essential python-dev python-smbus
git clone https://github.com/adafruit/Adafruit_Python_ADS1x15
cd Adafruit_Python_ADS1x15
sudo python setup.py install
```

## [Optional] Database
### Setting up
We can setup our pi to store our data on persistent storage.
```
sudo apt install mariadb-server
sudo service apache2 restart
sudo mysql_secure_installation
```

We can now set up our database. We log in to the mysql command line using our root account.
```
sudo mysql -u root -p
```

In the mysql command line we can create the database and the table.
```
CREATE DATABASE goniometer;
USE goniometer;
CREATE TABLE readings(dtg text NOT NULL, angle text NOT NULL, name text);
```

We also need to install the python library to connect to the mysql database.
```
sudo apt-get install libmariadbclient-dev
pip install mysql-connector
```

### Linking to a webpage
We will use the CherryPy framework for this.
```sudo pip install cherrypy```

Import the library
```python
import cherrypy
import time
import Adafruit_ADS1x15
import mysql.connector as mariadb
import re
```

Define the class and expose a method for reading new data.
```python
class Goniometer(object):
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
```

We then define the measure method.
```python
    @cherrypy.expose
    def measure(self, name="Test Name"):
        # guard clause against malicious input
        name = name.tolower()
        pattern = re.compile("[a-z ]+")
        if !pattern.fullmatch(name):
            return "Use only letters and spaces"
        reading = stable_reading() if type == "static" else max_reading()
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
```

To take measurements
```
    def stable_reading(self):
        adc = Adafruit_ADS1x15.ADS1115()
        readings = list()
        for i in range(10):
            reading = adc.read_adc(0, gain=1)
            readings.append(reading)
            time.sleep(0.125)
        return sum(readings) / len(readings)

    def max_reading(self):
        adc = Adafruit_ADS1x15.ADS1115()
        readings = list()
        # for 6.25 seconds
        for i in range(200):
            reading = adc.read_adc(0, gain=1)
            readings.append(reading)
            time.sleep(0.03125)
        return max(readings)
```

Then we write the main program.
```python
if __name__ == '__main__':
    cherrypy.quickstart(Goniometer())
```

For full code refer [here](https://github.com/ece4180/ece4180.github.io/blob/master/recorddb.py).
