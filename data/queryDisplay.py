
from PyQt5 import QtWidgets 

class QueryDisplay(QtWidgets.QWidget):

	def __init__(self, container, parent):
		super(QueryDisplay, self).__init__(container)
		
		self.parent = parent

		self.init_ui()

	def init_ui(self):
		layout = QtWidgets.QVBoxLayout()
		
		self.tableWidget = QtWidgets.QTableWidget(self)
		self.createTable(self.parent.query["col_names"], self.parent.query["data"])
		layout.addWidget(self.tableWidget) 
		
		self.setLayout(layout) 

	def createTable(self, col_names, col_values):
		# Create table
		self.tableWidget.setColumnCount(len(col_names))
		self.tableWidget.setRowCount(len(col_values)+1)

		for col, name in enumerate(col_names):
			self.tableWidget.setItem(0,col, 
				QtWidgets.QTableWidgetItem(name))

		for row, row_values in enumerate(col_values):
			for col, cell in enumerate(row_values):
				self.tableWidget.setItem(row+1, col,
					QtWidgets.QTableWidgetItem("{}".format(cell)))
