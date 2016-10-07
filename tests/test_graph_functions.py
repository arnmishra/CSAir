""" Tests for the Graph Functions in graph_functions.py

PyCharm Error Code Documented: https://youtrack.jetbrains.com/issue/PY-20171
"""

import unittest
from scripts.graph_functions import *

TEST_FILE = "../data/test_data.json"
POSSIBLE_CONNECTIONS = ["", "BOG-LIM", "LIM-BOG", "LIM-MEX", "LIM-SCL", "MEX-LIM", "SCL-LIM"]
CITY_CODES = ["SCL", "BOG", "MEX", "LIM"]
CITY_NAMES = ["Santiago", "Bogota", "Mexico City", "Lima"]


class TestGraphFunctions(unittest.TestCase):

    def test_create_graph(self):
        """ Tests creating a graph by checking number of metros and number of connections. """
        test_airline = add_file_data_to_graph(map_file_path=TEST_FILE)
        metros = test_airline.get_all_nodes()
        self.assertEqual(len(metros), 4)
        for city_code in metros:
            self.assertTrue(city_code in CITY_CODES)
            connected_nodes = metros[city_code].get_connected_nodes()
            if city_code != "LIM":
                self.assertEqual(len(connected_nodes), 1)
            else:
                self.assertEqual(len(connected_nodes), 3)

    def test_get_map(self):
        """ Test map url to confirm it is correct by checking connections at end of url. """
        test_airline = add_file_data_to_graph(map_file_path=TEST_FILE)
        url = get_map_of_routes(test_airline, False)
        url_connections = url.split("=")[1].split(",")
        url_connections.sort()
        self.assertEqual(POSSIBLE_CONNECTIONS, url_connections)

    def test_get_all_cities(self):
        """ Test that all cities are returned correctly. """
        test_airline = add_file_data_to_graph(map_file_path=TEST_FILE)
        cities = get_all_cities(test_airline)
        for i in range(len(cities)):
            self.assertEqual(cities[i][0], CITY_CODES[i])
            self.assertEqual(cities[i][1], CITY_NAMES[i])

    def test_hub_cities(self):
        """ Test all hub cities are determined correctly based on threshold numbers. """
        test_airline = add_file_data_to_graph(map_file_path=TEST_FILE)
        hub_string_3_threshold = get_hub_cities(test_airline, 3)
        self.assertEqual(hub_string_3_threshold, "3 routes: Lima\n")
        hub_string_2_threshold = get_hub_cities(test_airline, 2)
        self.assertEqual(hub_string_2_threshold, "3 routes: Lima\n")
        hub_string_1_threshold = get_hub_cities(test_airline, 1)
        self.assertEqual(hub_string_1_threshold, "1 routes: Santiago, Bogota, Mexico City\n3 routes: Lima\n")

    def test_cities_by_continent(self):
        """ Test that cities are grouped correctly by continent. """
        test_airline = add_file_data_to_graph(map_file_path=TEST_FILE)
        continent_separated_string = get_cities_by_continent(test_airline)
        self.assertEqual(continent_separated_string, "North America: Mexico City\n"
                                                     "South America: Santiago, Bogota, Lima\n")

    def test_average_population(self):
        """ Test that the average population is determined correctly. """
        test_airline = add_file_data_to_graph(map_file_path=TEST_FILE)
        average_distance_string = get_average_distance(test_airline)
        self.assertEqual(average_distance_string, "Average Distance of Flights: 2854")

    def test_smallest_city(self):
        """ Test that the smallest city is found correctly. """
        test_airline = add_file_data_to_graph(map_file_path=TEST_FILE)
        smallest_city_string = get_smallest_city(test_airline)
        self.assertEqual(smallest_city_string, "Smallest City: Santiago with population 6000000")

    def test_biggest_city(self):
        """ Test that the biggest city is found correctly. """
        test_airline = add_file_data_to_graph(map_file_path=TEST_FILE)
        biggest_city_string = get_biggest_city(test_airline)
        self.assertEqual(biggest_city_string, "Biggest City: Mexico City with population 23400000")

    def test_average_distance(self):
        """ Test that the average distance is found correctly. """
        test_airline = add_file_data_to_graph(map_file_path=TEST_FILE)
        average_distance_string = get_average_distance(test_airline)
        self.assertEqual(average_distance_string, "Average Distance of Flights: 2854")

    def test_shortest_flight(self):
        """ Test that the shortest flight is found correctly. """
        test_airline = add_file_data_to_graph(map_file_path=TEST_FILE)
        shortest_flight_string = get_shortest_single_flight(test_airline)
        self.assertEqual(shortest_flight_string, "Shortest Flight: from Bogota to Lima (1879)")

    def test_longest_flight(self):
        """ Test that the longest flight is found correctly. """
        test_airline = add_file_data_to_graph(map_file_path=TEST_FILE)
        longest_flight_string = get_longest_single_flight(test_airline)
        self.assertEqual(longest_flight_string, "Longest Flight: from Mexico City to Lima (4231)")

    def test_delete_city(self):
        """ Test that a city and all ingoing and outgoing routes are deleted. """
        test_airline = add_file_data_to_graph(map_file_path=TEST_FILE)
        delete_city(test_airline, "LIM")
        cities = test_airline.get_all_nodes()
        self.assertFalse(test_airline.get_node("LIM"))
        for city_code in cities:
            city = test_airline.get_node(city_code)
            self.assertEqual(len(city.get_connected_nodes()), 0)

    def test_delete_route(self):
        """ Test that deleting a route removes it from the network. """
        test_airline = add_file_data_to_graph(map_file_path=TEST_FILE)
        delete_route(test_airline, "SCL", "LIM", "n")
        delete_route(test_airline, "LIM", "MEX", "y")

        santiago = test_airline.get_node("SCL")
        lima = test_airline.get_node("LIM")
        mexico = test_airline.get_node("MEX")

        self.assertTrue("LIM" not in santiago.get_connected_nodes())
        self.assertTrue("SCL" in lima.get_connected_nodes())
        self.assertTrue("MEX" not in lima.get_connected_nodes())
        self.assertTrue("LIM" not in mexico.get_connected_nodes())

    def test_add_city(self):
        """ Test that adding a new city works properly. """
        test_airline = add_file_data_to_graph(airline_network=Graph(), map_file_path=TEST_FILE)
        add_city(test_airline, {"code": "test_data"})
        all_nodes = test_airline.get_all_nodes()
        self.assertTrue("test_data" in all_nodes)

    def test_add_route(self):
        """ Test that adding a new route works properly. """
        test_airline = add_file_data_to_graph(airline_network=Graph(), map_file_path=TEST_FILE)
        add_route(test_airline, "n", "SCL", "MEX", 100)
        add_route(test_airline, "y", "SCL", "BOG", 100)

        santiago = test_airline.get_node("SCL")
        bogota = test_airline.get_node("BOG")
        mexico = test_airline.get_node("MEX")

        self.assertTrue("MEX" in santiago.get_connected_nodes())
        self.assertTrue("SCL" not in mexico.get_connected_nodes())
        self.assertTrue("BOG" in santiago.get_connected_nodes())
        self.assertTrue("SCL" in bogota.get_connected_nodes())

    def test_get_shortest_path(self):
        """ Test to confirm that the correct path, distance, cost, and time are calculated for a Path. """
        test_airline = add_file_data_to_graph(airline_network=Graph(), map_file_path=TEST_FILE)
        expected_result = "['BOG', u'LIM', 'SCL']\nTotal Distance = 4332\n" \
                          "Total Cost = $1393.55\nTotal Time = 8hrs 30mins"
        actual_result = get_shortest_path(test_airline, "BOG", "SCL")
        self.assertEqual(expected_result, actual_result)
