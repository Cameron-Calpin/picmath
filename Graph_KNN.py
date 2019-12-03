import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from matplotlib.colors import ListedColormap, BoundaryNorm
import matplotlib.patches as mpatches
import matplotlib.patches as mpatches

filename = 'selected_crimes/All_Crimes_Shuffled.csv'
names = ['OFFENSE', 'X_Coordinates', 'Y_Coordinates', 'Zones']


dataset = pd.read_csv(filename, names=names)

# convert dataframe from string to float
X = pd.to_numeric(dataset['X_Coordinates'])
X = pd.to_numeric(dataset['Y_Coordinates'])

# This is a [x, 2] matrix, with X_Coordinates and
# Y_Coorinates as the columns
X = dataset.iloc[:, 1:-1].values
# X = pandas.to_numeric(X)
# for h in range(len(X)):
# 	print X[h]

# This is a [x, 1] matrix, with OFFENSES (Crimes)
# as the prediction columns
y = dataset.iloc[:, 0].values
# print y
crimes = dataset['OFFENSE']
# zones = dataset['Zones']

# Assignming variables and splitting up our data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.0005, random_state=42)

def plot_fruit_knn(X, y, n_neighbors, weights):
	# print X
	# print y
	X_lat = dataset['X_Coordinates']
	X_lon = dataset['Y_Coordinates']
	# print X_mat

	# Create color maps
	cmap_light = ListedColormap(['#FFAAAA', '#AAFFAA', '#AAAAFF','#AFAFAF'])
	cmap_bold  = ListedColormap(['#FF0000', '#00FF00', '#0000FF','#AFAFAF'])
	clf = KNeighborsClassifier(n_neighbors=n_neighbors, weights=weights)
	clf.fit(X, y)

	# Plot the decision boundary by assigning a color in the color map
	# to each mesh point.  
	mesh_step_size = .001  # step size in the mesh
	plot_symbol_size = 25

	x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
	y_min, y_max = X[:, -1].min() - 1, X[:, -1].max() + 1
	xx, yy = np.meshgrid(np.arange(x_min, x_max, mesh_step_size), 
		np.arange(y_min, y_max, mesh_step_size))
	Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])

	# Put the result into a color plot
	Z = Z.reshape(xx.shape)
	plt.figure()
	plt.pcolormesh(xx, yy, Z, cmap=cmap_light)

	# Plot training points
	for h in range(len(X_lon)):
		# print crimes[h]
		# print type(X_lon[h])
		if crimes[h] == 'AGGRAVATED ASSAULT':
			plt.scatter(X_lat[h], X_lon[h], c='blue')
		elif crimes[h] == 'DRUG/NARCOTICS OFFENSES':
			plt.scatter(X_lat[h], X_lon[h], c='red')
		elif crimes[h] == 'LARCENY':
			plt.scatter(X_lat[h], X_lon[h], c='green')
		elif crimes[h] == 'ROBBERY':
			plt.scatter(X_lat[h], X_lon[h], c='purple')
		elif crimes[h] == 'SEX ASSAULT, RAPE':
			plt.scatter(X_lat[h], X_lon[h], c='orange')
		elif crimes[h] == 'VEHICLE THEFT':
			plt.scatter(X_lat[h], X_lon[h], c='brown')
		elif crimes[h] == 'OVERDOSE':
			plt.scatter(X_lat[h], X_lon[h], c='cyan')
		else:
			plt.scatter(X_lat[h], X_lon[h], c='black')
	# plt.scatter(dataset['X_Coordinates'], dataset['Y_Coordinates'], s=plot_symbol_size, c=7, cmap=cmap_bold, edgecolor = 'black')
	plt.xlim(xx.min(), xx.max())
	plt.ylim(yy.min(), yy.max())
	patch0 = mpatches.Patch(color='blue', label='AGGRAVATED ASSAULT')
	patch1 = mpatches.Patch(color='red', label='DRUG/NARCOTICS OFFENSES')
	patch2 = mpatches.Patch(color='green', label='LARCENY')
	patch3 = mpatches.Patch(color='cyan', label='OVERDOSE')
	patch4 = mpatches.Patch(color='purple', label='ROBBERY')
	patch5 = mpatches.Patch(color='orange', label='SEX ASSAULT, RAPE')
	patch6 = mpatches.Patch(color='brown', label='VEHICLE THEFT')
	plt.legend(handles=[patch0, patch1, patch2, patch3, patch4, patch5, patch6])
	plt.xlabel('latitude')
	plt.ylabel('longitude')
	plt.title("4-Class classification (k = %i, weights = '%s')"
	           % (n_neighbors, weights))    
	plt.show()

plot_fruit_knn(X_train, y_train, 38, 'uniform')