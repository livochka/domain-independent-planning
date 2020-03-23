from random import randint
import networkx as nx
import matplotlib.pyplot as plt
from math import floor, sqrt


class Connection:
    """
    Represents a connection between two nodes in a graph
    """

    FACT_CONNECTED = "(connected {} {})"
    FACT_DISTANCE = "(= (distance {} {}) {})"

    def __init__(self, nodes, distance):
        self.nodes = nodes
        self.distance = distance
        if self.distance == 0:
            self.distance += 1

    def get_initial_state(self):
        """
        Generating initial state, the fact of connection and distance between two nodes
        :return: list(str1, str2...) in form ["(connected n1 n2)" ... ]
        """
        return [Connection.FACT_CONNECTED.format(str(self.nodes[0]), str(self.nodes[1])),
                Connection.FACT_CONNECTED.format(str(self.nodes[1]), str(self.nodes[0])),
                Connection.FACT_DISTANCE.format(str(self.nodes[0]), str(self.nodes[1]), str(self.distance)),
                Connection.FACT_DISTANCE.format(str(self.nodes[1]), str(self.nodes[0]), str(self.distance))]


class Node:
    """
    Represents a node in the graph
    """

    ID = 0
    CHAR = "n"

    def __init__(self):
        self.ID = Node.ID
        Node.ID += 1
        self.objs = []

    def add_obj(self, obj):
        self.objs.append(obj)

    def is_empty(self):
        return len(self.objs) == 0

    def __str__(self):
        return Node.CHAR + str(self.ID)



class Map:

    def __init__(self, nodes=None, connections=None):
        self.nodes = nodes
        self.connections = connections
        self.nodes_coordinates_mapping = None
        self.graph = None

    def __len__(self):
        return len(self.nodes)

    def get_node(self, number):
        for node in self.nodes:
            if node.ID == number:
                return node

    def get_objects(self):
        return self.nodes

    def get_distance(self, n1, n2):
        node1, node2 = self.get_node(n1), self.get_node(n2)
        return nx.dijkstra_path_length(self.graph, node1, node2)

    def get_initial_state(self):
        return [connection.get_initial_state() for connection in self.connections]

    def visualize(self):
        nx.draw(self.graph, nx.get_node_attributes(self.graph, 'pos'),
                with_labels=True, node_size=100, node_color='yellow')
        labels = nx.get_edge_attributes(self.graph, 'weight')
        nx.draw_networkx_edge_labels(self.graph, nx.get_node_attributes(self.graph, 'pos'),
                                     edge_labels=labels, font_size=7)
        plt.show()

    def generate_nodes(self, nnodes, scale):
        coordinates, nodes = [], []
        map_size = scale * nnodes

        def assign_coordinate(size, coordinates):
            candidate = (randint(0, size), randint(0, size))
            while candidate in coordinates:
                candidate = (randint(0, size), randint(0, size))
            return candidate


        for node_id in range(nnodes):
            coordinate = assign_coordinate(map_size, coordinates)
            nodes.append(Node())
            coordinates.append(coordinate)

        coordinates_map = dict(zip(nodes, coordinates))
        self.nodes = nodes
        self.nodes_coordinates_mapping = coordinates_map
        return coordinates_map

    def generate_connections(self, rate=2, scale=50):
        coordinates = self.nodes_coordinates_mapping.items()
        sorted_coordinates = sorted(list(coordinates), key=lambda x: sqrt(x[1][0]**2 + x[1][1]**2))
        connections = []

        def calculate_distance(pos1, pos2):
            return sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2) / (scale / 2)

        for node_i in range(len(sorted_coordinates)):
            ncon = randint(1, rate) + 1
            node1 = sorted_coordinates[node_i]
            for node_j in range(node_i + 1, node_i + ncon):
                node2 = sorted_coordinates[node_j % len(sorted_coordinates)]
                distance = floor(calculate_distance(node1[1], node2[1]))
                connections.append(Connection([node1[0], node2[0]], distance))

        self.connections = connections


    def generate_random_configuration(self, nnodes=10, scale=50):
        self.generate_nodes(nnodes, scale)
        self.generate_connections(scale=scale)

        G = nx.Graph()
        for node in self.nodes_coordinates_mapping:
            G.add_node(node, pos=self.nodes_coordinates_mapping[node])
        for connection in self.connections:
            G.add_edge(connection.nodes[0], connection.nodes[1], weight=connection.distance)

        self.graph = G
        return self


if __name__ == "__main__":
    map = Map().generate_random_configuration(4)
    map.visualize()
    print("Distance:", map.get_distance(0,  1))





