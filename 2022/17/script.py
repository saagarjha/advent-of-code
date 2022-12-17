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
pattern

shapes = [
	["####"],
	[".#.", "###", ".#."],
	["..#", "..#", "###"],
	["#", "#", "#", "#"],
	["##", "##"],
]

grid = [("|" + "." * 7 + "|").map(_0) for _ in range(10000)]

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
for i in range(2022):
	shape = shapes[i % shapes.len]
	height = shape.len
	r = current - height
	c = 3
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

	# for r in range(grid.len - 20, grid.len):
	# 	r, grid[r].str_join()
	# print()

# for r in range(grid.len - grid.len, grid.len):
# 	 r, grid[r].str_join()
	
grid.map(_0[1:-1].str_join.__())[::-1].last_index_by(_0 == ".......") - 1

