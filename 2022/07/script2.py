#!/usr/bin/env aoc_repl.py

from collections import Counter
import inspect
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

class File:
	def __init__(self):
		self.children = []
		self.size = 0

	def fix_size(self):
		if self.size:
			return
		for child in self.children:
			child.fix_size()
			self.size += abs(child.size)
		self.size = -self.size

path = []
files = {"/": File()}

def path_str(path):
	return path.str_join("/").replace("//", "/")

for terminal in input.split("$ ")[1:]:
	command = terminal.split("\n")
	(command, output) = (command[0], command[1:])
	# command, output
	if command.startswith("cd"):
		p = command[3:]
		if p == "..":
			path = path[:path.len-1]
		else:
			path.append(p)
	elif command.startswith("ls"):
		for file in output:
			if not file.len:
				continue
			(size, name) = file.split(" ")
			try:
				file = files[path_str(path + [name])]
			except:
				file = File()
				files[path_str(path + [name])] = file
			if size == "dir":
				file.size = 0
			else:
				file.size = int(size)
			files[path_str(path)].children.append(file)

sum = 0
files["/"].fix_size()
sizes = []
for file in files:
	if files[file].size < 0:
		file, -files[file].size
		sizes.append(-files[file].size)
sizes.sorted().first_by(_0 >= 30000000- (70000000 + files["/"].size))
-files["/"].size-30000000
sizes.sorted()
