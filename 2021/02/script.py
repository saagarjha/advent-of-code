#!/usr/bin/env python3

import pathlib

h = 0
v = 0
input = pathlib.Path("input").read_text().strip()
for line in input.split("\n"):
	if line.startswith("forward"):
		h += int(line[len("forward"):])
	elif line.startswith("up"):
		v += int(line[len("up"):])
	elif line.startswith("down"):
		v -= int(line[len("down"):])
	
print(h * v)
