import logging
from PyQt5 import QtWidgets

class ListDisplay(QtWidgets.QWidget):
	def __init__(self, title_text, click_callback, button_callback=None, button_text="+", parent=None):
		super(ListDisplay, self).__init__(parent)
		self.logger = logging.getLogger(__name__)

		self.title_text = title_text 
		self.init_ui(click_callback, button_callback, button_text)

	def init_ui(self, click_callback, button_callback, button_text):
		main_layout = QtWidgets.QVBoxLayout()

		main_frame = QtWidgets.QFrame(self)
		main_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
		sub_layout = QtWidgets.QVBoxLayout(main_frame)

		title_layout = QtWidgets.QHBoxLayout()
		title = QtWidgets.QLabel()
		title.setText(self.title_text)
		title_layout.addStretch()
		title_layout.addWidget(title)
		title_layout.addStretch()
		sub_layout.addLayout(title_layout)

		self.db_list = QtWidgets.QListWidget()
		self.db_list.itemClicked.connect(
			lambda item: click_callback(
				self.db_list.itemWidget(item)))
		# self.db_list.itemDoubleClicked.connect(
		# 	lambda item: click_callback(
		# 		self.db_list.itemWidget(item)))
		sub_layout.addWidget(self.db_list)

		if button_callback:
			add_btn = QtWidgets.QPushButton(button_text)
			add_btn.clicked.connect(button_callback)
			btn_layout = QtWidgets.QHBoxLayout()
			btn_layout.addStretch()
			btn_layout.addWidget(add_btn)
			btn_layout.addStretch()
			sub_layout.addLayout(btn_layout)

		main_layout.addWidget(main_frame)
		self.setLayout(main_layout)

	# def clearList(self):
		# while self.db_list.count() > 0:
		# 	self.logger.debug(self.db_list.count())
		# 	self.logger.debug("Removed {w} from list {name}".format(name=self.title_text, w=str(self.db_list.takeItem(0))))

	def updateList(self, widgets):
		self.logger.debug("Updating list {name}: [{content}]".format(
			name=self.title_text, content=", ".join(map(str, widgets))))
		
		self.db_list.clear()
		for w in widgets:
			list_item = QtWidgets.QListWidgetItem(self.db_list)
			list_item.setSizeHint(w.sizeHint())
			self.db_list.addItem(list_item)
			self.db_list.setItemWidget(list_item, w)

if __name__ == "__main__":
	logger = logging.getLogger(__name__)
	logger.setLevel(logging.DEBUG)
	logger_formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
	ch = logging.StreamHandler()
	ch.setLevel(logging.DEBUG)
	logger.addHandler(ch)

	import sys
	app = QtWidgets.QApplication(sys.argv)
	
	test_label1 = QtWidgets.QLabel("test content1")
	test_label2 = QtWidgets.QLabel("test content2")

	stuff = [test_label1, test_label2]
	l = None

	class aa:
		counter = 0
		def a(self):
			print(self.counter)
			# if self.counter == 0:
			# 	l.updateList([test_label1])
			# 	print("here")
			# else:
			l.updateList(stuff)
			print("here1")

			print("here2")
			self.counter += 1
			print("here3")
		# l.updateList()
	a = aa()

	def c(widget):
		print("click:", widget.text())
	def dc(name, query):
		print("double click:", name, query)
	
	l = ListDisplay(None, "testing",
		new_callback=a.a, click_callback=c)

	l.show()

	sys.exit(app.exec_())