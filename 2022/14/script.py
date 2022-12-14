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
paths = input.split("\n")
grid = [["." for _ in range(1000)] for _ in range(1000)]
for path in paths:
	points = path.split(" -> ").map(`<_0.split(",").map(int)`>)
	for (p1, p2) in points.window(2):
		if p1[0] == p2[0]:
			for i in sj_irange(p1[1], p2[1]):
				grid[p1[0]][i] = "#"
		else:
			for i in sj_irange(p1[0], p2[0]):
				grid[i][p1[1]] = "#"

grid = grid.transpose()

for i in range(1000):
	r = 0
	c = 500
	while True:
		if r > 700:
			print(i)
			sys.exit()
		if grid[r + 1][c] == ".":
			r += 1
		elif grid[r + 1][c] != ".":
			if grid[r + 1][c - 1] == ".":
				r += 1
				c -= 1
			elif grid[r + 1][c + 1] == ".":
				r += 1
				c += 1
			else:
				break
	# print(r, c)
	# print()
	grid[r][c] = "O"



for r in sj_irange(0, 10):
	for c in sj_irange(490, 510):
		print(grid[r][c], end="")
	print()
