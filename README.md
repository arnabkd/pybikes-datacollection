Pybikes data collection script
===

Requirements
- python 2.7+
- pybikes module (get it from https://github.com/eskerda/PyBikes )

Usage
====
Note: Step 1 and 2 is only for people with access to a server.

1. SSH into the server 
2. Start a screen with a nice value of 11 or higher:
  `$nice -n 11 screen`
3. Start the script:
   `python datacollector.py`


Misc notes
====
- Tweak the cities array as you wish to collect data for other cities
- Tweak the timer for the thread in `save_stations_JSON ` to change how often data is collected.


If you have any suggestions or ideas, feel free to clone and send a pull request. Or email me :)
