
import os
from PyQt5 import QtWidgets 

class ScriptEntry(QtWidgets.QWidget):
	def __init__ (self, location, delete_callback, parent=None):
		super(ScriptEntry, self).__init__(parent)

		self.location = location

		self.init_ui(delete_callback)

	def init_ui(self, delete_callback):
		main_layout = QtWidgets.QVBoxLayout()

		main_frame = QtWidgets.QFrame(self)
		main_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
		sub_layout = QtWidgets.QVBoxLayout(main_frame)

		self.name_label = QtWidgets.QLabel()
		self.name_label.setText(self.getName())
		sub_layout.addWidget(self.name_label)

		self.location_label = QtWidgets.QLabel()
		self.location_label.setText(self.location)
		sub_layout.addWidget(self.location_label)

		delete_button = QtWidgets.QPushButton("Delete")
		delete_button.clicked.connect(
			lambda: delete_callback(self.location))
		sub_layout.addWidget(delete_button)

		main_layout.addWidget(main_frame)
		self.setLayout(main_layout)

	def getLocation(self):
		return self.location

	def getName(self):
		return os.path.basename(self.location)

