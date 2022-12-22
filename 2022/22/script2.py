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

max_len = map.map(_0.len).max()

for i in range(map.len):
	map[i] = map[i] + " " * (max_len - map[i].len)

edges = {}

length = 4 if "AOC_SAMPLE" in os.environ else 50
def top_in(r, c):
	result = []
	for i in range(length):
		result += [(r, c + i, 1)]
	return result

def top_out(r, c):
	result = []
	for i in range(length):
		result += [(r - 1, c + i, 3)]
	return result

def bottom_in(r, c):
	result = []
	for i in range(length):
		result += [(r, c + i, 3)]
	return result

def bottom_out(r, c):
	result = []
	for i in range(length):
		result += [(r + 1, c + i, 1)]
	return result

def left_in(r, c):
	result = []
	for i in range(length):
		result += [(r + i, c, 0)]
	return result

def left_out(r, c):
	result = []
	for i in range(length):
		result += [(r + i, c - 1, 2)]
	return result

def right_in(r, c):
	result = []
	for i in range(length):
		result += [(r + i, c, 2)]
	return result

def right_out(r, c):
	result = []
	for i in range(length):
		result += [(r + i, c + 1, 0)]
	return result

if "AOC_SAMPLE" in os.environ:
	for (o, i) in zip(top_out(0, 8), top_in(4, 0).reversed()):
		edges[o] = i
	for (o, i) in zip(top_out(4, 0), top_in(0, 8).reversed()):
		edges[o] = i


	for (o, i) in zip(left_out(0, 8), top_in(4, 4)):
		edges[o] = i
	for (o, i) in zip(top_out(4, 4), left_in(0, 8)):
		edges[o] = i


	for (o, i) in zip(bottom_out(7, 0), bottom_in(12, 8).reversed()):
		edges[o] = i
	for (o, i) in zip(bottom_out(11, 8), bottom_in(7, 0).reversed()):
		edges[o] = i


	for (o, i) in zip(left_out(8, 8), bottom_in(7, 4).reversed()):
		edges[o] = i
	for (o, i) in zip(bottom_out(7, 4), left_in(8, 8).reversed()):
		edges[o] = i


	for (o, i) in zip(left_out(4, 0), bottom_in(11, 12).reversed()):
		edges[o] = i
	for (o, i) in zip(bottom_out(11, 12), left_in(4, 0).reversed()):
		edges[o] = i

	for (o, i) in zip(right_out(4, 11), top_in(8, 12).reversed()):
		edges[o] = i
	for (o, i) in zip(top_out(8, 12), right_in(4, 11).reversed()):
		edges[o] = i

	for (o, i) in zip(right_out(0, 11), right_in(8, 15).reversed()):
		edges[o] = i
	for (o, i) in zip(right_out(8, 15), right_in(0, 11).reversed()):
		edges[o] = i
else:
# 12
# 3
#45 
#6

	for (o, i) in zip(top_out(0, 50), left_in(150, 0)):
		edges[o] = i
	for (o, i) in zip(left_out(150, 0), top_in(0, 50)):
		edges[o] = i

	for (o, i) in zip(top_out(0, 100), bottom_in(199, 0)):
		edges[o] = i
	for (o, i) in zip(bottom_out(199, 0), top_in(0, 100)):
		edges[o] = i

	for (o, i) in zip(right_out(0, 149), right_in(100, 99).reversed()):
		edges[o] = i
	for (o, i) in zip(right_out(100, 99), right_in(0, 149).reversed()):
		edges[o] = i

	for (o, i) in zip(left_out(0, 50), left_in(100, 0).reversed()):
		edges[o] = i
	for (o, i) in zip(left_out(100, 0), left_in(0, 50).reversed()):
		edges[o] = i

	for (o, i) in zip(left_out(50, 50), top_in(100, 0)):
		edges[o] = i
	for (o, i) in zip(top_out(100, 0), left_in(50, 50)):
		edges[o] = i

	for (o, i) in zip(bottom_out(49, 100), right_in(50, 99)):
		edges[o] = i
	for (o, i) in zip(right_out(50, 99), bottom_in(49, 100)):
		edges[o] = i

	for (o, i) in zip(bottom_out(149, 50), right_in(150, 49)):
		edges[o] = i
	for (o, i) in zip(right_out(150, 49), bottom_in(149, 50)):
		edges[o] = i


for r in sj_irange(-1, map.len):
	for c in sj_irange(-1, map[0].len):
		# if r == 5 and c == 12:
		# 	print("*", end="")
		# 	continue
		found = False
		for i in range(0, 4):
			if (r, c, i) in edges:
				print(edges[(r, c, i)][2], end="")
				found = True
				break
		if not found:
			if r >= 0 and r < map.len and c >= 0 and c < map[0].len:
				print(map[r][c], end="")
			else:
				print("*", end="")
	print()

def last_index_by(list, predicate):
	for i in sj_range(0, list.len).reversed():
		if predicate(list[i]):
			return i
	return None

r = 0
c = map[0].first_index_by(_0 == ".")
direction = 0

# r = 148
# c = 91
# direction = 0
# moves = [9]

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
			new_direction = direction
			if new_r >= map.len or new_r < 0 or new_c >= map[r].len or new_c < 0 or map[new_r][new_c] == " ":
				(new_r, new_c, new_direction) = edges[(new_r, new_c, direction)]
			if map[new_r][new_c] == "#":
				continue
			else:
				r = new_r
				c = new_c
				direction = new_direction
	directions = [">", "v", "<", "^"]
	# for i in range(map.len):
	# 	for j in range(map[i].len):
	# 		if i == r and j == c:
	# 			print(directions[direction], end="")
	# 		else:
	# 			print(map[i][j], end="")
	# 	print()
	# print()

r, c, direction

(r + 1) * 1000 + 4 * (c + 1) + direction
