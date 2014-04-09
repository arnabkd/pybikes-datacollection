import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import time, datetime

#Setup
fig = plt.figure()
ax = fig.add_subplot(111, projection = '3d')

#Set axis labels
ax.set_zlabel("Number of bikes")
ax.set_ylabel("Time of day (local time)")
ax.set_xlabel("ID")

#Get data
fo = open("/ifi/bifrost/m01/arnabkd/git/thesis/pybikes-datacollection/2013-2014 Oslo/bikes/2013-04-30", 'r')
file_content = fo.read()
fo.close()


def get_3Ddata(file_content):
  states = {}
  for line in file_content.split('\n'):
     if (len(line) > 5):
        timestamp, state = eval(line)
        states[timestamp] = state
  return states

data = get_3Ddata(file_content)

bikes_data = []

for timestamp in data.keys():
  H_val = (int) (datetime.datetime.fromtimestamp(timestamp).strftime("%H"))

  #Get the state data for this timestamp
  state = data[timestamp]
  bikes_data.append([state.keys()[0], H_val, state[state.keys()[0]]])
  if (state.keys()[0] is not 1):
     print "Adding for ID: %s" %(state.keys()[0])
     print state
  
  #for id in state.keys():
    #y_val = id
    #z_val = state[id]
    #bikes_data.append([x_val, y_val, z_val])

#Draw scatter plot
for id,time_of_day,bikes in np.array(bikes_data):
  ax.scatter(id,time_of_day,bikes)

plt.show()
