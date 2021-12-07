#!/usr/bin/env python3

import pathlib

from collections import Counter
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
numbers = input.split(",").map(int)
min = numbers.min()
max = numbers.max()
sum = 0
low_sum = 1111111111
low_i = -1
for i in sj_irange(min, max):
	sum = 0
	for crab in numbers:
		sum += abs(i - crab)
	if sum < low_sum:
		low_i = i
		low_sum = sum
print(low_sum)
