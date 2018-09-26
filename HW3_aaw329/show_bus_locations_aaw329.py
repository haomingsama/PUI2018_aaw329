import json
try:
    import urllib2 as urllib
except ImportError:
    import urllib.request as urllib
import os
import sys


if len(sys.argv) != 3:
    print("Usage: %s %s %s" % (sys.argv[0], "<API_KEY>", "<BUS_LINE>"))
    sys.exit(1)


api_key  = sys.argv[1]
bus_line = sys.argv[2]

print("Gathering info for bus line: %s" % bus_line)

# Build URL based on API key and requested bus line
url = ("http://api.prod.obanyc.com/api/siri/vehicle-monitoring.json"
       "?key=%s"
       "&LineRef=%s"
       % (api_key, bus_line))

# Testing with a JSON file locally
#with open("bus.json", "r") as f:
#    data = f.read()

# Get information from API and read with urllib/json libraries
response = urllib.urlopen(url)
data = response.read().decode("utf-8")
bus_dict = json.loads(data)

# Find number of busses
try:
    bus_count = len(bus_dict["Siri"]
                            ["ServiceDelivery"]
                            ["VehicleMonitoringDelivery"]
                            [0]
                            ["VehicleActivity"])
except KeyError:
    print("Invalid bus line requested.")
    sys.exit(1)
print("There are %d active busses" % bus_count)

# For each bus, print the coordinates of the bus
for i in range(bus_count):
    latitude = (bus_dict["Siri"]
                        ["ServiceDelivery"]
                        ["VehicleMonitoringDelivery"]
                        [0]
                        ["VehicleActivity"]
                        [i]
                        ["MonitoredVehicleJourney"]
                        ["VehicleLocation"]
                        ["Latitude"])
    longitude = (bus_dict["Siri"]
                         ["ServiceDelivery"]
                         ["VehicleMonitoringDelivery"]
                         [0]
                         ["VehicleActivity"]
                         [i]
                         ["MonitoredVehicleJourney"]
                         ["VehicleLocation"]
                         ["Longitude"])
    print("Bus ID %d is at latitude/longitude (%2.6f,%2.6f)" 
          % (i, latitude, longitude))

