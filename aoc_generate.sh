#!/bin/bash

set -eux

if [ "$PWD" != "/Users/saagarjha/Developer/advent-of-code/2022" ]; then
	exit 1
fi

mkdir "$1"
cat > "$1/script.py" <<EOF
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
EOF
chmod +x "$1/script.py"
touch "$1/input"
touch "$1/sample"
subl "$1/script.py"
subl "$1/sample"
subl "$1/input"
../hud "./$1" 2> /dev/null & disown
