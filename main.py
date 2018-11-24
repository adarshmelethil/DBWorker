
import sys as _sys

import logging as _logging

_logger = _logging.getLogger(__name__)
_logger.setLevel(_logging.DEBUG)
_logger_formatter = _logging.Formatter('%(name)s - %(levelname)s - %(message)s')
_ch = _logging.StreamHandler()
_ch.setLevel(_logging.DEBUG)
_ch.setFormatter(_logger_formatter)
_logger.addHandler(_ch)

from PyQt5 import QtWidgets as _QtWidgets

from UI import MainWindow as _MainWindow
from UI import TabDisplay as _TabDisplay
from UI import ListDisplay as _ListDisplay
from UI.Database import DatabaseEntry as _DatabaseEntry
from UI.Database import DatabaseDisplay as _DatabaseDisplay
from UI.Database import DatabaseFourm as _DatabaseFourm
from UI.Database import QueryEntry as _QueryEntry
from UI.Database import QueryDisplay as _QueryDisplay
from UI.Computation import ComputationEntry as _ComputationEntry
from UI.Computation import ComputationDisplay as _ComputationDisplay

from data import Query as _Query

from data import DB_TYPES as _DB_TYPES
from data import getDatabase as _getDatabase
_app = _QtWidgets.QApplication(_sys.argv)

# list<{name, location, type}>
_databases = []
_db_list = None

_scripts = []
_script_list = None

_tab_display = None

def _queryClicked(_query_entry):
	_queries = _getQueries()
	_query = None
	for _qk,_qv in _queries:
		if _qk == _query_entry.name:
			_query = _qv
	if _query is None:
		raise NameError("'{qname}' was not found".format(_query_entry.name))
	_query_display = _QueryDisplay(col_names=_query.col_names, rows=_query.data)
	_openTab("Query_{qname}".format(qname=_query_entry.name), _query_display)

def _getQueries(_db_name=""):
	if _db_name:
		return [(gk,gv) for gk,gv in globals().items() if gk[0]!="_" and type(gv) is _Query and gv.db_name==_db_name]
	else:
		return [(gk,gv) for gk,gv in globals().items() if gk[0]!="_" and type(gv) is _Query]

def _refreshQueries(_db_name):
	_db_widget = _tab_display.getTabWithName("DB_{name}".format(name=_db_name))
	_query_entries = [_QueryEntry(
		name=q_n, col_names=q_v.keys(), num_of_results=q_v.getNumOfEntries(), 
		delete_callback=_deleteQuery, exec_callback=_execQuery) 
	for q_n,q_v in _getQueries(_db_widget.name)]
	_db_widget.updateQueries(_query_entries)

def _execQuery(_query_name):
	_query_obj = eval(_query_name)
	_db_name = _query_obj.db_name
	_query_str = _query_obj.query
	for _db in _databases:
		if _db["info"]["name"] == _db_name:
			_query_res = _db["db_obj"].runSelectQuery(_query_str)
			_query_res.setDBName(_db["info"]["name"])
			exec('''
global {query_name}
{query_name}=_query_res
			'''.format(query_name=_query_name))
			_refreshQueries(_db_name)

def _deleteQuery(_query_name):
	_query_obj = eval(_query_name)
	_db_name = _query_obj.db_name
	exec('''
global {qname}
del {qname}'''.format(qname=_query_name))
	_refreshQueries(_db_name)

def _addQuery(_db_name, _query_name, _query_str):
	query = None
	for _db in _databases:
		if _db["info"]["name"] == _db_name:
			_query = _db["db_obj"].runSelectQuery(_query_str)
			_query.setDBName(_db["info"]["name"])
			exec('''
global {query_name}
{query_name}=_query
			'''.format(query_name=_query_name))
			_refreshQueries(_db["info"]["name"])

def _openTab(_name, _widget):
	_cur_names, _cur_widgets = _tab_display.getCurrentTabs()
	if _name in _cur_names:
		return # tab already open
	_cur_names.append(_name)
	_cur_widgets.append(_widget)
	_tab_display.updateTabs(_cur_names, _cur_widgets)


