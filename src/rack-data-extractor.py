
import pybikes, datetime, time, threading, logging, string, os

system = 'bixi'
name = ['bixi-toronto']

city_obj = pybikes.getBikeShareSystem('bixi', 'bixi-toronto')

jc = "{ \"city\": \"%s\", \"longitude\": \"%f\", \"latitude\": \"%f\",\"stations\": [\n"%(city_obj.meta['city'], city_obj.meta['longitude'], city_obj.meta['latitude'])

jc += "]}"
print jc

city_obj.update()
