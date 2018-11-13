
from PyQt5 import QtWidgets 

try:
	from data.queryDisplay import QueryDisplay
except:
	from queryDisplay import QueryDisplay

class QueryEntry(QtWidgets.QWidget):
	def __init__ (self, parent, name, query, delete_func, exec_func):
		super(QueryEntry, self).__init__(parent)
		
		self.name = name 
		self.query = query

		self.num_entries = len(self.query["data"])
	
		self.delete_func = delete_func
		self.exec_func = exec_func
		self.init_ui()
		self.query_disp = QueryDisplay(None, self)

	def init_ui(self):
		info_layout = QtWidgets.QHBoxLayout()

		self.info_label = QtWidgets.QLabel()
		self.info_label.setText(
			"{name}: {cols} #({num_entries})".format(
				name=self.name, cols=", ".join(self.query["col_names"]), num_entries=len(self.query["data"])))
		info_layout.addWidget(self.info_label)

		self.delete_btn = QtWidgets.QPushButton("Delete")
		self.delete_btn.clicked.connect(self.delete_func)
		info_layout.addWidget(self.delete_btn)

		self.exec_btn = QtWidgets.QPushButton("Exec")
		self.exec_btn.clicked.connect(self.exec_func)
		info_layout.addWidget(self.exec_btn)

		self.setLayout(info_layout)

	def GetDisplay(self):
		return self.query_disp, "Query_{}".format(self.name)

	def getName(self):
		return self.name

if __name__ == "__main__":
	import sys
	app = QtWidgets.QApplication(sys.argv)
	query = {
		"col_names": ("test_name", "test_name2"),
		"data": [1]* 23
	}
	def delf():
		print("del")
	def execf():
		print("exec")
	qe = QueryEntry(None, "test_name", query, delf, execf)
	qe.show()
	
	sys.exit(app.exec_())

