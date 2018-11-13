
from PyQt5 import QtWidgets 

try:
	from data.database import getDatabase
	from data.dbDisplay import DatabaseDisplay
except ImportError:
	from database import getDatabase 
	from dbDisplay import DatabaseDisplay

class DatabaseEntry(QtWidgets.QWidget):
	def __init__ (self, parent, name, location, db_type):
		super(DatabaseEntry, self).__init__(parent)
		self.parent = parent

		self.name = name 
		self.location = location
		self.db_type = db_type

		self.db = getDatabase(self.db_type, location=location)
		self.init_ui()
		self.db_disp = DatabaseDisplay(None, self)

	def GetDisplay(self):
		return self.db_disp, "DB_{}".format(self.name)

	def init_ui(self):
		self.data_layout = QtWidgets.QVBoxLayout()

		self.name_label = QtWidgets.QLabel()
		self.name_label.setText(self.name)
		self.data_layout.addWidget(self.name_label)

		self.location_label = QtWidgets.QLabel()
		self.location_label.setText(self.location)
		self.data_layout.addWidget(self.location_label)

		self.setLayout(self.data_layout)

	def setName(self, name):
		self.name = name
		self.name_label.setText(self.name)
		self.db_disp.updateNameLabel()

	def setLocation(self, location):
		self.location = location
		self.location_label.setText(self.location)
		self.db_disp.updateNameLabel()

	def setType(self, db_type):
		self.db_type = db_type
		self.db = getDatabase(db_type=self.db_type, location=self.location)	
		self.db_disp.updateTableInfo()
		self.db_disp.updateQuery()
		self.db_disp.updateNameLabel()
		
if __name__ == "__main__":
	import sys
	app = QtWidgets.QApplication(sys.argv)

	de = DatabaseEntry(None, "test_name", "test.db", "SQLite")
	de.show()
	
	sys.exit(app.exec_())


