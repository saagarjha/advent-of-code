#!/usr/bin/env aoc_repl.py

from collections import Counter
import inspect
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

input = pathlib.Path(input_filename).read_text().strip()
x = 1
cycle = 0
total = 0
signal = 0
for instruction in input.split("\n"):
	old_x = x
	cycle, instruction
	if instruction == "noop":
		cycle += 1
		added = False
	else:
		cycle += 2
		x += int(instruction.split(" ")[1])
		added = True
	if (cycle + 20) // 40 > total:
		total += 1
		cycle, (total * 40 - 20) * (old_x if added else x), x, old_x
		signal += (total * 40 - 20) * (old_x if added else x)

signal
