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
numbers = input.split("\n").map(`<_0.map(int)`>)
numbers
count = 0
max_score = 0
for r in range(0, numbers.len):
	for c in range(0, numbers[r].len):
		score1 = 0
		score2 = 0
		score3 = 0
		score4 = 0
		for r2 in sj_range(r - 1, -1):
			if numbers[r2][c] >= numbers[r][c]:
				score1 += 1
				break
			score1 += 1
		for r2 in sj_range(r + 1, numbers.len):
			if numbers[r2][c] >= numbers[r][c]:
				score2 += 1
				break
			score2 += 1
		for c2 in sj_range(c - 1, -1):
			if numbers[r][c2] >= numbers[r][c]:
				score3 += 1
				break
			score3 += 1
		for c2 in sj_range(c + 1, numbers[r].len):
			if numbers[r][c2] >= numbers[r][c]:
				score4 += 1
				break
			score4 += 1
		score = score1 * score2 * score3 * score4
		r, c, score1, score2, score3, score4, score
		max_score = max(score, max_score)
max_score
