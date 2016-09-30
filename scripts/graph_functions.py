""" File to hold all Graph data manipulation done for CSAir. """

import webbrowser
import json
import sys

from framework.graph import Graph
import user_prompts

MAP_BASE_URL = "http://www.gcmap.com/mapui?P="


def create_graph_from_file(map_file_path="data/map_data.json"):
    """ Creates graph object from JSON File with data about airline mappings.

    :param map_file_path: The File Path to use to get the Graph data
    :return: graph object that is created
    """
    try:
        map_data_file = open(map_file_path, "r")
    except Exception, e:
        print e
        sys.exit(1)
    map_data = json.load(map_data_file)
    airline_network = Graph()
    for metro in map_data["metros"]:
        airline_network.add_node(metro["code"], metro)
    for route in map_data["routes"]:
        airline_network.add_connection(route["ports"][0], route["ports"][1], route["distance"])
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
        for destination in connected_nodes:
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
        for destination in connected_routes:
            if not shortest_distance or shortest_distance > connected_routes[destination]:
                start_city = metro.get_data()["name"]
                end_city = destination.get_data()["name"]
                shortest_distance = connected_routes[destination]
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
        for destination in connected_routes:
            if not longest_distance or longest_distance < connected_routes[destination]:
                start_city = metro.get_data()["name"]
                end_city = destination.get_data()["name"]
                longest_distance = connected_routes[destination]
    return "Longest Flight: from %s to %s (%i)" % (start_city, end_city, longest_distance)

