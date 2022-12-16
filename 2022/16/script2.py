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

limit = 25

def move(valves, remaining, current, total_dist, total):
	v1 = valves[0]
	distance = v1[1]
	if total_dist + distance >= limit:
		return (valves[1:], remaining, current, total_dist, total)
	return ([(valves[0][0], 0)] + valves[1:].map(`<(_0[0], _0[1] - distance)`>), remaining, current, total_dist + v1[1], total + current * distance)

def open(valves, remaining, current, total_dist, total, nodes):
	if total_dist >= limit:
		return ([], remaining, current, total_dist, total, nodes)
	total_dist += 1
	total += current
	new = []
	new_nodes = []
	for valve in valves:
		if valve[1] == 0:
			current += valve[0].flow
			new_nodes.append(valve[0])
		new.append((valve[0], valve[1] - 1))
	return (new, remaining, current, total_dist, total, nodes + new_nodes)

def calculate(current, total_dist, total):
	return total + max(limit - total_dist + 1, 0) * current

correct = ["OK", "HF", "CQ", "GV", "GR", "JI", "XM", "OH"]

def visit(valves, remaining, current, total_dist, total, nodes):
	# if nodes[0:correct.len].map(_0.name) == correct:
	# 	valves, remaining, current, total_dist, total, nodes

	max_value = 0
	new = move(valves, remaining, current, total_dist, total)
	(valves, remaining, current, total_dist, total) = new

	if total_dist > limit:
		valves, remaining, current, total_dist, total, nodes

	if valves.len == 0:
		return max(max_value, calculate(current, total_dist, total))

	(valves, remaining, current, total_dist, total, nodes) = open(valves, remaining, current, total_dist, total, nodes)

	if valves.len == 0:
		return max(max_value, calculate(current, total_dist, total))

	replacements = valves.filter(_0[1] < 0)
	keep = valves.filter(_0[1] >= 0)


	if valves.len == 0:
		return max(max_value, calculate(current, total_dist, total))		
	elif replacements.len == 1:
		for valve1 in remaining:
			distance = distances[(replacements[0][0], valve1)]
			new = (keep + [(valve1, distance)]).sorted(_0[1] < _1[1])
			max_value = max(max_value, visit(new, remaining - {valve1}, current, total_dist, total, nodes))
		else:
			if keep.len:
				max_value = max(max_value, visit(keep, remaining, current, total_dist, total, nodes))
	elif replacements.len == 2:
		for valve1 in remaining:
			new_remaining = remaining - {valve1}
			for valve2 in new_remaining:
				d1 = distances[(replacements[0][0], valve1)]
				d2 = distances[(replacements[1][0], valve2)]
				new = [(valve1, d1), (valve2, d2)].sorted(_0[1] < _1[1])
				max_value = max(max_value, visit(new, new_remaining - {valve2}, current, total_dist, total, nodes))

	return max(max_value, calculate(current, total_dist, total))

max_value = 0

important_valves = important_valves[:]

for valve1 in important_valves:
	# visit([(valve1, distances[(valves_lookup["AA"], valve1)])], set(important_valves) - {valve1}, 0, 0, 0, [])
	remaining = set(important_valves) - {valve1}
	for valve2 in remaining:
		print(valve1, valve2)
		d1 = distances[(valves_lookup["AA"], valve1)]
		d2 = distances[(valves_lookup["AA"], valve2)]
		if d1 > d2:
			continue

		v = visit([(valve1, d1), (valve2, d2)], remaining - {valve2}, 0, 0, 0, [])
		max_value = max(max_value, v)
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
