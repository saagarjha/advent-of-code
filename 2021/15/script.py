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
map = input.split("\n").map(_0.map.__(int))

print(map)
map.map(_0.str_join.__()).str_join("\n")

risk = [[0] * map[i].len for i in range(map.len)]

risk[-1][-1] = map[-1][-1]

for c in range(map[0].len - 1)[::-1]:
	risk[-1][c] = map[-1][c] + risk[-1][c + 1]

for r in range(map.len - 1)[::-1]:
	risk[r][-1] = map[r][-1] + risk[r + 1][-1]

for r in range(map.len - 1)[::-1]:
	for c in range(map[0].len - 1)[::-1]:
		risk[r][c] = min(risk[r + 1][c], risk[r][c + 1]) + map[r][c]

risk.map(_0.str_join.__(" ")).str_join("\n")

risk[0][0] - map[0][0]
