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

rope = [[0, 0] for _ in range(0, 10)]

positions = {(0, 0)}

def neighbors8(r, c):
	neighbors = []
	for row in sj_irange(r - 1, r + 1):
		for column in sj_irange(c - 1, c + 1):
			# if (row != r or column != c):
			neighbors.append((row, column))
	return neighbors

def move(direction, head):
	if direction == "U":
		head[0] -= 1
	elif direction == "D":
		head[0] += 1
	elif direction == "L":
		head[1] -= 1
	elif direction == "R":
		head[1] += 1

fixes = {
	(-2, -2): (-1, -1),
	(-2, -1): (-1, 0),
	(-2, 0): (-1, 0),
	(-2, 1): (-1, 0),
	(-2, 2): (-1, 1),

	(-1, -2): (0, -1),
	(-1, 2): (0, 1),

	(0, -2): (0, -1),
	(0, 2): (0, 1),

	(1, -2): (0, -1),
	(1, 2): (0, 1),

	(2, -2): (1, -1),
	(2, -1): (1, 0),
	(2, 0): (1, 0),
	(2, 1): (1, 0),
	(2, 2): (1, 1),
}

def fix(head, tail):
	diff = (tail[0] - head[0], tail[1] - head[1])
	if diff in fixes:
		tail[0] = head[0] + fixes[diff][0]
		tail[1] = head[1] + fixes[diff][1]
	# 	return True
	# else:
	# 	return False

for m in input.split("\n"):
	(direction, distance) = m.split(" ")
	for i in range(0, int(distance)):
		move(direction, rope[0])
		direction, rope[0]
		for i in range(0, rope.len - 1):
			fix(rope[i], rope[i + 1])
		positions.add(tuple(rope[-1]))
	# for r in range(-15, 15):
	# 	for c in range(-15, 15):
	# 		last = rope.first_index_by(_0 == [r, c])
	# 		if last != None:
	# 			print(last, end="")
	# 		else:
	# 			print("*", end="")
	# 	print()
	# print()


positions.len

for r in range(-15, 15):
	for c in range(-15, 15):
		print("*" if (r, c) in positions else " ", end="")
	print()
