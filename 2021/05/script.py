#!/usr/bin/env python3

import pathlib

import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0, os.path.dirname(os.path.dirname(currentdir)))

from aoc import *

input = pathlib.Path("input").read_text().strip()
strings = input.split("\n")
lines = []
for string in strings:
	(p1, p2) = string.split("->")
	line = (p1.split(",").map(int), p2.split(",").map(int))
	lines.append(line)

matrix = [[0] * 1000 for _ in range(1000)]
for line in lines:
	if line[0][0] == line[1][0]:
		print("h", line)
		start = line[0][1]
		end = line[1][1]
		if end < start:
			(start, end) = (end, start)
		for i in range(start, end + 1):
			print(line[0][0], i)
			matrix[line[0][0]][i] += 1
	if line[0][1] == line[1][1]:
		print("v", line)
		start = line[0][0]
		end = line[1][0]
		if end < start:
			(start, end) = (end, start)
		for i in range(start, end + 1):
			matrix[i][line[0][1]] += 1

count = 0
for r in matrix:
	for c in r:
		if c >= 2:
			count += 1
print(matrix.map(str).str_join("\n"))
print(count)
