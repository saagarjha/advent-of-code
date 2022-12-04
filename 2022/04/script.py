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
assignments = []
for line in input.split("\n"):
	assignments.append(line.split(",").map(`<_0.split("-").map(int)`>))

sum = 0
for assignment in assignments:
	(a, b) = (assignment[0], assignment[1])
	if (a[0] <= b[0] and a[1] >= b[1]) or (b[0] <= a[0] and b[1] >= a[1]):
		sum += 1
sum
