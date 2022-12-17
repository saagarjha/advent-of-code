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

pattern = pathlib.Path(input_filename).read_text().strip()
# pattern

shapes = [
	["####"],
	[".#.", "###", ".#."],
	["..#", "..#", "###"],
	["#", "#", "#", "#"],
	["##", "##"],
]

grid = [("|" + "." * 7 + "|").map(_0) for _ in range(20000)]

grid[-1] = "---------".map(_0)

current = grid.len - 4

def intersects(shape, r, c):
	for r2 in range(0, shape.len):
		for c2 in range(0, shape[r2].len):
			if grid[r + r2][c + c2] != "." and shape[r2][c2] != ".":
				return True
	return False

def place(shape, r, c):
	for r2 in range(0, shape.len):
		for c2 in range(0, shape[r2].len):
			if shape[r2][c2] != ".":
				grid[r + r2][c + c2] = "#"

j = 0

seen = {}

i = 0

found_cycle = False

while i < 10 ** 12:
	shape = shapes[i % shapes.len]
	height = shape.len
	r = current - height
	c = 3

	heights = []
	for column in range(1, grid[0].len - 1):
		height = 0
		for row in range(current, grid.len):
			if grid[row][column] != ".":
				heights.append(height)
				break
			height += 1
	# current, heights
	heights = tuple(heights)
	if (i % shapes.len, j % pattern.len, heights) in seen and not found_cycle:
		(cycle_start, start_height) = seen[(i % shapes.len, j % pattern.len, heights)]
		cycle_end = i
		end_height = current
		cycle_length = cycle_end - cycle_start
		i += (10 ** 12 - cycle_end) // cycle_length * cycle_length
		found_cycle = True
	else:
		seen[(i % shapes.len, j % pattern.len, heights)] = (i, current)

	while True:
		# r, c
		old_c = c
		if pattern[j % pattern.len] == "<":
			c = max(c - 1, 0)
		else:
			c = min(c + 1, grid[r].len - shape.map(_0.len).max())
		j += 1
		if intersects(shape, r, c):
			c = old_c
		r += 1
		if not intersects(shape, r, c):
			continue
		r -= 1
		break
	# place, r, c
	place(shape, r, c)
	current = min(r - 3, current)
	i += 1


cycle_height = start_height - end_height
cycle_length = cycle_end - cycle_start

cycles = (10 ** 12 - cycle_end) // cycle_length

bottom = grid.map(_0[1:-1].str_join.__())[::-1].last_index_by(_0 == ".......") - 1
bottom + cycle_height * cycles

# i
# for r in range(grid.len - bottom - 10, grid.len - bottom + 100):
# 	 r, grid[r].str_join()
