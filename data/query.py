
import numpy as np
import numbers

class Query:
	def __init__(self, query, data):
		self.db_name = "not set"
		self.query = query
		self.col_names = list(map(lambda v: v.strip(), 
			query.split("FROM")[0][len("SELECT "):].strip().split(",")))
		self.data = data

	def setDBName(self, db_name):
		self.db_name = db_name

	def __getitem__(self, key):
		if type(key) is not str:
			raise KeyError("key needs to be a string, got '{}'".format(key)) 
		
		if query_name not in self.col_names:
			raise KeyError("{key} is not found in query".format(key=key))
				
		if not self.history[query_name]["ran"]:
			self.executeSelect(query_name)

		col_index = self.col_names.index(column_name)

		res_vals = [row[col_index] for row in self.data]
		if len(res_vals) > 0 and isinstance(res_vals[0], numbers.Number):
			return np.array(res_vals)
		return res_vals

	def __contains__(self, key):
		return key in col_names

	def keys(self):
		return self.col_names
	
	def getNumOfEntries(self):
		return len(self.data)

	def __str__(self):
		return "<{total}|({cols})>".format(cols=", ".join(self.col_names), total=len(self.data))

