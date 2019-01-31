#! python
'''Plot and list system loads at different temperatures

Receive the Distribution System number or the Interconnect number and find the system configuration and load.
The temperature range is from -36C to +20C.
Plot the load vs temperature curve and output the results in a neat, organized table'''

#Created by: Raza Anees

import numpy as np, matplotlib.pyplot as plt, pyodbc, sys, re, numpy.polynomial.polynomial as poly, time

def ds_checker(inp):
	'''Ensure that a proper DS number is entered with the format xx-xxxx

	inp = String representing the DS number
	'''
	compiler = re.compile(r'^\w{2}-\w{4}$')
	mo = compiler.search(inp)
	return mo

def intt_checker(inp):
	'''Ensure that a proper interconnect number is entered with 5 numbers'''
	compiler = re.compile(r'^\w{5}$')
	mo = compiler.search(inp)
	return mo

def print_load(x, y, chosen_phf, ds):
	'''Print a well-structured and organized table.

	x = First column of the table
	y = Second column of the table
	ds = Input used to display the correct DS # in the table's title
	'''
	print ("Load vs Temperature of DS %s" %ds).center(30)
	print "-"*30
	print "Temperature (C)".ljust(20) + "PHF".center(10) + "Load (G/d)".rjust(10)
	for i in xrange(len(x)):
		print str(x[i]).ljust(20, '.') + str(chosen_phf[i]).center(10) + str(int(round(y[i]))).rjust(10)

def print_system_info(ds, intt, config, cl):
	'''Print information for a system in a structured table.

	ds = Distribution System number (string)
	intt = Interconnect number (string)
	config = System configuration (string) (isolated or integrated)
	cl = Customer list of the system (list)
	'''
	print "System Information".center(57)
	print "DS".ljust(8) + "INT #".center(12) + "Configuration".center(18) + "Number of Customers".rjust(10)
	print "-"*57
	print str(ds).ljust(8) + intt.center(12) + config.center(18) + str(len(cl)).rjust(10)
	
def print_multiple_stations(ds, intts, cl):
	'''Print a well-structured table for integrated distribution systems.

	ds = Distribution System number (string)
	intts = All interconnects in the system (tuple)
	cl = Customer list of the system (list)
	'''  
	print "System Information".center(57)
	print "DS".ljust(8) + "INT #".center(12) + "Configuration".center(18) + "Split (%)".rjust(10)
	print "-"*57
	for i in xrange(len(intts)):
		print str(ds).ljust(8) + intts[i][0].center(12) + "Integrated".center(18) + str(round(float(intts[i][1])*100, 3)).rjust(10)
	print "Number of customers: {}".format(str(len(cl)).ljust(57))
	
def print_multiple_loads(x, y, chosen_phf, intts):
	'''Print the load of all stations in a well-structured table'''
	for i in xrange(len(intts)):
		print "\n"
		print ("Load vs Temperature of INT %s" %intts[i][0]).center(30)
		print "-"*30
		print "Temperature (C)".ljust(20) + "PHF".center(10) + "Load (G/d)".rjust(10)
		for j in xrange(len(x)):
			print str(x[j]).ljust(20, '.') + str(chosen_phf[j]).center(10) +str(int(round(y[j])*intts[i][1])).rjust(10)

def import_dist():
	db_file = r'N:\Data\DistributionSystem\DB_DistributionSystemInformation_Live_W7.mdb'
	
	odbc_conn = 'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)}; DBQ=%s' \
						 % (db_file)
	conn = pyodbc.connect(odbc_conn)
	
	return conn
		
def find_ds_by_intt(intt, con):
	query = '''
SELECT OS.[DS #], DS.[System Configuration]
FROM (tblInterconnections AS [INT] INNER JOIN tblOperatingSystem AS OS ON INT.AssignedOperatingSystem = OS.[OS Unique ID])
INNER JOIN tblDistributionSystems AS DS ON OS.[DS #] = DS.[DS Unique ID]
WHERE (INT.[Interconnection#] = ?);'''


