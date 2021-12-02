#!/usr/bin/env python3

import pathlib

h = 0
v = 0
aim = 0
input = pathlib.Path("input").read_text().strip()
for line in input.split("\n"):
	if line.startswith("forward"):
		d = int(line[len("forward"):])
		h += d
		v += d * aim
	elif line.startswith("up"):
		aim += int(line[len("up"):])
	elif line.startswith("down"):
		aim -= int(line[len("down"):])
	
print(h * v)
