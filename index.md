---
title: ECE4180 project
youtubeId: ybji16u608U
---

# IoT Goniometer

## ECE4180 Spring 2020 Final Project

## Project Members: Emily Wilson, Joseph Malone, Jeremy Kwok, Kenneth Chua

### Introduction

The IoT Goniometer is a device which uses a goniometer to measure a joint's function such as an elbow or a knee, based on their degree of movement. The measurements collected will then be uploaded to the internet using the Raspberry PI Zero.

### Motivation

Currently, there is a physical/analog goniometer which only take static measurements of patients for doctors. However, the current method does not take into account the degree of movement when the patient is doing strenuous activities such as running. This project will help patients to have both their static and dynamic measurements taken while assisting doctors to automatically track their patients progress.

### Demonstration

*Insert Video Demonstration Here*
{% include youtube.html id=page.youtubeId %}

### Components

The following are the components used to built this project:
* Goniometer
* [Flex Sensor](https://os.mbed.com/components/Flex-Sensor/)
* Raspberry Pi Zero
* ADC Convertor

### Main Program
---
**NOTE**

If your raspberry pi has not been set up with the correct libraries, please see [how to setup the rpi.](/setup.md)

---
**Running the application**

We are using CherryPy and Jinja2 to create a web application that can will display static, dynamic, and previous goniometer readings.

The application is broken into two parts, the goniometer class to take static and dynamic readings (in `goniometer.py`) and the history class to display previous static measurements (in `history.py`).

In `app.py`, we combine the goniometer and history classes, with the goniometer as the root of the application.
```
root = Goniometer()
root.history = HistoryPage()
```
We then set the application to run on the Raspberry Pi's IP address so other computers on the same network can access the application.
```
cherrypy.config.update({'server.socket_host': '192.168.1.148'})
```
To run the application, we can just run the `app.py` file on the Raspberry Pi.
```
python3 app.py
```
And we can access the application by going to http://192.168.1.148:8080 in a browser on any computer connected to the same network as the Pi.
Please see [here](https://github.com/ece4180/ece4180.github.io/blob/master/app.py) for full code.

**Explanation of the code**

*Goniometer*

The goniometer can take two kinds of measurements, a static reading and a dynamic reading.
The static reading takes 100 samples and averages the readings from the flex sensor and the ADC to give one reading which is then converted to an angle using an equation from calibrating the goniometer.
```
for i in range(100):
      reading = adc.read_adc(0, gain=1)
      readings.append(reading)
      time.sleep(0.0125)
```
To calibrate the goniometer we recorded the flex sensor reading at different angles, then graphed flex sensor reading vs. angle and generated a trendline for the data.
{{ insert image of graph after calibration }}
The web application then redirects to the static reading display page which shows the static reading as well as gives an option to take another reading without going back to the home page.
{{ insert image of static reading page }}

The dynamic reading takes 10 readings of the flex sensor then averages them for a stable reading and does this 200 times, reading the flex sensor for a total of 6.25 seconds.
```
for i in range(200):
      _readings = list()
      for i in range(10):
          reading = adc.read_adc(0, gain=1)
          _readings.append(reading)
      readings.append(Goniometer.get_angle(sum(_readings) / len(_readings)))
      time.sleep(0.03125)
```
The web application then redirects to the dynamic reading display page, which shows the maximum angle reached as well as a graph of the goniometer reading vs. time.
{{ insert picture of dynamic reading page here }}

Full measurement code can be found [here](https://github.com/ece4180/ece4180.github.io/blob/master/recordadc.py) and web application code for the goniometer portion can be found [here](https://github.com/ece4180/ece4180.github.io/blob/master/goniometer.py)



### Running as a script

To script the reading of the flex sensor, we can use a [Common Gateway Interface](https://en.wikipedia.org/wiki/Common_Gateway_Interface) dynamic page written in python.
We need to write the script in the ```/usr/lib/cgi-bin``` directory.
Firstly, we need to identify that it is a python script and import the relevant libraries.
```
#!/usr/bin/python
import time
import Adafruit_ADS1x15
```

We then initialise the ADC component and take a reading
```
adc = Adafruit_ADS1x15.ADS1115()
reading = adc.read_adc(0, gain=1)
```

We can then transform the reading into the relative angle using
```

```

Finally, we read the current time and print the webpage
```
print 'Content-Type: text/html'
print ''
print '<html>'
print '<head>'
print '<title>Goniometer</title>'
print '</head>'
print '<body>'
print '<h2>Current Flex Sensor Info</h2>'
print 'ADC reading:', reading, '<br />'
print 'Current time:', dtg, '<br />'
print 'The angle is:', 'degrees'
print '</body>'
print '</html>'
```

To see the full code refer to [this](https://github.com/ece4180/ece4180.github.io/blob/master/recordadc.cgi).

We also need to enable cgi, make it executable and restart our webserver.
```
sudo a2enmod cgi
sudo chmod +x /usr/lib/cgi-bin/recordadc.cgi
systemctl restart apache2
```

The readings should now be avaliable at ```[ip address]/cgi-bin/recordadc.cgi``` on the same network.

### If we want readings to be saved we can use a mysql db
Please see [here](/setup.md#optional-database) for full instructions.
