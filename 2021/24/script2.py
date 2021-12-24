#!/usr/bin/env python3

from collections import Counter
import os
import pathlib
import sys
import inspect

# from claripy import *

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0, os.path.dirname(os.path.dirname(currentdir)))

from aoc import *

input_filename = "input"
if "AOC_SAMPLE" in os.environ:
	input_filename = "sample"

input = pathlib.Path(input_filename).read_text().strip()
lines = input.split("\n")
instructions = []
for line in lines:
	instructions.append(tuple(line.split()))

def assign(variable, value):
	global w
	global x
	global y
	global z
	if variable == "w":
		w = value
	if variable == "x":
		x = value
	if variable == "y":
		y = value
	if variable == "z":
		z = value

def parse(operator):
	global w
	global x
	global y
	global z
	try:
		value = int(operator)
		return value
	except:
		if operator == "w":
			return w
		if operator == "x":
			return x
		if operator == "y":
			return y
		if operator == "z":
			return z

n = 71131151917891

w = 0
x = 0
y = 0
z = 0
input_i = 0

for instruction in instructions:
	if instruction[0] == "inp":
		print(z, int(str(n)[input_i]), end=" ")
		assign(instruction[1], int(str(n)[input_i]))
		input_i += 1
	elif instruction[0] == "add":
		assign(instruction[1], parse(instruction[1]) + parse(instruction[2]))
	elif instruction[0] == "mul":
		assign(instruction[1], parse(instruction[1]) * parse(instruction[2]))
	elif instruction[0] == "div":
		assign(instruction[1], parse(instruction[1]) // parse(instruction[2]))
	elif instruction[0] == "mod":
		assign(instruction[1], parse(instruction[1]) % parse(instruction[2]))
	elif instruction[0] == "eql":
		if instruction[2] == "w":
			print(x)
		assign(instruction[1], parse(instruction[1]) == parse(instruction[2]))
print(z)
