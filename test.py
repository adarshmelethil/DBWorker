import sqlite3


db= '/Users/adarsh/work/personal/DBWorker/test.db'
conn = sqlite3.connect(db)
c = conn.cursor()


c.execute("select * from test2;")
results = c.fetchall()

results[0][0] = 123
print(results)

# class a:
#   def __init__(a, name):
#     a.name = name

#   def hi(self):
#     print("hi %s" % self.name)

#   @classmethod
#   def hello(cls):
#     print("class method hi")

# foo = a("foo")
# bar = a("bar")

# print(__name__)

# import test2
# test2.a()


# def b():
#   print("my name is", __name__)

# import test2
# print(__name__)
