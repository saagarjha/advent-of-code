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

def print_sprite():
	global total
	if x in range(cycle % 40 - 2, cycle % 40 - 2 + 3):
		print("#", end="")
	else:
		print(".", end="")
	if (cycle) // 40 > total:
		total += 1
		print()


for instruction in input.split("\n"):
	if instruction == "noop":
		cycle += 1
		print_sprite()
	else:
		cycle += 1
		print_sprite()
		cycle += 1
		print_sprite()
		x += int(instruction.split(" ")[1])
