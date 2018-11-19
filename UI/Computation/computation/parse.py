
import re

VALID_OPS = "\+\-\*\/\^"

class ComputationTextError(Exception):
	def __init__(self, msg):
		super(ComputationTextError, self).__init__(msg)

def validLine(index, line):
	line_split = line.split("=")

	if len(line_split) < 2:
		raise ComputationTextError(
			"Couldn't find '=': #{line_index}: '{line}'".format(
				line_index=index, line=line))
	if len(line_split) > 2:
		raise ComputationTextError(
			"Found multiple '=': #{line_index}: '{line}'".format(
				line_index=index, line=line))

	return line_split[0], line_split[1]

def validDBVar(var):
	var_split = var.split(".")

def parseExpression(var_dict, expression):
	vars = re.split('[^a-zA-Z\_1-9\.]', expression)
	for v in vars:
		try: 
			value = float(vars)

		except ValueError:
	print(expression, vars)

	return vars 
	# for character in expression:


# returns list of variables, and tree
def parseRawText(text):
	statements = text.split("\n") 

	parsed = {}
	for i, l in enumerate(statements):
		clean_line = re.sub('\s+', '',l)
		if not clean_line:
			continue
		var, expression = validLine(i+1, clean_line)

		new_exp = parseExpression(parsed, expression)
		parsed[var] = new_exp

	return parsed

if __name__ == "__main__":
	test_input = """
a = 1.3

bb = 22
k_k = a + bb + 4
c = k_k / a + b * k_k
"""
	try:
		print("ans", parseRawText(test_input))
	except Exception as e:
		print(e)