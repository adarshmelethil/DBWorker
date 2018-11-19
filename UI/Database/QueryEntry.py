import logging
from PyQt5 import QtWidgets 

class QueryEntry(QtWidgets.QWidget):
	def __init__ (self, name, col_names, num_of_results, delete_callback, exec_callback, parent=None):
		super(QueryEntry, self).__init__(parent)
		self.logger = logging.getLogger(__name__)
		
		self.name = name 
		self.col_names = col_names
		self.num_of_results = num_of_results
	
		self.init_ui(delete_callback, exec_callback)
		self.setInfo()

	def init_ui(self, delete_callback, exec_callback):
		main_layout = QtWidgets.QVBoxLayout()

		main_frame = QtWidgets.QFrame(self)
		main_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
		sub_layout = QtWidgets.QHBoxLayout(main_frame)

		self.info_label = QtWidgets.QLabel()
		sub_layout.addWidget(self.info_label)

		self.delete_btn = QtWidgets.QPushButton("Delete")
		self.delete_btn.clicked.connect(
			lambda: delete_callback(self.name))
		sub_layout.addWidget(self.delete_btn)

		self.exec_btn = QtWidgets.QPushButton("Exec")
		self.exec_btn.clicked.connect(
			lambda: exec_callback(self.name))
		sub_layout.addWidget(self.exec_btn)

		main_layout.addWidget(main_frame)
		self.setLayout(main_layout)
		
	def setInfo(self):
		self.info_label.setText(
			"{name}: {cols} |#({num_entries})".format(
				name=self.name, 
				cols=", ".join(self.col_names), 
				num_entries=self.num_of_results))

	def setName(self, name):
		self.name = name 
		self.setInfo()

	def setColumnNames(self, col_names):
		self.col_names = col_names 
		self.setInfo()

	def setNumberOfResults(self, num_of_results):
		self.num_of_results = num_of_results
		self.setInfo()

if __name__ == "__main__":
	import sys
	app = QtWidgets.QApplication(sys.argv)

	def delFunc(name):
		print("del:", name)

	def execFunc(name):
		print("exec", name)

	qe = QueryEntry(None,
		name="qname",
		col_names=("col1", "col2"),
		num_of_results=123,
		delete_callback=delFunc,
		exec_callback=execFunc)

	qe.show()
	
	sys.exit(app.exec_())

