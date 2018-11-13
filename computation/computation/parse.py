
import re

VALID_OPS = "\+\-\*\/\^"

class ComputationTextError(Exception):
	def __init__(self, msg):
		super(ComputationTextError, self).__init__(msg)

def validLine(index, line):
	line_split = line.split("=")
	print(line, line_split)
	if len(line_split) < 2:
		raise ComputationTextError(
			"Couldn't find '=': #{line_index}: '{line}'".format(
				line_index=index, line=line))
	if len(line_split) > 2:
		raise ComputationTextError(
			"Found multiple '=': #{line_index}: '{line}'".format(
				line_index=index, line=line))

	return line_split[0], line_split[1]

def parseExpression(var_dict, expression):

	for character in expression:


# returns list of variables, and tree
def parseRawText(text):
	statements = text.split("\n") 

	parsed = {}
	for i, l in enumerate(statements):
		clean_line = re.sub('\s+', '',l)
		if not clean_line:
			continue
		var, expression = validLine(i+1, clean_line)

		parsed[var] = expression

	return parsed

if __name__ == "__main__":
	test_input = """
a = 1

b = 2

c = a + b
"""
	try:
		print(parseRawText(test_input))
	except Exception as e:
		print(e)