
import os as _os
import sys as _sys
import traceback as _traceback
import numpy as _np 

import logging as _logging

_logger = _logging.getLogger(__name__)
_logger.setLevel(_logging.DEBUG)
_logger_formatter = _logging.Formatter('%(name)s - %(levelname)s - %(message)s')
_ch = _logging.StreamHandler()
_ch.setLevel(_logging.DEBUG)
_ch.setFormatter(_logger_formatter)
_logger.addHandler(_ch)

from PyQt5 import QtWidgets as _QtWidgets

import UI as _UI
from UI import Database as _Database
from UI import Computation as _Computation

from data import Query as _Query

from data import DB_TYPES as _DB_TYPES
from data import getDatabase as _getDatabase
_app = _QtWidgets.QApplication(_sys.argv)

# list<dict{
# 	"info": dict{"name", "location", "db_type"},
# 	"db_obj": database()
# }>
_databases = []
_db_list = None # List UI
_query_list = None # List UI

_scripts = []
_script_list = None # List UI
_script_var_list = None # List UI

_tab_display = None # Tab UI
_log_display = None # Logging

def _queryClicked(_query_entry):
	_queries = _getQueries()
	_query = None
	for _qk,_qv in _queries:
		if _qk == _query_entry.name:
			_query = _qv
	if _query is None:
		raise NameError("'{qname}' was not found".format(_query_entry.name))
	_query_display = _Database.QueryDisplay(col_names=_query.col_names, rows=_query.data)
	_openTab("Query_{qname}".format(qname=_query_entry.name), _query_display)

def _getQueries(_db_name=""):
	if _db_name:
		return [(gk,gv) for gk,gv in globals().items() if gk[0]!="_" and type(gv) is _Query and gv.db_name==_db_name]
	else:
		return [(gk,gv) for gk,gv in globals().items() if gk[0]!="_" and type(gv) is _Query]

def _getComputationVars():
	return [(gk, gv) for gk,gv in globals().items() if gk[0]!="_" and type(gv) is not _Query]

def _refreshQueries(_db_name):
	_db_widget = _tab_display.getTabWithName("DB_{name}".format(name=_db_name))
	_query_entries_1 = [_Database.QueryEntry(
		name=q_n, col_names=q_v.keys(), num_of_results=q_v.getNumOfEntries(), 
		delete_callback=_deleteQuery, exec_callback=_execQuery) 
		for q_n,q_v in _getQueries(_db_widget.name)]
	_query_entries_2 = [_Database.QueryEntry(
		name=q_n, col_names=q_v.keys(), num_of_results=q_v.getNumOfEntries(), 
		delete_callback=_deleteQuery, exec_callback=_execQuery)
		for q_n,q_v in _getQueries(_db_widget.name)]
	_db_widget.updateQueries(_query_entries_1)
	_query_list.updateList(_query_entries_2)

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
			_query_names.append(_query_name)

def _deleteQuery(_query_name):
	_query_obj = eval(_query_name)
	_db_name = _query_obj.db_name
	exec('''
global {qname}
del {qname}'''.format(qname=_query_name))
	_refreshQueries(_db_name)
	_query_names.remove(_query_name)

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
	_db_list.updateList([_Database.DatabaseEntry(**d["info"]) for d in _databases])
	_logger.debug("Adding database: ({db_name})".format(db_name=_name))

def _removeDatabase(_name):
	for _i, _db in enumerate(_databases):
		if _db.name == _name:
			_logger.debug("Removing database: {name}".format(
				name=_name))
			del _databases[_i]
			_db_list.updateList([_Database._DatabaseEntry(**d["info"]) for d in _databases])
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
	_Database.DatabaseFourm("", "", "", 
		_DB_TYPES.keys(), update_callback=_updateDatabase)

def _refreshScriptList():
	_script_list.updateList([_Computation.ScriptEntry(_s['location'], _deleteCompEntry) for _s in _scripts])

def _deleteCompEntry(location):
	for i, _s in enumerate(_scripts):
		if _s['location'] == location:
			del _scripts[i]
			_refreshScriptList()
			return

