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
for line in lines:
	for c in line:
		if c == "(" or c == "[" or c == "{" or c == "<":
			stack.append(c)
		if c == "]":
			if stack[-1] == "[":
				stack = stack[:-1]
			else:
				score += 57
				break
		if c == "}":
			if stack[-1] == "{":
				stack = stack[:-1]
			else:
				score += 1197
				break
		if c == ")":
			if stack[-1] == "(":
				stack = stack[:-1]
			else:
				score += 3
				break
		if c == ">":
			if stack[-1] == "<":
				stack = stack[:-1]
			else:
				score += 25137
				break
print(score)
