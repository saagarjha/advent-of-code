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

input = pathlib.Path(input_filename).read_text()
lines = input.split("\n")
map = lines[:-3]
all_moves = lines[-2]
moves = []
for move in all_moves.chunk_by(`<(_0 in "0123456789") == (_1 in "0123456789")`>):
	move = move.str_join()
	try:
		moves.append(int(move))
	except:
		moves.append(move)

# moves
# map.str_join("\n")

r = 0
c = map[0].first_index_by(_0 == ".")
direction = 0

max_len = map.map(_0.len).max()

for i in range(map.len):
	map[i] = map[i] + " " * (max_len - map[i].len)

map_transposed = map.transpose()

def last_index_by(list, predicate):
	for i in sj_range(0, list.len).reversed():
		if predicate(list[i]):
			return i
	return None

for move in moves:
	if move == "R":
		direction += 1
		if direction >= 4:
			direction -= 4
	elif move == "L":
		direction -= 1
		if direction < 0:
			direction += 4
	else:
		for i in range(move):
			if direction == 0:
				new_r = 0
				new_c = 1
			elif direction == 1:
				new_r = 1
				new_c = 0
			elif direction == 2:
				new_r = 0
				new_c = -1
			elif direction == 3:
				new_r = -1
				new_c = 0
			new_r, new_c = r + new_r, c + new_c
			# if direction == 2:
			# 	print(new_r + 1, new_c + 1, map[r][new_c])
			# print(new_r, new_c)
			if new_r >= map.len or (map[new_r][c] == " " and direction == 1):
				new_r = map_transposed[c].first_index_by(_0 != " ")
			elif new_r < 0 or (map[new_r][c] == " " and direction == 3):
				new_r = last_index_by(map_transposed[c], (_0 != " "))
			elif new_c >= map[r].len or (map[r][new_c] == " " and direction == 0):
				new_c = map[r].first_index_by(_0 != " ")
			elif new_c < 0 or (map[r][new_c] == " " and direction == 2):
				new_c = last_index_by(map[r], (_0 != " "))
			if map[new_r][new_c] == "#":
				continue
			else:
				r = new_r
				c = new_c
	directions = [">", "v", "<", "^"]
	# for i in range(map.len):
	# 	for j in range(map[i].len):
	# 		if i == r and j == c:
	# 			print(directions[direction], end="")
	# 		else:
	# 			print(map[i][j], end="")
	# 	print()
	# print()
	# move, r + 1, c + 1, direction

r, c, direction

(r + 1) * 1000 + 4 * (c + 1) + direction
