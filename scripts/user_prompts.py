""" File to facilitate incoming queries and outgoing results with the user. """

from graph_functions import *
from colorama import Fore

INITIAL_PROMPT = ("\n0 - List of all cities\n"
                  "1 - Information About Individual City\n"
                  "2 - Statistics about CSAir\n"
                  "3 - Get Map of all Routes in CSAir Network\n")

STATISTIC_PROMPT = ("\nEnter the number associated with the statistic:\n"
                    "0 - Longest Single Flight\n"
                    "1 - Shortest Single Flight\n"
                    "2 - Average Distance of Flights\n"
                    "3 - Biggest City in CSAir Network\n"
                    "4 - Smallest City in CSAir Network\n"
                    "5 - Average Population of cities in CSAir Network\n"
                    "6 - List of Cities by Continent in CSAir Network\n"
                    "7 - CSAir's Hub Cities\n")


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
    city_name = raw_input("Enter the city code for which you want the information: ").strip()
    metro_data = airline_network.get_node(city_name)
    for key in metro_data:
        print_message(key + " : " + str(metro_data[key]))


def prompt_user_for_input(airline_network):
    """ Prompts users for what information they want about CSAir

    :param airline_network:
    """
    response = raw_input(INITIAL_PROMPT)
    while not response or int(response) > 3 or int(response) < 0:
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


def get_statistic(statistic_code, airline_network):
    """ Maps the user entered code to the correct statistic to query

    :param statistic_code: Code the user entered
    :param airline_network: Graph Object with CSAir Information
    :return: The data the user queried for
    """
    if statistic_code == 0:
        return get_longest_single_flight(airline_network)
    if statistic_code == 1:
        return get_shortest_single_flight(airline_network)
    if statistic_code == 2:
        return get_average_distance(airline_network)
    if statistic_code == 3:
        return get_biggest_city(airline_network)
    if statistic_code == 4:
        return get_smallest_city(airline_network)
    if statistic_code == 5:
        return get_average_population(airline_network)
    if statistic_code == 6:
        return get_cities_by_continent(airline_network)
    if statistic_code == 7:
        min_hub = user_prompts.get_hub_city_threshold()
        return get_hub_cities(airline_network, min_hub)


def print_message(message):
    print(Fore.GREEN + message + Fore.RESET)