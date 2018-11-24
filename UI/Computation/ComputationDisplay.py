import logging
from PyQt5 import QtWidgets

class ComputationDisplay(QtWidgets.QWidget):
	def __init__(self, parent=None):
		super(ComputationDisplay, self).__init__(parent)

		self.init_ui()

	def init_ui(self):
		layout = QtWidgets.QVBoxLayout()

		self.result_table = QtWidgets.QTableWidget(self)
		layout.addWidget(self.result_table)

		self.text_area = QtWidgets.QTextEdit()
		layout.addWidget(self.text_area)

		process_btn = QtWidgets.QPushButton("Enter")
		process_btn.clicked.connect(self.processInput)
		layout.addWidget(process_btn)

		self.setLayout(layout) 

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
	