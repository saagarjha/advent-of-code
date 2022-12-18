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

visited = set()

explore = deque([(0, 0, 0)])

while len(explore):
	next = explore.pop()
	(x, y, z) = next
	if (x, y, z) in visited:
		continue
	for off_x in sj_irange(-1, 1):
		for off_y in sj_irange(-1, 1):
			for off_z in sj_irange(-1, 1):
				if [off_x, off_y, off_z].filter(_0 == 0).len != 2:
					continue
				new = (x + off_x, y + off_y, z + off_z)
				(new_x, new_y, new_z) = new
				if new.filter(`<_0 < 0 or _0 >= size`>).len:
					continue
				if grid[new_x][new_y][new_z]:
					new, off_x, off_y, off_z
					total += 1
				else:
					visited.add((x, y, z))
					explore.append(new)

total
