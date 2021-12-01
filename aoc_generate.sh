#!/bin/sh

set -eux

if [ "$PWD" != "/Users/saagarjha/Developer/advent-of-code/2021" ]; then
	exit 1
fi

mkdir "$1"
cat > "$1/script.py" <<EOF
#!/usr/bin/env python3

import pathlib

input = pathlib.Path("input").read_text().strip()
numbers = list(map(int, input.split("\n")))
EOF
chmod +x "$1/script.py"
subl "$1/script.py"
