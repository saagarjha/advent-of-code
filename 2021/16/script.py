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

class Packet:
	def __init__(self, n):
		print(n)
		self.version = int(n[0:3], 2)
		self.type = int(n[3:6], 2)
		if self.type == 4:
			number = ""
			i = 6
			while True:
				part = n[i:i+5]
				number += part[1:]
				if part[0] == "0":
					break
				i += 5
			self.value = int(number, 2)
			self.length = i + 5
		else:
			if n[6] == "0":
				self.parse_children(n[7+15:], int(n[7:7+15], 2))
			else:
				self.parse_children(n[7+11:], None, int(n[7:7+11], 2))

	def parse_children(self, n, length=None, count=None):
		self.children = []
		i = 0
		while True:
			if count and self.children.len == count:
				break
			if length and i == length:
				break
			child = Packet(n[i:])
			self.children.append(child)
			i += child.length
		if count:
			self.length = 7 + 11 + self.children.map(_0.length).fold(operator.add)
		else:
			self.length = 7 + 15 + length

def version_sum(packet):
	if packet.type == 4:
		return packet.version
	else:
		return packet.version + packet.children.map(version_sum).fold(operator.add)

input = pathlib.Path(input_filename).read_text().strip()
number = int(input, 16)
number = format(number, f"0{input.len * 4}b")
# Packet(number).length
root = Packet(number)
version_sum(root)
