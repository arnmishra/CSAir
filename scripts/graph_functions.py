""" File to hold all Graph data manipulation done for CSAir. """

import webbrowser
import json
import sys
import math
from Queue import PriorityQueue

from framework.graph import Graph

MAP_BASE_URL = "http://www.gcmap.com/mapui?P="
ACCELERATION = ((750.0/60)**2)/(2*200)  # a = v^2/(2*d) in km/min^2


def add_file_data_to_graph(airline_network=Graph(), map_file_path="data/output_data.json"):
    """ Creates graph object from JSON File with data about airline mappings. This
    includes making each connection bidirectional between the cities.

    :param airline_network: If no airline network graph provided, create new network.
    :param map_file_path: The File Path to use to get the Graph data
    :return: graph object that is created
    """
    try:
        map_data_file = open(map_file_path, "r")
    except Exception, e:
        print e
        return False
    map_data = json.load(map_data_file)
    if "unidirectional" in map_data:
        unidirectional = map_data["unidirectional"]
    else:
        unidirectional = False
    for metro in map_data["metros"]:
        airline_network.add_node(metro["code"], metro)
    for route in map_data["routes"]:
        airline_network.add_connection(route["ports"][0], route["ports"][1], route["distance"])
        if not unidirectional:
            airline_network.add_connection(route["ports"][1], route["ports"][0], route["distance"])
    return airline_network


def get_map_of_routes(airline_network, open_route_url=True):
    """ Creates a URL and opens it if the flag is True to show a map of the CSAir Network

    http://stackoverflow.com/questions/4302027/how-to-open-a-url-in-python
    :param airline_network: Graph Object with CSAir Information
    :param open_route_url: Whether or not to open the url automatically
    :return:
    """
    all_metros = airline_network.get_all_nodes()
    route_url = MAP_BASE_URL
    for city_code in all_metros:
        metro = all_metros[city_code]
        connected_nodes = metro.get_connected_nodes()
        for destination_code in connected_nodes:
            destination = airline_network.get_node(destination_code)
            route_url += "%s-%s," % (city_code, destination.get_data()["code"])
    if open_route_url:
        webbrowser.open(route_url)
    return route_url


def get_all_cities(airline_network):
    """ Gets all city codes and names from Graph Object

    :param airline_network: Graph Object with CSAir Information
    :return: list of city codes + city names
    """
    city_names = []
    airline_nodes = airline_network.get_all_nodes()
    for city_code in airline_nodes:
        metro_data = airline_nodes[city_code].get_data()
        city_names.append([metro_data["code"], metro_data["name"]])
    return city_names


def get_hub_cities(airline_network, min_hub):
    """ Gets all Hubs based on User Specified baseline number of routes

    :param airline_network: Graph Object with CSAir Information
    :param min_hub: Minimum number of routes for a city to be considered a hub
    :return: list of hub cities and how many routes they have
    """
    all_metros = airline_network.get_all_nodes().values()
    hubs = {}
    for metro in all_metros:
        connected_routes = metro.get_connected_nodes()
        num_routes = len(connected_routes)
        if num_routes >= min_hub:
            if num_routes in hubs:
                hubs[num_routes] += ", " + metro.get_data()["name"]
            else:
                hubs[num_routes] = metro.get_data()["name"]
    hub_list_string = ""
    for num_routes in hubs:
        hub_list_string += "%i routes: %s\n" % (num_routes, hubs[num_routes])
    return hub_list_string


def get_cities_by_continent(airline_network):
    """ List of cities by each continent they are in.

    :param airline_network: Graph Object with CSAir Information
    :return: Mapping of continents to all cities in them
    """
    all_metros = airline_network.get_all_nodes().values()
    continents_served = {}
    for metro in all_metros:
        metro_data = metro.get_data()
        continent = metro_data["continent"]
        if continent in continents_served:
            continents_served[continent] += ", " + metro_data["name"]
        else:
            continents_served[continent] = metro_data["name"]
    continents_list_string = ""
    for continent in continents_served:
        continents_list_string += "%s: %s\n" % (continent, continents_served[continent])
    return continents_list_string


def get_average_population(airline_network):
    """ Calculates the average population of the cities in the CSAir network.

    :param airline_network: Graph Object with CSAir Information
    :return: Average Population
    """
    all_metros = airline_network.get_all_nodes().values()
    all_populations = 0
    num_cities = 0
    for metro in all_metros:
        metro_data = metro.get_data()
        all_populations += metro_data["population"]
        num_cities += 1
    return "Average population: " + str(all_populations / num_cities)


def get_smallest_city(airline_network):
    """ Finds the smallest city by population in the CSAir network.

    :param airline_network: Graph Object with CSAir Information
    :return: Smallest City
    """
    all_metros = airline_network.get_all_nodes().values()
    smallest_metro = None
    for metro in all_metros:
        metro_data = metro.get_data()
        if not smallest_metro or metro_data["population"] < smallest_metro["population"]:
            smallest_metro = metro_data
    return "Smallest City: " + smallest_metro["name"] + " with population " + str(smallest_metro["population"])


