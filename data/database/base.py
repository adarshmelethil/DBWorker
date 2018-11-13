
import os

from abc import ABC, abstractmethod

class BaseDatabase(ABC):
	def __init__(self, location):
		self.location = location
		# Cache
		self.tables = dict()
		self.history = dict()

	@abstractmethod
	def __enter__(self): 
		raise NotImplementedError("required for executing sql statements")

	@abstractmethod
	def __exit__(self, exc_type, exc_value, traceback):
		raise NotImplementedError("required for executing sql statements")

	# return map of table_name -> [col_names]
	@abstractmethod
	def getTables(self):
		raise NotImplementedError("Required to display and get a values from table")

	def __getitem__(self, key):
		if type(key) is not str:
			raise KeyError("key needs to be a string, got '{}'".format(key)) 
		key_split = key.split(".")
		if len(key_split) < 2:
			raise KeyError("Please specify the query name and coloum using the delimiter '.', got '{}'".format(key))
		query_name = key_split[0]
		column_name = ".".join(key_split[1:])
		if query_name not in self.history:
			raise KeyError("{query} is not found in query history".format(query=query_name))
		if column_name not in self.history[query_name]["col_names"]:
			raise KeyError("{col_name} is not found in query history in query {query}".format(query=query_name, col_name=column_name))
		
		if not self.history[query_name]["ran"]:
			self.executeSelect(query_name)

		col_index = self.history[query_name]["col_names"].index(column_name)
		return [cols[col_index] for cols in self.history[query_name]["data"]]

	def __contains__(self, key):
		try:
			self[key]
			return True
		except KeyError as ke:
			return False

	def columnNames(self, table_name):
		with self as conn:
			cursor = conn.execute('SELECT * FROM %s' % table_name)
			names = [description[0] for description in cursor.description]
			return names
	
	def keys(self):
		keys = list()
		for query_name in self.history:
			for col in self.history[query_name]["col_names"]:
				keys.append("{qn}.{col}".format(qn=query_name,col=col))
		return keys

	def getQueryData(self, query_name):
		return self.history[query_name]["col_names"], self.history[query_name]["data"]

	def getHistory(self):
		return self.history
	
	def deleteHistory(self, query_name):
		del self.history[query_name]

	def getNumOfEntries(self, query_name):
		return len(self.history[query_name]["data"])
		
	# Lint Query
	def addSelectQuery(self, name, query):
		if name in self.history:
			return "Query name already exists"
		if "FROM" not in query or "SELECT" not in query:
			return "Missing FROM or SELECT keyword form query"

		col_names = list(map(lambda v: v.strip(), 
			query.split("FROM")[0][len("SELECT "):].strip().split(",")))
		if col_names[0] == "*":
			return "Please use specific coloumn names in the form <table name>.<column name>"
		if len(col_names[0].split(".")) == 0:
			return "Please specify the table name as well as the column name"

		self.history[name] = {
			"query": query,
			"col_names": col_names,
			"data": [],
			"ran": False
		}

		try:
			self.executeSelect(name)
		except Exception as e:
			self.deleteHistory(name)
			return "Failed to exec SQL statement '{}'.\nError: {}".format(self.history[name]['query'], e)


	def executeSelect(self, name):
		with self as conn:
			cursor = conn.execute(self.history[name]["query"])
			data = cursor.fetchall()
			self.history[name]["data"] = data 
			self.history[name]["ran"] = True

		return len(self.history[name]["data"])
	
	def getValuesFromTable(self, table_name, col_names=[], condition_str="", save=True):
		col_str = "{}".format(",".join(map(lambda c: "{}.{}".format(table_name, c),col_names))) if col_names \
			else "{}".format(",".join(map(lambda c: "{}.{}".format(table_name, c), self.getTables()[table_name])))
		query_str = "SELECT {cols} FROM {tab_name}".format(
			cols=col_str, tab_name=table_name) + \
		"" if condition_str == "" else " WHERE {}".format(condition_str)

		return self.addSelectQuery("{}_ALL".format(table_name), query_str)



