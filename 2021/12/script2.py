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

def visit(edge, visited, double):
	# print(edge, visited, double)
	if edge == "end":
		return 1
	paths = 0
	for e in edges[edge]:
		copy = visited.copy()
		if e.lower() != e:
			paths += visit(e, visited, double)
		elif not e in visited:
			copy.add(e)
			paths += visit(e, copy, double)
			copy.remove(e)
		elif not double and e != "start":
			copy.add(e)
			paths += visit(e, copy, e)
			copy.remove(e)
	return paths

print(visit("start", {"start"}, None))
