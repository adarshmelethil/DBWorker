import logging
from PyQt5 import QtWidgets 
from PyQt5.QtCore import Qt

class MainWindow(QtWidgets.QWidget):
	def __init__(self, top_left, top_center, top_right, bottom, parent=None):
		super(MainWindow, self).__init__(parent)
		self.logger = logging.getLogger(__name__)
		
		self.init_ui(top_left, top_center, top_right, bottom)

	def init_ui(self, top_left, top_center, top_right, bottom):
		main_layout = QtWidgets.QVBoxLayout()

		main_frame = QtWidgets.QFrame(self)
		main_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
		sub_layout = QtWidgets.QHBoxLayout(main_frame)
		
		# hbox = QtWidgets.QHBoxLayout()

		horizontal_splitter = QtWidgets.QSplitter(Qt.Horizontal)
		horizontal_splitter.addWidget(top_left)
		horizontal_splitter.addWidget(top_center)
		horizontal_splitter.addWidget(top_right)

		vertical_splitter = QtWidgets.QSplitter(Qt.Vertical)
		vertical_splitter.addWidget(horizontal_splitter)
		vertical_splitter.addWidget(bottom)
		sub_layout.addWidget(vertical_splitter)
		
		main_layout.addWidget(main_frame)
		self.setLayout(main_layout)

if __name__=="__main__":
	import sys
	app = QtWidgets.QApplication(sys.argv)

	t_l = QtWidgets.QLabel("top left")
	t_c = QtWidgets.QLabel("top center")
	t_r = QtWidgets.QLabel("top right")
	b = QtWidgets.QLabel("bottom")

	m = MainWindow(None,
		top_left=t_l,
		top_center=t_c,
		top_right=t_r,
		bottom=b)

	m.show()

	sys.exit(app.exec_())

