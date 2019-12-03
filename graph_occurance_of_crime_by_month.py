import pandas
from pandas import ExcelWriter
from pandas.plotting import scatter_matrix
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import datetime
from itertools import groupby
import itertools
import glob
import os
# from sklearn.cross_validation import train_test_split
# from sklearn.linear_model import LinearRegression
from mlxtend.regressor import LinearRegression

path = r'/home/frostbyte/Desktop/CNU/MATH 395/picmath/selected_crimes'
all_files = glob.glob(path + "/*.csv")

filenames = []
intercepts = []
slopes = []

# filename = 'thats_a_lot_of_csv_files/DrugNarcotics_Offenses.csv'
for filename in all_files[:]:
	print filename

	if filename == '/home/frostbyte/Desktop/CNU/MATH 395/picmath/thats_a_lot_of_csv_files/Police_Incident_Reports.csv':
		continue
	else:

		# filename = all .csv files in thats_a_lot_of_csv_files
		names = ['REPORT NUMBER', 'DATE', 'TIME', 'OFFENSE', 'ADDRESS', 'X_Coordinates', 'Y_Coordinates', 'Zones']
		dataset = pandas.read_csv(filename, names=names)
		# print dataset.shape
		# Creates csv sheets
		# df = pandas.read_excel(xlsxfile, sheet)
		# woo = df.to_csv(sheet_file, encoding='utf-8', index=False)
		# print(woo)

		x = dataset.X_Coordinates.tolist()
		y = dataset.Y_Coordinates.tolist()

		dates = dataset.DATE.tolist()
		times = dataset.TIME.tolist()
		# print(dates)

		new_dates = dates[1:]
		# print new_dates
		datee = []
		for i in range(len(new_dates)):
			datee.append(str(new_dates[i]))


		# for i in range(len(datee)):
			# print(datee[i])
		# print(datee)


		# slice off the day in datetime
		new_new_dates = [w[:-3] for w in datee]
		# print(new_new_dates)

		# tally up month duplicates
		month_count = [len(list(group)) for key, group in groupby(new_new_dates)]
		# print(month_count)

		# for i in range(len(new_dates)):
		# 	more_dates = datetime.datetime.strptime(new_dates[i], "%Y-%m-%d")
			# print(more_dates)

		# remove duplicates
		new_new_dates = list(dict.fromkeys(new_new_dates))
		new_new_dates.sort()
		# print(new_new_dates)


		index = np.arange(len(new_new_dates))
		# plt.bar(index, month_count)
		# plt.xlabel('Month', fontsize=8)
		# plt.ylabel('Occurance', fontsize=8)
		# plt.xticks(index, new_new_dates, fontsize=8, rotation=30)
		# plt.title('Aggravated Assault Occurances by Month')
		# plt.show()

		# index = np.arange(len(new_new_dates))
		# plt.scatter(index, month_count)
		# plt.xlabel('Month', fontsize=8)
		# plt.ylabel('Occurance', fontsize=8)
		# plt.xticks(index, new_new_dates, fontsize=8, rotation=30)
		# plt.title('Aggravated Assault Occurances by Month')
		# plt.show()

		mult_index = []
		for i in range(len(index)):
			mult_index.append(i)	# if mult-dim array, put [i]
		# print mult_index

		mult_month_count = []
		for j in month_count:
			mult_month_count.append([j])
		# print mult_month_count

		X = np.array(mult_index)[:, np.newaxis]
		y = np.array(month_count)
		# print len(X)
		# print len(y)
		# print "X: ", X
		# print "y: ", y

		# Linear Regression
		# reg = LinearRegression(minibatches=None)
		# reg.fit(X, y)

		reg = LinearRegression(minibatches=None)
		reg.fit(X, y)

		# X_train, X_test, y_train, y_test

		file_name = filename[70:]
		file_name = file_name.replace(".csv", "")
		# print file_name
		# print reg.w_
		print 'Intercept: %.2f' % reg.b_
		print 'Slope: %.2f\n' % reg.w_[0]

		filenames.append(file_name)
		intercepts.append(reg.b_)
		slopes.append(reg.w_)

		plt.scatter(X, y, c='blue')
		plt.plot(X, reg.predict(X), color='red')
		plt.show()



		# mult_index_X_train = mult_index[:-15]
		# mult_index_X_test = mult_index[-20:]

		# mult_month_count_y_train = mult_month_count[:-15]
		# mult_month_count_y_test = mult_month_count[-20:]

		# lm = LinearRegression()
		# lm.fit(mult_index_X_train, mult_month_count_y_train)

		# mult_month_count_y_pred = lm.predict(mult_index_X_test)

		# plt.scatter(mult_index_X_test, mult_month_count_y_pred, color='blue', linewidth=3)
		# plt.show()

		print intercepts
		print filenames
		print slopes

		path_to_excel = r"/home/frostbyte/Desktop/CNU/MATH 395/picmath/LinearRegressionTests.xlsx"
		writer = pandas.ExcelWriter(path_to_excel)
		continue

# for i in range(len(intercepts)):
# 	df = pandas.DataFrame({'Intercept':intercepts[i], 'Slope':[slopes[i]]})
# 	df.to_excel(writer, sheet_name=filenames[i])
# 	writer.save()
# writer.close()