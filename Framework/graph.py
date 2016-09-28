# http://www.bogotobogo.com/python/python_graph_data_structures.php


class Node:
    def __init__(self, data):
        self.data = data
        self.connected_nodes = {}

    def add_edge(self, node, weight):
        self.connected_nodes[node] = weight

    def get_connected_nodes(self):
        return self.connected_nodes

    def get_data(self):
        return self.data


class Graph:
    def __init__(self):
        self.nodes = {}

    def add_node(self, key, data):
        node = Node(data)
        self.nodes[key] = node

    def get_all_nodes(self):
        return self.nodes

    def get_node(self, key):
        return self.nodes[key].get_data()

    def add_connection(self, start_key, end_key, weight):
        start_node = self.nodes[start_key]
        end_node = self.nodes[end_key]
        start_node.add_edge(end_node, weight)
        end_node.add_edge(start_node, weight)
