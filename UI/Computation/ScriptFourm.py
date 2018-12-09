import os 
import logging
from PyQt5 import QtWidgets 

class ScriptFourm(QtWidgets.QMainWindow):
	def __init__(self, location, update_callback, parent=None):
		super(ScriptFourm, self).__init__(parent)
		self.logger = logging.getLogger(__name__)

		self.location = location 

		self.update_callback = update_callback
		self.init_ui()

	def init_ui(self):
		main_frame = QtWidgets.QFrame(self)
		main_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
		sub_layout = QtWidgets.QVBoxLayout(main_frame)

		# Location input
		location_layout = QtWidgets.QHBoxLayout()
		location_layout.addWidget(QtWidgets.QLabel("Location:"))

		self.location_input = QtWidgets.QLineEdit()
		self.setLocation(self.location)
		location_layout.addWidget(self.location_input)
		file_btn = QtWidgets.QPushButton("Open Script")
		file_btn.clicked.connect(
			lambda:self.setLocation(QtWidgets.QFileDialog.getOpenFileName(
					self, 'Open Script', os.getenv('HOME'))[0]))
		location_layout.addWidget(file_btn)
		sub_layout.addLayout(location_layout)

		# Button - cancel
		button_layout = QtWidgets.QHBoxLayout()
		button_layout.addStretch()
		cancel_btn = QtWidgets.QPushButton("Cancel")
		cancel_btn.clicked.connect(self.close)
		button_layout.addWidget(cancel_btn)
		
		# Button - update / add
		update_btn = QtWidgets.QPushButton("Update")
		update_btn.clicked.connect(self.callUpdate)
		button_layout.addWidget(update_btn)
		
		sub_layout.addLayout(button_layout)

		self.setCentralWidget(main_frame)
		self.show()

	def setLocation(self, location):
		self.location = location
		self.location_input.setText(self.location)

	def callUpdate(self):
		resp = self.update_callback(
			self.location_input.text())
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

