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
map = input.split("\n")
map = ["." * map.len] * 20 + map + ["." * map.len] * 20
map = map.map(`<list("." * 20 + _0 + "." * 20)`>)

options = [0, 1, 2, 3]

class Elf:
	def __init__(self):
		pass

	def consider(self, grid, r, c):
		all_neighbors = [(-1, -1), (-1, 0), (-1, 1)] +  [(1, -1), (1, 0), (1, 1)] + [(-1, -1), (0, -1), (1, -1)] + [(-1, 1), (0, 1), (1, 1)]
		if all_neighbors.map(`<grid[r + _0[0]][c + _0[1]]`>).first_index_by(_0 == "#") == None:
			return (r, c)

		for option in options:
			if option == 0:
				neighbors = [(-1, -1), (-1, 0), (-1, 1)]
				new = (-1, 0)
			elif option == 1:
				neighbors = [(1, -1), (1, 0), (1, 1)]
				new = (1, 0)
			elif option == 2:
				neighbors = [(-1, -1), (0, -1), (1, -1)]
				new = (0, -1)
			elif option == 3:
				neighbors = [(-1, 1), (0, 1), (1, 1)]
				new = (0, 1)
			else:
				pass
			if self.check_neighbors(grid, r, c, neighbors):
				# _ = self.options.pop(self.options.first_index_of(option))
				# self.options.append(option)
				return (r + new[0], c + new[1])
		return (r, c)

	def check_neighbors(self, grid, r, c, neighbors):
		for neighbor in neighbors:
			if grid[r + neighbor[0]][c + neighbor[1]] == "#":
				return False
		return True

elves = {}
for r in range(map.len):
	for c in range(map[r].len):
		if map[r][c] == "#":
			elves[Elf()] = (r, c)

# elvee
for i in range(10):
	counts = Counter()
	moves = {}
	for elf in elves:
		new = elf.consider(map, *elves[elf])
		# elves[elf], new
		moves[elf] = new
		counts[new] += 1
	final = {}
	for move in moves:
		if counts[moves[move]] > 1:
			final[move] = elves[move]
		else:
			final[move] = moves[move]
	elves = final
	positions = set(final.map(`<final[_0]`>))
	for r in range(map.len):
		for c in range(map[r].len):
			map[r][c] = "#" if (r, c) in positions else "."
	# for r in range(18, map.len - 18):
	# 	for c in range(18, map.len - 18):
	# 		print(map[r][c], end="")
	# 	print()
	# print()
	options = options[1:] + [options[0]]

for r in range(0, map.len):
	for c in range(0, map.len):
		print(map[r][c], end="")
	print()
print()

positions = elves.map(`<elves[_0]`>)
(positions.map(_0[0]).max() - positions.map(_0[0]).min() + 1) * (positions.map(_0[1]).max() - positions.map(_0[1]).min() + 1) - positions.len