"""
SELECT 
	OS.[DS #],
	DS.[System Configuration]
FROM 

	tblInterconnections AS INT
INNER JOIN tblOperatingSystem AS OS
	ON INT.AssignedOperatingSystem = OS.[OS Unique ID]
INNER JOIN tblDistributionSystems as DS
	ON OS.[DS #] = DS.[DS Unique ID]

WHERE
	INT.[Interconnection#] = ?

"""
	cursor = con.cursor()
	cursor.execute(query,intt)
	row = cursor.fetchone()
	cursor.close()
	del cursor
	
	if row:
		ds = row[0]
		config = row[1]
	else:
		print "This INT does not exist in the database. Please check the number and try again."
		time.sleep(3)
		sys.exit()
	
	return ds, config

def find_all_intt(ds, con):
	query = '''
SELECT INT.[Interconnection#], INT.[Split]
FROM (tblInterconnections AS [INT] LEFT JOIN tblOperatingSystem AS OS ON INT.AssignedOperatingSystem = OS.[OS Unique ID])
WHERE OS.[DS #] = ? and INT.[Status] = ?;
	'''
	
	cursor = con.cursor()
	cursor.execute(query, [ds, "Active"])
	intts = cursor.fetchall()
	cursor.close()
	del cursor
	return intts
	
def check_split(intts):
	for i in xrange(len(intts)):
		if intts[i][1] == None:
			print "\nINT {} does not have a split recorded for it. \
You should do this one by hand. Don't forget to update the Distribution database \
with the correct split value!".format(intts[i][0])
			intts[i][1] = 0
	return intts
				
def import_demand(database):
	db_file = database

	odbc_conn = 'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)}; DBQ=%s' \
						 % (db_file)
	conn = pyodbc.connect(odbc_conn)

	return conn

def retrieve_ds(ds, con):
		query = '''
SELECT assign.[Svc Pt #], assign.DS, demand.[Base Factor], demand.[Heat Factor], demand.[HUC 3-Year Peak Demand], demand.[FactorQualityCode], cat.[Rate Code]
FROM ((tblSvcPtAssignment AS assign INNER JOIN tblSvcPtDemand AS demand ON assign.[Svc Pt #] = demand.[Svc Pt #])
INNER JOIN tblSvcPtCategory as cat ON assign.[Svc Pt #] = cat.[Svc Pt #])
INNER JOIN tblSvcPtInfo as info ON assign.[Svc Pt #] = info.[Svc Pt #]
WHERE assign.DS = ? and info.[Svc Pt Active] = ?;'''
		cursor = con.cursor()

		cursor.execute(query, [ds, -1])
		df = cursor.fetchall()
		cursor.close()
		del cursor
		con.close()
		return df
		
def retrieve_ds_north(ds, con):
		query = '''
SELECT assign.[Svc Pt #], assign.DS, demand.[Base Factor], demand.[Heat Factor], demand.[HUC 3-Year Peak Demand], demand.[FactorQualityCode], cat.[Rate Code]
FROM ((tblSvcPtAssignment AS assign INNER JOIN tblSvcPtDemand AS demand ON assign.[Svc Pt #] = demand.[Svc Pt #])
INNER JOIN tblSvcPtCategory as cat ON assign.[Svc Pt #] = cat.[Svc Pt #])
INNER JOIN tblSvcPtInfo as info ON assign.[Svc Pt #] = info.[Svc Pt #]
WHERE assign.DS = ? and info.[Svc Pt Active] = ?;'''
		cursor = con.cursor()

		cursor.execute(query, [ds, -1])
		df = cursor.fetchall()
		cursor.close()
		del cursor
		con.close()
		return df
		
def check_rate(cl):
	normal_rate = ['LOW', 'MID', 'HIGH', None]
	abnormal = []
	
	for i, customer in enumerate(cl):
		# customer["Rate"] not in normal_rate
		for k,v in customer.items():
			if (k == "Rate") and (v not in normal_rate):
				abnormal.append(cl[i].copy())
		
	normal = [x for x in cl if x not in abnormal]
	return normal, abnormal

