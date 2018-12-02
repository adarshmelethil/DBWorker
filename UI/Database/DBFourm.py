import os 
import logging
from PyQt5 import QtWidgets 

class DatabaseFourm(QtWidgets.QMainWindow):
	def __init__(self, name, location, db_type, all_db_types, update_callback, parent=None):
		super(DatabaseFourm, self).__init__(parent)
		self.logger = logging.getLogger(__name__)
		
		self.name = name 
		self.location = location 
		self.db_type = db_type 
		self.all_db_types = all_db_types

		self.update_callback = update_callback
		self.init_ui()

	def init_ui(self):
		main_frame = QtWidgets.QFrame(self)
		main_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
		sub_layout = QtWidgets.QVBoxLayout(main_frame)

		# name input
		name_layout = QtWidgets.QHBoxLayout()
		name_layout.addWidget(QtWidgets.QLabel("Name:"))
		self.name_input = QtWidgets.QLineEdit()
		self.name_input.setText(self.name)
		name_layout.addWidget(self.name_input)
		sub_layout.addLayout(name_layout)

		# Location input
		location_layout = QtWidgets.QHBoxLayout()
		location_layout.addWidget(QtWidgets.QLabel("Location:"))

		self.location_input = QtWidgets.QLineEdit()
		self.location_input.setText(self.location)
		location_layout.addWidget(self.location_input)
		file_btn = QtWidgets.QPushButton("Open database")
		file_btn.clicked.connect(
			lambda:self.setLocation(
				QtWidgets.QFileDialog.getOpenFileName(
					self, 'Open database', os.getenv('HOME'))[0]))
		location_layout.addWidget(file_btn)
		sub_layout.addLayout(location_layout)
		
		self.db_types = QtWidgets.QComboBox()
		for t in self.all_db_types:
			self.db_types.addItem(t)
		if self.db_type in self.all_db_types:
			self.db_types.setCurrentIndex(
				self.db_types.findText(self.db_type))
		sub_layout.addWidget(self.db_types)

		# Button - cancel
		button_layout = QtWidgets.QHBoxLayout()
		button_layout.addStretch()
		cancel_btn = QtWidgets.QPushButton("Cancel")
		cancel_btn.clicked.connect(self.close)
		button_layout.addWidget(cancel_btn)
		# Button - Delete
		delete_btn = QtWidgets.QPushButton("Delete")
		delete_btn.clicked.connect(self.callDelete)
		button_layout.addWidget(delete_btn)
		# Button - update / add
		update_btn = QtWidgets.QPushButton("Update")
		update_btn.clicked.connect(self.callUpdate)
		button_layout.addWidget(update_btn)
		sub_layout.addLayout(button_layout)

		self.setCentralWidget(main_frame)
		self.show()

	def setName(self, name):
		self.name = name 
		self.name_input.setText(self.name)

	def setLocation(self, location):
		self.location = location
		self.location_input.setText(self.location)

	def callDelete(self):
		resp = self.update_callback(self.name,"","","")
		if not resp:
			self.close()
			return
		QtWidgets.QMessageBox.critical(self, "Failed to delete:", resp)

	def callUpdate(self):
		resp = self.update_callback(self.name, 
			self.name_input.text(), 
			self.location_input.text(),
			self.db_types.currentText())
		if not resp:
			self.close()
			return
		QtWidgets.QMessageBox.critical(self, "Failed to update:", resp)

if __name__=="__main__":
	import sys
	app = QtWidgets.QApplication(sys.argv)
	
	def update(old_name, new_name, location, dbtype):
		print("update: '{}' -> '{}', '{}', '{}'".format(old_name, new_name, location, dbtype))

	dbf = DatabaseFourm(None, 
		name="cur_name", location="cur_location", db_type="a", 
		all_db_types=["a","b"], update_callback=update)

	dbf.show()
	
	sys.exit(app.exec_())


