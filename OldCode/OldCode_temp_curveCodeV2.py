#!/usr/bin/env python
import sys
import re
import pyodbc
import numpy as np
from terminaltables import SingleTable

DB_FILE = r'N:\Data\DistributionSystem\DB_DistributionSystemInformation_Live_W7.mdb'

NORTH_DEMAND_DB = r'N:\Data\Demand\DB_Demand-North_ver2_Live_W7.mdb'
#NORTH_TEMP = np.array([-40, -35, -30, -25, -20, -15, -10, -5, 0, 5, 10, 15, 20])

SOUTH_DEMAND_DB = r'N:\Data\Demand\DB_Demand-South_ver2_Live_W7.mdb'
#SOUTH_TEMP = np.array([-36, -30, -25, -20, -15, -10, -5, 0, 5, 10, 15, 20])

TEMP_CONSTANT = {
  "0811": [-36, -30, -25, -20, -15, -10, -5, 0, 5, 10, 15, 20],
  "0341": [-40, -35, -30, -25, -20, -15, -10, -5, 0, 5, 10, 15],
  "0211": [-42, -35, -30, -25, -20, -15, -10, -5, 0, 5, 10, 15],
  "0411": [-41, -35, -30, -25, -20, -15, -10, -5, 0, 5, 10, 15],
  "0600": [-36, -30, -25, -20, -15, -10, -5, 0, 5, 10, 15, 20],
  "0700": [-37, -30, -25, -20, -15, -10, -5, 0, 5, 10, 15, 20],
  }

PHF_CONSTANT = {
  "0811": [1.15, 1.20, 1.24, 1.28, 1.32, 1.36, 1.40, 1.44, 1.48, 1.52, 1.56, 1.56],
  "0341": [1.10, 1.12, 1.15, 1.17, 1.20, 1.22, 1.25, 1.27, 1.30, 1.32, 1.35, 1.37],
  "0211": [1.07, 1.12, 1.16, 1.19, 1.23, 1.26, 1.30, 1.33, 1.37, 1.40, 1.44, 1.47],
  "0411": [1.06, 1.13, 1.18, 1.24, 1.29, 1.35, 1.40, 1.46, 1.51, 1.57, 1.62, 1.67],
  "0600": [1.12, 1.20, 1.26, 1.33, 1.39, 1.46, 1.52, 1.59, 1.65, 1.72, 1.78, 1.78],
  "0700": [1.08, 1.16, 1.21, 1.27, 1.32, 1.38, 1.43, 1.49, 1.54, 1.60, 1.65, 1.66],
  }

#NORTH_PHFS = [
#  [1.5, 1.55, 1.6, 1.65, 1.67, 1.7, 1.71, 1.75, 1.77, 1.8, 1.82, 1.9, 1.9],
#  [1.1, 1.12, 1.15, 1.19, 1.23, 1.31, 1.35, 1.37, 1.4, 1.45, 1.49, 1.54, 1.54],
#  [1.1, 1.13, 1.16, 1.21, 1.27, 1.33, 1.35, 1.39, 1.41, 1.45, 1.5, 1.55, 1.55 ],
#  [1.1, 1.15, 1.175, 1.21, 1.25, 1.28, 1.32, 1.36, 1.39, 1.425, 1.47, 1.51, 1.51],
#]
#SOUTH_PHFS = [
#  [1.35, 1.5, 1.6, 1.72, 1.9, 2.1, 2.15, 2.4, 2.7, 2.9, 3.3, 3.6],
#  [1.1, 1.18, 1.225, 1.25, 1.28, 1.34, 1.39, 1.43, 1.48, 1.51, 1.55, 1.55],
#  [1.1, 1.18, 1.23, 1.27, 1.31, 1.36, 1.43, 1.47, 1.52, 1.53, 1.63, 1.63],
#  [1.1, 1.16, 1.22, 1.28, 1.34, 1.41, 1.47, 1.55, 1.63, 1.71, 1.79, 1.79],
#]

