""" Main File to facilitate creation of Graph of Airlines and User Interaction """

import json
import sys

from framework.graph import Graph
from scripts.user_prompts import prompt_user_for_input

MAP_FILE = "map_data.json"


def create_graph_from_file():
    """ Creates graph object from JSON File with data about airline mappings.

    :return: graph object that is created
    """
    try:
        map_data_file = open(MAP_FILE, "r")
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


def main():
    """ Main function to create graph and prompt user for input. """
    airline_network = create_graph_from_file()
    while True:
        prompt_user_for_input(airline_network)

if __name__ == "__main__":
    main()
