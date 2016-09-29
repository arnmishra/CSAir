""" Generic Graph class consisting of Nodes.

Source used to understand python classes:
http://www.bogotobogo.com/python/python_graph_data_structures.php
"""


class Node:
    """ Node class to store data in the graph.

    Each Node stores an adjacency list
    of all connected Nodes in the form of a dictionary that maps connected
    Node to its weight. Each Node also stores the data pertaining to it.
    """
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
    """ Graph class to hold data about all nodes.

    The Graph class stores all the Nodes that are part of it in a dictionary
    that maps a key that the user provides to each node in the Graph. The Graph
    also adds an edge from both start to end as well as end to start each time a
    new connection is created to ensure each pair of nodes are connected both ways.
    """
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
