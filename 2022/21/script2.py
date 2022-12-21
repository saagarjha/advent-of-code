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
expressions = {}

for line in input.split("\n"):
	name, expression = line.split(": ")
	expressions[name] = expression

def calc(expression):
	if expression == "x":
		return "x"
	try:
		return int(expression)
	except:
		(n1, op, n2) = expression.split(" ")
		return "(" + str(calc(expressions[n1])) + f") {op} (" + str(calc(expressions[n2])) + ")"

n1, op, n2 = expressions["root"].split(" ")
expressions["root"] = n1 + " = " + n2
expressions["humn"] = "x"
calc(expressions["root"])
# Plugged into Mathematica