def check_huc(cl):
	g_fqc = ["0", "1", "20"]
	bad_fqc_customers = []
	
	for customer in cl:
		if (customer["Rate"] == "HIGH") and (customer["FQC"] not in g_fqc):
			bad_fqc_customers.append(customer)
				
	normal = [x for x in cl if x not in bad_fqc_customers]
	return normal, bad_fqc_customers
				
def make_float(data, col):
	'''Convert all of the values from a given column in a table to floating point decimals.'''
	for row in data:
		for k ,v in row.items():
			if k == col:
				row[k] = float(v)

def make_plot(temps, loads, ds):
	fig= plt.figure(figsize=(20,9))
	ax = fig.add_subplot(111)
	
	for item in [fig, ax]:
		item.patch.set_visible(False)
	
	major_ticks = np.arange(0, max(loads)+max(loads)/10, round(max(loads)/10,1))
	minor_ticks = np.arange(0, max(loads)+max(loads)/10, round(max(loads)/20,1))
	ax.set_yticks(major_ticks)
	ax.set_yticks(minor_ticks, minor=True)
	
	ax.grid(which='minor', alpha=0.5, linestyle='-', color='r')
	ax.grid(which='major', alpha=0.3, linestyle='--', color='black', \
			linewidth=2)
	
	x = xrange(len(temps))
	x_2 = np.linspace(0,len(temps)-1, num=len(temps))
	plt.xticks(x, temps)
	plt.xticks(x_2, temps)
	ax.xaxis.labelpad = 20
	
	plt.title('Load vs Temperature of DS '+ds)
	plt.xlabel('Temperature (C)')
	plt.ylabel('Load (GJ/d)')
	
	y = np.round(loads, decimals=1)
	ax.yaxis.labelpad = 20
	
	plt.scatter(x, y, s=25, color='blue', marker='o')
	
	coeff = poly.polyfit(temps, loads, 5)
	fit = poly.polyval(temps,coeff)
	equation = "y= {}x^5 + {}x^4 + {}x^3 + {}x^2 + {}x + {}".format(coeff[5], coeff[4],coeff[3], coeff[2], coeff[1], coeff[0])
	
	plt.plot(x_2, fit, linestyle='-', color='black')
	plt.text(0.1, 0.1, equation, transform=ax.transAxes, fontsize=9)

	plt.show()
	return equation

