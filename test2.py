

# def a():
#   print(__name__)

# import test
# test.b()

# print(__name__)

class TestError(Exception):
  pass

def a():
  raise TestError("NO!")

try:
  a()
except NameError:
  print("Caught exception")

