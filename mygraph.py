import pyautogui as pg
import time
from multiprocessing import Process, Pipe, Queue


class Graph:
    x_offset = 15
    y_offset_start = 700
    y_offset_final = 360
    width = 0
    height = 0

    def __init__(self, node_distance):
        self.node_distance = node_distance

        screen_width = 1920
        while (self.width * node_distance) < screen_width:
            self.width = self.width + 1

        screen_height = 1080
        while (self.height * node_distance) < (screen_height - self.y_offset_final):
            self.height = self.height + 1

        print("width: " + str(self.width))
        print("height: " + str(self.height))

        self.nodes = [[Node(x, i, self.x_offset, self.y_offset_final, self.node_distance)
                       for x in range(self.width)] for i in range(self.height)]
        self.edges = []

    def print_nodes(self):
        print("Now printing nodes:")
        for row in self.nodes:
            for node in row:
                print(node)

    def print_edges(self):
        print("Now printing edges:")
        for edge in self.edges:
            print(edge)

    def add_edge(self, node1, node2, material):
        self.edges.append(Edge(node1, node2, material))

    def mouse_over_nodes(self, q):
        pg.moveTo(50, 700)
        pg.click()
        for row in self.nodes:
            for node in row:
                info = q.get()
                if info == 'break':
                        print("YEAAAAAA")
                pg.moveTo(node.x_pixels, node.y_pixels, 0.01)


class Node:
    def __init__(self, x_coord, y_coord, x_offset, y_offset_start, node_distance):
        self.x, self.y = x_coord, y_coord

        self.x_pixels = x_offset + node_distance*self.x
        self.y_pixels = y_offset_start + node_distance*self.y

        self.id = str(self.x) + ":" + str(self.y)
        # is_passable is a bool representing if a pipe could pass through this point. True by default
        self.is_passable = True

    def __str__(self):
        return "Node ID: " + self.id


class Edge:

    def __init__(self, node1, node2, transporting_type):
        self.node1 = node1
        self.node2 = node2
        self.transporting_type = transporting_type

    def __str__(self):
        return self.node1.id + "-->" + self.node2.id
