#!/usr/bin/env aoc_repl.py

from collections import Counter, deque
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
		self.options = {}

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

	best = 0

	for (new_robots, new_supplies) in buying_options(blueprint, supplies):
		best = max(best, find_best(blueprint, list_add(robots, new_robots), list_add(robots, new_supplies), geodes + robots[3], remaining_time - 1))

	best = max(best, find_best(blueprint, robots, list_add(robots, supplies), geodes + robots[3], remaining_time - 1))

	blueprint.best[key] = best

	return best

# Note: actually ran this loop through xargs -P by hand
sum = 0
for i in range(blueprints.len):
	blueprint = blueprints[i]
	sum += (i + 1) * find_best(blueprints[i], [1, 0, 0, 0], [0, 0, 0, 0], 0, 24)
sum
