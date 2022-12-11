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

class Monkey:
	def __init__(self, items, operation, test, true, false):
		self.items = items
		self.operation = operation
		self.test = test
		self.true = true
		self.false = false
		self.inspect = 0


input = pathlib.Path(input_filename).read_text().strip()
list = input.split("\n\n")
monkeys = []

for thing in list:
	split = thing.split("\n")
	items = split[1].replace("  Starting items: ", "").split(",").map(int)
	operation = split[2].replace("  Operation: new = ", "")
	test = int(split[3].replace("  Test: divisible by ", ""))
	true = int(split[4].last)
	false = int(split[5].last)
	# items, operation, test, true, false
	monkeys.append(Monkey(items, operation, test, true, false))

for round in range(0, 20):
	for monkey in monkeys:
		for i in range(0, monkey.items.len):
			new = eval(monkey.operation.replace("old", str(monkey.items[i])))
			new = new // 3
			new, test, monkey.true, monkey.false, new % monkey.test == 0
			monkey.inspect += 1
			if new % monkey.test == 0:
				monkeys[monkey.true].items.append(new)
			else:
				monkeys[monkey.false].items.append(new)
		monkey.items = []
	monkeys.map(_0.items)


n = monkeys.map(_0.inspect).sorted()
n[-1] * n[-2]
