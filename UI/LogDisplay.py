
from PyQt5 import QtWidgets 
from PyQt5 import QtGui

class LogDisplay(QtWidgets.QWidget):
	def __init__ (self, title="Logs", parent=None):
		super(LogDisplay, self).__init__(parent)

		self.log = ""
		self.init_ui(title)

	def init_ui(self, title):
		main_layout = QtWidgets.QVBoxLayout()

		main_frame = QtWidgets.QFrame(self)
		main_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
		sub_layout = QtWidgets.QVBoxLayout(main_frame)

		title_label = QtWidgets.QLabel(title)
		sub_layout.addWidget(title_label)

		self.log_output = QtWidgets.QTextEdit()
		self.log_output.moveCursor(QtGui.QTextCursor.End)
		self.log_output.setReadOnly(True)
		self.log_output.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
		font = self.log_output.font()
		font.setFamily("Courier")
		font.setPointSize(10)
		sub_layout.addWidget(self.log_output)

		main_layout.addWidget(main_frame)
		self.setLayout(main_layout)

	def addLogging(self, new_log):
		self.log += " - " * 10 + "\n"
		self.log += new_log + "\n"
		self.log_output.setText(self.log)

	def clear(self):
		self.log = ""
		self.log_output.setText(self.log)
