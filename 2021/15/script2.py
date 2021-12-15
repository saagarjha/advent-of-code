#!/usr/bin/env python3

from collections import Counter
import heapq
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
map = input.split("\n").map(_0.map.__(int))

print(map)
map.map(_0.str_join.__()).str_join("\n")

big_map = [[0] * map[0].len * 5 for _ in range(map.len * 5)]

for r in map.indices():
	for c in map[r].indices():
		for i in range(0, 5):
			for j in range(0, 5):
				# print(r, c)
				# print(r + (i * map.len), c + (j * map[0].len))
				big_map[r + (i * map.len)][c + (j * map[0].len)] = map[r][c] + i + j
				while big_map[r + (i * map.len)][c + (j * map[0].len)] > 9:
					big_map[r + (i * map.len)][c + (j * map[0].len)] -= 9

big_map.map(_0.str_join.__()).str_join("\n")
map = big_map

risk = [[10000000000000] * map[i].len for i in range(map.len)]

risk[0][0] = 0
risk = Matrix(risk)
map = Matrix(map)

remaining = [(risk[0, 0], (0, 0))]
while len(remaining):
	last = heapq.heappop(remaining)[1]
	# print(last)
	# last = remaining.pop()[1]
	for neighbor in map.neighbors4(*last):
		# print(neighbor)
		if risk[neighbor[0], neighbor[1]] > risk[last[0], last[1]] + map[neighbor[0], neighbor[1]]:
			risk[neighbor[0], neighbor[1]] = risk[last[0], last[1]] + map[neighbor[0], neighbor[1]]
			heapq.heappush(remaining, (risk[neighbor[0], neighbor[1]], neighbor))

print(risk[risk.rows - 1, risk.columns - 1])
