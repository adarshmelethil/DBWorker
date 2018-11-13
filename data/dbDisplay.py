

from PyQt5 import QtWidgets 

try:
	from data.database import getDatabase
	from data.queryEntry import QueryEntry
except ImportError:
	from database import getDatabase
	from queryEntry import QueryEntry



class DatabaseDisplay(QtWidgets.QWidget):
	def __init__(self, container, parent):
		super(DatabaseDisplay, self).__init__(container)

		self.parent = parent

		self.init_ui()

	def init_ui(self):
		database_page = QtWidgets.QVBoxLayout()
		
		self.info_name_label = QtWidgets.QLabel()
		self.updateNameLabel()
		database_page.addWidget(self.info_name_label)

		# Table Info
		self.table_info = QtWidgets.QLabel()
		self.updateTableInfo()
		database_page.addWidget(self.table_info)
		
		# Existing 
		self.query_history_list = QtWidgets.QListWidget()
		self.query_history_list.itemDoubleClicked.connect(self.getQueryDisplay)
		self.updateQuery()
		database_page.addWidget(self.query_history_list)

		# New Select Query executeSelect
		query_layout = QtWidgets.QGridLayout()
		query_layout.setColumnStretch(2, 6)
		query_description_name = QtWidgets.QLabel()
		query_description_name.setText("Name")
		query_layout.addWidget(query_description_name, 0, 0)
		query_description = QtWidgets.QLabel()
		query_description.setText("SQL Qurey. e.g. SELECT tbName.colName FROM tbName ...")
		query_layout.addWidget(query_description, 0, 1)
		
		self.query_name = QtWidgets.QLineEdit(self)
		self.query_input = QtWidgets.QLineEdit(self)
		query_add = QtWidgets.QPushButton("Add")
		query_add.clicked.connect(self.addQuery)
		query_layout.addWidget(self.query_name, 1, 0)
		query_layout.addWidget(self.query_input, 1, 1)
		query_layout.addWidget(query_add, 1, 4)
		database_page.addLayout(query_layout)

		database_page.addStretch()
		# self.info_container_widget = QtWidgets.QWidget()
		self.setLayout(database_page)

	def getQueryDisplay(self, item):
		query_entry = self.query_history_list.itemWidget(item)
		self.executeSelect(query_entry.name)
		self.parent.parent.parent.updateTab(
				*query_entry.GetDisplay())

	def addQuery(self):
		q_name = self.query_name.text()
		query = self.query_input.text()
		resp = self.parent.db.addSelectQuery(q_name, query)
		if resp:
			QtWidgets.QMessageBox.critical(self, "Error", resp)
			return
		self.updateQuery()

	def updateNameLabel(self):
		self.info_name_label.setText("{dbtype}/{name}: {location}".format(
			dbtype=self.parent.db_type, 
			name=self.parent.name, 
			location=self.parent.location))

	def updateTableInfo(self):
		tables = self.parent.db.getTables()
		string_arr = list()
		if tables:
			string_arr.append("Table Name: Column Name | Column Name | ...")
			for table_name in tables:
				string_arr.append(table_name + ": " +\
				" | ".join(tables[table_name]) if tables[table_name] else "No columns found")
		else:
			string_arr.append("No tables found")

		self.table_info.setText("\n".join(string_arr))

	def updateQuery(self):
		self.query_history_list.clear()
		query_history = self.parent.db.getHistory()
		for q_name in query_history:
			qe = QueryEntry(
				parent=self,
				name=q_name,
				query=query_history[q_name],
				delete_func=lambda: self.deleteQuery(q_name),
				exec_func=lambda: self.executeSelect(q_name))
			list_item = QtWidgets.QListWidgetItem(self.query_history_list)
			list_item.setSizeHint(qe.sizeHint())
			self.query_history_list.addItem(list_item)
			self.query_history_list.setItemWidget(list_item, qe)

	def displayQuery(self, item):
		qurey_entry = self.query_history_list.itemWidget(item)
		print("Display Query")
	
	def deleteQuery(self, name):
		self.parent.db.deleteHistory(name)
		self.updateQuery()

	def executeSelect(self, name):
		self.parent.db.executeSelect(name)
		self.updateQuery()

	# self.updateNameLabel()
	# self.updateTableInfo()
	# self.updateQuery()

if __name__ == "__main__":
	import sys
	class DB:
		def addSelectQuery(self, q_name, query):
			pass
		def getHistory(self):
			return {"test_query": {
				"query": "TEST QUERY",
				"col_names": ["test_col1","test_col2"],
				"data": [(1, 2), (3, 4)],
				"ran": True
			}}

		def getTables(self):
			return {"test_tb": ["test_col1","test_col2"]}

	class Parent(QtWidgets.QWidget):
		db_type = "test_type"
		name = "test_name"
		location = "test_location"
		db = DB()

	app = QtWidgets.QApplication(sys.argv)
	data_disp = DatabaseDisplay(None, Parent())
	data_disp.show()
	
	sys.exit(app.exec_())

