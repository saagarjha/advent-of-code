#!/usr/bin/env python3

import pathlib

input = pathlib.Path("input").read_text().strip()

picks = [int(x) for x in input.split("\n")[0].split(",")]

boards_str = "\n".join(input.split("\n")[2:]).split("\n\n")

boards = []
for b in boards_str:
	board = [[int(x) for x in line.split()] for line in b.split("\n")]
	boards += [board]

def mark_board(board, n):
	for r in range(len(board)):
		for c in range(len(board[r])):
			if board[r][c] == n:
				board[r][c] = -1

	for r in range(len(board)):
		if board[r] == [-1] * len(board):
			return True

	found = True
	for c in range(len(board[0])):
		for r in range(len(board)):
			if board[r][c] != -1:
				found = False
		if found:
			return True

	return False


for pick in picks:
	for board in boards:
		# print(board)
		if mark_board(board, pick):
			sum = 0
			for r in board:
				for c in r:
					if c != -1:
						sum += c
			sum *= pick
			print(sum)


