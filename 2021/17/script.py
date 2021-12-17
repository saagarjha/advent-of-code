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
input = input["target area: ".len:]
(a, b) = input.split(", ")
(x1, x2) = a[2:].split("..").map(int)
(y1, y2) = b[2:].split("..").map(int)

good = []
# for vel_x in range(0, 100):
# 	for vel_y in range(0, 100):
for vel_x in range(0, 100):
	for vel_y in range(0, 1000):
		x = 0
		y = 0
		vel_xx = vel_x
		vel_yy = vel_y
		highest = -1000000000
		# print(vel_x, vel_y)
		for step in range(0, 1000):
			# print(x, y)
			x += vel_xx
			y += vel_yy
			highest = max(y, highest)
			# print(x1, x2, y1, y2)
			if x1 <= x <= x2 and y1 <= y <= y2:
				good.append(highest)
			vel_xx = max(vel_xx - 1, 0)
			if vel_xx == 0 and not (x1 <= x <= x2):
				break
			vel_yy -= 1
good.sort()
good[-1]
