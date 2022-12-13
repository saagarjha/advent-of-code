#!/usr/bin/env aoc_repl.py

from collections import Counter
import inspect
import operator
import os
import pathlib
import sys
import itertools

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0, os.path.dirname(os.path.dirname(currentdir)))

from aoc import *

input_filename = "input"
if "AOC_SAMPLE" in os.environ:
	input_filename = "sample"

input = pathlib.Path(input_filename).read_text().strip()
packets = input.split("\n\n").map(`<_0.split("\n")`>)

def compare(packet1, packet2):
	packet1, " vs ", packet2
	if isinstance(packet1, int) and isinstance(packet2, int):
		return packet2 - packet1
	elif isinstance(packet1, list) and isinstance(packet2, list):
		for l, r in itertools.zip_longest(packet1, packet2):
			if l == None:
				return 1
			elif r == None:
				return -1
			value = compare(l, r)
			if value != 0:
				return value

	elif isinstance(packet1, int):
		return compare([packet1], packet2)
	elif isinstance(packet2, int):
		return compare(packet1, [packet2])

	return 0

count = 0
for i in range(packets.len):
	p = packets[i]
	packet1 = eval(p[0])
	packet2 = eval(p[1])
	v = compare(packet1, packet2)
	if v > 0:
		count += i + 1
	print(i + 1, v)
	print()

count
