#!/usr/bin/env python3

import ast
import pathlib
import sys

class Visitor(ast.NodeTransformer):
	def visit_Module(self, node):
		new_body = []
		for expression in node.body:
			if isinstance(expression, ast.Expr):
				assign = ast.copy_location(
					ast.Assign([ast.Name("__repl_intermediate", ast.Store())], expression.value), expression
				)
				ast.fix_missing_locations(assign)
				new_body.append(assign)
				condition = ast.copy_location(
					ast.If(ast.Name("__repl_intermediate", ast.Load()), [
						ast.Expr(ast.Call(ast.Name('print', ast.Load()), [ast.Name("__repl_intermediate", ast.Load())], []))
					], []), expression
				)
				ast.fix_missing_locations(condition)
				new_body.append(condition)
			else:
				new_body.append(expression)
		node.body = new_body
		return node

if __name__ == "__main__":
	file = sys.argv[1]
	tree = ast.parse(pathlib.Path(file).read_text(), file, mode="exec")
	new_tree = Visitor().visit(tree)
	exec(compile(new_tree, file, mode='exec'))
