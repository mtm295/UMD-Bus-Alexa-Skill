"""
File: bus.py
Authors:
Date Created:
Last Updated:
"""
import requests
import json

# Base URL for UMD Api Bus
base_url = 'https://api.umd.io/v0/bus/'

# URL containing the bus routes from the umd api
routes_url = 'https://api.umd.io/v0/bus/routes/'

# URL containing the locations of the Route 117 Bus from the umd api
locations_url = 'https://api.umd.io/v0/bus/routes/117/locations/'

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

# url = 'https://api.umd.io/v0/bus/routes/117/arrivals/univview/'
# response = requests.get(url)
# json_data = json.loads(response.text)
# print (json_data)

def get_routes():
    # URL containing the bus routes from the umd api
    routes_url = base_url + 'routes'

    # Prints the request content of the url
    print_url(routes_url)

# def get_closest_stop()

def get_bus_timing(bus_route, bus_stop):
    # Generates URL containing the bus timing
    bus_timing_url = routes_url + bus_route + 'arrivals/' + bus_stop

    # Requests the bus timings from the API
    print_json(bus_timing_url)

# Function Calls
get_bus_timing(117,'univview')
