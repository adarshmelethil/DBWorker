import logging
from PyQt5 import QtWidgets 

class TabDisplay(QtWidgets.QWidget):
	def __init__(self, parent=None):
		super(TabDisplay, self).__init__(parent)
		self.logger = logging.getLogger(__name__)

		self.init_ui()

	def init_ui(self):
		main_layout = QtWidgets.QVBoxLayout()

		main_frame = QtWidgets.QFrame(self)
		main_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
		sub_layout = QtWidgets.QVBoxLayout(main_frame)
		

		self.tabs = QtWidgets.QTabWidget()
		self.tabs.setTabsClosable(True)
		self.tabs.setMovable(True)
		self.tabs.tabCloseRequested.connect(self.tabs.removeTab)
		sub_layout.addWidget(self.tabs)

		main_layout.addWidget(main_frame)
		self.setLayout(main_layout)

	def updateTabs(self, names, widgets):
		self.tabs.clear()
		for w, n in zip(widgets, names):
			self.tabs.addTab(w, n)

	def getTabWithName(self, tab_name):
		for i in range(self.tabs.count()):
			if self.tabs.tabText(i) == tab_name:
				return self.tabs.widget(i)
		return None 

	def getCurrentTabs(self):
		return [self.tabs.tabText(i) for i in range(self.tabs.count())], [self.tabs.widget(i) for i in range(self.tabs.count())]

if __name__=="__main__":
	import sys
	app = QtWidgets.QApplication(sys.argv)
	
	test_contests = ["test content 1", "test content 2", "test content 3"]
	test_names = ["test tab 1","test tab 2", "test tab 3"]
	
	t = TabDisplay()
	t.updateTabes(
		[QtWidgets.QLabel(c) for c in test_contests],
		test_names)
	t.updateTabes(
		[QtWidgets.QLabel(c) for c in test_contests[1:]],
		test_names[1:])

	t.show()

	sys.exit(app.exec_())
