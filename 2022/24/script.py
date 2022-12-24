#!/usr/bin/env aoc_repl.py

from collections import Counter, defaultdict, deque
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

input = pathlib.Path(input_filename).read_text().strip()
map = input.split("\n").map(`<_0.map(`<_0`>)`>)

for r in range(map.len):
	for c in range(map[r].len):
		if map[r][c] == ".":
			map[r][c] = []
		elif map[r][c] != "#":
			map[r][c] = [map[r][c]]

maps = {}
maps[0] = map

def print_map(map):
	for r in map:
		for c in r:
			if c.len == 0:
				print(".", end="")
			elif c.len == 1:
				print(c.first, end="")
			else:
				print(c.len, end="")
		print()
	print()

def map_bound(i, low, high):
	if i < low:
		return high - (low - i)
	elif i >= high:
		return low + (i - high)
	else:
		return i

def evolved_map(step):
	if step in maps:
		return maps[step]
	old_map = evolved_map(step - 1)
	new_map = [[[] for _ in range(old_map[0].len)] for _ in range(old_map.len)]
	for r in range(old_map.len):
		for c in range(old_map[r].len):
			if old_map[r][c] == "#":
				new_map[r][c] = old_map[r][c]
			else:
				for i in old_map[r][c]:
					if i == "^":
						new_map[map_bound(r - 1, 1, new_map.len - 1)][c].append(i)
					elif i == "v":
						new_map[map_bound(r + 1, 1, new_map.len - 1)][c].append(i)
					elif i == "<":
						new_map[r][map_bound(c - 1, 1, new_map[r].len - 1)].append(i)
					elif i == ">":
						new_map[r][map_bound(c + 1, 1, new_map[r].len - 1)].append(i)
	maps[step] = new_map
	return new_map


def neighbors5(map, r, c):
	def inside(r, c):
		return (r == 0 and c == 1) or (r == map.len - 1 and c == map[r].len - 2) or (r >= 1 and r < map.len - 1 and c >= 1 and c < map[r].len)
	neighbors = []
	if inside(r - 1, c):
		neighbors.append((r - 1, c))
	if inside(r, c - 1):
		neighbors.append((r, c - 1))
	if inside(r, c + 1):
		neighbors.append((r, c + 1))
	if inside(r + 1, c):
		neighbors.append((r + 1, c))
	return neighbors + [(r, c)]

options = [(0, 1)]
step = 0
while True:
	new_options = set()
	for option in options:
		(r, c) = option
		if r == map.len - 1 and c == map[r].len - 2:
			sys.exit()
		map = evolved_map(step + 1)
		for neighbor in neighbors5(map, r, c):
			if not map[neighbor[0]][neighbor[1]].len:
				# "n", neighbor
				new_options.add(neighbor)
		# print_map(map)
	options = new_options
	step += 1
	step
