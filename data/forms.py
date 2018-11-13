import os 

from PyQt5 import QtWidgets 

from data.database import DB_TYPES

class DatabaseForm(QtWidgets.QMainWindow):
	def __init__(self, parent, change_call_back, name="", location="",dbtype=""):
		super(DatabaseForm, self).__init__(parent)

		self.change_call_back = change_call_back
		self.init_ui(cur_name=name, location=location, dbtype=dbtype)

	def init_ui(self, cur_name="", location="", dbtype=""):
		form_layout = QtWidgets.QVBoxLayout()

		# name input
		name_layout = QtWidgets.QHBoxLayout()
		name_layout.addWidget(QtWidgets.QLabel("Name:"))
		self.name_input = QtWidgets.QLineEdit()
		self.name_input.setText(cur_name)
		name_layout.addWidget(self.name_input)
		form_layout.addLayout(name_layout)

		# Location input
		location_layout = QtWidgets.QHBoxLayout()
		location_layout.addWidget(QtWidgets.QLabel("Location:"))
		self.location_input = QtWidgets.QLineEdit()
		self.location_input.setText(location)
		location_layout.addWidget(self.location_input)
		file_btn = QtWidgets.QPushButton("Open database")
		file_btn.clicked.connect(
			lambda:self.location_input.setText(
				QtWidgets.QFileDialog.getOpenFileName(
					self, 'Open database', os.getenv('HOME'))[0]))
		location_layout.addWidget(file_btn)
		form_layout.addLayout(location_layout)
		
		self.db_types = QtWidgets.QComboBox()
		for t in DB_TYPES.keys():
			self.db_types.addItem(t)
		if dbtype != "":
			self.db_types.setCurrentIndex(
				self.db_types.findText(dbtype))
		form_layout.addWidget(self.db_types)

		# Button - cancel
		button_layout = QtWidgets.QHBoxLayout()
		button_layout.addStretch()
		cancel_btn = QtWidgets.QPushButton("Cancel")
		cancel_btn.clicked.connect(self.close)
		button_layout.addWidget(cancel_btn)
		# Button - Delete
		delete_btn = QtWidgets.QPushButton("Delete")
		delete_btn.clicked.connect(
			lambda: self.makeChange(cur_name, "", "", ""))
		button_layout.addWidget(delete_btn)
		# Button - update / add
		update_btn = QtWidgets.QPushButton("Update")
		update_btn.clicked.connect(
			lambda: self.makeChange(
				cur_name,
				self.name_input.text(), 
				self.location_input.text(),
				self.db_types.currentText()))
		button_layout.addWidget(update_btn)
		form_layout.addLayout(button_layout)

		window_widget = QtWidgets.QWidget()
		window_widget.setLayout(form_layout)
		self.setCentralWidget(window_widget)
		self.show()

	def makeChange(self, old_name, name, location, dbtype):
		resp = self.change_call_back(old_name, name, location, dbtype)
		if not resp:
			self.close()
			return
		
		QtWidgets.QMessageBox.critical(self, "Error", resp)

		