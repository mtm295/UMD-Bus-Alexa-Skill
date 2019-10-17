"""
File: bus.py
Authors: Sanjay Murugesan, Martin McCarley
Date Created: 15 Oct 2019 12:09am
Last Updated: 17 Oct 2019 1:40pm
"""
import requests
import json
import geocoder

g = geocoder.ip('me')
curr_lat = float(g.latlng[0])
curr_long = float(g.latlng[1])



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
    # Retrives the dict of routes and their route_ids
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

# Takes in a list of stop objects from a specific route, along with the current latitude and longitude
# Loop through the list of stops, and compute the distance from current location to each stop, keeping
# track of the closest stop to current distance. Return the id of the closest stop at the end.
def find_diff(curr_lat, curr_long, stop_list):
    closest_stop_id = ''
    min_diff = 999
    for stop in stop_list:
        d = abs(float(curr_lat) - float(stop['lat'])) + abs(float(curr_long) - float(stop['lon']))
        if d < min_diff:
            min_diff = d
            closest_stop_id = stop['stop_id']

    return (closest_stop_id)


# Call the above helper. Once you get the id of the stop closest to your current location, 
# pass that stop id into the url, and get the info for the current circulating buses of bus_route.
# From that, grab the time in seconds from the first bus in that list (which is the bus that will reach
# stop 'stop_id' first), and return that time.
def time_to_closest_stop(bus_route, stop_id):
    url = 'https://api.umd.io/v0/bus/routes/' + bus_route +'/arrivals/' + stop_id
    response = requests.get(url)
    json_data = json.loads(response.text)
    ret = json_data['predictions']['direction']['prediction'][0]['seconds']

    return (ret)


# To implement, we would have to grab and store the location data of each of the stops
#  Might take actuaally walking around and dropping Google Map pins at the stops
# Current Call Result: Returns the number of bus stops within the system of buses
def get_closest_stop(bus_route):
    stop_coord_list = []
    stop_url = base_url + '/stops'
    s = get_route_stop_objs(bus_route)

    ret = find_diff(curr_lat,curr_long, s)

    return ret

# Given a bus route, returns all the stop objects on the bus route
def get_route_stop_objs(bus_route):
    stop_objs = []
    ids = get_route_stop_ids(bus_route)
    for id in ids:
        stop_obj_url = base_url + '/stops/' + id
        response = requests.get(stop_obj_url)
        json_data = json.loads(response.text)
        stop_objs.append(json_data[0])
    
    return (stop_objs)

# Given a bus route, returns all the stop titles on the bus route
def get_route_stop_titles(bus_route):
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

def get_route_stop_ids(bus_route):
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
    return stop_ids

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



# Testing

# print(get_route_stops_title(117))
# print(get_route_stops_title(bus_name_to_route('Blue')))
# print (get_closest_stop('117'))
b_r = '122'
print (time_to_closest_stop(b_r, get_closest_stop(b_r)))




