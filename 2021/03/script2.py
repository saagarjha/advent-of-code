#!/usr/bin/env python3

import pathlib

input = pathlib.Path("input").read_text().strip()
numbers = input.split("\n")

gamma = 0
epsilon = 0

oxygen = numbers
co2 = numbers

for i in range(len(numbers[0])):
	oxygen_zeros = 0
	oxygen_ones = 0
	co2_zeros = 0
	co2_ones = 0
	for n in oxygen:
		if n[i] == "0":
			oxygen_zeros += 1
		else:
			oxygen_ones += 1

	for n in co2:
		if n[i] == "0":
			co2_zeros += 1
		else:
			co2_ones += 1

	if oxygen_zeros <= oxygen_ones:
		oxygen = [n for n in oxygen if n[i] == "1"]
	else:
		oxygen = [n for n in oxygen if n[i] == "0"]

	if co2_zeros <= co2_ones:
		co2 = [n for n in co2 if n[i] == "0"]
	else:
		co2 = [n for n in co2 if n[i] == "1"]

	print(oxygen, co2)


	if len(oxygen) == 1:
		o = int(oxygen[0], 2)

	if len(co2) == 1:
		c = int(co2[0], 2)
	
print(o * c)