if __name__ == '__main__':
	print "Hello, \nThank you for using the load temperature program!"
	option = str(raw_input("What information do you have? \nType '1' to enter a DS or '2' to enter an INT: "))
	
	while True:
		if option == '1':
			intt = ''
			print "\nLooks like you want to enter a DS #. If this is true, go ahead and enter it. \n\ If you wanted to enter an INT #, then type 'no'"
			ds = str(raw_input("Enter DS # to continue or 'no' to go back: "))
			if ds_checker(ds):
				break
			elif ds.lower() == 'no':
				pass
			else:
				print ds, " doesn't look like a proper DS # to me. Try again"
				continue
			
		elif option == '2':
			ds = ''
			print "\nLooks like you want to enter an INT #. If this is true, go ahead and enter it. \n\If you wanted to enter a DS # instead, then type 'no'"
			intt = str(raw_input("Enter INT # to continue or 'no' to go back: "))
			if intt_checker(intt):
				break
			elif intt.lower() == "no":
				pass
			else:
				print "I don't recognize this as an interconnect number. Re-check and try again"
				continue
		else:
			print "\nI didn't understand that. Please type '1' for DS or '2' for INT"
			option = str(raw_input())
			continue
			
		if ds.lower() == "no" or intt.lower() == "no":
			print "It looks like you chose the wrong option the first time.\n"
			print "Please launch the program again. Goodbye!"
			time.sleep(3)
			sys.exit()

	dist_db = import_dist()
	
	if option == '1':
		if ds == "03-0032":
			print "That's the City of Calgary!! I can't do that!"
			time.sleep(3)
			print "..just kidding. I'm working on it but you'll have to hold tight"
		
		intts = find_all_intt(ds, dist_db)
		
		if intts == []:
			print "I don't think that this Distribution system exists or it doesn't have an active station."
			time.sleep(3)
			sys.exit()
		
		config = find_ds_by_intt(intts[0][0], dist_db)[1]
		
		if len(intts) == 1:
			print "DS {} is an isolated system supplied by INT {}".format(ds, intts[0][0])
		else:
			print "DS {} is an integrated system supplied by:".format(ds)
			for a in xrange(len(intts)):
				print "INT {}".format(intts[a][0])
			check_split(intts)
				
	if option == '2':
		
		ds, config = find_ds_by_intt(intt, dist_db)
		
		intts = find_all_intt(ds, dist_db)
		if intts == []:
			print "INT {} is not active and DS {} does not have any other active stations.".format(intt, ds)
			time.sleep(3)
			sys.exit()
		
		if config.lower() == 'isolated':
			print "INT {} is an isolated station in DS {}".format(intt, ds)
		elif config.lower() == 'integrated':
			print "INT {} is in an integrated system, DS {}, with the following stations:\n".format(intt, ds)
			for a in xrange(len(intts)):
				if intts[a][0] != intt:
					print "INT {}".format(intts[a][0])
			check_split(intts)
	
	dist_db.close()
	
	# Check if the splits of an integrated system add up to one
	incorrect_splits = 'y'
	split_sum = 0
	if len(intts) > 1:
		for i in intts:
			split_sum += i[1]
		if split_sum != 1:
			incorrect_splits = 'n'
	
	print "\nI'm retrieving the demand file. Please wait.."
	
	if ds.startswith("01"): region = "n"
	else: region = "s"
	
	if region == "n":
		dem_db = import_demand(r'N:\Data\Demand\DB_Demand-North_ver2_Live_W7.mdb')
		df = retrieve_ds_north(ds, dem_db)
	else:
		dem_db = import_demand(r'N:\Data\Demand\DB_Demand-South_ver2_Live_W7.mdb')
		df = retrieve_ds(ds, dem_db)
	
	headers = ["Service Pt #", "DS", "Base Factor [GJ/d]", "Heat Factor [GJ/d]", "HUC 3-Year Peak Demand", "FQC", "Rate"]
	cl = [dict(zip(headers, df[i])) for i in xrange(len(df))]
	cl, ab = check_rate(cl)
	cl, b_fqc = check_huc(cl)
	
	# Check for any customers that do not have a regularly seen rate
	if len(ab) > 0:
		print "I have found some customers in this system that should be investigated"
		for customer in ab:
			print customer["Service Pt #"], customer["Rate"]
		print "\nThose customers have been excluded from the load calculation."
	
	# Check for HUC with bad FQC
	if len(b_fqc) > 0:
		print "\nThere are some high use customers with bad factor quality codes in this system.\
These customers are:\n"
		print "Service Pt #".ljust(20), "Rate".center(10), "FQC".center(10), "3-year peak demand".rjust(10)
		for customer in b_fqc:
			print customer["Service Pt #"].ljust(20), customer["Rate"].center(10), customer["FQC"].center(10), str(customer["HUC 3-Year Peak Demand"]).rjust(10)
		fqc = raw_input("Do you want to include the 3-year peak of these customers in the load calculation? [y/n]\
\nIf yes, the three year peak will be added to the load at EACH temperature. \
Otherwise, these customers will be excluded and can be manually added later. ")
	
					
	make_float(cl, 'Base Factor [GJ/d]')
	make_float(cl, 'Heat Factor [GJ/d]')
	
	bf = 0
	hf = 0
	
	for customer in cl:
		for k, v in customer.items():
			if k == 'Base Factor [GJ/d]':
				bf += v
			if k == 'Heat Factor [GJ/d]':
				hf += v
	
	if region == 'n': 
		temps = np.array([-40, -35, -30, -25, -20, -15, -10, -5, 0, 5, 10, 15, 20])
	else:
		temps = np.array([-36, -30, -25, -20, -15, -10, -5, 0, 5, 10, 15, 20])
	bp = float(raw_input('What is the balance point of the system? \n'))
	dd = bp - temps
	dd[dd < 0] = 0
	
	loads = []
	
	for day in dd:
		load = (bf +hf*day)
		loads.append(load)
	
	loads = np.asarray(loads)
	
	phf_100_n = [1.5, 1.55, 1.6, 1.65, 1.67, 1.7, 1.71, 1.75, 1.77, 1.8, 1.82, 1.9, 1.9]
	phf_1000_n = [1.1, 1.12, 1.15, 1.19, 1.23, 1.31, 1.35, 1.37, 1.4, 1.45, 1.49, 1.54, 1.54]
	phf_10000_n = [1.1, 1.13, 1.16, 1.21, 1.27, 1.33, 1.35, 1.39, 1.41, 1.45, 1.5, 1.55, 1.55 ]
	phf_100000_n = [1.1, 1.15, 1.175, 1.21, 1.25, 1.28, 1.32, 1.36, 1.39, 1.425, 1.47, 1.51, 1.51]

	phf_100_s = [1.35, 1.5, 1.6, 1.72, 1.9, 2.1, 2.15, 2.4, 2.7, 2.9, 3.3, 3.6]
	phf_1000_s = [1.1, 1.18, 1.225, 1.25, 1.28, 1.34, 1.39, 1.43, 1.48, 1.51, 1.55, 1.55]
	phf_10000_s = [1.1, 1.18, 1.23, 1.27, 1.31, 1.36, 1.43, 1.47, 1.52, 1.53, 1.63, 1.63]
	phf_100000_s = [1.1, 1.16, 1.22, 1.28, 1.34, 1.41, 1.47, 1.55, 1.63, 1.71, 1.79, 1.79]
	
	this_one = [] # Identify the chosen PHF vector

	if (region == 'n') and (len(cl) < 100):
		loads = loads*phf_100_n
		this_one = phf_100_n
	elif (region == 'n') and (len(cl) < 1000):
		loads = loads*phf_1000_n
		this_one = phf_1000_n
	elif (region == 'n') and (len(cl) < 10000):
		loads = loads*phf_10000_n
		this_one = phf_10000_n
	elif (region == 'n') and (len(cl) >= 10000):
		loads = loads*phf_100000_n
		this_one = phf_100000_n
	# elif (region == 's') and (len(cl) < 100):
	#	loads = loads*phf_100_s
	elif (region == 's') and (len(cl) < 1000):
		loads = loads*phf_1000_s
		this_one = phf_1000_s
	elif (region == 's') and (len(cl) < 10000):
		loads = loads*phf_10000_s
		this_one = phf_10000_s
	elif (region == 's') and (len(cl) >= 10000):
		loads = loads*phf_100000_s
		this_one = phf_100000_s
		
	
	if len(b_fqc) > 0 and fqc == "y":
		total_3_yr = []
		for customer in b_fqc:
			total_3_yr.append(customer["HUC 3-Year Peak Demand"])
		loads = loads + sum(total_3_yr)
		cl += b_fqc
	
	if (option == '1' and len(intts) == 1) or (config.lower() == 'isolated'):
		print "\n"
		print_system_info(ds,intts[0][0],config,cl)
		print "\n"
		print_load(temps, loads, this_one, ds)
	
	elif (option == '2' and config.lower() == 'integrated') or (len(intts) > 1):
		print "\n"
		print_multiple_stations(ds, intts, cl)
		if incorrect_splits == 'n':
			print "Sum of station splits: " + str(split_sum)
			raw_input('''\nThe station splits of this system do not add up to 1.
Press ENTER to acknowledge and continue.''')
		print ""
		print_multiple_loads(temps, loads, this_one, intts)
		
	try:
		equation = make_plot(temps, loads, ds)
	except ValueError:
		print "\nThe load on this system is too low to be plotted properly."
	
	
	print "\nThe equation of the polynomial fit is: \n{}".format(equation)
	
	raw_input('Press ENTER to exit')