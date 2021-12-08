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
numbers = input.split("\n").map(lambda x: x.split("|")[0].split())
results = input.split("\n").map(lambda x: x.split("|")[1].split())
# print(numbers)

total = 0
for i in numbers.indices():
	n = numbers[i]
	r = results[i]
	seven = set(n.first_by(lambda x: x.len == 3))
	one = set(n.first_by(lambda x: x.len == 2))
	eight = set(n.first_by(lambda x: x.len == 7))
	four = set(n.first_by(lambda x: x.len == 4))
	test235 = n.filter(lambda x: x.len == 5).map(set)
	diff = four - one
	test23 = []
	for test in test235:
		if len(test.union(diff)) == test.len:
			five = test
		else:
			test23.append(test)
	diff = eight - four
	for test in test23:
		if len(test.union(diff)) == test.len:
			two = test
		else:
			three = test
	test069 = []
	for test in n:
		test = set(test)
		if test == one or test == two or test == three or test == four or test == five or test == seven or test == eight:
			pass
		else:
			test069.append(test)
	for test in test069:
		if len(test.union(seven)) != test.len:
			six = test
	# print(six)
	test09 = []
	for test in test069:
		if test != six:
			test09.append(test)
	for test in test09:
		if len(test.union(five)) != test.len:
			zero = test
		else:
			nine = test
	solved = [zero, one, two, three, four, five, six, seven, eight, nine]
	number = ""
	for digit in r:
		number += str(solved.first_index_by(lambda x: set(x) == set(digit)))
	total += int(number)
	# print(top)
	# print(two_or_five)
print(total)
