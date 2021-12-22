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
steps_str = input.split("\n")
steps = []
for line in steps_str:
	split = line.split(" ")
	steps.append((split[0], split[1].split(",").map(_0[2:].split.__("..").map.__(int))))

reactor = {}
for x in sj_irange(-50, 50):
	for y in sj_irange(-50, 50):
		for z in sj_irange(-50, 50):
			reactor[(x, y, z)] = 0

def bounded(low, high):
	return range(max(low, -50), min(high, 50) + 1)

for step in steps:
	print(step)
	for x in bounded(step[1][0][0], step[1][0][1]):
		for y in bounded(step[1][1][0], step[1][1][1]):
			for z in bounded(step[1][2][0], step[1][2][1]):
				if step[0] == "on":
					reactor[(x, y, z)] = 1
				else:
					reactor[(x, y, z)] = 0

count = 0
for x in sj_irange(-50, 50):
	for y in sj_irange(-50, 50):
		for z in sj_irange(-50, 50):
			if reactor[(x, y, z)]:
				count += 1
count
