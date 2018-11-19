import logging
from PyQt5 import QtWidgets 

class DatabaseEntry(QtWidgets.QWidget):
	def __init__ (self, name, location, db_type, parent=None):
		super(DatabaseEntry, self).__init__(parent)
		self.logger = logging.getLogger(__name__)

		self.name = name 
		self.location = location 
		self.db_type = db_type
		self.name_layout = "{dbtype}:{name}"
		self.init_ui()

	def init_ui(self):
		main_layout = QtWidgets.QVBoxLayout()

		main_frame = QtWidgets.QFrame(self)
		main_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
		sub_layout = QtWidgets.QVBoxLayout(main_frame)

		self.name_label = QtWidgets.QLabel()
		sub_layout.addWidget(self.name_label)
		self.setNameDBType()

		self.location_label = QtWidgets.QLabel()
		self.location_label.setText(self.location)
		sub_layout.addWidget(self.location_label)

		main_layout.addWidget(main_frame)
		self.setLayout(main_layout)

	def setNameDBType(self):
		self.name_label.setText(
			self.name_layout.format(
				dbtype=self.db_type, name=self.name))

	def setName(self, name):
		self.name = name
		self.setNameDBType()		

	def setLocation(self, location):
		self.location = location
		self.location_label.setText(self.location)
		
	def setType(self, db_type):
		self.db_type = db_type
		self.setNameDBType()

	def __str__(self):
		return "{dbtype}/{name}:{location}".format(
			dbtype=self.db_type, name=self.name, location=self.location)

if __name__ == "__main__":
	import sys

	app = QtWidgets.QApplication(sys.argv)

	de = DatabaseEntry(None, "test_name", "test.db", "SQLite")
	de.show()
	
	sys.exit(app.exec_())


