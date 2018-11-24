
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QScrollArea, QPushButton, QFileDialog

filenames = []


class TestGui(QWidget):
	def __init__(self):
		super(TestGui, self).__init__()
		self.lay = QHBoxLayout()
		self.sA = QScrollArea()
		self.sA_lay = QVBoxLayout()
		self.sA.setLayout(self.sA_lay)
		self.closeGui = QPushButton("Close")
		self.add_file_button = QPushButton("Add File")
		self.lay.addWidget(self.closeGui)
		self.lay.addWidget(self.add_file_button)
		self.lay.addWidget(self.sA)
		self.setLayout(self.lay)

		self.connect_()
		self.show()

	def connect_(self):
		self.add_file_button.clicked.connect(self.__add_file_to_list)
		self.closeGui.clicked.connect(self.close)
		return

	def __add_file_to_list(self):
		fname = QFileDialog.getOpenFileName()
		global filenames
		print(fname)
		filenames.append(fname[0])
		button = QPushButton(fname[0])
		self.sA_lay.addWidget(button)
		return


app = QApplication(sys.argv)
t = TestGui()
sys.exit(app.exec_())



