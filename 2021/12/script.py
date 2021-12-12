#!/usr/bin/env python3

from collections import Counter
from collections import defaultdict
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
paths = input.split("\n")
edges = defaultdict(set)
for path in paths:
	(a, b) = path.split("-")
	edges[a].add(b)
	edges[b].add(a)
print(edges)

def visit(edge, visited):
	print(edge, visited)
	if edge == "end":
		return 1
	paths = 0
	for e in edges[edge]:
		copy = visited.copy()
		if not e in visited:
			if e.lower() == e:
				copy.add(e)
			paths += visit(e, copy)
			if e.lower() == e:
				copy.remove(e)
	return paths

print(visit("start", {"start"}))
