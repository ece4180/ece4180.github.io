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
To set up the raspberry pi to use the i2c sensor, we can use the gui to enable the i2c protocol. Afterward we need to check that the ```/etc/modules``` file contains the following line at the end of file.
```i2c-dev```
Remember to reboot after enabling the i2c protocol.
Use ```sudo i2cdetect -y 1``` to ensure it is working. It will show the address where the ADS is detected.

We need to download the library for our ADS ADC.
```
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

In the mysql command line we can create the databaase and the table.
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

### Code
Firstly, we need to import the relevant libraries.
```
import time
import Adafruit_ADS1x15
import mysql.connector as mariadb
```

We then initialise the ADC component, take a reading and get the current time.
```
adc = Adafruit_ADS1x15.ADS1115()
reading = adc.read_adc(0, gain=1)
dtg = time.strftime('%Y-%m-%d %H:%M:%S, time.localtime())
```

We then print the info we are adding and attempt to add it into the database.
```
print 'Local current time:', dtg
print 'flex value:', reading

try:
    conn = mariadb.connect(user='root', password='', database='goniometer')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO readings(dtg, angle, name) VALUES(%s,%s,%s)''', (dtg,reading,name))
    conn.commit()
except mariadb.Error as error:
    print 'Error: {}'.format(error)
```

We then check that the id has changed and close the connection.
```
finally:
    print 'The last inserted id was:', cursor.lastrowid
    conn.close()
````

### Linking to a webpage
