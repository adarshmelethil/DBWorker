
from PyQt5 import QtWidgets 

class ComputationEntry(QtWidgets.QWidget):
	def __init__ (self, container, parent, name):
		super(ComputationEntry, self).__init__(container)

		self.parent = parent
		self.name = name 

		self.init_ui()
		self.comp_disp = ComputationDisplay(None, self)

	def init_ui(self):
		layout = QtWidgets.QHBoxLayout()
		
		self.name_label = QtWidgets.QLabel()
		self.name_label.setText(self.name)
		layout.addWidget(self.name_label)

		layout.addStretch()

		del_btn = QtWidgets.QPushButton("delete")
		del_btn.clicked.connect(
			lambda: self.parent.deleteComputation(self.name))
		layout.addWidget(del_btn)

		self.setLayout(layout)

	def GetDisplay(self):
		return self.comp_disp, "COMP_{}".format(self.name)

