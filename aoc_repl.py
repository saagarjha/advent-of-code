#!/usr/bin/env python3

import ast
import pathlib
import sys
import os

class Visitor(ast.NodeTransformer):
	def fixup_body(self, node, body):
		new_body = []
		for expression in getattr(node, body):
			if isinstance(expression, ast.Expr):
				assign = ast.copy_location(
					ast.Assign([ast.Name("__repl_intermediate", ast.Store())], expression.value), expression
				)
				ast.fix_missing_locations(assign)
				new_body.append(assign)
				condition = ast.copy_location(
					ast.If(ast.Compare(ast.Name("__repl_intermediate", ast.Load()), [ast.NotEq()], [ast.Constant(None)]), [
						ast.Expr(ast.Call(ast.Name("print", ast.Load()), [ast.Name("__repl_intermediate", ast.Load())], []))
					], []), expression
				)
				ast.fix_missing_locations(condition)
				new_body.append(condition)
			else:
				new_body.append(expression)
			if not (isinstance(node, ast.If) and \
				isinstance(node.test, ast.Compare) and \
				isinstance(node.test.left, ast.Name) and \
				node.test.left.id == "__repl_intermediate"):
				self.generic_visit(node)
		setattr(node, body, new_body)

classes = {
	"Module": ["body"],
	"FunctionDef": ["body"],
	"AsyncFunctionDef": ["body"],
	"ClassDef": ["body"],
	"For": ["body", "orelse"],
	"AyncFor": ["body", "orelse"],
	"While": ["body", "orelse"],
	"If": ["body", "orelse"],
	"With": ["body"],
	"AsyncWith": ["body"],
	"Try": ["body", "orelse", "finalbody"],
	"TryStar": ["body", "orelse", "finalbody"],
	"ExceptHandler": ["body", "orelse", "finalbody"],
}

for _class in classes:
	def visit(self, node):
		for body in classes[_class]:
			self.fixup_body(node, body)
			return node
	setattr(Visitor, f"visit_{_class}", visit)

def lambda_replace(source):
	start = 0
	end = 0
	new_source = ""
	level = 0
	i = 0
	while i < len(source):
		c = source[i]
		i += 1
		if c == "`":
			c = source[i]
			i += 1
			if c == "<":
				level += 1
				new_source += "(lambda *__lambda_args: "
			elif c == ">":
				assert level > 0
				level -= 1
				new_source += ")"
			else:
				raise SyntaxError("Mismatched backticks")
		elif c == "_" and level > 0:
			number = ""
			while source[i].isdigit():
				number += source[i]
				i += 1
			new_source += f"__lambda_args[{number}]"
		else:
			new_source += c
	return new_source

if __name__ == "__main__":
	file = sys.argv[1]
	source = lambda_replace(pathlib.Path(file).read_text())
	tree = ast.parse(source, file, mode="exec")
	new_tree = Visitor().visit(tree)
	os.environ["AOC_REPL"] = "1"
	exec(compile(new_tree, file, mode="exec"))
