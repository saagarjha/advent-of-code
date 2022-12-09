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

head = [0, 0]
tail = [0, 0]

positions = {(0, 0)}

def neighbors8(r, c):
	neighbors = []
	for row in sj_irange(r - 1, r + 1):
		for column in sj_irange(c - 1, c + 1):
			if (row != r or column != c):
				neighbors.append((row, column))
	return neighbors

def move(direction):
	if direction == "U":
		head[0] -= 1
	elif direction == "D":
		head[0] += 1
	elif direction == "L":
		head[1] -= 1
	elif direction == "R":
		head[1] += 1
	if not neighbors8(*head).filter(_0 == tuple(tail)).first:
		if head[0] - tail[0] == 2:
			tail[0] += 1
			if head[1] != tail[1]:
				tail[1] = head[1]
		elif head[0] - tail[0] == -2:
			tail[0] -= 1
			if head[1] != tail[1]:
				tail[1] = head[1]
		elif head[1] - tail[1] == 2:
			tail[1] += 1
			if head[0] != tail[0]:
				tail[0] = head[0]
		elif head[1] - tail[1] == -2:
			tail[1] -= 1
			if head[0] != tail[0]:
				tail[0] = head[0]
	head, tail

for m in input.split("\n"):
	(direction, distance) = m.split(" ")
	for i in range(0, int(distance)):
		move(direction)
		positions.add(tuple(tail))

positions.len
