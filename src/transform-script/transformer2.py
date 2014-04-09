import sys, os, glob, datetime, json
from collections import namedtuple

"""
  File I/IO
"""
def get_file_content(filepath):
  fo = open(filepath, "r")
  content = fo.read()
  fo.close()
  return content

def get_file_lines(filepath):
  fo = open(filepath, "r")
  content = fo.readlines()
  fo.close()
  return content

"""
  Create a timestamp
"""
def get_timestamp(ts):
  st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H:%M:%S')
  return st

"""
  Transform old content into new-style data
"""
def transform(old_content, target_dir, racks):
  #Each line should create a new file
  for line in old_content:
    res = eval(line)
    filename = target_dir + get_timestamp(res[0]) + ".json"
    #print "epoch", res[0], "=> FileName: ", (target_dir+filename)
    #print filename
   
    #Create a new file, transform the content and write to it
    status = res[1]

    #Add missing stations
    missing_stations = filter(lambda x: x not in status.keys(), racks.keys())
    for station in missing_stations:
      status[station] = 0
    
    #Transform content
    json_content = "{ \"city\": %s, \"time\": %s\n, \"stations\": [\n"%("\"Oslo\"", res[0])
    size = len(status)
    
    for key in status.keys():
      if key in racks.keys():
        bikes = status[key]
        free = racks[key]['capacity'] - bikes
        json_content += "{\"id\": %s, \"bikes\": %s, \"free\": %s},\n"%(key, bikes,free)
        
      
    json_content = json_content[:-2]
    json_content += "]}\n"

    fo = open(filename, "w")
    fo.write(json_content)
    fo.close()
  

"""
   Get rack data from a file with a list of namedtuples (in this format)
"""
def get_rack_data(rack_data_file):
  invalid_racks = []
  racks_info = get_file_lines(rack_data_file)
  Rack = namedtuple("Rack", ['number','description','latitude', 'longitude', 'online', 'bikes', 'locks'])
  racks = {}

  for line in racks_info:
    rack = eval(line)
    rack_dict = {}
    rack_dict ['id'] = rack.number
    rack_dict ['description'] = rack.description
    rack_dict ['latitide'] = rack.latitude
    rack_dict ['longitude'] = rack.longitude
    rack_dict ['capacity'] = rack.bikes + rack.locks
    
    #if rack_dict ['capacity'] < 1:
    invalid_racks.append(rack.number)
    racks[rack.number] = rack_dict

  return invalid_racks, racks

"""
   Sanitize the capacities of the invalid racks, given a list of files to extract maximums from.
   Write a racks-dict.json to the src_dir
"""
def sanitize_rack_capacities(src_dir, files_list, racks, invalid_racks):
  #print files_list
  print "Invalid capacities for racks: ", invalid_racks
  print "Trying to find proper value in %s files"%(len(files_list))
  Rack = namedtuple("Rack", ['number','description','latitude', 'longitude', 'online', 'bikes', 'locks'])
  
  for f in files_list:
    content = get_file_lines(f)
    
    for line in content:
      status = eval(line)[1]
      for rack in invalid_racks:
        #If the new capacity exceeds what is previously recorded
        if rack in status.keys() and status[rack] > racks[rack]['capacity']:
          #print "updating capacity for rack %s to %s"%(rack, status[rack])
          racks[rack]['capacity'] = status[rack]
  json_content = json.dumps(racks, indent=4, sort_keys=True)
  fo = open(src_dir + "racks_dict.json", "w")
  fo.write(json_content)
  fo.close()

##############################################################################################################
################## Transform script ##########################################################################
##############################################################################################################

#Scan for files in this directory
src_dir = "../../2013-2014-Oslo/bikes2/"
files = glob.glob(src_dir + "20*")
#print "%s files found in %s, that contain oslobysykkel data"%(len(files), src_dir)

#Create a data directory if one does not exist  
target_dir = src_dir + "new-style-data/"
#print "targetDir exists:", os.path.exists(target_dir) 
if not os.path.exists(target_dir):
  print "creating directory",target_dir
  os.mkdir(target_dir)
  print "Directory created successfully" if  os.path.exists(target_dir) else "Could not create directory"


invalid_racks, racks = get_rack_data(src_dir + "racks.txt")
if len(invalid_racks) > 0:
  sanitize_rack_capacities(src_dir, files, racks, invalid_racks)

for id in racks.keys():
  print racks[id]

"""
i = 0
for old_style_file in files:
  old_content = get_file_lines(old_style_file)
  transform(old_content, target_dir, racks)
  i += 1
  print "transformed %s files"%(i)
  
"""
