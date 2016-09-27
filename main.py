import json
import sys
from Framework.graph import Graph
from Framework.statistics import get_statistic

MAP_FILE = "map_data.json"


def prompt_user_for_input(airline_network):
    prompt = '\nFor a list of all cities, enter "0".\n'
    prompt += 'For information about a single city, enter "1".\n'
    prompt += 'For statistics about CSAir, enter "2".\n'

    response = int(raw_input(prompt))

    if response == 0:
        print airline_network.get_all_cities()
    elif response == 1:
        city_name = raw_input("Enter the city code for which you want the information: ").strip()
        metro_data = airline_network.get_city(city_name)
        for key in metro_data:
            print key, ":", metro_data[key]
    elif response == 2:
        prompt = "\nEnter the number associated with the statistic:\n"
        prompt += "0 - Longest Single Flight\n"
        prompt += "1 - Shortest Single Flight\n"
        prompt += "2 - Average Distance of Flights\n"
        prompt += "3 - Biggest City in CSAir Network\n"
        prompt += "4 - Smallest City in CSAir Network\n"
        prompt += "5 - Average Population of cities in CSAir Network\n"
        prompt += "6 - List of Cities by Continent in CSAir Network\n"
        prompt += "7 - CSAir's Hub Cities\n"
        statistic_code = int(raw_input(prompt))
        print get_statistic(statistic_code, airline_network)
    else:
        response = -1
    return response


def main():
    try:
        map_data_file = open(MAP_FILE, "r")
    except:
        print "Incorrect File Path"
        return 1
    map_data = json.load(map_data_file)
    airline_network = Graph()
    for metro in map_data["metros"]:
        airline_network.add_node(metro)
    for route in map_data["routes"]:
        airline_network.add_connection(route["ports"][0], route["ports"][1], route["distance"])
    response = 0
    while response != -1:
        response = prompt_user_for_input(airline_network)

if __name__ == "__main__":
    main()
