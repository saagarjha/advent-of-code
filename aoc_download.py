#!/usr/bin/env python3

import html.parser
import os
import pathlib
import time
import urllib.request

class Parser(html.parser.HTMLParser):
	def __init__(self):
		html.parser.HTMLParser.__init__(self)
		self.in_pre = False
		self.in_code = False
		self.data = None

	def handle_starttag(self, tag, attrs):
		# print(tag)
		if self.data:
			return
		if tag == "pre":
			self.in_pre = True
		elif tag == "code" and self.in_pre:
			self.in_code = True

	def handle_endtag(self, tag):
		self.in_pre = False
		self.in_code = False

	def handle_data(self, data):
		if self.in_pre and self.in_code:
			self.data = data

if __name__ == "__main__":
	(year, challenge)  = os.getcwd().split("/")[-2:]
	challenge = int(challenge)
	while True:
		try:
			session = pathlib.Path("../../session").read_text().strip()
			print(f"Downloading input for {year} {challenge}...")
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
	while True:
		try:
			print(f"Downloading sample for {year} {challenge}...")
			text = urllib.request.urlopen(f"https://adventofcode.com/{year}/day/{challenge}").read().decode()
			# print(text)
			parser = Parser()
			parser.feed(text)
			if parser.data:
				pathlib.Path("sample").write_text(parser.data)
				print("Downloaded {} lines.".format(len(parser.data.split("\n"))))
				break
		except KeyboardInterrupt:
			break
		# except:
		# 	time.sleep(10)
