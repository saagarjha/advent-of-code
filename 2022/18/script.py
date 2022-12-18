#!/usr/bin/env aoc_repl.py

from collections import Counter, deque
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
cubes = input.split("\n").map(`<_0.split(",").map(int)`>)

size = 25

grid = [[[False] * size for _ in range(size)] for _ in range(size)]

total = 0
for cube in cubes:
	grid[cube[0] + 1][cube[1] + 1][cube[2] + 1] = True
	# if cube.filter(_0 >= size).len:
	# 	print(cube)
	total += 1

total_neighbors = 0

seen = {}

for x in sj_range(1, grid.len - 1):
	for y in sj_range(1, grid.len - 1):
		for z in sj_range(1, grid.len - 1):
			if grid[x][y][z]:
				neighbors = 0
				for off_x in sj_irange(-1, 1):
					for off_y in sj_irange(-1, 1):
						for off_z in sj_irange(-1, 1):
							if [off_x, off_y, off_z].filter(_0 == 0).len == 2:
								if grid[x + off_x][y + off_y][z + off_z]:
									# x, y, z, "",  x + off_x, y + off_y, z + off_z
									seen[(x, y, z, off_x, off_y, off_z)] = (x + off_x, y + off_y, z + off_z, off_x, off_y, off_z)
								neighbors += grid[x + off_x][y + off_y][z + off_z]
				total_neighbors += neighbors

seen.len

for c1 in seen:
	x, y, z, off_x, off_y, off_z = seen[c1]
	if (x, y, z, -off_x, -off_y, -off_z) not in seen:
		print(x, y, z, off_x, off_y, off_z)

total_neighbors
total * 6 - total_neighbors

