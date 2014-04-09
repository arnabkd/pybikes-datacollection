import pybikes, datetime, time, threading, logging, string

#Constants
LOG_FILENAME = "datacollection.log"
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)
system = 'bixi'
names = ['bixi-toronto' ,'capital-bixi', 'bixi-montreal']

#City objects
city_objects = []

"""
  Create city objects
"""
def create_city_objects():
  for name in names:
    ob = pybikes.getBikeShareSystem(system, name)
    ob.update()
    city_objects.append(ob)

"""
  Create a timestamp
"""
def get_timestamp():
  ts = time.time()
  st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H:%M:%S')
  return st

"""
  Create lightweight json object
"""
def city_json(city):
  json_file_content = "{ \"city\": \"%s\", \"time\": %d \n, \"stations\": [\n"%(city.meta['city'], time.time())
  stations_json = []
  for station in city.stations:
    stations_json.append("{ \"id\": " + str(station.id) + ", \"bikes\": " + str(station.bikes) + ", \"free\": " + str(station.free) + "}\n")
  json_file_content += string.join(stations_json, ",")      
  json_file_content += "\n]\n}"

  return json_file_content


"""
  Save JSON files for stations
"""
def save_stations_JSON():
  timestamp = get_timestamp()
  logging.debug("Running save_stations_JSON at " + timestamp)
  print ("Running save_stations_JSON at " + timestamp)
  try:
    for city in city_objects:
      city.update()
      json_file_content = city_json(city)
      print json_file_content
      json_file_name = "../data/" + city.meta['city'] + "/" + get_timestamp() + ".json"
      
      fo = open(json_file_name, "wb")
      fo.write(json_file_content)
      fo.close()
      logging.debug("Wrote data to " + json_file_name)
  except:
    logging.exception("Error (something awful happened):")
  threading.Timer(300, save_stations_JSON).start()


#Start log
logging.debug("Starting datacollection at " + get_timestamp())
print ("Starting datacollection at " + get_timestamp())
create_city_objects()
save_stations_JSON()
