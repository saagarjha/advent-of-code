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
lines = input.split("\n")
polymer = lines[0]

insertions = []
for line in lines[2:]:
	insertions.append(line.split(" -> "))

insertions
new_polymer = ""
for _ in range(10):
	new_polymer = ""
	print(polymer.len)
	for pair in polymer.window(2):
		found = None
		for insertion in insertions:
			if pair[0] + pair[1] == insertion[0][0] + insertion[0][1]:
				found = pair[0] + insertion[1]
				break
		new_polymer += found if found else pair[0] + pair[1]
	polymer = new_polymer + (pair[1] if found else "")
counts = Counter(polymer)
ns = []
for i in counts:
	ns.append(counts[i])
counts
ns.sort()
print(ns[-1] - ns[0])
# print(new_polymer)
