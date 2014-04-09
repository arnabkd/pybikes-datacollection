import time, datetime, numpy as np
from os import listdir
from os.path import isfile, join
from oslobysykkel import get_racks

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

old_data_dir = "/ifi/bifrost/m01/arnabkd/git/thesis/pybikes-datacollection/src/testdir/"

def get_file_lines(filepath):
  fo = open(filepath, "r")
  content = fo.readlines()
  fo.close()
  return content
  
def get_file_content(filepath):
  fo = open(filepath, "r")
  content = fo.read()
  fo.close()
  return content
  
"""
  Create a timestamp
"""
def get_timestamp(ts):
  st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H:%M:%S')
  return st

"""
  Return hour of day
"""
def get_hour_of_day(ts):
  return datetime.datetime.fromtimestamp(ts).strftime('%H')

"""
  Input is a dict in the form {station_id: available_bikes} if available_bikes > 0
"""
def transform_content(state):
   pass


"""
  Split files in a directory
"""
def split_files(srcdir):
  files = [f for f in listdir(old_data_dir) if isfile(join(old_data_dir,f))]
  for file in files:
    split_file(srcdir, file)



"""
  Split a file
"""
def split_file(srcdir, file):
  content = get_file_content(srcdir+file)

  #Make a list of states 
  states = []
  for line in content:
    states.append(eval(line))

  #Every element in the states list has a timestamp and the state itself
  for timestamp,state in states:
    #new_fo = open(srcdir + get_timestamp(timestamp) + ".json", "w")
    #print "file name should be ", new_fo.name
    #print "content should be \n", state
    content = transform_content(state)
    #print content
    #new_fo.close()


def get_missing_keys(L, subL):
  for elem in subL:
    L.remove(elem)
  return L


"""
  Parse old-style-data
"""
def parse(data):
  #Parse data per hour
  for hourly_data in data:
    missing_stations = get_missing_keys(racks_dict.keys(), hourly_data[1].keys())
    #print "Missing stations for %s: %s" %(get_timestamp(hourly_data[0]), missing_stations)

    for station in missing_stations:
      hourly_data[1][station] = 0

  return data  

"""
  Transform to numpy array
"""
def transform_to_lists(data):
  X,Y,Z = [],[],[]
  
  for t in data:
    h = get_hour_of_day(t[0])
    for id in t[1].keys():
       capacity = racks_dict[id]["capacity"]
       distance = racks_dict[id]["distance"]

       #Ignore 0-capacity nodes (causes division by zero failures)
       if capacity is not 0:
         X.append((int) (h))
         Y.append((float) (distance))
         Z.append((float) ((t[1][id] *100.0) / capacity))
  
  #return [[t[0], t[1], t[2]] for t in zip(X,Y,Z)]
  return X,Y,Z

try:
  #Set up hardcoded rack data
  rack_data_file = "../../2013-2014 Oslo/bikes/racks-dict.txt"
  racks_dict = eval(get_file_content(rack_data_file))
    
  #Test old-style data
  old_style_data = get_file_lines("../2013-2014 Oslo/bikes/2013-06-22")
  data = [eval(entry) for entry in old_style_data]


  #data = parse(data)
  #X,Y,Z = transform_to_lists(data)

#X is [0,1,4,5,2,3,23] with values ranging from 0-24
#Y is [0.52,1.73,4.48,5.3,2.2,3.45,2.3] with values ranging from 0-7.0
#Z is [44.5,12.5,4.3,5,92.02] with values ranging from 0-100.0
"""
#Plot the readings
fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")

ax.scatter(X,Y,Z, c="b", marker="^")

ax.set_xlabel("Time of day (hour)")
ax.set_ylabel("Distance from central bike rack")
ax.set_zlabel("Percentage of bikes available")

plt.show()
"""
