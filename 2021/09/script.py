#!/usr/bin/env python3

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
heights = input.split("\n").map(lambda x: x.map(int))
# print(heights)
low = []

def inside(r, c):
	return r >= 0 and r < heights.len and c >= 0 and c < heights[0].len

for r in heights.indices():
	for c in heights[r].indices():
		good = True
		if inside(r - 1, c) and heights[r][c] >= heights[r - 1][c]:
			good = False
		if inside(r + 1, c) and heights[r][c] >= heights[r + 1][c]:
			good = False
		if inside(r, c - 1) and heights[r][c] >= heights[r][c - 1]:
			good = False
		if inside(r, c + 1) and heights[r][c] >= heights[r][c + 1]:
			good = False
		if good:
			# print(r, c)
			low.append(heights[r][c])
print(sum(low.map(lambda x: x + 1)))
