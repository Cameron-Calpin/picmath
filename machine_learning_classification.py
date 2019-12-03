import pandas
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import random
from sklearn.linear_model import LinearRegression
from mlxtend.regressor import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
	
filename = 'selected_crimes/All_Crimes_Shuffled.csv'
names = ['OFFENSE', 'X_Coordinates', 'Y_Coordinates', 'Zones']


dataset = pandas.read_csv(filename, names=names)

# convert dataframe from string to float
X = pandas.to_numeric(dataset['X_Coordinates'])
X = pandas.to_numeric(dataset['Y_Coordinates'])

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
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

scaler = StandardScaler()
scaler.fit(X_train)

X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)

classifier = KNeighborsClassifier(n_neighbors=38)
classifier.fit(X_train, y_train)

y_pred = classifier.predict(X_test)

print confusion_matrix(y_test, y_pred)
print classification_report(y_test, y_pred)
print 'Accuracy Score: ', accuracy_score(y_test, y_pred)
print '\n\n'

'''
Logistic Regression
'''
logreg = LogisticRegression()
logreg.fit(X_train, y_train)

print '\n\nLogistic Regression'
print '---------------------'
print 'Accuracy of Logistic regression classifier on training set: {:.2f}'.format(logreg.score(X_train, y_train))
print 'Accuracy of Logistic regression classifier on test set: {:.2f}'.format(logreg.score(X_test, y_test))

'''
Decision Tree
'''
clf = DecisionTreeClassifier().fit(X_train, y_train)

print '\n\nDecision Tree'
print '--------------'
print 'Accuracy of Decision Tree classifier on training set: {:.2f}'.format(clf.score(X_train, y_train))
print 'Accuracy of Decision Tree classifier on test set: {:.2f}'.format(clf.score(X_test, y_test))

'''
K-Nearest Neighbors
'''
knn = KNeighborsClassifier()
knn.fit(X_train, y_train)

print '\n\nK-Nearest Neighbors'
print '--------------------'
print 'Accuracy of K-NN classifier on training set: {:.2f}'.format(knn.score(X_train, y_train))
print 'Accuracy of K-NN classifier on test set: {:.2f}'.format(knn.score(X_test, y_test))

'''
Linear Discriminant Analysis
'''
lda = LinearDiscriminantAnalysis()
lda.fit(X_train, y_train)

print '\n\nLinear Discriminant Analysis'
print '----------------------------'
print 'Accuracy of LDA classifier on training set: {:.2f}'.format(lda.score(X_train, y_train))
print 'Accuracy of LDA classifier on test set: {:.2f}'.format(lda.score(X_test, y_test))

'''
Gaussian Naive Bayes
'''
gnb = GaussianNB()
gnb.fit(X_train, y_train)

print '\n\nGaussian Naive Bayes'
print '---------------------'
print 'Accuracy of GNB classifier on training set: {:.2f}'.format(gnb.score(X_train, y_train))
print 'Accuracy of GNB classifier on test set: {:.2f}'.format(gnb.score(X_test, y_test))

'''
Support Vector Machine
'''
svm = SVC()
svm.fit(X_train, y_train)

print '\n\nSupport Vector Machine'
print '-----------------------'
print 'Accuracy of SVM classifier on training set: {:.2f}'.format(svm.score(X_train, y_train))
print 'Accuracy of SVM classifier on test set: {:.2f}'.format(svm.score(X_test, y_test))

'''
One way to help you find the best value of K is to plot
the graph of K value and the corresponding error rate 
for the dataset.

We plot the mean error for the predicted values of test 
set for all the K values between 1 and 40.

Calculate the mean of error for all the predicted values 
where K ranges from 1 and 40.
'''
error = []

for i in range(1, 40):  
    knn = KNeighborsClassifier(n_neighbors=i)
    knn.fit(X_train, y_train)
    pred_i = knn.predict(X_test)
    error.append(np.mean(pred_i != y_test))

# plt.figure(figsize=(12, 6))  
# plt.plot(range(1, 40), error, color='red', linestyle='dashed', marker='o',  
# 	markerfacecolor='blue', markersize=10)
# plt.title('Error Rate K Value')  
# plt.xlabel('K Value')  
# plt.ylabel('Mean Error') 
# plt.show()