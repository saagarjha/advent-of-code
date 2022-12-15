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

bound = 4000000

for row in range(0, bound):
	row
	inside = [False for _ in range(sensors.len)]
	stops = []
	for i in range(sensors.len):
		s = sensors[i]
		vert = s[1] - abs(row - s[0][1])
		if vert < 0:
			continue
		stops.append((s[0][0] - vert, i, True))
		stops.append((s[0][0] + vert, i, False))
	stops += [(0,), (bound,)]
	stops = stops.sorted(`<_0[0] < _1[0]`>)
	started = False
	last = -1
	for stop in stops:
		if stop == (0,):
			started = True
		elif stop == (bound,):
			started = False
		else:
			(position, index, start) = stop
			if started and inside.reduce(True, `<_0 and not _1`>) and abs(position - last) > 1:
				(position - 1) * 4000000 + row
				sys.exit()
			if start:
				inside[index] = True
			else:
				inside[index] = False
				last = position
