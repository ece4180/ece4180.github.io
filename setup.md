# Setup
## [Optional] Database
## Webserver
## ADS 1115
To set up the raspberry pi to use the i2c sensor, we need to ensure it is up to date and configured to use the i2c protocol.
```
sudo apt-get update
sudo apt-get upgrade
```
We can use the gui to enable the i2c protocol. Afterward we need to check the ```/etc/modules``` file contains the following line at the end of file.
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
