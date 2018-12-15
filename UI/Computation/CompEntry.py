
import os
from PyQt5 import QtWidgets 
import numpy as np 

class CompEntry(QtWidgets.QWidget):
	def __init__ (self, name, val, parent=None):
		super(CompEntry, self).__init__(parent)

		self.name = name 
		self.val = val
		self.getValString()

		self.init_ui()

	def getValString(self):
		if type(self.val) is list:
			if len(self.val) > 10:
				self.val_string = "list<{}>".format(len(self.val))
			else:
				self.val_string = "{}".format(self.val)
		elif type(self.val) is np.ndarray:
			_toolarge = False
			for _l in self.val.shape:
				if _l > 10:
					_toolarge = True
					break 
			if _toolarge:
				self.val_string = "Matrix shape: {}".format(self.val.shape)
			else:
				self.val_string = "\n{}".format(self.val)
		else:
			self.val_string = "{}".format(self.val)

	def init_ui(self):
		main_layout = QtWidgets.QVBoxLayout()

		main_frame = QtWidgets.QFrame(self)
		main_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
		sub_layout = QtWidgets.QVBoxLayout(main_frame)

		self.name_label = QtWidgets.QLabel()
		self.name_label.setText(self.name)
		sub_layout.addWidget(self.name_label)

		self.value_label = QtWidgets.QLabel()
		self.value_label.setText(self.val_string)
		sub_layout.addWidget(self.value_label)

		main_layout.addWidget(main_frame)
		self.setLayout(main_layout)

	def getLocation(self):
		return self.location

	def getName(self):
		return os.path.basename(self.location)

