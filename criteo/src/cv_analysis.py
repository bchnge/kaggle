### cv_analysis.py

from pandas import DataFrame, HDFStore, Series, concat
import numpy as np
from sklearn.cross_validation import StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score, log_loss
import random as rd
import argparse

# Set parameters
parser = argparse.ArgumentParser()
parser.add_argument('-f', '--fields', nargs='+', type = str, help = "Fields to extract from table")
parser.add_argument('-x', '--seedno', type = int, help = 'set random seed number')
parser.add_argument('-a', '--train_pos', type = str, help = 'name of dataframe to save results to')
parser.add_argument('-b', '--train_neg', type = str, help = 'name of store to save results to')
parser.add_argument('-c', '--test', type = str, help = 'name of store to save results to')
parser.add_argument('-v', '--crossval',  action='store_true', default = False)
parser.add_argument('-s', '--submit', type = str, help = 'name of store to save results to', default = None)

args = parser.parse_args()

# Open data stores
train_store = HDFStore('queries/train_queries.h5')
test_store = HDFStore('queries/test_queries.h5')

# Extract data frames
train_df = concat([train_store[args.train_pos], train_store[args.train_neg]])
test_df = test_store[args.test]

# Close data stores
train_store.close()
test_store.close()

# Replace '' with NaN
for f in args.fields:
	train_df[f] = train_df[f].replace('',np.nan)
	test_df[f] = test_df[f].replace('',np.nan)

# Obtain imputation values
median_values = train_df.ix[:, args.fields].median(axis = 0)
mean_values = train_df.ix[:, args.fields].mean(axis = 0)
impute_values = mean_values 

# set up imputation dictionary
impute_dict = dict(zip(args.fields, impute_values))
train_df = train_df.fillna(impute_dict)
test_df = test_df.fillna(impute_dict)

y = train_df['Label'].values
X = train_df.ix[:,args.fields].values	

test_X = test_df.ix[:,args.fields].values

if args.crossval == True:
	print "Performing cross validation..."
	## CV
	cv = StratifiedKFold(y, n_folds = 3, shuffle = True, random_state = args.seedno)

	score = []
#	clf = LogisticRegression(C = 0.5, random_state = args.seedno)
	clf = RandomForestClassifier(n_estimators = 50, random_state = args.seedno)
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

if args.submit != None:
	# Make final predictions on test set
	print "Training final model..."
	clf.fit(X,y)

	print "Making test predictions..." 
	result = CLF.predict_proba(test_X)
	y_hat = [class_prob[1] for class_prob in result]
	submission = DataFrame(test_df['Id'])
	submission['Predicted'] = Series(y_hat, index = submission.index)
	submission.to_csv(args.submit, index = False)
