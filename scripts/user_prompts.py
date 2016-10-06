""" File to facilitate incoming queries and outgoing results with the user. """

from graph_functions import *
from colorama import Fore
import user_prompts

INITIAL_PROMPT = ("\n0 - List of all cities\n"
                  "1 - Information About Individual City\n"
                  "2 - Statistics about CSAir\n"
                  "3 - Get Map of all Routes in CSAir Network\n"
                  "4 - Modify the Network\n"
                  "5 - Export back to JSON\n"
                  "6 - Add new JSON File Data to Network\n")

STATISTIC_PROMPT = ("\n0 - Longest Single Flight\n"
                    "1 - Shortest Single Flight\n"
                    "2 - Average Distance of Flights\n"
                    "3 - Biggest City in CSAir Network\n"
                    "4 - Smallest City in CSAir Network\n"
                    "5 - Average Population of cities in CSAir Network\n"
                    "6 - List of Cities by Continent in CSAir Network\n"
                    "7 - CSAir's Hub Cities\n"
                    "8 - Get Information About a Route\n"
                    "9 - Get Shortest Route Between Cities\n")

MODIFICATION_PROMPT = ("\n0 - Remove a City\n"
                       "1 - Remove a Route\n"
                       "2 - Add a City\n"
                       "3 - Add a Route\n"
                       "4 - Edit Data About A City\n")


def get_hub_city_threshold():
    """ Get the threshold number of routes for a city to be considered a hub.

    :return: Minimum number of routes
    """
    min_hub = int(raw_input("Minimum number of routes for hub: "))
    return min_hub


def print_all_cities(airline_network):
    """ Gets all cities from graph object and prints city codes and names.

    :param airline_network: Graph object of CSAir flights.
    """
    cities = get_all_cities(airline_network)
    for city in cities:
        print_message(city[0] + " " + city[1])


def print_individual_city(airline_network):
    """ Prints all metadata about an individual city that the user queries for.

    :param airline_network: Graph object of CSAir flights.
    """
    city_code = raw_input("Enter the city code for which you want the information: ").strip()
    metro = airline_network.get_node(city_code)
    if not metro:
        print_error("Incorrect City Code: " + city_code)
        return
    metro_data = metro.get_data()
    for key in metro_data:
        print_message(key + " : " + str(metro_data[key]))
    metro_connections = metro.get_connected_nodes()
    if len(metro_connections) > 0:
        print_message("Connections to:")
        for connection_code in metro_connections:
            connection = airline_network.get_node(connection_code)
            print_message("\t%s (%i miles)" %(connection.get_data()["name"], metro_connections[connection_code]))


def prompt_user_for_input(airline_network):
    """ Prompts users for what information they want about CSAir

    :param airline_network:
    """
    response = raw_input(INITIAL_PROMPT)
    while not response or int(response) > 6 or int(response) < 0:
        response = raw_input()
    response = int(response)

    if response == 0:
        print_all_cities(airline_network)
    elif response == 1:
        print_individual_city(airline_network)
    elif response == 2:
        statistic_code = int(raw_input(STATISTIC_PROMPT))
        print_message(get_statistic(statistic_code, airline_network))
    elif response == 3:
        url = get_map_of_routes(airline_network)
        print_message(url)
    elif response == 4:
        modification_code = int(raw_input(MODIFICATION_PROMPT))
        make_modification(modification_code, airline_network)
    elif response == 5:
        download_data_to_json(airline_network)
        print_message("Data outputted to data/output_data.json.")
    elif response == 6:
        file_name = raw_input("Put new JSON file in data folder. Enter the name of the JSON File: ")
        add_file_data_to_graph(airline_network, "data/" + file_name + ".json")


def get_statistic(statistic_code, airline_network):
    """ Maps the user entered code to the correct statistic to query

    :param statistic_code: Code the user entered
    :param airline_network: Graph Object with CSAir Information
    :return: The data the user queried for
    """
    if statistic_code == 0:
        return get_longest_single_flight(airline_network)
    elif statistic_code == 1:
        return get_shortest_single_flight(airline_network)
    elif statistic_code == 2:
        return get_average_distance(airline_network)
    elif statistic_code == 3:
        return get_biggest_city(airline_network)
    elif statistic_code == 4:
        return get_smallest_city(airline_network)
    elif statistic_code == 5:
        return get_average_population(airline_network)
    elif statistic_code == 6:
        return get_cities_by_continent(airline_network)
    elif statistic_code == 7:
        min_hub = user_prompts.get_hub_city_threshold()
        return get_hub_cities(airline_network, min_hub)
    elif statistic_code == 8:
        city_codes = []
        print "Enter city codes one at a time in order of your route. Enter 'done' when you are finished."
        input_code = raw_input("Enter a city code: ")
        while input_code.lower() != "done":
            city_codes.append(input_code)
            input_code = raw_input("Enter a city code: ")
        return get_route_data(airline_network, city_codes)
    elif statistic_code == 9:
        start_route = raw_input("Enter the start city: ")
        end_route = raw_input("Enter the destination city: ")
        return get_shortest_path(airline_network, start_route, end_route)


def make_modification(modification_code, airline_network):
    """ Maps the user entered code to the correct modification to the airline network

        :param modification_code: Code the user entered
        :param airline_network: Graph Object with CSAir Information
        :return: The data the user queried for
        """
    if modification_code == 0:
        city_code = raw_input("Enter the City Code of the City you want to remove: ")
        delete_city(airline_network, city_code)
    elif modification_code == 1:
        start_route = raw_input("Enter the start of the route you want to remove: ")
        end_route = raw_input("Enter the destination of the route you want to remove: ")
        bidirectional = raw_input("Do you want to remove both directions of the route? (Y/N): ")
        # Remove the city if there aren't any ingoing or outgoing connections
        delete_route(airline_network, start_route, end_route, bidirectional)
    elif modification_code == 2:
        city_data = {"code": None, "name": None, "country": None, "continent": None, "timezone": None,
                     "coordinates": None, "population": None, "region": None}
        for data in city_data:
            city_data[data] = raw_input("Enter the new city's %s: " % data)
        add_city(airline_network, city_data)
    elif modification_code == 3:
        start_route = raw_input("Enter the start of the route you want to add: ")
        end_route = raw_input("Enter the destination of the route you want to add: ")
        weight = int(raw_input("Enter the distance of the route: "))
        bidirectional = raw_input("Do you want to add both directions of the route? (Y/N): ")
        add_route(airline_network, bidirectional, start_route, end_route, weight)
    elif modification_code == 4:
        city_code = raw_input("Enter the City Code of the City you want to modify: ")
        city_data = airline_network.get_node(city_code).get_data()
        print "If you want to modify the following data, enter the new data. Otherwise, enter a new line to skip."
        for data in city_data:
            if data == "code":
                continue  # Don't modify the City Code.
            new_data = raw_input("Current city's %s = %s. Replace with: " % (data, city_data[data]))
            if new_data:
                city_data[data] = new_data


def print_message(message):
    print(Fore.GREEN + message + Fore.RESET)


def print_error(message):
    print(Fore.RED + message + Fore.RESET)
