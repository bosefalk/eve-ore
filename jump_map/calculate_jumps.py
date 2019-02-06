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
from timeit import default_timer as timer
import itertools
import pickle
from tqdm import tqdm

conn = sqlite3.connect("sqlite-latest.sqlite")
cur = conn.cursor()
# Kor-Azor is regionID 10000065
# First we will do a search within only the Kor-Azor region, but that won't catch all possible shortest paths
# as there are some shortcuts through neighbours. Once we've found the shortest path within Kor-Azor we do another
# search in the extended region database, but stop searching down any path once we're above the shortest Kor-Azor path
# for performance reasons
cur.execute("SELECT fromSolarSystemID, toSolarSystemID FROM mapSolarSystemJumps WHERE toRegionID IN (10000065)")
rows = cur.fetchall()

solarSystemDict = dict()
# For each unique entry fromSolarSystemID (first list element) look up all possible second list elements (toSolarSystemID)
for r in rows:
    solarSystemDict[str(r[0])] = set([str(i[1]) for i in rows if str(i[0]) == str(r[0])])


cur = conn.cursor()
# Neighbouring regions:
# 10000043, 10000067, 10000052, 10000049, 10000054
cur.execute("SELECT fromSolarSystemID, toSolarSystemID FROM mapSolarSystemJumps "
            "WHERE toRegionID IN (10000065, 10000043, 10000067, 10000052, 10000049, 10000054)")

rows = cur.fetchall()
conn.close()

solarSystemDictExtended = dict()

# For each unique entry fromSolarSystemID (first list element) look up all possible second list elements (toSolarSystemID)
for r in rows:
    solarSystemDictExtended[str(r[0])] = set([str(i[1]) for i in rows if str(i[0]) == str(r[0])])


# Breadth-first search for shortest path
# From https://eddmann.com/posts/depth-first-search-and-breadth-first-search-in-python/

# Search through each depth layer of the graph before moving onto the next layer (i.e. check if goal is
# within 1 jump of the start, if not move on to see if within 2 jumps and so on)

def bfs_paths(graph, start, goal):
    queue = [(start, [start])]
    while queue:
        (vertex, path) = queue.pop(0)
        for next in graph[vertex] - set(path):
            if next == goal:
                yield path + [next]
            else:
                queue.append((next, path + [next]))


def shortest_path(graph, start, goal):
    try:
        return next(bfs_paths(graph, start, goal))
    except StopIteration:
        return None


def calc_jumps(from_id, to_id):

    s_path = shortest_path(solarSystemDictExtended, from_id, to_id)
    return(len(s_path) - 1)

# Find all possible combinations of solar systems within Kor-Azor region + neighboring systems
uniqueSolarSystems = list(solarSystemDict.keys())
#
#
# solarSystemsCombinations = list()
# for subset in itertools.combinations(uniqueSolarSystems, 2):
#     solarSystemsCombinations.append(subset)
#
# sSC_list = list()
# for b in solarSystemsCombinations:
#     sSC_list.append(list(b))
#
#
# # Calculate the jump distances between all elements in the combined list
# for item in tqdm(sSC_list):d
#     item.append(calc_jumps(item[0], item[1]))

# Save as class to define findJumps method
class jumpMap:

    # jump_list should be a list of lists where the first two elements are
    # solar system ids, and the third the number of jumps between them
    def __init__(self, jump_list):
        self.jump_list = jump_list

    def findJumps(self, from_id, to_id):
        nJumps = [a[2] for a in self.jump_list if
                  ((a[0] == from_id) and (a[1] == to_id)) or
                  ((a[1] == to_id) and (a[0] == from_id))]
        return(int(nJumps))


# We want to find the number of jumps from Nahol, ID 30005069
nahol_jumps = list()
for item in uniqueSolarSystems:
    nahol_jumps.append(['30005069', item])

for item in tqdm(nahol_jumps):
    item.append(calc_jumps(item[0], item[1]))

jumpMap_Nahol = jumpMap(nahol_jumps)
pickle.dump(jumpMap_Nahol, open("jumpMap_Nahol.pickle", "wb" ), pickle.HIGHEST_PROTOCOL)