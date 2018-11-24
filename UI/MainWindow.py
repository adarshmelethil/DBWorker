import logging
from PyQt5 import QtWidgets 
from PyQt5.QtCore import Qt

class MainWindow(QtWidgets.QWidget):
	def __init__(self, left_top, left_bottom, center, right_top, right_bottom, parent=None):
		super(MainWindow, self).__init__(parent)
		self.logger = logging.getLogger(__name__)
		
		self.init_ui(left_top, left_bottom, center, right_top, right_bottom)

	def init_ui(self, left_top, left_bottom, center, right_top, right_bottom):
		main_layout = QtWidgets.QVBoxLayout()

		main_frame = QtWidgets.QFrame(self)
		main_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
		sub_layout = QtWidgets.QHBoxLayout(main_frame)
		
		# hbox = QtWidgets.QHBoxLayout()
		left_splitter = QtWidgets.QSplitter(Qt.Vertical)
		if left_top is not None:
			left_splitter.addWidget(left_top)
		if left_bottom is not None:
			left_splitter.addWidget(left_bottom)

		right_splitter = QtWidgets.QSplitter(Qt.Vertical)
		if right_top is not None:
			right_splitter.addWidget(right_top)
		if right_bottom is not None:
			right_splitter.addWidget(right_bottom)

		main_splitter = QtWidgets.QSplitter(Qt.Horizontal)
		main_splitter.addWidget(left_splitter)
		if center is not None:
			main_splitter.addWidget(center)
		main_splitter.addWidget(right_splitter)

		sub_layout.addWidget(main_splitter)
		
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

