
import os
from PyQt5 import QtWidgets 

class ComputationEntry(QtWidgets.QWidget):
	def __init__ (self, location, parent=None):
		super(ComputationEntry, self).__init__(parent)

		self.location = location

		self.init_ui()

	def init_ui(self):
		main_layout = QtWidgets.QVBoxLayout()

		main_frame = QtWidgets.QFrame(self)
		main_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
		sub_layout = QtWidgets.QVBoxLayout(main_frame)

		self.name_label = QtWidgets.QLabel()
		self.name_label.setText(os.path.basename(self.location))
		sub_layout.addWidget(self.name_label)

		self.location_label = QtWidgets.QLabel()
		self.location_label.setText(self.location)
		sub_layout.addWidget(self.location_label)

		main_layout.addWidget(main_frame)
		self.setLayout(main_layout)

	def getLocation(self):
		return self.location

