""" File to facilitate incoming queries and outgoing results with the user. """

from graph_functions import get_statistic, get_all_cities

INITIAL_PROMPT = ("\n0 - List of all cities\n"
                  "1 - Information About Individual City\n"
                  "2 - Statistics about CSAir\n")

STATISTIC_PROMPT = ("\nEnter the number associated with the statistic:\n"
                    "0 - Longest Single Flight\n"
                    "1 - Shortest Single Flight\n"
                    "2 - Average Distance of Flights\n"
                    "3 - Biggest City in CSAir Network\n"
                    "4 - Smallest City in CSAir Network\n"
                    "5 - Average Population of cities in CSAir Network\n"
                    "6 - List of Cities by Continent in CSAir Network\n"
                    "7 - CSAir's Hub Cities\n")


def print_all_cities(airline_network):
    """ Gets all cities from graph object and prints city codes and names.

    :param airline_network: Graph object of CSAir flights.
    """
    cities = get_all_cities(airline_network)
    for city in cities:
        print city[0], city[1]


def print_individual_city(airline_network):
    """ Prints all metadata about an individual city that the user queries for.

    :param airline_network: Graph object of CSAir flights.
    """
    city_name = raw_input("Enter the city code for which you want the information: ").strip()
    metro_data = airline_network.get_node(city_name)
    for key in metro_data:
        print key, ":", metro_data[key]


def prompt_user_for_input(airline_network):
    """ Prompts users for what information they want about CSAir

    :param airline_network:
    """
    response = raw_input(INITIAL_PROMPT)
    while not response or int(response) > 2 or int(response) < 0:
        response = raw_input()
    response = int(response)

    if response == 0:
        print_all_cities(airline_network)
    elif response == 1:
        print_individual_city(airline_network)
    elif response == 2:
        statistic_code = int(raw_input(STATISTIC_PROMPT))
        print get_statistic(statistic_code, airline_network)
