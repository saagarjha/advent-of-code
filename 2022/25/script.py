#!/usr/bin/env aoc_repl.py

from collections import Counter, defaultdict, deque
import heapq
import inspect
import itertools
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

lookup = {
	"0": 0,
	"1": 1,
	"2": 2,
	"-": -1,
	"=": -2,
}
reverse_lookup = {
	0: "0",
	1: "1",
	2: "2",
	-1: "-",
	-2: "=",
}

def decimal(number):
	reversed = number.reversed()
	value = 0
	for i in range(reversed.len):
		# reversed[i], 5 ** i
		value += (5 ** i) * lookup[reversed[i]]
	return value

sum = 0
for line in input.split("\n"):
	sum += decimal(line.map(_0))

digits = []
while sum > 0:
	remainder = sum % 5
	sum, remainder
	sum //= 5
	if remainder > 2:
		remainder = (remainder - 5)
		sum += 1
	digits.append(remainder)

for digit in digits.reversed():
	print(reverse_lookup[digit], end="")
