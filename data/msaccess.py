
# import pyodbc

from .base_database import BaseDatabase

class MSAccess(BaseDatabase):
	def __init__(self, location):
		super(MSAccess, self).__init__(location)
		self.odbc_conn_str = 'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)}; DBQ=%s'

	def __enter__(self): 
		print("Not Implemented __entry__")
		return None

	def __exit__(self, exc_type, exc_value, traceback):
		print("Not Implemented __exit__")
		return None

	# placeholder
	def getTables(self):
		tables_map = {
			"table1": ["col1", "col2"],
			"table2": ["col1"],
			"table3": ["col1", "col2", "col3"]
		}

		return tables_map
