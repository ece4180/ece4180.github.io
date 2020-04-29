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

Finally, we need to grant permissions to a root user to use the database as root locally.
```
sudo mysql -u root -p
{ login with password created above }
```
In the mariadb console run
```
GRANT ALL PRIVILEGES on *.* to 'root'@'localhost' IDENTIFIED BY '<password>';
FLUSH PRIVILEGES;
```
then exit and restart mysql.
```
sudo service mysql restart
```

### Linking to a webpage
We will use the CherryPy framework for this with Jinja2 for HTML templating.
```
sudo pip3 install cherrypy
pip3 install jinja2
```

We will also need matplotlib and a raspbian dependency for graphing dynamic goniometer measurements.
```
pip3 install matplotlib
sudo apt-get install libatlas-base-dev
```

The app should have all of the dependencies it needs now, so running
`python3 app.py`
will serve the web application at the Raspberry Pi's IP address.
