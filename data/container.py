
import os

from PyQt5 import QtWidgets

from data.forms import DatabaseForm
from data.dbEntry import DatabaseEntry

class DatabaseContainer(QtWidgets.QWidget):
	def __init__(self, container, parent):
		super().__init__(container)

		self.parent = parent

		self.init_ui()

	def init_ui(self):
		v_box = QtWidgets.QVBoxLayout()

		title = QtWidgets.QLabel()
		title.setText("Data")
		v_box.addWidget(title)

		self.db_list = QtWidgets.QListWidget()
		self.db_list.itemClicked.connect(
			lambda item: DatabaseForm(self, self.updateDB, 
				self.db_list.itemWidget(item).name, 
				self.db_list.itemWidget(item).location,
				self.db_list.itemWidget(item).db_type))
		self.db_list.itemClicked.connect(
			lambda item: self.parent.updateTab(
				*self.db_list.itemWidget(item).GetDisplay()))
		v_box.addWidget(self.db_list)

		add_btn = QtWidgets.QPushButton("+")
		add_btn.clicked.connect(
			lambda: DatabaseForm(self, self.updateDB))
		h_box = QtWidgets.QHBoxLayout()
		h_box.addStretch()
		h_box.addWidget(add_btn)
		h_box.addStretch()
		v_box.addLayout(h_box)

		self.setLayout(v_box)

	def updateDB(self, old_name, new_name, location, dbtype):
		if old_name == "":
			if new_name == "" or location == "":
				return "Name and location can not be empty"
			# No duplicate names allowed
			for db_index in range(self.db_list.count()):
				db = self.db_list.itemWidget(self.db_list.item(db_index))
				if db.name == new_name:
					return "Name '{name}' already in use".format(name=new_name)
			# New
			new_db = DatabaseEntry(self, new_name, location, dbtype)
			new_db_item = QtWidgets.QListWidgetItem(self.db_list)
			new_db_item.setSizeHint(new_db.sizeHint())
			self.db_list.addItem(new_db_item)
			self.db_list.setItemWidget(new_db_item, new_db)
			return
		for db_index in range(self.db_list.count()):
			db = self.db_list.itemWidget(self.db_list.item(db_index))
			if db.name == old_name:
				# Delete
				if new_name == "" and location == "":
					self.db_list.takeItem(db_index)
					return
				if old_name != new_name:
					for db_index2 in range(self.db_list.count()):
						db2 = self.db_list.itemWidget(self.db_list.item(db_index2))
						if db2.getName() == new_name:
							return "Name '{name}' already in use".format(name=new_name)
				# Update
				db.setName(new_name)
				db.setLocation(location)
				db.setType(dbtype)
				return
		return "Failed to find '{name}'".format(name=old_name)

if __name__ == "__main__":
	import sys
	app = QtWidgets.QApplication(sys.argv)
	
	msa = DatabaseContainer(None)
	msa.show()

	sys.exit(app.exec_())