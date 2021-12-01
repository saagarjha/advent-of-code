#!/usr/bin/env python3

import pathlib

input = pathlib.Path("input").read_text().strip()
numbers = list(map(int, input.split("\n")))
j = 0
for i in range(len(numbers)-1):
	if numbers[i] <= numbers[i+1]:
		print(numbers[i], numbers[i + 1])
		j += 1

print(j)
