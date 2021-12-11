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
octopi = input.split("\n").map(lambda x: x.map(int))
print(octopi.map(lambda x: x.map(str).str_join("")).str_join("\n"))
print()

def neighbors(r, c):
	neighbors = []
	if r - 1 >= 0:
		neighbors += [(r - 1, c)]
		if c - 1 >= 0:
			neighbors += [(r - 1, c - 1)]
		if c + 1 < octopi.len:
			neighbors += [(r - 1, c + 1)]
	if c - 1 >= 0:
		neighbors += [(r, c - 1)]
	if c + 1 < octopi.len:
		neighbors += [(r, c + 1)]
	if r + 1 < octopi.len:
		neighbors += [(r + 1, c)]
		if c - 1 >= 0:
			neighbors += [(r + 1, c - 1)]
		if c + 1 < octopi.len:
			neighbors += [(r + 1, c + 1)]
	return neighbors

total = 0
for _ in range(100):
	for r in octopi.indices():
		for c in octopi[r].indices():
			octopi[r][c] += 1

	while True:
		flashes = []
		for r in octopi.indices():
			for c in octopi[r].indices():
				if octopi[r][c] > 9:
					flashes.append((r, c))
					total += 1
		if not flashes.len:
			break
		for flash in flashes:
			for n in neighbors(*flash):
				# print(n)
				octopi[n[0]][n[1]] += 1
			octopi[flash[0]][flash[1]] = -100000
		# print(flashes)
		flashes = []

	for r in octopi.indices():
		for c in octopi[r].indices():
			if octopi[r][c] < -10000:
				octopi[r][c] = 0
	print(octopi.map(lambda x: x.map(str).str_join("")).str_join("\n"))
	print("asdf")
print(total)
