#!/bin/sh

set -eux

if [ "$PWD" != "/Users/saagarjha/Developer/advent-of-code/2021" ]; then
	exit 1
fi

mkdir "$1"
cat > "$1/script.py" <<EOF
#!/usr/bin/env python3

import pathlib

import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0, os.path.dirname(os.path.dirname(currentdir)))

from aoc import *

input = pathlib.Path("input").read_text().strip()
numbers = input.split("\n")
EOF
chmod +x "$1/script.py"
subl "$1/script.py"
