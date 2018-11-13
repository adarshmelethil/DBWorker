
from data import DatabaseContainer
from computation import ComputationContainer

from PyQt5 import QtWidgets 

class TabDisplay(QtWidgets.QWidget):
	def __init__(self, parent):
		super(TabDisplay, self).__init__(parent)

		self.init_ui()

	def init_ui(self):
		self.layout = QtWidgets.QVBoxLayout(self)

		self.tabs = QtWidgets.QTabWidget()
		self.tabs.setTabsClosable(True)
		self.tabs.setMovable(True)
		self.tabs.tabCloseRequested.connect(self.tabs.removeTab)
		self.layout.addWidget(self.tabs)

		self.setLayout(self.layout)

	def addTab(self, widget, name):
		for i in range(self.tabs.count()):
			if self.tabs.tabText(i) == name:
				return
		self.tabs.addTab(widget, name)
		
	def deleteWidget(self, name):
		for i in range(self.tabs.count()):
			if self.tabs.tabText(i) == name:
				self.closeTab(i)
				return
		return "Couldn't find tab with the name '{}'".format(name)

class AppMainScreen(QtWidgets.QWidget):
	def __init__(self, parent=None, start_x=400,start_y=200, height=400, width=1000):
		super(AppMainScreen, self).__init__(parent)

		self.init_ui(start_x, start_y, height, width)

	def init_ui(self, start_x, start_y, height, width):
		main_layout = QtWidgets.QGridLayout()
		main_layout.setColumnStretch(1, 4)

		self.db_container = DatabaseContainer(self, self)
		main_layout.addWidget(self.db_container, 0, 0, 1, 1)

		# self.cell_display = CellDisplay(self, 2, 3)
		# main_layout.addWidget(self.cell_display, 0, 1, 3, 1)

		self.info_display = TabDisplay(self)
		main_layout.addWidget(self.info_display, 0, 1, 3, 1)

		self.comp_container = ComputationContainer(self, self)
		main_layout.addWidget(self.comp_container, 0, 4, 1, 1)

		# self.cell_display2 = CellDisplay(self, 3, 4)
		# main_layout.addWidget(self.cell_display2, 0, 2, 1, 1)

		# main_layout.addWidget(App(), 1,1)

		self.setLayout(main_layout) 
		self.setGeometry(start_x, start_y, width, height)
		self.setWindowTitle('Database Work')	
		self.show()
		# QSplitter
	
	def updateTab(self, widget=None, name=""):
		if widget is None:
			self.info_display.deleteWidget(widget)
			return 

		self.info_display.addTab(widget, name)

if __name__ == "__main__":
	import sys
	app = QtWidgets.QApplication(sys.argv)
	main_screen = AppMainScreen()
	sys.exit(app.exec_())
