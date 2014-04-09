from math import sin, cos, sqrt, atan2, radians
from transformer import get_file_content
import collections

def get_distance(pos1,pos2):
  lat1, lon1 = pos1
  lat2, lon2 = pos2
  R = 6373.0
  lat1 = radians(lat1); lon1 = radians(lon1)
  lat2 = radians(lat2); lon2 = radians(lon2)
  
  dlon = lon2 - lon1
  dlat = lat2 - lat1
  a = (sin(dlat/2))**2 + cos(lat1) * cos(lat2) * (sin(dlon/2))**2
  c = 2 * atan2(sqrt(a), sqrt(1-a))
  distance = R * c
  
  return distance

#Hardcoded station information:
Rack = collections.namedtuple("Rack", "number description latitude longitude online bikes locks")
rack_info_file = "../2013-2014 Oslo/bikes/racks.txt"
rack_info = get_file_content(rack_info_file)
racks = [eval(line) for line in rack_info]
center_x, center_y = 59.912579999999998, 10.74193

rack_data_file = "../2013-2014 Oslo/bikes/racks-dict.txt"
fo = open(rack_data_file, 'w')
fo.write("{ \n")

for rack in racks:
  line = ("%d: {\'distance\': %f, \'capacity\': %d}, \n") %(rack.number, get_distance((center_x,center_y), (rack.latitude, rack.longitude)), (rack.bikes + rack.locks))
  fo.write(line)
  
fo.write("}")
fo.close()