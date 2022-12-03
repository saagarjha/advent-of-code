#!/usr/bin/env python3

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
rucksacks = input.split("\n")
rucksacks
sum = 0
for rucksack in rucksacks:
	part1 = rucksack[:rucksack.len // 2]
	part2 = rucksack[rucksack.len // 2:]
	c = list(set(part1).intersection(set(part2)))[0]
	if c.lower() == c:
		sum += ord(c) - ord('a') + 1
	else:
		sum += ord(c.upper()) - ord('A') + 26 + 1

sum

