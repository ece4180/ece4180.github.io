---
title: ECE4180 project
youtubeId: ybji16u608U
---

# IoT Goniometer

## ECE4180 Spring 2020 Final Project 

## Project Members: Emily Watson, Joseph Malone, Jeremy Kwok, Kenneth Chua

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

If your raspberry pi has not been set up with the correct libraries, please see [how to setup the rpi.](https://github.com/ece4180/ece4180.github.io/blob/master/setup.md)

---
*Explantion of Code*
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

To see the full code refer to [this].

We also need to enable cgi, make it executable and restart our webserver.
```
sudo a2enmod cgi
sudo chmod +x /usr/lib/cgi-bin/recordadc.cgi
systemctl restart apache2
```

The readings should now be avaliable at ```[ip address]/cgi-bin/recordadc.cgi``` on the same network.
