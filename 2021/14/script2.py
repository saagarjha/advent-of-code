#!/usr/bin/env python3

from collections import defaultdict
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

mapping = dict(insertions)

counts = {}
for insertion in insertions.map(_0[0]):
	counts[insertion] = 0

for pair in polymer.window(2).map(_0[0] + _0[1]):
	counts[pair] += 1

new_counts = counts.copy()
for i in range(40):
	# print(characters)
	# print(counts)
	for count in new_counts:
		new_counts[count] = 0
	for count in counts:
		new1 = count[0] + mapping[count]
		new2 = mapping[count] + count[1]
		new_counts[new1] += counts[count]
		new_counts[new2] += counts[count]
	# print(new_counts)
	# print()
	print(counts)
	counts = new_counts.copy()

characters = defaultdict(int)
for count in counts:
	characters[count[0]] += counts[count]
	characters[count[1]] += counts[count]
characters[polymer[0]] += 1
characters[polymer[-1]] += 1
for character in characters:
	characters[character] //= 2
counts = []
for character in characters:
	counts.append(characters[character])
counts.sort()
print(counts[-1] - counts[0])

