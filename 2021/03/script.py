#!/usr/bin/env python3

import pathlib

input = pathlib.Path("input").read_text().strip()
numbers = input.split("\n")

gamma = 0
epsilon = 0

for i in range(len(numbers[0])):
	zeros = 0
	ones = 0
	for n in numbers:
		if n[i] == "0":
			zeros += 1
		else:
			ones += 1

	if zeros < ones:
		epsilon |= 1
	else:
		gamma |= 1

	# print(gamma, epsilon)
	epsilon <<= 1
	gamma <<= 1
	
# print(gamma, epsilon)
print(gamma * epsilon // 4)
