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

cache = {}
def play(players, scores, turn, universes):
	player = turn % 2
	if scores[not player] >= 21:
		wins = [0, 0]
		wins[not player] = universes
		return wins
	state = tuple([players, scores, player].flatten())
	if state in cache:
		return cache[state].map(_0 * universes)
	# print(players, scores)
	multipliers = {
		3: 1,
		4: 3,
		5: 6,
		6: 7,
		7: 6,
		8: 3,
		9: 1,
	}
	total = [0, 0]
	for multiplier in multipliers:
		new_players = players.copy()
		new_scores = scores.copy()
		# print(new_players, new_scores, multiplier)
		new_players[player] += multiplier
		new_players[player] = (new_players[player] - 1) % 10 + 1
		new_scores[player] += new_players[player]
		# print(new_players, new_scores, multiplier)
		wins = play(new_players, new_scores, turn + 1, multipliers[multiplier])
		for i in wins.indices():
			total[i] += wins[i]
	cache[state] = total
	return total.map(_0 * universes)
		

input = pathlib.Path(input_filename).read_text().strip()
numbers = input.split("\n")
players = [0, 0]
players[0] = int(numbers[0]["Player 1 starting position: ".len:])
players[1] = int(numbers[1]["Player 1 starting position: ".len:])
players
play(players, [0, 0], 0, 1).sorted()
