#!/usr/bin/env python3

import pathlib

input = pathlib.Path("input").read_text().strip()
numbers = list(map(int, input.split("\n")))
j = 0
for i in range(len(numbers)-3):
	a = numbers[i]
	b = numbers[i + 1]
	c = numbers[i + 2]
	d = numbers[i + 3]
	# e = numbers[i + 4]
	if a + b +c < b + c +d :
		print(numbers[i], numbers[i + 1])
		j += 1

print(j)
