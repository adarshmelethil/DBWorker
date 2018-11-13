
import sqlite3

import string
import random

def rendomString(N):
	return ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase) for _ in range(N))

conn = sqlite3.connect('test.db')
c = conn.cursor()

new_table1 = rendomString(5)
c.execute('''CREATE TABLE %s (id INTEGER, name TEXT, val1 INTEGER, val2 REAL)''' % new_table1)
test_values1 = [
	(i, rendomString(5), random.randint(0,10000), random.uniform(0, 1)) 
	for i in range(100)
]
c.executemany('INSERT INTO %s VALUES (?,?,?,?)' % new_table1, test_values1)

new_table2 = rendomString(5)
c.execute('''CREATE TABLE %s (id INTEGER, name TEXT, val1 INTEGER, val2 REAL, %s_id INTEGER)''' % (new_table2, new_table1))
test_values2 = [
	(i-50, rendomString(5), random.randint(0,10000), random.uniform(0, 1), i) 
	for i in range(50, 150)
]
c.executemany('INSERT INTO %s VALUES (?,?,?,?,?)' % new_table2, test_values2)

c.execute("SELECT name FROM sqlite_master WHERE type='table';")
_tables = c.fetchall()
print(len(_tables))
for t in _tables:
	print(t[0])

conn.commit()
conn.close()