def get_biggest_city(airline_network):
    """ Finds the largest city by population in the CSAir network.

    :param airline_network: Graph Object with CSAir Information
    :return: Biggest City
    """
    all_metros = airline_network.get_all_nodes().values()
    biggest_metro = None
    for metro in all_metros:
        metro_data = metro.get_data()
        if not biggest_metro or metro_data["population"] > biggest_metro["population"]:
            biggest_metro = metro_data
    return "Biggest City: " + biggest_metro["name"] + " with population " + str(biggest_metro["population"])


def get_average_distance(airline_network):
    """ Calculates the average distance between cities in the CSAir network.

    :param airline_network: Graph Object with CSAir Information
    :return: Average Distance
    """
    all_metros = airline_network.get_all_nodes().values()
    total_distance = 0
    num_routes = 0
    for metro in all_metros:
        connected_routes = metro.get_connected_nodes()
        for destination in connected_routes:
            total_distance += connected_routes[destination]
            num_routes += 1
    return "Average Distance of Flights: " + str(total_distance / num_routes)


def get_shortest_single_flight(airline_network):
    """ Gets the shortest possible flight in the CSAir network.

    :param airline_network: Graph Object with CSAir Information
    :return: Shortest flight.
    """
    all_metros = airline_network.get_all_nodes().values()
    shortest_distance = None
    start_city = None
    end_city = None
    for metro in all_metros:
        connected_routes = metro.get_connected_nodes()
        for destination_code in connected_routes:
            if not shortest_distance or shortest_distance > connected_routes[destination_code]:
                start_city = metro.get_data()["name"]
                destination_node = airline_network.get_node(destination_code)
                end_city = destination_node.get_data()["name"]
                shortest_distance = connected_routes[destination_code]
    return "Shortest Flight: from %s to %s (%i)" % (start_city, end_city, shortest_distance)


def get_longest_single_flight(airline_network):
    """ Gets the longest possible flight in the CSAir network.

    :param airline_network: Graph Object with CSAir Information
    :return: Longest flight.
    """
    all_metros = airline_network.get_all_nodes().values()
    longest_distance = None
    start_city = None
    end_city = None
    for metro in all_metros:
        connected_routes = metro.get_connected_nodes()
        for destination_code in connected_routes:
            if not longest_distance or longest_distance < connected_routes[destination_code]:
                start_city = metro.get_data()["name"]
                destination_node = airline_network.get_node(destination_code)
                end_city = destination_node.get_data()["name"]
                longest_distance = connected_routes[destination_code]
    return "Longest Flight: from %s to %s (%i)" % (start_city, end_city, longest_distance)


def delete_city(airline_network, delete_city_code):
    """ Delete a city and all references to it from the network

    :param airline_network: Graph Object with CSAir Information
    :param delete_city_code: City Code of City to be Deleted
    """
    airline_network.delete_node(delete_city_code)
    all_cities = airline_network.get_all_nodes()
    for city_code in all_cities:
        connections_to_city = all_cities[city_code].get_connected_nodes()
        if delete_city_code in connections_to_city.keys():
            del connections_to_city[delete_city_code]


def delete_route(airline_network, start_city_code, end_city_code, bidirectional):
    """ Delete a route in one or both directions as determined by the bidirectional flag

    :param airline_network: Graph Object with CSAir Information
    :param start_city_code: Starting City of the Route
    :param end_city_code: Ending City of the Route
    :param bidirectional: Whether to delete both directions of the route or not
    """
    airline_network.delete_connection(start_city_code, end_city_code)
    if bidirectional.lower() == "y":
        airline_network.delete_connection(end_city_code, start_city_code)


def add_city(airline_network, city_data):
    """ Add a city and its metadata to the network.

    :param airline_network: Graph Object with CSAir Information
    :param city_data: Data about new city
    """
    city_code = city_data["code"]
    airline_network.add_node(city_code, city_data)


def add_route(airline_network, bidirectional, start_route, end_route, weight):
    """Adds a route to the network

    :param airline_network: Graph Object with CSAir Information
    :param bidirectional: Whether or not to make the route bidirectional
    :param start_route: Starting city
    :param end_route: Ending city
    :param weight: Distance of the route
    """
    airline_network.add_connection(start_route, end_route, weight)
    if bidirectional.lower() == "y":
        airline_network.add_connection(end_route, start_route, weight)


def download_data_to_json(airline_network):
    """Re-download all the data to an output json file.

    http://stackoverflow.com/questions/12309269/how-do-i-write-json-data-to-a-file-in-python
    http://stackoverflow.com/questions/12943819/how-to-python-prettyprint-a-json-file
    :param airline_network: Graph Object with CSAir Information
    """
    compiled_json = {"unidirectional": True, "metros": [], "routes": []}
    all_nodes = airline_network.get_all_nodes()
    for city_code in all_nodes:
        node_data = all_nodes[city_code].get_data()
        compiled_json["metros"].append(node_data)
        connections = all_nodes[city_code].get_connected_nodes()
        for destination_code in connections:
            route = {"ports": [node_data["code"], destination_code], "distance": connections[destination_code]}
            compiled_json["routes"].append(route)
    with open("data/output_data.json", 'w') as json_file:
        json.dump(compiled_json, json_file, indent=4, sort_keys=True)


