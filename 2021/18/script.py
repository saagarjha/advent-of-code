#!/usr/bin/env python3

from collections import Counter
import math
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

def add(n1, n2):
	return [n1, n2]

def find_explode(n):
	depth = 0
	path = []
	index = 0
	last_regular = None
	exploding = None
	skip_one = False
	while True:
		if isinstance(n[index], list):
			path += [(n, index)]
			depth += 1
			if depth >= 4:
				if not exploding and isinstance(n[index], list) and isinstance(n[index][0], int) and isinstance(n[index][1], int):
					exploding = n[index]
					# print("found", exploding)
					if last_regular:
						# print(last_regular[0][last_regular])
						last_regular[0][last_regular[1]] += exploding[0]
					n[index] = 0
					skip_one = True
					continue
			n = n[index]
			index = 0
		else:
			# print(n)
			# print(n[index])
			last_regular = (n, index)
			if exploding and not skip_one:
				print("right", n, index)
				n[index] += exploding[1]
				return True
			skip_one = False
			index += 1
			while index >= n.len:
				if not path.len:
					return False
				(n, index) = path.pop()
				depth -= 1
				index += 1

def find_split(n):
	depth = 0
	path = []
	index = 0
	last_regular = None
	exploding = None
	skip_one = False
	while True:
		if isinstance(n[index], list):
			path += [(n, index)]
			n = n[index]
			index = 0
		else:
			# print(n[index])
			if n[index] >= 10:
				number = n[index]
				n[index] = [math.floor(number / 2), math.ceil(number / 2)]
				return True
			index += 1
			while index >= n.len:
				if not path.len:
					return False
				(n, index) = path.pop()
				index += 1


def reduce(n):
	while True:
		if find_explode(n):
			continue
		if find_split(n):
			print("split", n)
			continue
		else:
			break


def magnitude(n):
	if isinstance(n[0], list):
		left = magnitude(n[0])
	else:
		left = n[0]
	if isinstance(n[1], list):
		right = magnitude(n[1])
	else:
		right = n[1]
	return 3 * left + 2 * right

input = pathlib.Path(input_filename).read_text().strip()
numbers = input.split("\n").map(eval)
sum = numbers[0]
for number in numbers[1:]:
	sum = add(sum, number)
	print(sum)
	reduce(sum)
	print("reduce")
	print(sum)
# numbers.str_join("\n")
# n = eval('[10, 10]')
# find_split(n)
# find_explode(n)
magnitude(sum)

