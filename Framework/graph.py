# http://www.bogotobogo.com/python/python_graph_data_structures.php


class Node:
    def __init__(self, metro_data):
        self.metro_data = metro_data
        self.connected_nodes = {}

    def add_edge(self, node, distance):
        self.connected_nodes[node] = distance

    def get_connected_nodes(self):
        return self.connected_nodes

    def get_metro_data(self):
        return self.metro_data


class Graph:
    def __init__(self):
        self.nodes = {}

    def add_node(self, metro_data):
        city_code = metro_data["code"]
        node = Node(metro_data)
        self.nodes[city_code] = node

    def get_all_nodes(self):
        return self.nodes

    def get_city(self, city_name):
        return self.nodes[city_name].get_metro_data()

    def get_all_cities(self):
        city_names = []
        for city_code in self.nodes:
            metro_data = self.nodes[city_code].get_metro_data()
            city_names.append(metro_data["name"])
        return city_names

    def add_connection(self, start_city, end_city, distance):
        start_node = self.nodes[start_city]
        end_node = self.nodes[end_city]
        start_node.add_edge(end_node, distance)
        end_node.add_edge(start_node, distance)
