"""
File: bus.py
Authors: Sanjay Murugesan, Martin McCarley
Date Created: 15 Oct 2019 12:09am
Last Updated: 15 Oct 2019 5:42pm
"""
import requests
import json

# Prints a string to seperate outputs of different function calls
def sep():
    print('+---------------+')

# Base URL for UMD Api Bus
base_url = 'https://api.umd.io/v0/bus'

# URL containing the bus routes from the umd api
routes_url = 'https://api.umd.io/v0/bus/routes'

# URL containing the locations of the Route 117 Bus from the umd api
locations_url = 'https://api.umd.io/v0/bus/routes/117/locations'

# Print URL Content
def print_url(url):
    # GET Request the URL
    response = requests.get(url)

    print (response.content)

# Print JSON Data of the URL
def print_json(url):
    # GET Request the URL
    response = requests.get(url)

    # Loads the Response Text into JSON
    json_data = json.loads(response.text)

    print (json_data)

## Routes
def get_routes():
    # GET Request the URL
    response = requests.get(routes_url)

    # Loads the Response Text into JSON
    json_data = json.loads(response.text)

    return json_data

def bus_name_to_route(bus_name):
    # Retrives the dict of routes and thier route_ids
    routes = get_routes()

    for route in routes:
        # If the specified bus_name appears in the Route Title return the route id
        if bus_name in route['title']:
            return route['route_id']

    print('Bus not found')
    return;

## Stops
# Given a stop id, returns the coresponding stop title
def stop_id_to_title(stop_id):
    # Generates URL that hold the data for the given stop id
    stop_url = base_url + '/stops/' + str(stop_id)

    # Requests the stop information from the API
    response = requests.get(stop_url)

    # Loads the response text as JSON
    json_data = json.loads(response.text)[0]

    # Returns the title
    return json_data['title']

# Given a stop title, returns the corresponding stop id
# Harder to do as API doesn't have backwards access
# WARNING: As of now, method is computationally inefficent, search the array of 335 stops for a match
#  Best case: Given stop id is first in the array; Worst case: Given stop id is at end of array
def stop_title_to_id(stop_title):
    return;

# To implement, we would have to grab and store the location data of each of the stops
#  Might take actuaally walking around and dropping Google Map pins at the stops
# Current Call Result: Returns the number of bus stops within the system of buses
def get_closest_stop():
    stop_url = base_url + '/stops'

    response = requests.get(stop_url)

    json_data = json.loads(response.text)

    return len(json_data)

# Given a bus route, returns all the stops on the bus route
def get_route_stops(bus_route):
    # Generates URL containg information on the specified bus stop
    route_stops_url = routes_url + '/' + str(bus_route)

    # Request the information from  the API
    response = requests.get(route_stops_url)

    # Loads the response text into JSON
    json_data = json.loads(response.text)

    # Grabs the list of stop ids
    stop_ids = json_data['stops']

    # Maps the list of stop ids to the stop title
    stop_titles = list(map(stop_id_to_title,stop_ids))

    # Returns the list of stops on the route
    return stop_titles

# url = 'https://api.umd.io/v0/bus/routes/117/arrivals/univview/'
# response = requests.get(url)
# json_data = json.loads(response.text)
# print (json_data)

# Grabs all the timings for the specified bus route reaching the specified stop
def get_bus_timing(bus_route, bus_stop):
    # Generates URL containing the bus timing, and sanatizes inputs
    bus_timing_url = routes_url + '/' + str(bus_route) + '/arrivals/' + str(bus_stop)

    # Request arrivals for bus_route to the given bus_stop
    response = requests.get(bus_timing_url)

    # Loads the Response Text into JSON
    json_data = json.loads(response.text)

    # Trys to grab the list of arrival predictions, if none found sets predictions to False
    try:
        predictions = json_data['predictions']['direction']['prediction']
    except(KeyError):
        predictions = False

    # If there are predictions, print the number of seconds for each prediction, else the bus is not running
    times = []
    if predictions:
        # Print the arrival times in ascending order
        for x in predictions:
            times.append(x['seconds'])
    else:
        print('Bus Not Running')

    print(times)
    return times

# Function Calls
## Bus Timing
# get_bus_timing(117,'univview')
# sep()
# get_bus_timing(128,'enclave_s')
# sep()
## Bus Name to Route
# print(bus_name_to_route('Blue'))
## Closest Stop
# print(get_closest_stop())
## Route Stops
print(get_route_stops(117))





