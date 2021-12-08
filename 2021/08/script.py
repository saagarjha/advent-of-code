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
numbers = input.split("\n").map(lambda x: x.split("|")[1].split()).flatten()
print(numbers)
sum = 0
for n in numbers:
	if n.len == 3 or n.len == 4 or n.len == 2 or n.len == 7:
		sum += 1
print(sum)
