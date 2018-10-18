import sqlite3
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from time import time
from IPython.display import display

from Data import Data

from sklearn.neighbors import KNeighborsClassifier

from sklearn.linear_model import RidgeClassifier
from sklearn.linear_model import Lasso
from sklearn.linear_model import ElasticNet

from sklearn.neural_network import MLPClassifier

from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV

from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler

from sklearn.tree import DecisionTreeClassifier

from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier

from sklearn.svm import SVC

from sklearn.metrics import classification_report

import warnings
from sklearn.exceptions import UndefinedMetricWarning

warnings.filterwarnings('ignore', category=UndefinedMetricWarning)

data = Data()
data.rpTime = True
data.computeHeadersMask()
samples = data.getSamples()
target = data.getTargets()

print("Total samples shape: {}".format(samples.shape))
print("Targets shape: {}".format(target.shape))

X_train, X_test, y_train, y_test = train_test_split(samples, target, random_state=5, )

indices = []
count = 0
for y in y_train:
	if list(y_train).count(y) < 5:
		index = list(y_train).index(y)
		indices.append(count)
		#y_train = np.delete(y_train, y)
		#X_train = np.delete(X_train, index, axis=0)
	count += 1
print(indices)
y_train = np.delete(y_train, indices)
X_train = np.delete(X_train, indices, axis=0)

indices = []
count = 0
for y in y_test:
	if list(y_test).count(y) < 5:
		index = list(y_test).index(y)
		indices.append(count)
		#y_test = np.delete(y_test, y)
		#X_test = np.delete(X_test, index, axis=0)
	count += 1
print(indices)
y_test = np.delete(y_test, indices)
X_test = np.delete(X_test, indices, axis=0)


#scaler = MinMaxScaler((0, 1))
scaler = StandardScaler()
scaler.fit(X_train)
X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)

print("X_train shape: {}".format(X_train.shape))
print("y_train shape: {}".format(y_train.shape))
print("Minimum for each feature\n{}".format(X_train.min(axis = 0)))
print("Maximum for each feature\n{}".format(X_train.max(axis = 0)))

classifier = None
algo = 8

if (algo == 0):
	classifier = KNeighborsClassifier(n_neighbors=3)

if (algo == 1):
	classifier = RidgeClassifier(alpha=1000)

if (algo == 2):
	classifier = Lasso(alpha=0.01, max_iter=100000)

if (algo == 3):
	classifier = ElasticNet(max_iter=100000)

if (algo == 4):
	classifier = MLPClassifier([8, 12, 8], alpha=0.0001, max_iter=10000, solver='adam', activation='logistic')

if (algo == 5):
	classifier = DecisionTreeClassifier(max_depth=14)

if (algo == 6):
	classifier = RandomForestClassifier(n_estimators=100, max_depth=10)

if (algo == 7):
	classifier = GradientBoostingClassifier(n_estimators=200, max_depth=15)

if (algo == 8):
	classifier = SVC(C=100, gamma=0.004)

if (algo == 9):
	t0 = time()
	# Set the parameters by cross-validation
	tuned_parameters = {'kernel': ['rbf'], 'gamma': [0.009, 0.008, 0.007, 0.006, 0.005, 0.004, 0.003, 0.002, 0.001, 0.0009, 0.0008, 0.0007, 0.0006, 0.0005, 0.0004, 0.0003, 0.0002, 0.0001, 9e-05, 8e-05, 7e-05, 6e-05, 5e-05, 4e-05, 3e-05, 2e-05, 1e-05],
    	'C': [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0, 100.0, 200.0, 300.0, 400.0, 500.0, 600.0, 700.0, 800.0, 900.0, 1000.0, 2000.0, 3000.0, 4000.0, 5000.0, 6000.0, 7000.0, 8000.0, 9000.0, 10000.0]}
	scores = ['precision', 'recall']
	for score in scores:
		print("# Tuning hyper-parameters for %s" % score)
		print()

		clf = GridSearchCV(SVC(), tuned_parameters, cv=5,
		                   scoring='%s_macro' % score)
		clf.fit(X_train, y_train)
		print("Done in %0.3fs" % (time() - t0))
		print()

		print("Best parameters set found on development set:")
		print()
		print(clf.best_params_)
		print()
		print("Grid scores on development set:")
		print()
		means = clf.cv_results_['mean_test_score']
		stds = clf.cv_results_['std_test_score']
		for mean, std, params in zip(means, stds, clf.cv_results_['params']):
		    print("%0.3f (+/-%0.03f) for %r"
		          % (mean, std * 2, params))
		print()

		print("Detailed classification report:")
		print()
		print("The model is trained on the full development set.")
		print("The scores are computed on the full evaluation set.")
		print()
		y_true, y_pred = y_test, clf.predict(X_test)
		print(classification_report(y_true, y_pred))
		print()
	

if algo != 9:
	classifier.fit(X_train, y_train)

	print("Train set score: {:.2f}".format(classifier.score(X_train, y_train)))
	print("Test set score: {:.2f}".format(classifier.score(X_test, y_test)))
