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

class Blueprint:
	def __init__(self, ore, clay, obsidian, geode):
		self.ore = ore
		self.clay = clay
		self.obsidian = obsidian
		self.geode = geode
		self.robots = [ore, clay, obsidian, geode]
		self.best = {}
		self.best_lower_bound = defaultdict(lambda: -1)
		self.options = {}
		self.max = self.robots.transpose().map(`<_0.max()`>)

	def __repr__(self):
		return f"{self.ore} {self.clay} {self.obsidian} {self.geode}"

blueprints = []

for line in input.split("\n"):
	line = line.split(": ")[1]
	line = line.split(".")
	ore = int(line[0].replace("Each ore robot costs ", "").replace(" ore", ""))
	clay = int(line[1].replace("Each clay robot costs ", "").replace(" ore", ""))
	obsidian = line[2].replace("Each obsidian robot costs ", "").split(" ore and ").map(`<_0.replace(" clay", "")`>).map(int)
	geode = line[3].replace("Each geode robot costs ", "").split(" ore and ").map(`<_0.replace(" obsidian", "")`>).map(int)
	blueprints.append(Blueprint((ore, 0, 0, 0), (clay, 0, 0, 0), (*obsidian, 0, 0), (geode[0], 0, geode[1], 0)))

# blueprints

def can_buy(robot, supplies):
	for robot, supply in zip(robot, supplies):
		if robot > supply:
			return False
	return True

def buying_options(blueprint, supplies):
	possibilities = []
	for i in range(blueprint.robots.len):
		robot = blueprint.robots[i]
		if can_buy(robot, supplies):
			new_supplies = buy(robot, supplies)
			new_robots = [0] * blueprint.robots.len
			new_robots[i] = 1
			possibilities.append((new_robots, new_supplies))
	return possibilities
	# if tuple(supplies) in blueprint.options:
	# 	return blueprint.options[tuple(supplies)]
	# possibilities = []
	# for i in range(blueprint.robots.len):
	# 	robot = blueprint.robots[i]
	# 	if can_buy(robot, supplies):
	# 		new_supplies = buy(robot, supplies)
	# 		base = [0] * blueprint.robots.len
	# 		base[i] += 1
	# 		possibilities.append((base, new_supplies))
	# 		for option in buying_options(blueprint, new_supplies):
	# 			possibilities.append((list_add(option[0], base), option[1]))
	# blueprint.options[tuple(supplies)] = possibilities
	# return possibilities

def buy(robot, supplies):
	new_supplies = []
	for robot, supply in zip(robot, supplies):
		new_supplies.append(supply - robot)
	return new_supplies

def list_add(l1, l2):
	return zip(l1, l2).map(_0[0] + _0[1])

def find_best(blueprint, robots, supplies, geodes, remaining_time):
	if remaining_time == 0:
		return geodes

	key = (tuple(robots), tuple(supplies), remaining_time)

	if key in blueprint.best:
		return blueprint.best[key]

	if zip(robots[:-1], blueprint.max[:-1]).filter(_0[0] > _0[1]).len:
		return -1

	optimistic = geodes + (robots[3] * remaining_time) + remaining_time * (remaining_time - 1) // 2
	if optimistic <= blueprint.best_lower_bound[remaining_time]:
		return -1

	best = 0

	for (new_robots, new_supplies) in buying_options(blueprint, supplies):
		best = max(best, find_best(blueprint, list_add(robots, new_robots), list_add(robots, new_supplies), geodes + robots[3], remaining_time - 1))

	best = max(best, find_best(blueprint, robots, list_add(robots, supplies), geodes + robots[3], remaining_time - 1))

	blueprint.best[key] = best

	# if blueprint.best_lower_bound[remaining_time] < best:
	# 	print(remaining_time, best, robots)
	blueprint.best_lower_bound[remaining_time] = max(best, blueprint.best_lower_bound[remaining_time])

	return best

product = 1
for blueprint in blueprints[:3]:
	product *= find_best(blueprint, [1, 0, 0, 0], [0, 0, 0, 0], 0, 32)
product
