#!/usr/bin/env aoc_repl.py

from collections import Counter
import inspect
import operator
import os
import pathlib
import sys

import heapq

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0, os.path.dirname(os.path.dirname(currentdir)))

from aoc import *

input_filename = "input"
if "AOC_SAMPLE" in os.environ:
	input_filename = "sample"

input = pathlib.Path(input_filename).read_text().strip()
grid = input.split("\n").map(`<_0.map(ord)`>)

grid = Matrix(grid)

for r in range(grid.rows):
	for c in range(grid.columns):
		if grid[r, c] == ord("S"):
			start = (r, c)
			grid[r, c] = ord("a")
		elif grid[r, c] == ord("E"):
			end = (r, c)
			grid[r, c] = ord("z")

def do_walk(start):
	queue = [(0, start, set())]

	memo = {}

	while len(queue):
		next = heapq.heappop(queue)[1:]
		(r, c) = next[0]
		# if next[0] == end:
		# 	visited.len + 1
			# break
		visited = next[1]
		if (r, c) in memo:
			if memo[(r, c)] <= visited.len:
				continue
		memo[(r, c)] = visited.len

		for neighbor in grid.neighbors4(r, c):
			# r, c, neighbor, grid[neighbor[0], neighbor[1]] - grid[r, c]
			if grid[neighbor[0], neighbor[1]] - grid[r, c] <= 1:
				heapq.heappush(queue, (visited.len + 1, neighbor, visited.union({(r, c)})))
	if end in memo:
		return memo[end]
	else:
		return 1000000000

shortest = 10000000000
for r in range(grid.rows):
	for c in range(grid.columns):
		if grid[r, c] == ord("a"):
			r, c
			shortest = min(do_walk((r, c)), shortest)

shortest
# for r in range(grid.rows):
# 	for c in range(grid.columns):
# 		if (r, c) in visited:
# 			print(chr(grid[r, c]).upper(), end="")
# 			# print(str(memo[(r, c)]).zfill(3), end=" ")
# 		else:
# 			print(chr(grid[r, c]), end="")
# 			# print("    ", end="")
# 	print()

# memo[end]
