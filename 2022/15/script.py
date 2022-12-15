#!/usr/bin/env aoc_repl.py

from collections import Counter, deque
import heapq
import inspect
import itertools
import operator
import os
import pathlib
import sys

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0, os.path.dirname(os.path.dirname(currentdir)))

from aoc import *

input_filename = "input"
if "AOC_SAMPLE" in os.environ:
	input_filename = "sample"

def distance(p1, p2):
	return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

input = pathlib.Path(input_filename).read_text().strip()

sensors = []
beacons = []

for line in input.split("\n"):
	(sensor, beacon) = line.split(": ")
	sensor = sensor.replace("Sensor at ", "").replace("x=", "").replace(" y=","").split(",").map(int)
	beacon = beacon.replace("closest beacon is at ", "").replace("x=", "").replace(" y=","").split(",").map(int)
	sensors.append((sensor, distance(sensor, beacon)))
	beacons.append(beacon)

# sensors

row = 2000000

points = set()
for s in sensors:
	vert = s[1] - abs(row - s[0][1])
	if vert < 0:
		continue
	# s[0], sj_irange(s[0][0] - vert, s[0][0] + vert), vert
	for i in sj_irange(s[0][0] - vert, s[0][0] + vert):
		if not [i, row] in beacons:
			points.add(i)
list(points).sorted().len