def get_route_data(airline_network, city_codes):
    """ Get specific information about a route across multiple cities. Specifically,
    get the total distance, total cost, and total time of the journey using given
    information about cost and acceleration of the flight.

    :param airline_network: Graph Object with CSAir Information
    :param city_codes: List of city codes in the route from start to finish.
    :return: String explaining the metadata about the route
    """
    if len(city_codes) < 2:
        return "Not enough city codes entered"
    total_distance = 0
    total_cost = 0
    total_time = 0
    cost_per_kilometer = 0.35
    start_code = city_codes[0]
    start_city = airline_network.get_node(start_code)
    for i in range(1, len(city_codes)):
        if not start_city:
            return "Invalid City Code: " + start_city
        city_code = city_codes[i]
        start_connections = start_city.get_connected_nodes()
        current_city = airline_network.get_node(city_code)
        if not current_city:
            return "Invalid City Code: " + city_code
        current_connections = current_city.get_connected_nodes()
        if city_code not in start_connections:
            return "Invalid Route"
        distance = start_connections[city_code]
        total_distance += distance
        total_cost += distance * cost_per_kilometer
        if cost_per_kilometer >= 0.05:
            cost_per_kilometer -= 0.05
        total_time += calculate_time(distance, city_codes, current_connections, i)
        start_city = airline_network.get_node(city_code)
    return "Total Distance = %i\nTotal Cost = $%.2f\nTotal Time = %ihrs %imins" \
           % (total_distance, total_cost, total_time/60, total_time % 60)


def calculate_time(distance, city_codes, current_connections, i):
    """ Helper function to calculate the time between cities and the layover time.
    The acceleration is understood to take 200 meters to hit 750 kmph. The time is
    returned in minutes.

    :param distance: Distance in this portion of the route.
    :param city_codes: A list of the codes in the route.
    :param current_connections: The flight connections from the current city.
    :param i: Which city code is currently being considered
    :return: The time it takes to travel the given distance
    """
    total_time = 0
    if distance >= 400:
        acceleration_time = math.sqrt((2 * 200) / ACCELERATION)  # t = sqrt(2d/a) in minutes
        cruising_time = (distance - 400.0) / (750.0 / 60)  # t = d/v in minutes
        total_time += 2 * acceleration_time + cruising_time  # cruising time + acceleration + deceleration
    else:
        acceleration_time = math.sqrt((2 * distance / 2) / ACCELERATION)  # in minutes
        total_time += 2 * acceleration_time  # acceleration + deceleration
    if i != len(city_codes) - 1:
        layover_time = 120 - 10 * (len(current_connections) - 1)  # in minutes
        if layover_time < 0:
            layover_time = 0
        total_time += layover_time
    return total_time


def initialize_dictionaries(all_cities, start_city):
    """ Helper function to initialize all the dictionaries regarding visited, distance,
    and previous nodes.

    :param all_cities: All the cities in the network
    :param start_city: The start city of the route
    :return: The initialized dictionaries
    """
    distance = {}
    previous_node = {}
    visited = {}
    for city_code in all_cities:
        if city_code == start_city:
            visited[city_code] = False
            distance[start_city] = 0
        else:
            distance[city_code] = float("inf")
            previous_node[city_code] = None
            visited[city_code] = False
    return distance, previous_node, visited


def get_shortest_path(airline_network, start_city, end_city):
    """ Dijsktra's algorithm implementation using a Priority Queue to sort shortest paths,
    a distance dictionary to store the shortest distance to each city, the previous node for
    each city to get there in that distance, and whether or not each city has been visited.

    :param airline_network: Graph Object with CSAir Information
    :param start_city: The starting city of the route
    :param end_city: The end city of the route
    :return: The route taken and the metadata about the route.
    """
    all_cities = airline_network.get_all_nodes()
    queue = PriorityQueue()
    distance, previous_node, visited = initialize_dictionaries(all_cities, start_city)
    current_city = start_city
    current_node = all_cities[current_city]
    connected_cities = current_node.get_connected_nodes()
    for connected_code in connected_cities:
        queue.put([connected_cities[connected_code], connected_code, current_city])

    while not queue.empty():
        visited[current_city] = True
        closest_values = queue.get()
        connected_city = closest_values[1]
        if distance[connected_city] > closest_values[0]:
            distance[connected_city] = closest_values[0]
            previous_node[connected_city] = closest_values[2]
        current_city = connected_city
        if current_city == end_city:
            break
        current_node = airline_network.get_node(current_city)
        connected_cities = current_node.get_connected_nodes()
        for connected_code in connected_cities:
            if not visited[connected_code]:
                queue.put([distance[current_city] + connected_cities[connected_code], connected_code, current_city])

    route = []
    current_city = end_city
    while current_city != start_city:
        route.insert(0, current_city)
        current_city = previous_node[current_city]
    route.insert(0, start_city)
    route_data = get_route_data(airline_network, route)
    return str(route) + "\n" + route_data
