
import logging
from PyQt5 import QtWidgets 
import numpy as np 
import csv

class ComputationDisplay(QtWidgets.QWidget):
	def __init__(self, parent=None):
		super(ComputationDisplay, self).__init__(parent)
		self.logger = logging.getLogger(__name__)
		
		self.val_dicts = dict()

		self.init_ui()
		
	def setAddCol(self, name, values):
		self.val_dicts[name] = values
		self.updateTable()

	def clearTable(self):
		self.val_dicts = dict()
		self.updateTable()

	def init_ui(self):
		main_layout = QtWidgets.QVBoxLayout()

		main_frame = QtWidgets.QFrame(self)
		main_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
		sub_layout = QtWidgets.QVBoxLayout(main_frame)
		
		self.tableWidget = QtWidgets.QTableWidget(self)
		sub_layout.addWidget(self.tableWidget) 
		
		button_layout = QtWidgets.QHBoxLayout()
		export_btn = QtWidgets.QPushButton("Export To CSV")
		export_btn.clicked.connect(self.exportCSV)
		button_layout.addWidget(export_btn)
		button_layout.addStretch()
		sub_layout.addLayout(button_layout) 

		main_layout.addWidget(main_frame)
		self.setLayout(main_layout)
		self.updateTable()

	def getVal(self, arr, index):
		if type(arr) is np.ndarray:
			if index >= arr.shape[0]:
				return 0
			else:
				return arr[index]
		elif type(arr) is list:
			if index >= len(arr):
				return 0
			else:
				return arr[index] 
		else:
			if index == 0:
				return arr
			else:
				0

	def exportCSV(self):
		filename = QtWidgets.QFileDialog.getSaveFileName()
		with open(filename[0], 'w') as csv_file:
			writer = csv.writer(csv_file)

			keys = self.val_dicts.keys()
			writer.writerow(keys)
			max_len = -1
			for k, v in self.val_dicts.items():
				if type(v) is np.ndarray:
					cur_len = v.shape[0]
				elif type(v) is list:
					cur_len = len(v)
				else:
					cur_len = 1
				if max_len < cur_len:
					max_len = cur_len
			for i in range(max_len):
				cur_row = []
				for k in keys:
					cur_row.append(self.getVal(self.val_dicts[k], i))
				writer.writerow(cur_row)

	def updateTable(self):
		# Create table
		self.tableWidget.setColumnCount(len(self.val_dicts.keys()))
		max_row = -1
		for n, v in self.val_dicts.items():
			if type(v) is np.ndarray:
				max_row = v.shape[0]
			elif type(v) is list:
				if len(v) > max_row:
					max_row = len(v)
			else:
				max_row = 1
		self.tableWidget.setRowCount(max_row+1)

		for col, name in enumerate(self.val_dicts):
			self.tableWidget.setItem(0,col, 
				QtWidgets.QTableWidgetItem(name))
			if type(self.val_dicts[name]) is np.ndarray:
				for (row, val) in np.ndenumerate(self.val_dicts[name]):
					self.tableWidget.setItem(row[0]+1, col,
						QtWidgets.QTableWidgetItem("{}".format(val)))
			elif type(self.val_dicts[name]) is list:
				for row, val in enumerate(self.val_dicts[name]):
					self.tableWidget.setItem(row+1, col,
						QtWidgets.QTableWidgetItem("{}".format(val)))
			else:
				self.tableWidget.setItem(1, col,
					QtWidgets.QTableWidgetItem("{}".format(self.val_dicts[name])))

if __name__ == "__main__":
	import sys
	app = QtWidgets.QApplication(sys.argv)
	
	comp_disp = ComputationDisplay( 
		val_dicts={"col_1":[1,2], "col_2":[2,3]})
	comp_disp.show()
	
	sys.exit(app.exec_())