def _makeNewDatabase(_name, _location, _db_type):
	_databases.append({
		"info":{
			"name":_name,
			"location":_location,
			"db_type":_db_type,
		},
		"db_obj": _getDatabase(db_type=_db_type, location=_location)
	})
	_db_list.updateList([_DatabaseEntry(**d["info"]) for d in _databases])
	_logger.debug("Adding database: ({db_name})".format(db_name=_name))

def _removeDatabase(_name):
	for _i, _db in enumerate(_databases):
		if _db.name == _name:
			_logger.debug("Removing database: {name}".format(
				name=_name))
			del _databases[_i]
			_db_list.updateList([_DatabaseEntry(**d["info"]) for d in _databases])
			return
	raise Exception("Could not find database '{}' to delete!".format(_name))

def _updateDatabase(_old_name, _new_name, _location, _db_type):
	# New database
	if not _old_name and _new_name and _location and _db_type:
		if _old_name != _new_name:
			for _i, _db in enumerate(_databases):
				if _db.name == _new_name:
					return "New name already in use."
		_makeNewDatabase(_name=_new_name, _location=_location, _db_type=_db_type)
	elif _db_type == "":
		_removeDatabase(_old_name)
	# Update database
	elif _new_name and _location:
		for _i, _db in enumerate(_databases):
			if _db.name == _new_name:
				return "New name already in use."
		_removeDatabase(_old_name)
		_makeNewDatabase(_name=_new_name, _location=_location, _db_type=_db_type)
	else:
		return "Name and location can not be left empty"
	_logger.debug("New Database list: [{dbs}]".format(dbs=", ".join(map(str,_databases))))

def _newDatabase():
	db_form = _DatabaseFourm("", "", "", 
		_DB_TYPES.keys(), update_callback=_updateDatabase)
	db_form.show()

def _updateScript(_old_name, _new_name, location):
	print("update_old_name",_old_name, _new_name, location)

def _newScript():
	# db_form = _DatabaseFourm("", "", "", 
	# 	_DB_TYPES.keys(), update_callback=_updateDatabase)
	# db_form.show()
	pass 
	# TODO - create new script, and replicate editing
	# Add edit button to db
	# save script, query, and db loading (session)

def _dbClick(_db_widget):
	_db_detail = _DatabaseDisplay(
		name=_db_widget.name, location=_db_widget.location, db_type=_db_widget.db_type, 
		item_callback=_queryClicked, add_callback=_addQuery)
	
	for _db in _databases:
		if _db["info"]["name"] == _db_widget.name:
			_db_detail.updateTableInfo(_db["db_obj"].getTables())
			break

	# _query_entries = [_QueryEntry(
	# 	name=q_n, col_names=q_v.keys(), num_of_results=q_v.getNumOfEntries(), 
	# 	delete_callback=_deleteQuery, exec_callback=_execQuery) 
	# for q_n,q_v in _getQueries(_db_widget.name)]
	# _db_detail.updateQueries(_query_entries)
	
	_openTab("DB_{name}".format(name=_db_widget.name), _db_detail)
	_refreshQueries(_db_widget.name)
	# print("single clicked", db_widget.name, db_widget.location, db_widget.db_type)
	# db_form = _DatabaseFourm( 
	# 	db_widget.name, db_widget.location, db_widget.db_type, 
	# 	_DB_TYPES.keys(), update_callback=_updateDatabase)
	# db_form.show()
	
_db_list = _ListDisplay(title_text="Databases", 
	new_callback=_newDatabase,
	click_callback=_dbClick)
_script_list = _ListDisplay(title_text="Scripts", 
	new_callback=_newDatabase,
	click_callback=_dbClick)
_tab_display = _TabDisplay()

# placeholder
_r_t = _QtWidgets.QLabel("right top")
_r_b = _QtWidgets.QLabel("right bottom")
_c = _QtWidgets.QLabel("center")
_l_t = _QtWidgets.QLabel("left top")
_l_b = _QtWidgets.QLabel("left bottom")

_main_widget = _MainWindow( 
	left_top=_db_list, 
	left_bottom=_l_b, 
	center=_tab_display, 
	right_top=_script_list,
	right_bottom=None)

_height = 600
_main_widget.setGeometry(200, 200, _height*(1+5**0.5)/2, _height)
_main_widget.setWindowTitle('Database Work')
_main_widget.show()
_sys.exit(_app.exec_())