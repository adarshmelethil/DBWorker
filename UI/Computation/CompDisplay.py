
import logging
from PyQt5 import QtWidgets 

class ComputationDisplay(QtWidgets.QWidget):
	def __init__(self, val_dicts, parent=None):
		super(ComputationDisplay, self).__init__(parent)
		self.logger = logging.getLogger(__name__)
		
		self.val_dicts = val_dicts

		self.init_ui()
		

	def init_ui(self):
		main_layout = QtWidgets.QVBoxLayout()

		main_frame = QtWidgets.QFrame(self)
		main_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
		sub_layout = QtWidgets.QVBoxLayout(main_frame)
		
		self.tableWidget = QtWidgets.QTableWidget(self)
		sub_layout.addWidget(self.tableWidget) 
		
		main_layout.addWidget(main_frame)
		self.setLayout(main_layout)
		self.updateTable()

	def updateTable(self):
		# Create table
		self.tableWidget.setColumnCount(len(self.val_dicts.keys()))
		max_row = -1
		for v in self.val_dicts:
			if len(v) > max_row:
				max_row = len(v)
		self.tableWidget.setRowCount(len(max_row)+1)

		for col, name in enumerate(self.val_dicts):
			self.tableWidget.setItem(0,col, 
				QtWidgets.QTableWidgetItem(name))
			for row, val in enumerate(self.val_dicts[name]):
				self.tableWidget.setItem(row+1, col,
					QtWidgets.QTableWidgetItem("{}".format(cell)))

if __name__ == "__main__":
	import sys
	app = QtWidgets.QApplication(sys.argv)
	
	comp_disp = ComputationDisplay( 
		val_dicts={"col_1":[1,2], "col_2":[2,3]})
	comp_disp.show()
	
	sys.exit(app.exec_())