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
	steps.append((split[1].split(",").map(_0[2:].split.__("..").map.__(int)), split[0] == "on"))

def intersection_bound(bound1, bound2):
	return (max(bound1[0], bound2[0]), min(bound1[1], bound2[1]))

def intersection(region1, region2):
	# print("asdf", region1,  "asdf", region2)
	if region1[0][1] < region2[0][0] or region2[0][1] < region1[0][0]:
		return None
	if region1[1][1] < region2[1][0] or region2[1][1] < region1[1][0]:
		return None
	if region1[2][1] < region2[2][0] or region2[2][1] < region1[2][0]:
		return None

	return [
		intersection_bound(region1[0], region2[0]),
		intersection_bound(region1[1], region2[1]),
		intersection_bound(region1[2], region2[2]),
	]

def size(region):
	return (region[0][1] - region[0][0] + 1) * (region[1][1] - region[1][0] + 1) * (region[2][1] - region[2][0] + 1)

regions = [
	([[-10000000, 10000000], [-10000000, 10000000], [-10000000, 10000000]], False),
]

for step in steps:
	print(step, regions.len)
	new_regions = []
	for region in regions:
		joined = intersection(region[0], step[0])
		if step[1] == region[1] or not joined:
			new_regions.append(region)
		else:
			temp_regions = []
			if joined[0][0] - 1 >= region[0][0][0]:
				temp_regions.append(([[region[0][0][0], joined[0][0] - 1], region[0][1], region[0][2]], region[1]))
			if region[0][0][1] >= joined[0][1] + 1:
				temp_regions.append(([[joined[0][1] + 1, region[0][0][1]], region[0][1], region[0][2]], region[1]))
			if joined[1][0] - 1 >= region[0][1][0]:
				temp_regions.append(([joined[0], [region[0][1][0], joined[1][0] - 1], region[0][2]], region[1]))
			if region[0][1][1] >= joined[1][1] + 1:
				temp_regions.append(([joined[0], [joined[1][1] + 1, region[0][1][1]], region[0][2]], region[1]))
			if joined[2][0] - 1 >= region[0][2][0]:
				temp_regions.append(([joined[0], joined[1], [region[0][2][0], joined[2][0] - 1]], region[1]))
			if region[0][2][1] >= joined[2][1] + 1:
				temp_regions.append(([joined[0], joined[1], [joined[2][1] + 1, region[0][2][1]]], region[1]))
			new_regions += temp_regions
			new_regions.append((joined, step[1]))
	regions = new_regions

sum = 0
for region in regions:
	if region[1]:
		sum += size(region[0])
sum
