'''
File: testbus.py
Authors: Martin McCarley, Sanjay Murugesan
Date Created: 15 Oct 2019
Last Updated: 

Purpose: A testing document for the functions in bus.py
'''

import bus

# Test all buses and their alt names 
def test_bus_name_to_route():

	colored_buses = [('Orange','115'),('Purple','116'),('Blue','117'),('Gold','118'),('Green','122')]
	full_name_buses = [('College Park Metro','104'),('Campus Connector','105'),('Adelphi','108'),
						('River Road','109'),('Silver Spring','111'),('Hyattsville','113'),
						('University View','114'),('Discovery District','123'),('Shady Grove','124'),
						('New Carrolton','126'),('Mazza GrandMarc','127'),('The Enclave','128'),
						('MGM/Enclave','131'),('The Varsity','132'), ('Grocery Shopping Shuttle','133'),
						('UMB Law','140'), ('Gaithersburg Park & Ride','141'), ('Columbia Park & Ride','142'),
						('Greenbelt','143'),('Bowie State - Enclave Express','bse')]
	alt_name_buses = [('Metro','104'),('Connector','105'),('View','114'),('Discovery','123'),
						('Mazza','127'),('GrandMarc','127'),('Enclave','128'),
						('MGM','131'),('Varsity','132'), ('Grocery','133'),('Shopping Shuttle','133'),
						('UMB','140'),('Law','140'),('Gaithersburg','141'), ('Columbia','142'),
						('Bowie','bse'),('Bowie State','bse')]
	
	for case in colored_buses:
		curr = bus.bus_name_to_route(case[0])
		if curr != case[1]:
			print(case[0] + ' did not properly map to Route ' + str(case[1]))
			print('Instead returned: ' + curr)

	for case in full_name_buses:
		curr = bus.bus_name_to_route(case[0])
		if curr != case[1]:
			print(case[0] + ' did not properly map to Route ' + str(case[1]))
			print('Instead returned: ' + curr)

	for case in alt_name_buses:
		curr = bus.bus_name_to_route(case[0])
		if curr != case[1]:
			print(case[0] + ' did not properly map to Route ' + str(case[1]))
			print('Instead returned: ' + curr)

# Test Suite
def test_suite():
	# Test Functions (Comment Out Test You do not want to run)
	test_bus_name_to_route()


### Function Calls ###
test_suite()