# Since I'm only interested in the market in one region, I pre-calculate all jump distances from the static API export
# from https://developers.eveonline.com/resource/resources
# Using the sqlite-latest export from here which is the same data but prepared in nice tables: https://www.fuzzwork.co.uk/dump/
# Table is mapSolarSystemJumps
# Graph calculations from https://www.python-course.eu/graphs_python.php

# First find the relevant systems by constellation from the sqlite database table, then use this to
# construct a dictionary in the form key = systemID, value = list of neighbouring systemIDs
# Then use this to construct a graph with the Graph class, and use a built-in method for finding
# all paths between two points from which we select the shortest one.
# To shorten searching time if any potential path is more than 20 jumps the search stops

import sqlite3
import csv

conn = sqlite3.connect("jump_map/sqlite-latest.sqlite")
cur = conn.cursor()
# Kor-Azor is regionID 10000065
# We also need to include systems in the neighbouring regions as sometimes it's faster to jump through there:
# 10000043, 10000067, 10000052, 10000049, 10000054
# This is very inefficient but since we're just doing it once it's ok
cur.execute("SELECT fromSolarSystemID, toSolarSystemID FROM mapSolarSystemJumps "
            "WHERE toRegionID IN (10000065, 10000043, 10000067, 10000052, 10000049, 10000054)")
rows = cur.fetchall()
conn.close()


solarSystemDict = dict()

# For each unique entry fromSolarSystemID (first list element) look up all possible second list elements (toSolarSystemID)
for r in rows:
    solarSystemDict[str(r[0])] = [str(i[1]) for i in rows if str(i[0]) == str(r[0])]

""" A Python Class
A simple Python graph class, demonstrating the essential 
facts and functionalities of graphs.
"""


class Graph(object):

    def __init__(self, graph_dict=None):
        """ initializes a graph object
            If no dictionary or None is given,
            an empty dictionary will be used
        """
        if graph_dict == None:
            graph_dict = {}
        self.__graph_dict = graph_dict

    def vertices(self):
        """ returns the vertices of a graph """
        return list(self.__graph_dict.keys())

    def edges(self):
        """ returns the edges of a graph """
        return self.__generate_edges()

    def add_vertex(self, vertex):
        """ If the vertex "vertex" is not in
            self.__graph_dict, a key "vertex" with an empty
            list as a value is added to the dictionary.
            Otherwise nothing has to be done.
        """
        if vertex not in self.__graph_dict:
            self.__graph_dict[vertex] = []

    def add_edge(self, edge):
        """ assumes that edge is of type set, tuple or list;
            between two vertices can be multiple edges!
        """
        edge = set(edge)
        (vertex1, vertex2) = tuple(edge)
        if vertex1 in self.__graph_dict:
            self.__graph_dict[vertex1].append(vertex2)
        else:
            self.__graph_dict[vertex1] = [vertex2]

    def __generate_edges(self):
        """ A static method generating the edges of the
            graph "graph". Edges are represented as sets
            with one (a loop back to the vertex) or two
            vertices
        """
        edges = []
        for vertex in self.__graph_dict:
            for neighbour in self.__graph_dict[vertex]:
                if {neighbour, vertex} not in edges:
                    edges.append({vertex, neighbour})
        return edges

    def __str__(self):
        res = "vertices: "
        for k in self.__graph_dict:
            res += str(k) + " "
        res += "\nedges: "
        for edge in self.__generate_edges():
            res += str(edge) + " "
        return res

    def find_path(self, start_vertex, end_vertex, path=None):
        """ find a path from start_vertex to end_vertex
            in graph """
        if path == None:
            path = []
        graph = self.__graph_dict
        path = path + [start_vertex]
        if start_vertex == end_vertex:
            return path
        if start_vertex not in graph:
            return None
        for vertex in graph[start_vertex]:
            if vertex not in path:
                extended_path = self.find_path(vertex,
                                               end_vertex,
                                               path)
                if extended_path:
                    return extended_path
        return None

    def find_all_paths(self, start_vertex, end_vertex, path=[]):
        """ find all paths from start_vertex to
            end_vertex in graph """
        graph = self.__graph_dict
        path = path + [start_vertex]
        if start_vertex == end_vertex:
            return [path]
        if start_vertex not in graph:
            return []
        paths = []
        for vertex in graph[start_vertex]:
            if vertex not in path:
                extended_paths = self.find_all_paths(vertex,
                                                     end_vertex,
                                                     path)
                for p in extended_paths:
                    paths.append(p)
                    if len(paths) > 20:
                        return paths
        return paths


solarSystemGraph = Graph(solarSystemDict)


def calc_jumps(from_id, to_id):
    # find_path gives a list of the shortest path to jump through, starting with the "current" system
    # so this minus 1 is the number of jumps
    all_paths = solarSystemGraph.find_all_paths(from_id, to_id)
    length_all_paths = [len(path) for path in all_paths]
    n_jumps = min(length_all_paths) - 1
    return(n_jumps)




# Test to make sure we get the same number of jumps as from a market window export. We're starting in
# system Nahol, ID 30005069
test_list = []

with open("jump_map/jump_test.csv", 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        test_list.append([str(30005069), str(row[0]), int(row[1])])

for item in test_list:
    item.append(calc_jumps(item[0], item[1]))


