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
fish = input.split(",").map(int)
fish = Counter(fish)
print(fish)
for _ in range(256):
	fish6 = fish[0]
	fish8 = fish[0]
	for i in sj_irange(1, 8):
		fish[i - 1] = fish[i]
	fish[6] += fish6
	fish[8] = fish8
	for i in sj_irange(0, 8):
		print(fish[i])
	print()
sum = 0
for i in fish:
	sum += fish[i]
print(sum)
# print(fish.len)
