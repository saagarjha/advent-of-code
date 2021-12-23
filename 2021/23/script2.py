#!/usr/bin/env python3

from collections import Counter
import copy
import heapq
import os
import pathlib
import sys
import random
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0, os.path.dirname(os.path.dirname(currentdir)))

from aoc import *

input_filename = "input"
if "AOC_SAMPLE" in os.environ:
	input_filename = "sample"

input = pathlib.Path(input_filename).read_text().strip()

lines = input.split("\n")
size = lines[1].filter(_0 == ".").len
initial = [None] * size
for r in [2, 3, 4, 5]:
	line = lines[r][1:]
	for i in line.indices():
		if line[i] in "ABCD":
			if initial[i]:
				initial[i].append(line[i])
			else:
				initial[i] = [line[i]]
initial

# initial = [
# 	None,
# 	None,
# 	["B", "B"],
# 	None,
# 	["A", "A"],
# 	None,
# 	["C", "C"],
# 	None,
# 	["D", "D"],
# 	None,
# 	None,
# ]

homes = {
	"A": 2,
	"B": 4,
	"C": 6,
	"D": 8,
}
costs = {
	"A": 1,
	"B": 10,
	"C": 100,
	"D": 1000,
}

def check_valid(position):
	for i in position.indices():
		if not position[i]:
			continue
		if isinstance(position[i], str):
			current = position[i]
			home = homes[current]
			for j in sj_irange(i, home):
				if j == i:
					continue
				if isinstance(position[j], str):
					home2 = homes[position[j]]
					locations = [i, j, home, home2].sorted()
					if locations == [home2, i, j, home] or locations == [home, j, i, home]:
						return False
	return True

positions = {}

def tuplify(position):
	return tuple(position.map(lambda x: tuplify(x) if isinstance(x, list) else x))

tries = [(0, random.random(), initial, None)]
last_cost = 0
seen_positions = {}
while tries.len:
	attempt = heapq.heappop(tries)
	key = tuplify(attempt[2])
	if key in seen_positions and seen_positions[key] <= attempt[0]:
		continue
	else:
		seen_positions[key] = attempt[0]
	if attempt[0] != last_cost:
		print(attempt[0], tries.len)
		last_cost = attempt[0]
		# print(attempt[2])
	done = True
	for i in homes:
		if attempt[2][homes[i]] != [i] * attempt[2][homes[i]].len:
			done = False
			break
	if done:
		cost = attempt[0]
		while attempt:
			print(attempt[2])
			attempt = attempt[3]
		print(cost)
		break
	for i in attempt[2].indices():
		current = attempt[2][i]
		if not current:
			continue
		if isinstance(current, str):
			home_loc = homes[current]
			home = attempt[2][home_loc]
			if home[1] and home[1] != current:
				continue
			if home[0]:
				continue
			good = True
			for j in sj_irange(i, homes[current]):
				if j == i:
					continue
				if isinstance(attempt[2][j], str):
					good = False
			if good:
				position = copy.deepcopy(attempt[2])
				position[i] = None
				home = position[home_loc]
				free_index = home.len - 1
				while free_index >= 0:
					if not home[free_index]:
						break
					if homes[home[free_index]] != home_loc:
						break
					free_index -= 1
				if free_index < 0 or home[free_index]:
					continue
				home[free_index] = current
				key = tuplify(position)
				if key in positions:
					position = positions[key]
				else:
					positions[key] = position
				heapq.heappush(tries, (attempt[0] + costs[current] * (abs(homes[current] - i) + 1 + free_index), random.random(), position, attempt))
		if isinstance(current, list):
			index = current.len - 1
			while index >= 0:
				if not current[index]:
					break
				if homes[current[index]] != i:
					break
				index -= 1
			if index < 0 or not current[index]:
				continue
			for index in current.indices():
				if current[index]:
					break
			for j in attempt[2].indices():
				if attempt[2][j] != None:
					continue
				good = True
				for k in sj_irange(i, j):
					if i == j:
						continue
					if attempt[2][k] and isinstance(attempt[2][k], str):
						good = False
				if good:
					position = copy.deepcopy(attempt[2])
					value = current[index]
					position[j] = current[index]
					position[i][index] = None
					key = tuplify(position)
					if check_valid(position):
						if key in positions:
							position = positions[key]
						else:
							positions[key] = position
						heapq.heappush(tries, (attempt[0] + costs[value] * (abs(j - i) + 1 + index), random.random(), position, attempt))
