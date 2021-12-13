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

def print_grid(points):
	points = set(points)
	for c in range(15):
		for r in range(15):
			if (r, c) in points:
				print("#", end="")
			else:
				print(".", end="")
		print()

input = pathlib.Path(input_filename).read_text().strip()
(points, folds_str) = input.split("\n\n")
points = points.split("\n").map(_0.split.__(",")).map(lambda x: (int(x[0]), int(x[1])))
folds = []
for f in folds_str.split("\n"):
	if f.startswith("fold along y="):
		folds.append(("y", int(f["fold along y=".len:])))
	else:
		folds.append(("x", int(f["fold along x=".len:])))
print(points, folds)

print_grid(points)

for fold in [folds[0]]:
	if fold[0] == "x":
		for i in points.indices():
			if points[i][0] > fold[1]:
				points[i] = (fold[1] - (points[i][0] - fold[1]), points[i][1])
		points = points.filter(_0[0] != fold[1])
	else:
		for i in points.indices():
			if points[i][1] > fold[1]:
				points[i] = (points[i][0], fold[1] - (points[i][1] - fold[1]))
		points = points.filter(_0[1] != fold[1])
	print("asdf")
	print_grid(points)
print(set(points).len)
# print(points)
# print("Asdf")

