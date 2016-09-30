""" Tests for the Graph in graph.py

PyCharm Error Code Documented: https://youtrack.jetbrains.com/issue/PY-20171
"""

import unittest
from framework.graph import *


class TestGraph(unittest.TestCase):

    def test_add_nodes(self):
        """ Test that a node can be added and gotten correctly. """
        graph = Graph()
        node = Node("test_data")
        graph.add_node("test_key", "test_data")
        test_node = graph.get_node("test_key")
        self.assertEqual(node.get_data(), test_node.get_data())

    def test_add_connection(self):
        """ Test that connections can be created and all nodes can be returned correctly. """
        graph = Graph()
        graph.add_node("first_test_key", "first_test_data")
        graph.add_node("second_test_key", "second_test_data")
        graph.add_connection("first_test_key", "second_test_key", 0)
        all_nodes = graph.get_all_nodes()
        for key in all_nodes:
            if key == "first_test_key":
                self.assertEqual(all_nodes["first_test_key"].get_data(), "first_test_data")
            elif key == "second_test_key":
                self.assertEqual(all_nodes["second_test_key"].get_data(), "second_test_data")
