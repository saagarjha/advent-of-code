#!/usr/bin/env python3

from collections import Counter
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
lines = input.split("\n")
print(lines)
stack = []
score = 0
incomplete = []
for line in lines:
	add = True
	for c in line:
		if c == "(" or c == "[" or c == "{" or c == "<":
			stack.append(c)
		if c == "]":
			if stack[-1] == "[":
				stack = stack[:-1]
			else:
				score += 57
				add = False
				break
		if c == "}":
			if stack[-1] == "{":
				stack = stack[:-1]
			else:
				score += 1197
				add = False
				break
		if c == ")":
			if stack[-1] == "(":
				stack = stack[:-1]
			else:
				score += 3
				add = False
				break
		if c == ">":
			if stack[-1] == "<":
				stack = stack[:-1]
			else:
				score += 25137
				add = False
				break
	if add:
		incomplete.append(stack)
	stack = []
scores = []
for inc in incomplete:
	score = 0
	print(inc[::-1])
	for c in inc[::-1]:
		if c == "(":
			score *= 5
			score += 1
		if c == "[":
			score *= 5
			score += 2
		if c == "{":
			score *= 5
			score += 3
		if c == "<":
			score *= 5
			score += 4
	scores.append(score)
scores.sort()
print(scores)
print(scores[scores.len // 2])
