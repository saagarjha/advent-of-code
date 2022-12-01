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
elves = input.split("\n\n").map(lambda x: x.split("\n").map(int))
elves = elves.map(lambda x: sum(x))
list.sort(elves)
elves[-1] + elves[-2] + elves[-3]


