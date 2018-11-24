import sys
from PyQt5 import QtWidgets

class Example(QtWidgets.QWidget):
	
	def __init__(self):
		super().__init__()
		
		self.initUI()
		
		
	def initUI(self):
		
		# self.statusBar().showMessage('Ready')
	
		# main_layout = QtWidgets.QGridLayout()
		# main_layout.setColumnStretch(1, 4)

		# label = QtWidgets.QLabel()
		# label.setText("Hello")

		# main_layout.addWidget(label, 0, 0, 1, 1)
		# self.setLayout(main_layout)

		self.setGeometry(300, 300, 250, 150)
		self.setWindowTitle('Statusbar')	
		self.show()


if __name__ == '__main__':
	
	app = QtWidgets.QApplication(sys.argv)
	ex = Example()
	
	main_layout = QtWidgets.QGridLayout()
	main_layout.setColumnStretch(1, 4)

	label = QtWidgets.QLabel()
	label.setText("Hello")

	main_layout.addWidget(label, 0, 0, 1, 1)

	ex.setLayout(main_layout)

	sys.exit(app.exec_())