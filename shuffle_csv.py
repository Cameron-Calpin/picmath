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
from sklearn.model_selection import train_test_split

path = r'/home/frostbyte/Desktop/CNU/MATH 395/picmath/selected_crimes'
all_files = glob.glob(path + "/*.csv")

filenames = []
intercepts = []
slopes = []

# filename = 'thats_a_lot_of_csv_files/DrugNarcotics_Offenses.csv'
# for filename in all_files[0:1]:
# 	print filename

	
filename = 'selected_crimes/All_Crimes.csv'
names = ['REPORT NUMBER', 'DATA', 'TIME', 'OFFENSE', 'ADDRESS', 'X_Coordinates', 'Y_Coordinates', 'Zones']

dataset = pandas.read_csv(filename, names=names)
new_dataset = dataset.sample(frac=1)
new_dataset.to_csv('<put name here>.csv')

print new_dataset