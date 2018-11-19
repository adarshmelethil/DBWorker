
import os
import sqlite3

from .base_database import BaseDatabase
	
class SQLite(BaseDatabase):
	def __init__(self, location):
		super(SQLite, self).__init__(location)

	def __enter__(self): 
		self.conn = sqlite3.connect(self.location)
		return self.conn
		
	def __exit__(self, exc_type, exc_value, traceback):
		self.conn.close()
		return False

	def getTables(self):
		tables_map = dict()
		with self as conn:
			cursor = conn.cursor()
			cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
			tables = cursor.fetchall()
		
		for table_name in tables:
			tables_map[table_name[0]] = self.columnNames(table_name[0])
		return tables_map

if __name__ == "__main__":
	import sys
	if len(sys.argv) == 1:
		print("need test db as first argument")
		sys.exit(1)
	
	if not os.path.isfile(sys.argv[1]):
		print("db file not found")

	db = SQLite(sys.argv[1])
	tables = db.getTables()
	keys = list(tables.keys())
	print("tables", tables)
	table_values = db.getValuesFromTable(keys[0])
	print("values from table {t}".format(t=keys[0]))
	print("resp", table_values)
	
	ks = table_values.keys()
	print("Keys", ks)
	print("datalen", table_values.getNumOfEntries())
	
	# if os.path.file 


