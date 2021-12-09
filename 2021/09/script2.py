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

def size(r, c, fixup=[]):
	if heights[r][c] == 9:
		return 0
	if not fixup.len:
		clean = True
	else:
		clean = False
	total = 1
	original = heights[r][c]
	fixup.append((r, c, original))
	heights[r][c] = -1
	# print(r, c, original)
	if inside(r - 1, c) and original < heights[r - 1][c]:
		total += size(r - 1, c, fixup)
	if inside(r + 1, c) and original < heights[r + 1][c]:
		total += size(r + 1, c, fixup)
	if inside(r, c - 1) and original < heights[r][c - 1]:
		total += size(r, c - 1, fixup)
	if inside(r, c + 1) and original < heights[r][c + 1]:
		total += size(r, c + 1, fixup)
	if clean:
		print(fixup)
		for fix in fixup:
			heights[fix[0]][fix[1]] = fix[2]
	return total
	

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
			low.append((r, c))

basins = low.map(lambda x: size(*x)).sorted()
print(basins[-1] * basins[-2] * basins[-3])

