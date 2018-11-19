import logging
from PyQt5 import QtWidgets 

class DatabaseDisplay(QtWidgets.QWidget):
	def __init__(self, name, db_type, location, item_callback, add_callback, parent=None):
		super(DatabaseDisplay, self).__init__(parent)
		self.logger = logging.getLogger(__name__)

		self.name = name
		self.location = location 
		self.db_type = db_type

		self.parent = parent

		self.init_ui(item_callback, add_callback)

	def init_ui(self, item_callback, add_callback):
		main_layout = QtWidgets.QVBoxLayout()

		main_frame = QtWidgets.QFrame(self)
		main_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
		sub_layout = QtWidgets.QVBoxLayout(main_frame)
		
		self.info_name_label = QtWidgets.QLabel()
		self.updateNameLabel()
		sub_layout.addWidget(self.info_name_label)

		# Table Info
		self.table_info = QtWidgets.QLabel()
		sub_layout.addWidget(self.table_info)
		
		# Existing 
		self.query_history_list = QtWidgets.QListWidget()
		self.query_history_list.itemDoubleClicked.connect(
			lambda item: item_callback(self.query_history_list.itemWidget(item)))
		sub_layout.addWidget(self.query_history_list)

		# New Select Query executeSelect
		query_layout = QtWidgets.QGridLayout()
		query_layout.setColumnStretch(2, 6)
		query_description_name = QtWidgets.QLabel()
		query_description_name.setText("Name")
		query_layout.addWidget(query_description_name, 0, 0)
		query_description = QtWidgets.QLabel()
		query_description.setText("SQL Qurey. e.g. SELECT tbName.colName FROM tbName ...")
		query_layout.addWidget(query_description, 0, 1)
		
		self.query_name = QtWidgets.QLineEdit()
		self.query_input = QtWidgets.QLineEdit()
		query_add = QtWidgets.QPushButton("Add")
		query_add.clicked.connect(
			lambda: add_callback(
				self.name,
				self.query_name.text(),
				self.query_input.text()))

		query_layout.addWidget(self.query_name, 1, 0)
		query_layout.addWidget(self.query_input, 1, 1)
		query_layout.addWidget(query_add, 1, 4)

		sub_layout.addLayout(query_layout)

		sub_layout.addStretch()

		main_layout.addWidget(main_frame)
		self.setLayout(main_layout)

	def updateNameLabel(self):
		self.info_name_label.setText("{dbtype}/{name}: {location}".format(
			dbtype=self.db_type, 
			name=self.name, 
			location=self.location))

	def updateTableInfo(self, tables):
		string_arr = list()
		if tables:
			string_arr.append("Table Name: Column Name | Column Name | ...")
			for table_name in tables:
				string_arr.append(table_name + ": " +\
				" | ".join(tables[table_name]) if tables[table_name] else "No columns found")
		else:
			string_arr.append("No tables found")

		self.table_info.setText("\n".join(string_arr))

	def updateQueries(self, widgets):
		self.query_history_list.clear()
		for w in widgets:
			list_item = QtWidgets.QListWidgetItem(self.query_history_list)
			list_item.setSizeHint(w.sizeHint())
			self.query_history_list.addItem(list_item)
			self.query_history_list.setItemWidget(list_item, w)

if __name__ == "__main__":
	import sys
	app = QtWidgets.QApplication(sys.argv)

	test_label = QtWidgets.QLabel()
	test_label.setText("test content")

	def item(widget):
		print("item:", widget.text())

	data_disp = None
	def add(name, query):
		print("add:", name, query)
		data_disp.updateQueries([test_label])

	
	data_disp = DatabaseDisplay(None, 
		name="dbname", db_type="dbtype", location="location", 
		item_callback=item, add_callback=add)

	data_disp.show()
	
	sys.exit(app.exec_())

