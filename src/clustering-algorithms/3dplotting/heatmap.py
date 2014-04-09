#from pylab import *
#from mpl_toolkits.mplot3d import Axes3D

#fig = figure()
#ax = Axes3D(fig)
import json

"""
  File I/O
"""
def get_file_content(filename):
  file_content = ''
  try:
    fo = open(filename, 'r')
    file_content = fo.read()
    fo.close()
  except:
    print 'file not found', filename
  
  return file_content

"""
  Rack data
"""
def get_rack_data(cityname):
  rack_dict = {}
  return rack_dict

def get_data_from_file(file):
  a = json.loads(get_file_content(file))
  
  return ""

#XYZ = [[8,0,90], [8,1,80], [10,2,70], [12,2,50], [16,1,30], [17,1,20]]

XYZ = get_data_from_file('/ifi/bifrost/m01/arnabkd/git/thesis/pybikes-datacollection/src/clustering-algorithms/testdata/2014-03-07_16:29:16.json')

print XYZ

"""
bikes_percentage = [e[0] for e in XYZ]
time_of_day = [e[1] for e in XYZ]
distance_from_center = [e[2] for e in XYZ]

bikes_percentage,time_of_day = np.meshgrid(bikes_percentage, time_of_day)

ax.plot_surface(bikes_percentage,time_of_day,distance_from_center, rstride=1, cstride=1, cmap='hot')

show()
"""