#PHFS_BIN = np.array([100, 1000, 10000, 100000])

BP_CONSTANT = {
  "0811": 15.1,
  "0341": 14.3,
  "0211": 14.8,
  "0411": 14.3,
  "0600": 14.9,
  "0700": 15.7,
}

CALGARY_DS = "03-0032"

def print_info(DS, INTs, loads, temps):
  # DS, INTs, CLs, loads
  INTs = [[INT[0], INT[1] if INT[1] else 0, INT[2]] for INT in INTs]
    
  table1 = [ ['Interconnection #', 'Split (%)', 'Weather Zone'] ] \
  + [[INT[0], INT[1]*100, INT[2]] for INT in INTs] \
  + [ ["Total Splits:", sum([INT[1] for INT in INTs]), ""] ]
  print(SingleTable(table1, title="Distribution System {0}".format(DS)).table)
  print

  table2 = [ ['Temperature', 'Load(GJ/d)'] ] \
  + zip(temps, loads)
  
  print(SingleTable(table2, title="Loads at Different Temperatures").table)

def ds_checker(value):
  return re.search(r'^[0-9]{2}-[0-9]{4}$', value)

def intt_checker(value):
  return re.search(r'^[0-9]{5}$', value)

def connectDB(db_file):
  odbc_conn = 'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)}; DBQ=%s' % (db_file)
  return pyodbc.connect(odbc_conn)

def find_all_int(conn, DS):
  query = u"""
    SELECT 
      INT.[Interconnection#],
      INT.[Split],
      INT.[WeatherZone]
    FROM
      (tblInterconnections AS [INT] LEFT JOIN tblOperatingSystem AS OS 
        ON INT.AssignedOperatingSystem = OS.[OS Unique ID])
    WHERE OS.[DS #] = ? and INT.[Status] = ?;
  """

  cursor = conn.cursor()
  cursor.execute(query, [DS, "Active"])
  INTs = cursor.fetchall()
  cursor.close()
  return INTs

def find_ds_by_int(conn, INT):
  query = """
    SELECT 
      OS.[DS #],
      DS.[System Configuration]
    FROM 
      tblInterconnections AS INT
    INNER JOIN tblOperatingSystem AS OS
      ON INT.AssignedOperatingSystem = OS.[OS Unique ID]
    INNER JOIN tblDistributionSystems AS DS
      ON OS.[DS #] = DS.[DS Unique ID]
    WHERE
      INT.[Interconnection#] = ?
  """

  cursor = conn.cursor()
  cursor.execute(query, INT)
  row = cursor.fetchone()
  cursor.close()

  if row:
    # ds, config
    return row[0], row[1]
  return None, None

def retrieve_ds(conn, ds):
  query = """
    SELECT 
      assign.[Svc Pt #],
      assign.DS,
      demand.[Base Factor],
      demand.[Heat Factor],
      demand.[HUC 3-Year Peak Demand],
      demand.[FactorQualityCode],
      cat.[Rate Code]
    FROM 
      ((tblSvcPtAssignment AS assign INNER JOIN tblSvcPtDemand AS demand 
        ON assign.[Svc Pt #] = demand.[Svc Pt #])
          INNER JOIN tblSvcPtCategory as cat 
            ON assign.[Svc Pt #] = cat.[Svc Pt #])
      INNER JOIN tblSvcPtInfo as info 
        ON assign.[Svc Pt #] = info.[Svc Pt #]
    WHERE assign.DS = ? and info.[Svc Pt Active] = ?;
  """
  cursor = conn.cursor()

  cursor.execute(query, [ds, -1])
  df = cursor.fetchall()
  cursor.close()
  del cursor
  conn.close()
  return df  

def check_rate(cl):
  abnormal = [customer
    for customer in cl
      if customer["Rate"] not in ['LOW', 'MID', 'HIGH', None]
  ]
  normal = [customer
    for customer in cl 
      if customer not in abnormal
  ]
  return normal, abnormal

