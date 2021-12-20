#!/usr/bin/env python3

import copy
from collections import Counter
import os
import pathlib
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0, os.path.dirname(os.path.dirname(currentdir)))

from aoc import *

input_filename = "input"
if "AOC_SAMPLE" in os.environ:
	input_filename = "sample"

input = pathlib.Path(input_filename).read_text().strip()
lines = input.split("\n")
algorithm = lines[0]
image = lines[2:]

extra = 20

grid = [[0] * (image.len + extra) for r in range(image.len + extra)]

for r in range(image.len):
	for c in range(image[r].len):
		grid[r + extra // 2][c + extra // 2] = 1 if image[r][c] == "#" else 0

grid_copy = copy.deepcopy(grid)
for _ in range(0, 2):
	for r in range(1, grid.len - 1):
		for c in range(1, grid.len - 1):
			bits = [
				grid[r - 1][c - 1],
				grid[r - 1][c],
				grid[r - 1][c + 1],
				grid[r][c - 1],
				grid[r][c],
				grid[r][c + 1],
				grid[r + 1][c - 1],
				grid[r + 1][c],
				grid[r + 1][c + 1],
			]
			grid_copy[r][c] = 1 if algorithm[int(bits.str_join(), 2)] == "#" else 0
	print(grid_copy.map(_0.str_join.__()).str_join("\n"))
	print()
	grid = copy.deepcopy(grid_copy)

sum = 0
for r in range(extra // 2 - 2, extra // 2 + image.len + 2):
	for c in range(extra // 2 - 2, extra // 2 + image.len + 2):
		sum += grid[r][c]
sum
