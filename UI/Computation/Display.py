import logging
from PyQt5 import QtWidgets

class ComputationDisplay(QtWidgets.QWidget):
	def __init__(self, name, parent=None):
		super(ComputationDisplay, self).__init__(parent)


		self.init_ui()

	def init_ui(self):
		main_layout = QtWidgets.QVBoxLayout()

		main_frame = QtWidgets.QFrame(self)
		main_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
		sub_layout = QtWidgets.QVBoxLayout(main_frame)

		self.text_area = QtWidgets.QTextEdit()
		sub_layout.addWidget(self.text_area)

		

		main_layout.addWidget(main_frame)
		self.setLayout(main_layout)

	def processInput(self):
		text = self.text_area.toPlainText()
		print(parseRawText)

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
	