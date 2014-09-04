### cv_analysis.py

from pandas import DataFrame, HDFStore, Series, concat
import numpy as np
from sklearn.cross_validation import StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score, log_loss
import random as rd
import argparse
import h5py


# Set parameters
parser = argparse.ArgumentParser()
parser.add_argument('-x', '--seedno', type = int, help = 'set random seed number')
parser.add_argument('-i', '--input_file', type = str, help = 'name of dataframe to save results to')
parser.add_argument('-n', '--dataname', type = str, help = 'name of dataframe to save results to')
parser.add_argument('-v', '--crossval',  action='store_true', default = False)
parser.add_argument('-s', '--submit', type = str, help = 'name of store to save results to', default = None)

args = parser.parse_args()

# Read data
h5f = h5py.File(args.input_file, 'r')
y = h5f[args.dataname][:,0]
X = h5f[args.dataname][:,1:]
h5f.close()

clf = LogisticRegression(C = 1, random_state = args.seedno)

# Perform cross validation
if args.crossval == True:
	print "Performing cross validation..."
	## CV
	cv = StratifiedKFold(y, n_folds = 3, shuffle = True, random_state = args.seedno)

	score = []
	for train_index, test_index in cv:
		print("TRAIN:", train_index, "TEST:", test_index)
		X_train, X_test = X[train_index], X[test_index]
		y_train, y_test = y[train_index], y[test_index]

		clf.fit(X_train, y_train)
		result = clf.predict_proba(X_test)
		cv_score = log_loss(y_test,result)
		print cv_score
		score.append(cv_score)

	print score
	print np.array(score).mean()
	print np.array(score).std()


# Retrain classifier and make submition
if args.submit != None:
	# Make final predictions on test set
	print "Training final model..."
	clf.fit(X,y)

	print "Making test predictions..." 
	result = clf.predict_proba(test_X)
	y_hat = [class_prob[1] for class_prob in result]
	submission = DataFrame(test_df['Id'])
	submission['Predicted'] = Series(y_hat, index = submission.index)
	submission.to_csv(args.submit, index = False)
