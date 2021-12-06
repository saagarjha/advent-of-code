#!/usr/bin/env python3

import pathlib

import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0, os.path.dirname(os.path.dirname(currentdir)))

from aoc import *

input_filename = "input"
if "AOC_SAMPLE" in os.environ:
	input_filename = "sample"

input = pathlib.Path(input_filename).read_text().strip()
fish = input.split(",").map(int)
for _ in range(80):
	new_fish = []
	for fish in fish:
		if fish == 0:
			new_fish.append(6)
			new_fish.append(8)
		else:
			new_fish.append(fish - 1)
	fish = new_fish
print(fish.len)
