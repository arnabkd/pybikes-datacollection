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

def missing_elements(L, subL):
  L2 = list(L)
  subL2 = list(subL)
  print "recieved a list with ", len(L2), "elements"
  print "received a sublist with", len(subL), "elements"
  for elem in subL2:
    if str(elem) in L2:
      L2.remove(elem)
  print "returning a list with", len(L2), "elements"
  return L2

"""
  Transform old content into new-style data
"""
def transform(old_content, target_dir, racks):
  #Each line should create a new file
  for line in old_content:
    res = eval(line)
    filename = target_dir + get_timestamp(res[0]) + ".json"
    #print "epoch", res[0], "=> FileName: ", (target_dir+filename)
   
    #Create a new file, transform the content and write to it
    status = res[1]

    #Add missing stations
    missing_stations = filter(lambda x: x not in status.keys(), racks.keys())
    for station in missing_stations:
      status[station] = 0
    
    #Transform content
    json_content = "{ \"city\": %s, \"time\": %s\n, \"stations\": [\n"%("\"Oslo\"", res[0])
        
    for id in status.keys():
      bikes = status[id]
      if id in racks.keys():
        free = racks[id]['capacity'] - bikes
        json_content += "{\"id\": %s, \"bikes\": %s, \"free\": %s},\n"%(id, bikes,free)
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
    rack_dict ['latitude'] = rack.latitude
    rack_dict ['longitude'] = rack.longitude
    rack_dict ['capacity'] = rack.bikes + rack.locks
    
    #if rack_dict ['capacity'] < 1:
    invalid_racks.append(rack.number)
    racks[(int)(rack.number)] = rack_dict

  return invalid_racks, racks

"""
   Sanitize the capacities of the invalid racks, given a list of files to extract maximums from.
   Write a racks-dict.json to the src_dir
"""
def sanitize_rack_capacities(src_dir, files_list, racks, invalid_racks):
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
  #json_content = json.dumps(racks, indent=4, sort_keys=True)
  #fo = open(src_dir + "racks_dict.json", "w")
  #fo.write(json_content)
  #fo.close()
  fo = open(src_dir + "racks_dict", "w")
  fo.write(str(racks))
  fo.close()




########################################################################
################## Transform script ####################################
########################################################################

#Scan for files in this directory
src_dir = "../../2013-2014-Oslo/bikes3/"
files = glob.glob(src_dir + "20*")
#print "%s files found in %s, that contain oslobysykkel data"%(len(files), src_dir)

#Create a data directory if one does not exist  
target_dir = src_dir + "new-style-data/"
#print "targetDir exists:", os.path.exists(target_dir) 
if not os.path.exists(target_dir):
  print "creating directory",target_dir
  os.mkdir(target_dir)
  print "Directory created successfully" if  os.path.exists(target_dir) else "Could not create directory"

racks = {}
processed_files = {}

#If there is no racks-dict.json file, create one from the racks.txt file, and sanitize all stations
if not os.path.exists(src_dir+"racks_dict"):
  print "There is no racks-dict file, create one from the racks.txt file, and sanitize all stations"
  invalid_racks, racks = get_rack_data(src_dir + "racks.txt")
  if len(invalid_racks) > 0:
    sanitize_rack_capacities(src_dir, files, racks, invalid_racks)
else:
  print "Racks information file found. Using eval to get racks-dict"
  content = get_file_content(src_dir + "racks_dict")
  racks = eval(content)



processed_files_jsonfile = src_dir + "processed_files.json"
if not os.path.exists(processed_files_jsonfile):
  processed_files = {"done": []}
else:
  processed_files = json.loads(get_file_content(processed_files_jsonfile))
i = 0
for old_style_file in files:
  if old_style_file not in processed_files['done']:
    old_content = get_file_lines(old_style_file)
    transform(old_content, target_dir, racks)
    i += 1
    print "Transformed file %s"%(old_style_file)
    processed_files['done'].append(old_style_file)

#Write the processed files list
fo =  open(processed_files_jsonfile, "w")
fo.write(json.dumps(processed_files, indent=4, sort_keys=True))
fo.close()

