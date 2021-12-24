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

# inp w			inp w		inp w		inp w		inp w		inp w		inp w		inp w		inp w		inp w		inp w		inp w		inp w		inp w		
# mul x 0		mul x 0		mul x 0		mul x 0		mul x 0		mul x 0		mul x 0		mul x 0		mul x 0		mul x 0		mul x 0		mul x 0		mul x 0		mul x 0		
# add x z		add x z		add x z		add x z		add x z		add x z		add x z		add x z		add x z		add x z		add x z		add x z		add x z		add x z		
# mod x 26		mod x 26	mod x 26	mod x 26	mod x 26	mod x 26	mod x 26	mod x 26	mod x 26	mod x 26	mod x 26	mod x 26	mod x 26	mod x 26	
# div z 1		div z 1		div z 1		div z 1		div z 26	div z 1		div z 1		div z 26	div z 1		div z 26	div z 26	div z 26	div z 26	div z 26	
# add x 14		add x 13	add x 15	add x 13	add x -2	add x 10	add x 13	add x -15	add x 11	add x -9	add x -9	add x -7	add x -4	add x -6	
# eql x w		eql x w		eql x w		eql x w		eql x w		eql x w		eql x w		eql x w		eql x w		eql x w		eql x w		eql x w		eql x w		eql x w		
# eql x 0		eql x 0		eql x 0		eql x 0		eql x 0		eql x 0		eql x 0		eql x 0		eql x 0		eql x 0		eql x 0		eql x 0		eql x 0		eql x 0		
# mul y 0		mul y 0		mul y 0		mul y 0		mul y 0		mul y 0		mul y 0		mul y 0		mul y 0		mul y 0		mul y 0		mul y 0		mul y 0		mul y 0		
# add y 25		add y 25	add y 25	add y 25	add y 25	add y 25	add y 25	add y 25	add y 25	add y 25	add y 25	add y 25	add y 25	add y 25	
# mul y x		mul y x		mul y x		mul y x		mul y x		mul y x		mul y x		mul y x		mul y x		mul y x		mul y x		mul y x		mul y x		mul y x		
# add y 1		add y 1		add y 1		add y 1		add y 1		add y 1		add y 1		add y 1		add y 1		add y 1		add y 1		add y 1		add y 1		add y 1		
# mul z y		mul z y		mul z y		mul z y		mul z y		mul z y		mul z y		mul z y		mul z y		mul z y		mul z y		mul z y		mul z y		mul z y		
# mul y 0		mul y 0		mul y 0		mul y 0		mul y 0		mul y 0		mul y 0		mul y 0		mul y 0		mul y 0		mul y 0		mul y 0		mul y 0		mul y 0		
# add y w		add y w		add y w		add y w		add y w		add y w		add y w		add y w		add y w		add y w		add y w		add y w		add y w		add y w		
# add y 0		add y 12	add y 14	add y 0		add y 3		add y 15	add y 11	add y 12	add y 1		add y 12	add y 3		add y 10	add y 14	add y 12	
# mul y x		mul y x		mul y x		mul y x		mul y x		mul y x		mul y x		mul y x		mul y x		mul y x		mul y x		mul y x		mul y x		mul y x		
# add z y		add z y		add z y		add z y		add z y		add z y		add z y		add z y		add z y		add z y		add z y		add z y		add z y		add z y		

# divisions = [1, 1, 1, 1, 1, 26, 1, 1, 26, 1, 26, 26, 26, 26,]
# addend1 = [14, 13, 15, 13, -2, 10, 13, -15, 11, -9, -9, -7, -4, -6,]
# addend2 = [0, 12, 14, 0, 3, 15, 11, 12, 1, 12, 3, 10, 14, 12,]

# for i in range(14):
# 	x = (z % 26) + addend1[i]
# 	z /= divisions[i]
# 	if x != input[i]:
# 		z *= 26
# 		z += input[i] + addend2[i]

# input[0] = 14, z = input[0]
# input[1] = intput[0] + 13, z = input[0] * 26 + input[1] + 12
# input[2] = input[1] + 27, z = (input[0] * 26 + input[1] + 12) * 26 + input[2] + 14
# input[3] = input[2] + 14, z = ((input[0] * 26 + input[1] + 12) * 26 + input[2] + 14) * 26 + input[3]
# input[4] = input[3] + 2, z = (input[0] * 26 + input[1] + 12) * 26 + input[2] + 14
# input[5] = input[2] + 24, z = ((input[0] * 26 + input[1] + 12) * 26 + input[2] + 14) * 26 + input[5] + 15
# input[6] = input[5] + 28, z = (((input[0] * 26 + input[1] + 12) * 26 + input[2] + 14) * 26 + input[5] + 15) * 26 + input[6] + 11
# input[7] = input[6] + 4, z = ((input[0] * 26 + input[1] + 12) * 26 + input[2] + 14) * 26 + input[5] + 15
# input[8] = input[5] + 26, z = (((input[0] * 26 + input[1] + 12) * 26 + input[2] + 14) * 26 + input[5] + 15) * 26 + input[8] + 1
# input[9] = input[8] + 8, z = ((input[0] * 26 + input[1] + 12) * 26 + input[2] + 14) * 26 + input[5] + 15
# input[10] = input[5] + 6, z = (input[0] * 26 + input[1] + 12) * 26 + input[2] + 14
# input[11] = input[2] + 7, z = input[0] * 26 + input[1] + 12
# input[12] = input[1] + 8, z = input[0]
# input[13] = input[0] - 6

n = 91297395919993

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
