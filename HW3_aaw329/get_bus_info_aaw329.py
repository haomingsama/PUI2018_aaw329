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

# Build URL based on API key and requested bus line
url = ("http://api.prod.obanyc.com/api/siri/vehicle-monitoring.json"
       "?key=%s"
       "&LineRef=%s"
       "&VehicleMonitoringDetailLevel=calls"  # Needed to get future stop info
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
    sys.stderr.write("Invalid bus line requested.\n")
    sys.exit(1)

# Write to a file named <BUS_LINE>.csv
f = open("%s.csv" % bus_line, "w")

# Create a list for each line of the CSV output, starting with the header
lines = ["Latitude,Longitude,Stop Name,Stop Status"]

# Append a line with the appropriate information for each bus
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
    try:
        stop_name = (bus_dict["Siri"]
                             ["ServiceDelivery"]
                             ["VehicleMonitoringDelivery"]
                             [0]
                             ["VehicleActivity"]
                             [i]
                             ["MonitoredVehicleJourney"]
                             ["OnwardCalls"]
                             ["OnwardCall"]
                             [0]
                             ["StopPointName"])
    except KeyError:
        stop_name = "N/A"
    try:
        stop_status = (bus_dict["Siri"]
                               ["ServiceDelivery"]
                               ["VehicleMonitoringDelivery"]
                               [0]
                               ["VehicleActivity"]
                               [i]
                               ["MonitoredVehicleJourney"]
                               ["OnwardCalls"]
                               ["OnwardCall"]
                               [0]
                               ["Extensions"]
                               ["Distances"]
                               ["PresentableDistance"])
    except KeyError:
        stop_status = "N/A"

    lines.append("%2.6f,%2.6f,%s,%s" % (latitude,
                                        longitude,
                                        stop_name,
                                        stop_status))

# Write the lines to the CSV file and close it
for line in lines:
    f.write(line + "\n")
f.close()
