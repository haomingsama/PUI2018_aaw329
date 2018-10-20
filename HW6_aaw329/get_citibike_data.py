import os
import sys


url_base = "https://s3.amazonaws.com/tripdata"


def get_citibike_data(filename):
    """
    Download Citi Bike data into PUIDATA directory if it's not there yet

    Takes filename as argument. For example, "201809-citibike-tripdata.csv".
    """

    # Exit if PUIDATA is not set. Otherwise, print the value.
    puidata = os.getenv("PUIDATA")
    if puidata is None:
        print("You must set the PUIDATA environment variable.")
        sys.exit(1)
    else:
        print("PUIDATA=%s" % puidata)

    # Check if the data is not there in .csv or .zip format
    if (not os.path.isfile(puidata + "/" + filename) and
        not os.path.isfile(puidata + "/" + filename + ".zip")):
        print("Downloading data")
        os.system("wget -O " + puidata + "/" + filename + ".zip" + " " + 
                  url_base + "/" + filename + ".zip")
        print("Unzipping data")
        os.system("unzip -d " + puidata + " " + 
                  puidata + "/" + filename + ".zip")
    # Check if the data _is_ there .zip format but not .csv, 
    # in which case we just need to unzip it
    elif (os.path.isfile(puidata + "/" + filename + ".zip") and
          not os.path.isfile(puidata + "/" + filename)):
        print("Unzipping data")
        os.system("unzip -d " + puidata + " " + 
                  puidata + "/" + filename + ".zip")

    # Finally, make sure the correct file is present
    if not os.path.isfile(puidata + "/" + filename):
        print("Problem acquiring data!")
        sys.exit(1)
    else:
        print("Successfully acquired data")
