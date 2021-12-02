#!/usr/bin/env python3

import os
import pathlib
import time
import urllib.request

if __name__ == "__main__":
	while True:
		try:
			session = pathlib.Path("../../session").read_text().strip()
			(year, challenge)  = os.getcwd().split("/")[-2:]
			challenge = int(challenge)
			print(f"Downloading challenge {challenge} for year {year}...")
			request = urllib.request.Request(f"https://adventofcode.com/{year}/day/{challenge}/input")
			request.add_header("Cookie", f"session={session}")
			input = urllib.request.urlopen(request).read()
			pathlib.Path("input").write_bytes(input)
			print("Downloaded {} lines.".format(len(input.decode().split("\n"))))
			break
		except KeyboardInterrupt:
			break
		except:
			time.sleep(10)
