from random import randint

class Connection:

    def __init__(self, node1, node2, length):
        self.node1 = node1
        self.node2 = node2
        self.length = length


class Node:

    def __init__(self, name):
        self.name = name
        self.objs = []

    def add_object(self, obj):
        self.objs.append(obj)


class Map:

    def __init__(self, nodes, connections):
        self.nodes = nodes
        self.connections = connections

    def visualize(self):
        pass


    def generate_random_map(self, nnodes=None, low=None, up=None):

        if nnodes is None:
            nnodes = randint(low, up)