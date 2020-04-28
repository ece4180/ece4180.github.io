import Adafruit_ADS1x15
import numpy as np
import time

def stable_reading():
    adc = Adafruit_ADS1x15.ADS1115()
    readings = list()
    for i in range(100):
        reading = adc.read_adc(0, gain=1)
        readings.append(reading)
        time.sleep(0.0125)
    return Goniometer.get_angle(sum(readings) / len(readings))

def dynamic_reading():
    adc = Adafruit_ADS1x15.ADS1115()
    readings = list()
    # for 6.25 seconds
    t = np.arange(0, 6.25, 0.03125)
    for i in range(200):
        _readings = list()
        for i in range(10):
            reading = adc.read_adc(0, gain=1)
            _readings.append(reading)
        readings.append(Goniometer.get_angle(sum(_readings) / len(_readings)))
        time.sleep(0.03125)

    return t, readings
