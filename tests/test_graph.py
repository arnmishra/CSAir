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
        """ Test that connections can be created properly. """
        graph = Graph()
        start_key = "first_test_key"
        start_data = "first_test_data"
        end_key = "second_test_key"
        end_data = "second_test_data"
        graph.add_node(start_key, start_data)
        graph.add_node(end_key, end_data)
        graph.add_connection(start_key, end_key, 0)
        start_node = graph.get_node(start_key)
        connected = start_node.get_connected_nodes()
        self.assertEqual(len(connected), 1)
        self.assertTrue(end_key in connected)

    def test_delete_connection(self):
        """ Test that a connection can be successfully deleted between nodes. """
        graph = Graph()
        start_key = "first_test_key"
        start_data = "first_test_data"
        end_key = "second_test_key"
        end_data = "second_test_data"
        graph.add_node(start_key, start_data)
        graph.add_node(end_key, end_data)
        graph.add_connection(start_key, end_key, 0)
        graph.delete_connection(start_key, end_key)
        all_nodes = graph.get_all_nodes()
        for key in all_nodes:
            node = all_nodes[key]
            self.assertEqual(len(node.get_connected_nodes()), 0)

    def test_delete_node(self):
        """ Test that a node can be deleted correctly. """
        graph = Graph()
        start_key = "first_test_key"
        start_data = "first_test_data"
        end_key = "second_test_key"
        end_data = "second_test_data"
        graph.add_node(start_key, start_data)
        graph.add_node(end_key, end_data)
        graph.add_connection(start_key, end_key, 0)
        graph.delete_node(end_key)
        all_nodes = graph.get_all_nodes()
        self.assertTrue(len(all_nodes) == 1)
        deleted_node = graph.get_node(end_key)
        self.assertFalse(deleted_node)

    def test_modify_node(self):
        """ Test that a node's data can be modified. """
        graph = Graph()
        key = "first_test_key"
        data = "first_test_data"
        modified_data = "second_test_data"
        graph.add_node(key, data)
        graph.set_node(key, modified_data)
        node = graph.get_node(key)
        self.assertEqual(node.get_data(), modified_data)
