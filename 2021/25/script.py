#!/usr/bin/env python3

from collections import Counter
import os
import pathlib
import sys
import inspect
import copy

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0, os.path.dirname(os.path.dirname(currentdir)))

from aoc import *

input_filename = "input"
if "AOC_SAMPLE" in os.environ:
	input_filename = "sample"

input = pathlib.Path(input_filename).read_text().strip()
seafloor = input.split("\n").map(_0.map.__(_0))

step = 0
while True:
	# print(seafloor.map(_0.str_join.__()).str_join("\n"))
	seafloor_copy = copy.deepcopy(seafloor)
	old_seafloor = copy.deepcopy(seafloor)
	for r in seafloor.indices():
		for c in seafloor[r].indices():
			if seafloor[r][c] == ">":
				if seafloor[r][(c + 1) % seafloor[r].len] == ".":
					seafloor_copy[r][c] = "."
					seafloor_copy[r][(c + 1) % seafloor[r].len] = ">"
	seafloor = copy.deepcopy(seafloor_copy)
	for r in seafloor.indices():
		for c in seafloor[r].indices():
			if seafloor[r][c] == "v":
				if seafloor[(r + 1) % seafloor.len][c] == ".":
					seafloor_copy[r][c] = "."
					seafloor_copy[(r + 1) % seafloor.len][c] = "v"
	step += 1
	# print()
	seafloor = copy.deepcopy(seafloor_copy)
	if seafloor == old_seafloor:
		print(step)
		break

