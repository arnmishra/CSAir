""" Generic Graph class consisting of Nodes.

Source used to understand python classes:
http://www.bogotobogo.com/python/python_graph_data_structures.php
"""


class Node:
    """ Node class to store data in the graph.

    Each Node stores an adjacency list of all connected Nodes in the form
    of a dictionary that maps the connected node's key to its weight.
    Each Node also stores the data pertaining to it.
    """
    def __init__(self, data):
        self.data = data
        self.connected_nodes = {}

    def add_edge(self, node_key, weight):
        self.connected_nodes[node_key] = weight

    def delete_edge(self, node_key):
        del self.connected_nodes[node_key]

    def get_connected_nodes(self):
        return self.connected_nodes

    def get_data(self):
        return self.data

    def set_data(self, data):
        self.data = data


class Graph:
    """ Graph class to hold data about all nodes.

    The Graph class stores all the Nodes that are part of it in a dictionary
    that maps a key that the user provides to each node in the Graph. The Graph
    also adds an edge from both start to end as well as end to start each time a
    new connection is created to ensure each pair of nodes are connected both ways.
    """
    def __init__(self):
        self.nodes = {}

    def get_all_nodes(self):
        return self.nodes

    def get_node(self, key):
        if key in self.nodes:
            return self.nodes[key]
        else:
            return None

    def add_node(self, key, data):
        node = Node(data)
        self.nodes[key] = node

    def set_node(self, key, data):
        if key in self.nodes:
            self.nodes[key].set_data(data)
            return True
        else:
            return False

    def delete_node(self, key):
        del self.nodes[key]

    def add_connection(self, start_key, end_key, weight):
        start_node = self.nodes[start_key]
        start_node.add_edge(end_key, weight)

    def delete_connection(self, start_key, end_key):
        start_node = self.nodes[start_key]
        start_node.delete_edge(end_key)
