import pandas
from pandas import ExcelWriter
from pandas.plotting import scatter_matrix
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap
from sklearn import neighbors, datasets
import datetime
from itertools import groupby
import itertools
import xlrd, datetime

path = r'/home/frostbyte/Desktop/CNU/MATH 395/picmath/thats_a_lot_of_csv_files'
all_files = glob.glob(path + "/*.csv")


for filename in all_files[0:1]:
	# print filename

	if filename == '/home/frostbyte/Desktop/CNU/MATH 395/picmath/thats_a_lot_of_csv_files/Police_Incident_Reports.csv':
		continue
	else:
	# print(sheet_file)


	# df = pandas.read_excel(xlsxfile, sheet)
	# woo = df.to_csv(sheet_file, encoding='utf-8', index=False)
	# print(woo)

	filename = 'Aggravated Assault.csv'
	names = ['DATE', 'TIME', 'Zones']
	dataset = pandas.read_csv(filename, names=names)

	zones = dataset.Zones.tolist()
	
	new_zones = zones[1:]
	# print new_zones

	O = 0
	R = 0
	C = 0
	NZ = 0
	M = 0
	for zone in new_zones:
		if zone == 'O':
			O = O + 1
		elif zone == 'R':
			R= R + 1
		elif zone == 'C':
			C = C + 1
		elif zone == 'M':
			M = M + 1
		else:
			NZ = NZ + 1
	
	print "Total zones: ", len(new_zones)
	print "O: ", O
	print "R: ", R
	print "C: ", C
	print "NZ: ", NZ
	print "M: ", M