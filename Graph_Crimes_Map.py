import pandas
from pandas import ExcelWriter
from pandas.plotting import scatter_matrix
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import sphviewer as sph
from matplotlib.colors import ListedColormap
from sklearn import neighbors, datasets
import datetime
from itertools import groupby
import itertools
import glob
import random
from mpl_toolkits.basemap import Basemap
from sklearn.linear_model import LinearRegression
from mlxtend.regressor import LinearRegression

path = r'/home/frostbyte/Desktop/CNU/MATH 395/picmath/selected_crimes'
all_files = glob.glob(path + "/*.csv")

filenames = []
intercepts = []
slopes = []

	
filename = 'selected_crimes/All_Crimes.csv'
names = ['REPORT NUMBER', 'DATE', 'TIME', 'OFFENSE', 'ADDRESS', 'X_Coordinates', 'Y_Coordinates', 'Zones']

'''
n - number of rows in the csv file
s - number of rows to plot
'''
n = 13998
s = 500
skip = sorted(random.sample(xrange(n), n-s))
dataset = pandas.read_csv(filename, names=names, skiprows=skip)

# Four [x, 1] column matrices
x = dataset['X_Coordinates']
y = dataset['Y_Coordinates']
crimes = dataset['OFFENSE']
zones = dataset['Zones']


'''
This will go through all the rows and determine if
the crime column matches any of the statements then
assigns that crime a dot color.
'''
for h in range(len(x)):
	# print crimes[h]
	print type(x[h])
	if crimes[h] == 'AGGRAVATED ASSAULT':
		plt.scatter(x[h], y[h], c='blue')
	elif crimes[h] == 'DRUG/NARCOTICS OFFENSES':
		plt.scatter(x[h], y[h], c='red')
	elif crimes[h] == 'LARCENY':
		plt.scatter(x[h], y[h], c='green')
	elif crimes[h] == 'ROBBERY':
		plt.scatter(x[h], y[h], c='purple')
	elif crimes[h] == 'SEX ASSAULT, RAPE':
		plt.scatter(x[h], y[h], c='orange')
	elif crimes[h] == 'VEHICLE THEFT':
		plt.scatter(x[h], y[h], c='brown')
	elif crimes[h] == 'OVERDOSE':
		plt.scatter(x[h], y[h], c='cyan')
	else:
		plt.scatter(x[h], y[h], c='black')

plt.show()



