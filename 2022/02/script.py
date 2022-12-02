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
rounds = input.split("\n").map(_0.split.__(" "))
total = 0
points = {
	"X": 1,
	"Y": 2,
	"Z": 3,
}

for round in rounds:
	total += points[round[1]]
	if round[0] == "A" and round[1] == "X":
		total += 3
	elif round[0] == "B" and round[1] == "Y":
		total += 3
	elif round[0] == "C" and round[1] == "Z":
		total += 3
	elif round[0] == "A" and round[1] == "Y":
		total += 6
	elif round[0] == "B" and round[1] == "Z":
		total += 6
	elif round[0] == "C" and round[1] == "X":
		total += 6
total
