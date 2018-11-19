import logging
from PyQt5 import QtWidgets 

class QueryDisplay(QtWidgets.QWidget):

	def __init__(self, col_names, rows, parent=None):
		super(QueryDisplay, self).__init__(parent)
		self.logger = logging.getLogger(__name__)
		
		self.col_names = col_names
		self.rows = rows

		self.init_ui()
		self.updateTable()

	def init_ui(self):
		main_layout = QtWidgets.QVBoxLayout()

		main_frame = QtWidgets.QFrame(self)
		main_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
		sub_layout = QtWidgets.QVBoxLayout(main_frame)
		
		self.tableWidget = QtWidgets.QTableWidget(self)
		sub_layout.addWidget(self.tableWidget) 
		
		main_layout.addWidget(main_frame)
		self.setLayout(main_layout) 

	def setColNames(self):
		self.col_names = col_names
		self.updateTable()
	def setRows(self):
		self.rows = rows 
		self.updateTable()

	def updateTable(self):
		# Create table
		self.tableWidget.setColumnCount(len(self.col_names))
		self.tableWidget.setRowCount(len(self.rows)+1)

		for col, name in enumerate(self.col_names):
			self.tableWidget.setItem(0,col, 
				QtWidgets.QTableWidgetItem(name))

		for row, row_values in enumerate(self.rows):
			for col, cell in enumerate(row_values):
				self.tableWidget.setItem(row+1, col,
					QtWidgets.QTableWidgetItem("{}".format(cell)))


if __name__ == "__main__":
	import sys
	app = QtWidgets.QApplication(sys.argv)
	
	query_disp = QueryDisplay(None, 
		["col_1", "col_2"], [(1,2),(2,3)])

	query_disp.show()
	
	sys.exit(app.exec_())