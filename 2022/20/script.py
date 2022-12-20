#!/usr/bin/env aoc_repl.py

from collections import Counter, defaultdict, deque
import heapq
import inspect
import itertools
import operator
import os
import pathlib
import sys

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0, os.path.dirname(os.path.dirname(currentdir)))

from aoc import *

input_filename = "input"
if "AOC_SAMPLE" in os.environ:
	input_filename = "sample"

input = pathlib.Path(input_filename).read_text().strip()
numbers = input.split("\n").map(int)

class Node:
	def __init__(self, value, backward, forward):
		self.value = value
		self.backward = backward
		self.forward = forward

	def __repr__(self):
		return f"({self.backward.value}, {self.value}, {self.forward.value})"

nodes = numbers.map(`<Node(_0, None, None)`>)

for (n1, n2) in nodes.window(2):
	n1.forward = n2
	n2.backward = n1

nodes[-1].forward = nodes[0]
nodes[0].backward = nodes[-1]

for node in nodes:
	if node.value == 0:
		continue

	node.forward.backward = node.backward
	node.backward.forward = node.forward

	if node.value < 0:
		next = node
		for _ in range(-node.value):
			next = next.backward
		node.backward = next.backward
		node.backward.forward = node
		node.forward = next
		next.backward = node
	else:
		next = node
		for _ in range(node.value):
			next = next.forward
		node.forward = next.forward
		node.forward.backward = node
		node.backward = next
		next.forward = node

	print_node = node.forward
	# while not print_node is node:
	# 	print(print_node.value, end=" ")
	# 	print_node = print_node.forward
	# print(node.value)

zero = nodes.first_by(_0.value == 0)

one_k = zero
for _ in range(1000):
	one_k = one_k.forward

two_k = one_k
for _ in range(1000):
	two_k = two_k.forward

three_k = two_k
for _ in range(1000):
	three_k = three_k.forward

[one_k, two_k, three_k].map(_0.value).sum()
