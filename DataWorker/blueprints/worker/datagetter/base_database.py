
import os

from abc import ABC, abstractmethod

from .query import Query 

class BaseDatabase(ABC):
	def __init__(self, location):
		self.location = location
		# Cache
		self.tables = dict()

	# Executed at the start of 'with' syntax
	@abstractmethod
	def __enter__(self): 
		raise NotImplementedError("required for executing sql statements")

	# Executed at the end of 'with' syntax
	@abstractmethod
	def __exit__(self, exc_type, exc_value, traceback):
		raise NotImplementedError("required for executing sql statements")

	# return map of table_name -> [col_names]
	@abstractmethod
	def getTables(self):
		raise NotImplementedError("Required to display and get a values from table")

	def columnNames(self, table_name):
		with self as conn:
			cursor = conn.execute('SELECT * FROM %s' % table_name)
			names = [description[0] for description in cursor.description]
			return names

	# Lint Query
	def runSelectQuery(self, query):
		data = self.executeSelect(query)
		return Query(query, data)
		# return "Failed to exec SQL statement '{}'.\nError: {}".format(query, e)

	def executeSelect(self, query):
		with self as conn:
			cursor = conn.execute(query)
			return cursor.fetchall()
	
	def getValuesFromTable(self, table_name, col_names=[], condition_str="", save=True):
		col_str = "{}".format(",".join(map(lambda c: "{}.{}".format(table_name, c),col_names))) if col_names \
			else "{}".format(",".join(map(lambda c: "{}.{}".format(table_name, c), self.getTables()[table_name])))
		query_str = "SELECT {cols} FROM {tab_name}".format(
			cols=col_str, tab_name=table_name) + \
		"" if condition_str == "" else " WHERE {}".format(condition_str)

		return self.runSelectQuery("{}_ALL".format(table_name), query_str)



