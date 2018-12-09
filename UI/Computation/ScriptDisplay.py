import logging
from PyQt5 import QtWidgets

class ScriptDisplay(QtWidgets.QWidget):
	def __init__(self, location, exec_callback, parent=None):
		super(ScriptDisplay, self).__init__(parent)

		self.location = location

		self.init_ui(exec_callback)

	def init_ui(self, exec_callback):
		main_layout = QtWidgets.QVBoxLayout()

		main_frame = QtWidgets.QFrame(self)
		main_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
		sub_layout = QtWidgets.QVBoxLayout(main_frame)

		self.text_area = QtWidgets.QTextEdit()
		sub_layout.addWidget(self.text_area)

		button_layout = QtWidgets.QHBoxLayout()
		load_button = QtWidgets.QPushButton("Load")
		load_button.clicked.connect(self.load)
		button_layout.addWidget(load_button)

		save_button = QtWidgets.QPushButton("Save")
		save_button.clicked.connect(self.save)
		button_layout.addWidget(save_button)

		exec_button = QtWidgets.QPushButton("execute")
		exec_button.clicked.connect(
			lambda: exec_callback(self.text_area.toPlainText()))
		button_layout.addWidget(exec_button)
		sub_layout.addLayout(button_layout)

		main_layout.addWidget(main_frame)
		self.setLayout(main_layout)
		self.load()

	def load(self):
		with open(self.location, "r") as _file:
			self.text_area.setText(_file.read())

	def save(self):
		with open(self.location, "w") as _file:
			_file.write(self.text_area.toPlainText())

	def createTable(self, col_names, col_values):
		# Create table
		self.result_table.setColumnCount(len(col_names))
		self.result_table.setRowCount(len(col_values)+1)

		for col, name in enumerate(col_names):
			self.result_table.setItem(0,col,
				QtWidgets.QTableWidgetItem(name))

		for row, row_values in enumerate(col_values):
			for col, cell in enumerate(row_values):
				self.result_table.setItem(row+1, col,
					QtWidgets.QTableWidgetItem("{}".format(cell)))
	