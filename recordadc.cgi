#!/usr/bin/python
import time
import Adafruit_ADS1x15

adc = Adafruit_ADS1x15.ADS1115()
reading = adc.read_adc(0, gain=1)

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
