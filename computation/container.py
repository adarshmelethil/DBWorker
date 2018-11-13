
import sys
import os

from PyQt5 import QtWidgets

try:
	from computation.computationEntry import ComputationEntry
except ImportError:
	from computationEntry import ComputationEntry


class ComputationContainer(QtWidgets.QWidget):
	def __init__(self, container, parent):
		super(ComputationContainer, self).__init__(container)

		self.parent = parent
		self.init_ui()

	def init_ui(self):
		v_box = QtWidgets.QVBoxLayout()
		title = QtWidgets.QLabel()
		title.setText("Computation")
		v_box.addWidget(title)

		self.computation_list = QtWidgets.QListWidget()
		# self.db_list.itemClicked.connect()
		self.computation_list.itemDoubleClicked.connect(
			lambda item: self.parent.updateTab(
					*self.computation_list.itemWidget(item).GetDisplay()))
		v_box.addWidget(self.computation_list)

		self.computation_name = QtWidgets.QLineEdit()
		add_btn = QtWidgets.QPushButton("+")
		add_btn.clicked.connect(self.newComputation)
		h_box = QtWidgets.QHBoxLayout()
		h_box.addStretch()
		h_box.addWidget(self.computation_name)
		h_box.addStretch()
		h_box.addWidget(add_btn)
		h_box.addStretch()
		v_box.addLayout(h_box)

		self.setLayout(v_box)
	

	def newComputation(self):
		name = self.computation_name.text()
		if name == "":
			QtWidgets.QMessageBox.critical(self, "Error", "Computation name can not be empty")
			return
		
		for comp_index in range(self.computation_list.count()):
			comp = self.computation_list.itemWidget(self.computation_list.item(db_index))
			if comp.name == name:
				QtWidgets.QMessageBox.critical(self, "Error", "Computation name is already in use")
				return
		
		new_comp = ComputationEntry(self.computation_list, self, name)
		new_comp_item = QtWidgets.QListWidgetItem(self.computation_list)
		new_comp_item.setSizeHint(new_comp.sizeHint())
		self.computation_list.addItem(new_comp_item)
		self.computation_list.setItemWidget(new_comp_item, new_comp)

	def deleteComputation(self, name):
		for comp_index in range(self.computation_list.count()):
			comp = self.computation_list.itemWidget(self.computation_list.item(comp_index))
			if comp.name == name:
				self.computation_list.takeItem(comp_index)
				return

if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	
	cc = ComputationContainer(None, None, )
	cc.show()
	
	sys.exit(app.exec_())