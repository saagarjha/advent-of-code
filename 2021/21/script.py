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

input = pathlib.Path(input_filename).read_text().strip()
numbers = input.split("\n")
players = [0, 0]
players[0] = int(numbers[0]["Player 1 starting position: ".len:])
players[1] = int(numbers[1]["Player 1 starting position: ".len:])
player0 = 0
player1 = 0
turn = 1
dice = 1
while True:
	if turn % 2:
		players[0] = (players[0] + dice + dice + 1 + dice + 2 - 1) % 10 + 1
		player0 += players[0]
	else:
		players[1] = (players[1] + dice + dice + 1 + dice + 2 - 1) % 10 + 1
		player1 += players[1]
	print(player0, player1)
	if player0 >= 1000:
		print(turn * 3 * player1)
		break
	elif player1 >= 1000:
		print(turn * 3 * player0)
		break
	turn += 1
	dice += 3

