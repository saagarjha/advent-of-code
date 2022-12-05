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

input = pathlib.Path(input_filename).read_text()
input = input.split("\n\n")
stacks = input[0]
new_stacks = []
for stack in stacks.split("\n")[:-1]:
	new_stacks.append(stack.chunk(4).map(_0.str_join.__()).map(`<_0.replace("[", "").replace("]", "").replace(" ", "")`>))
moves = input[1].strip().split("\n")
stacks = new_stacks.transpose()
for r in range(0, stacks.len):
	for c in range(0, stacks[r].len):
		if not stacks[r][c].len:
			stacks[r][c] = None
	stacks[r] = stacks[r][::-1]

def do_move(stacks, source, dest):
	stacks[source] = stacks[source].filter(_0)
	stacks[dest].append(stacks[source].last)
	stacks[dest] = stacks[dest].filter(_0)
	stacks[source] = stacks[source][:-1]

for move in moves:
	(count, location) = move.split(" from ")
	count = int(count.replace("move ", ""))
	location = location.split(" to ").map(int)
	count, location
	for i in range(0, count):
		do_move(stacks, location[0] - 1, location[1] - 1)
		stacks.str_join("\n")

stacks.map(_0.last).str_join()
