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

def matches(scanner1, scanner2):
	offsets = []
	for m1 in scanner1:
		for m2 in scanner2:
			offsets.append((m1[0] - m2[0], m1[1] - m2[1], m1[2] - m2[2]))
	offsets_count = Counter(offsets)
	max_offset = None
	for offset in offsets_count:
		if offsets_count[offset] >= 12:
			max_offset = offset
			break
	if max_offset:
		offset_scanner = []
		# print(max_offset)
		for m in scanner2:
			offset_scanner.append((m[0] + max_offset[0], m[1] + max_offset[1], m[2] + max_offset[2]))
		# print(scanner1)
		# print(scanner1.sorted())
		# print(offset_scanner.sorted())
		points = set(scanner1 + offset_scanner)
		return (True, points)
	return (False, None)

	# 	print(scanner1)
	# 	print(offsets)
	# print((scanner1.len ** 2) - offsets_count.len)
	# for offset in offsets:
	# 	if offsets[offset] >= 12:
	# 		print(offsets)

def rotations(scanner):
	permutations = [
		[0, 1, 2],
		[0, 2, 1],
		[1, 0, 2],
		[1, 2, 0],
		[2, 0, 1],
		[2, 1, 0],
	]
	rotations = []
	for permutation in permutations:
		for x_flip in [-1, 1]:
			for y_flip in [-1, 1]:
				for z_flip in [-1, 1]:
					s = []
					for m in scanner:
						(x, y, z) = (m[permutation[0]], m[permutation[1]], m[permutation[2]])
						s.append((x * x_flip, y * y_flip, z * z_flip))
					rotations.append(s)
	return rotations

input = pathlib.Path(input_filename).read_text().strip()
scanners_str = input.split("\n\n").map((_0.split.__("\n")[1:]))
scanners = []
for scanner in scanners_str:
	scanners.append(scanner.map(_0.split.__(",").map.__(int)))
all_points = scanners[0]
remaining = set(range(1, scanners.len))
while remaining.len:
	all_rotations = rotations(all_points)
	done = False
	for i in remaining.copy():
		print(i, remaining)
		if done:
			break
		for rotation1 in all_rotations:
			if done:
				break
			for rotation2 in rotations(scanners[i]):
				(good, new) = matches(rotation1, rotation2)
				if good:
					all_points = new
					remaining.remove(i)
					done = True
					break
print(all_points.len)
			
