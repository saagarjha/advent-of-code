#!/usr/bin/env aoc_repl.py

from collections import Counter, deque, defaultdict
import heapq
import inspect
import itertools
import operator
import os
import pathlib
import sys

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0, os.path.dirname(os.path.dirname(currentdir)))

from aoc import *

input_filename = "input"
if "AOC_SAMPLE" in os.environ:
	input_filename = "sample"

class Valve:
	def __init__(self, name, flow, children):
		self.name = name
		self.flow = flow
		self.children = children

	def __repr__(self):
		return f"{self.name}" 

input = pathlib.Path(input_filename).read_text().strip()

valves = []

for line in input.split("\n"):
	valve, rest = line.split(" has flow rate=")
	valve = valve.replace("Valve ", "")
	rate, rest = rest.split(";")
	rate = int(rate)
	valves.append(Valve(valve, rate, rest.replace(" tunnels lead to valves ", "").replace(" tunnel leads to valve ", "").split(", ")))

valves_lookup = dict(valves.map(`<(_0.name, _0)`>))

class Graph(object):
	def __init__(self):
		pass
	
	def get_nodes(self):
		return valves
	
	def get_outgoing_edges(self, node):
		out = []
		for valve in node.children:
			out.append(valves_lookup[valve])
		return out
	
	def value(self, node1, node2):
		return 1 if node2.name in node1.children else (1 if node1.name in node2.children else 10000000000)

def dijkstra_algorithm(graph, start_node):
	unvisited_nodes = list(graph.get_nodes())
 
	# We'll use this dict to save the cost of visiting each node and update it as we move along the graph   
	shortest_path = {}
 
	# We'll use this dict to save the shortest known path to a node found so far
	previous_nodes = {}
 
	# We'll use max_value to initialize the "infinity" value of the unvisited nodes   
	max_value = sys.maxsize
	for node in unvisited_nodes:
		shortest_path[node] = max_value
	# However, we initialize the starting node's value with 0   
	shortest_path[start_node] = 0
	
	# The algorithm executes until we visit all nodes
	while unvisited_nodes:
		# The code block below finds the node with the lowest score
		current_min_node = None
		for node in unvisited_nodes: # Iterate over the nodes
			if current_min_node == None:
				current_min_node = node
			elif shortest_path[node] < shortest_path[current_min_node]:
				current_min_node = node
				
		# The code block below retrieves the current node's neighbors and updates their distances
		neighbors = graph.get_outgoing_edges(current_min_node)
		for neighbor in neighbors:
			tentative_value = shortest_path[current_min_node] + graph.value(current_min_node, neighbor)
			if tentative_value < shortest_path[neighbor]:
				shortest_path[neighbor] = tentative_value
				# We also update the best path to the current node
				previous_nodes[neighbor] = current_min_node
 
		# After visiting its neighbors, we mark the node as "visited"
		unvisited_nodes.remove(current_min_node)
	
	return previous_nodes, shortest_path

graph = Graph()

dijkstra_algorithm(graph, valves[0])[1]

important_valves = valves.filter(_0.flow != 0)
distances = defaultdict(lambda: 1000000000)
for valve in valves:
	shortest = dijkstra_algorithm(graph, valve)[1]
	for v2 in shortest:
		distances[(valve, v2)] = min(distances[(valve, v2)], shortest[v2])
		distances[(v2, valve)] = min(distances[(valve, v2)], shortest[v2])

def cost(permutation):
	current = permutation.first.flow
	total_dist = distances[(valves_lookup["AA"], permutation.first)] + 1 + 1
	total = 0
	for (v1, v2) in permutation.window(2):
		distance = distances[(v1, v2)]
		# total, current, total_dist, v1.name, v2.name, distance
		if total_dist + distance >= 30:
			break

		# for i in range(distance):
		# 	total_dist + i, current

		total_dist += distance
		total += current * distance
		if total_dist >= 30:
			break
		total_dist += 1

		# total_dist, current

		total += current
		current += v2.flow
	# for i in sj_irange(total_dist, 30):
	# 	i, current
	total += max(30 - total_dist + 1, 0) * current
	return total

def visit(v1, remaining, current, total_dist, total, nodes):
	max_value = 0
	if nodes.map(_0.name) == ["DD", "BB", "JJ", "HH", "CC"]:
		remaining, current, total_dist, total
	for v2 in remaining:
		distance = distances[v1, v2]
		if total_dist + distance >= 30:
			continue
		new_dist = total_dist + distance
		new_total = total + current * distance
		if new_dist >= 30:
			max_value = max(max_value, new_total)
			continue
		new_dist += 1
		new_total += current
		new_current = current + v2.flow
		max_value = max(max_value, visit(v2, remaining - {v2}, new_current, new_dist, new_total, nodes + [v2]))
	max_value = max(max_value, total + max(30 - total_dist + 1, 0) * current)
	return max_value

max_value = 0

for valve in important_valves:
	max_value = max(max_value, visit(valve, set(important_valves) - {valve}, valve.flow, distances[(valves_lookup["AA"], valve)] + 1 + 1, 0, [valve]))
max_value
# max_value = 0
# count = 0
# for permutation in itertools.permutations(important_valves):
# 	count += 1
# 	if count % 1000 == 0:
# 		count
# 	# if permutation.map(_0.name) == ["DD", "BB", "JJ", "HH", "EE", "CC"]:
# 	# 	print("asdf", cost(permutation))
# 	new = cost(permutation)
# 	if new > max_value:
# 		new, permutation
# 		max_value = new
# max_value