def _makeNewScript(location):
	_scripts.append({
		"location": location,
	})
	_refreshScriptList()

def _updateScript(location):
	if not _os.path.isfile(location):
		return "Not a file"
	for _s in _scripts:
		if _s['location'] == location:
			return "Location already exists"
	_makeNewScript(location)

def _newScript():
	_computation_form = _Computation.ScriptFourm("", 
		update_callback=_updateScript)

def _dbClick(_db_widget):
	_db_detail = _Database.DatabaseDisplay(
		name=_db_widget.name, location=_db_widget.location, db_type=_db_widget.db_type, 
		item_callback=_queryClicked, add_callback=_addQuery)
	
	for _db in _databases:
		if _db["info"]["name"] == _db_widget.name:
			_db_detail.updateTableInfo(_db["db_obj"].getTables())
			break

	_openTab("DB_{name}".format(name=_db_widget.name), _db_detail)
	_refreshQueries(_db_widget.name)

def _runScript(_content):
	try:
		exec(_content)
		for lk,lv in locals().items():
			if lk[0]!= "_":
				globals()[lk] = lv
		_vars = _getComputationVars()
		# print("_vars:", _vars)
		_qlabels_list = []
		for _k,_v in _vars:
			if type(_v) is list:
				if len(_v) > 10:
					_val = "list<{}>".format(len(_v))
				else:
					_val = "{}".format(_v)
			elif type(_v) is _np.ndarray:
				_toolarge = False
				for _l in _v.shape:
					if _l > 10:
						_toolarge = True
						break 
				if _toolarge:
					_val = "Matrix shape: {}".format(_v.shape)
				else:
					_val = "\n{}".format(_v)
			else:
				_val = "{}".format(_v)

			_qlabels_list.append(
				_QtWidgets.QLabel("{name} - {val}".format(name=_k,val=_val)))

		_script_var_list.updateList(_qlabels_list)

	except Exception as _e:
		# _QtWidgets.QMessageBox.critical(None, "Failed to run script", "{}".format(se))
		_tb = _traceback.format_exc()
		_log_display.addLogging("Failed to run script\n: {}".format(_tb))

def _scriptClick(_script_widget):
	_openTab(
		"Script_{name}".format(name=_script_widget.getName()), 
		_Computation.ScriptDisplay(
			_script_widget.getLocation(),
			exec_callback=_runScript))
	# ScriptDisplay
	# print(_script_widget.getLocation())

def _openCompVars(comps_widget):
	print(comps_widget.text())
	# _openTab(ComputationDisplay()

_db_list = _UI.ListDisplay(title_text="Databases", 
	new_callback=_newDatabase,
	click_callback=_dbClick)
_query_list = _UI.ListDisplay(title_text="Query Variables",
	add_button=False,
	new_callback=None,
	click_callback=_queryClicked)

_script_list = _UI.ListDisplay(title_text="Scripts", 
	new_callback=_newScript,
	click_callback=_scriptClick)
_script_var_list = _UI.ListDisplay(title_text="Script Variables",
	add_button=False,
	new_callback=None,
	click_callback=_openCompVars)

_tab_display = _UI.TabDisplay()
_log_display = _UI.LogDisplay()

# placeholder
_r_t = _QtWidgets.QLabel("right top")
_r_b = _QtWidgets.QLabel("right bottom")
_c_t = _QtWidgets.QLabel("center top")
_c_b = _QtWidgets.QLabel("center bottom")
_l_t = _QtWidgets.QLabel("left top")
_l_b = _QtWidgets.QLabel("left bottom")

_main_widget = _UI.MainWindow(
	left_top=_db_list,
	left_bottom=_query_list,
	center_top=_tab_display,
	center_bottom=_log_display,
	right_top=_script_list,
	right_bottom=_script_var_list)

_height = 600
_main_widget.setGeometry(200, 200, _height*(1+5**0.5)/2, _height)
_main_widget.setWindowTitle('Database Work')
_main_widget.show()
_sys.exit(_app.exec_())