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
numbers = input.split("\n").map(`<_0.map(int)`>)
numbers
count = 0
for r in range(0, numbers.len):
	for c in range(0, numbers[r].len):
		visible1 = True
		visible2 = True
		visible3 = True
		visible4 = True
		for r2 in sj_range(0, r):
			if numbers[r2][c] >= numbers[r][c]:
				visible1 = False
		for r2 in sj_range(r + 1, numbers.len):
			if numbers[r2][c] >= numbers[r][c]:
				visible2 = False
		for c2 in sj_range(0, c):
			if numbers[r][c2] >= numbers[r][c]:
				visible3 = False
		for c2 in sj_range(c + 1, numbers[r].len):
			if numbers[r][c2] >= numbers[r][c]:
				visible4 = False
		if any([visible1, visible2, visible3, visible4]):
			count += 1
			# r, c
count
