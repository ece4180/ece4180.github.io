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

The goniometer can take two kinds of measurements, a static reading and a dynamic reading, which we can select from in the main measure page of the application.
![static measure page](https://github.com/ece4180/ece4180.github.io/raw/master/public/images/static_measure_page.png)
The static reading takes 100 samples and averages the readings from the flex sensor and the ADC to give one reading which is then converted to an angle using an equation from calibrating the goniometer.
```
for i in range(100):
      reading = adc.read_adc(0, gain=1)
      readings.append(reading)
      time.sleep(0.0125)
```

To calibrate the goniometer so that we can calculate an angle from the flex sensor reading, we recorded the flex sensor reading at different angles, then graphed flex sensor reading vs. angle and generated a trendline for the data.
![goniometer calibration graph](https://github.com/ece4180/ece4180.github.io/raw/master/public/images/calibration_graph.png)

The web application then redirects to the static reading display page which shows the static reading as well as gives an option to take another reading without going back to the home page.
![static reading page](https://github.com/ece4180/ece4180.github.io/raw/master/public/images/static_reading.png)

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
![dynamic reading webpage](https://github.com/ece4180/ece4180.github.io/raw/master/public/images/dynamic_screenshot.png)

Full measurement code can be found [here](https://github.com/ece4180/ece4180.github.io/blob/master/recordadc.py) and web application code for the goniometer portion can be found [here](https://github.com/ece4180/ece4180.github.io/blob/master/goniometer.py)

*History Page*

The history page makes a mysql query for the 20 most recent static measurements in the database
```
cursor.execute('''SELECT * FROM readings ORDER BY dtg DESC LIMIT 20''')
```
then displays the measurements in a table.
![history page](https://github.com/ece4180/ece4180.github.io/raw/master/public/images/history_page.png)

We can also use the search bar to search for records by patient name. This makes another mysql query for the 20 most recent static measurements taken on that patient.
```
cursor.execute('''SELECT * FROM readings WHERE name=%s ORDER BY dtg DESC''', (patient_name,));
```
![history page with name search](https://github.com/ece4180/ece4180.github.io/raw/master/public/images/history_name_search.png)

Full code for the history page can be found [here](https://github.com/ece4180/ece4180.github.io/raw/master/history.py)