def check_huc(cl):
  bad_FQC_customers = [customer
    for customer in cl 
      if customer["Rate"] == "HIGH" and 
        customer["FQC"] not in ["0", "1", "20"] 
  ]
  normal = [customer
    for customer in cl
      if customer not in bad_FQC_customers
  ]
  return normal, bad_FQC_customers

class DSNotFound(Exception):
  pass
class INTNotFound(Exception):
  pass

def make_float(CLs, key):
  for CL in CLs:
    CL[key] = float(CL[key])

def ds_path(db_conn, db_north, db_south, DS):
  if DS is CALGARY_DS:
    print "Warning this will take a while"

  INTs = find_all_int(db_conn, DS)

  if len(INTs) == 0:
    raise DSNotFound()

  if DS.startswith("01"):
    # North
    DFs = retrieve_ds(db_north, DS)
#    temps = NORTH_TEMP
#    PHFs = NORTH_PHFS
  else:
    # South
    DFs = retrieve_ds(db_south, DS)
#    temps = SOUTH_TEMP
#    PHFs = SOUTH_PHFS

  headers = ["Service Pt #", "DS", "Base Factor [GJ/d]", "Heat Factor [GJ/d]", "HUC 3-Year Peak Demand", "FQC", "Rate"]
  CLs = [dict(zip(headers, df)) for df in DFs]
  
  CLs, ab = check_rate(CLs)
  CLs, b_fqc = check_huc(CLs)
  
  make_float(CLs, 'Base Factor [GJ/d]')
  make_float(CLs, 'Heat Factor [GJ/d]')
  
  bf = sum([CL['Base Factor [GJ/d]'] for CL in CLs])
  hf = sum([CL['Heat Factor [GJ/d]'] for CL in CLs])
  print(bf, hf)

  bp = np.array(BP_CONSTANT[INTs[0][2]])
  PHFs = np.array(PHF_CONSTANT[INTs[0][2]])
  temps = np.array(TEMP_CONSTANT[INTs[0][2]])
  
  dd = bp - temps
  dd[dd < 0] = 0

  loads = np.array([bf+hf*day for day in dd])
  print(loads)
  loads = loads*PHFs

#  loads = np.asarray([bf+hf*day for day in dd])
#  loads *= PHFs[np.digitize(len(loads), PHFS_BIN)]
  if len(b_fqc) > 0:
    fqc = raw_input("""
Do you want to include the 3-year peak of these customers in the load calculation? [y/n]
If yes, the three year peak will be added to the load at EACH temperature.
Otherwise, these customers will be excluded and can be manually added later.
""")
    if fqc.lower() == "y":
      loads += sum([customer["HUC 3-Year Peak Demand"] for customer in b_fqc])
      CLs += b_fqc

  print_info(DS, INTs, loads, temps)

def int_path(db_conn, db_north, db_south, INT):  
  DS, _ = find_ds_by_int(db_conn, INT)
  
  if not DS:
    raise INTNotFound()

  ds_path(db_conn, db_north, db_south, DS)

# TODO:
# print ab, and b_fqc
if __name__ == "__main__":
  print "Hello, \nThank you for using the load temperature program!"

  db_conn = connectDB(DB_FILE)
  db_north = connectDB(NORTH_DEMAND_DB)
  db_south = connectDB(SOUTH_DEMAND_DB)

  while True:
    option = str(raw_input("Enter your DS (XX-XXXX) or INT (XXXXX):"))

    DS = ds_checker(option)
    INT = intt_checker(option)

    if not DS and not INT:
      print "Invalid DS or INT"
      continue

    try: 

      if DS:
        DS = DS.group(0)
        ds_path(db_conn, db_north, db_south, DS)
      elif INT:
        INT = INT.group(0)
        int_path(db_conn, db_north, db_south, INT)

    except DSNotFound:
      print "I don't think that this Distribution system exists or it doesn't have an active station."
      print "try again"
      continue

    except INTNotFound:
      print "I don't think the interconnection number is correct"
      print "try again"
      continue 
    break

