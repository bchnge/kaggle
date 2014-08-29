# eval_class_performance.py
import numpy as np
from sklearn.metrics import log_loss
from sklearn.linear_model import ElasticNetCV, LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import StratifiedKFold
from pandas import HDFStore, concat
import argparse
from sklearn.naive_bayes import GaussianNB


parser = argparse.ArgumentParser()
parser.add_argument('-f', '--fields', nargs='+', type = str, help = "Fields to extract from table")
parser.add_argument('-x', '--seedno', type = int, help = 'set random seed number')
parser.add_argument('-a', '--train_pos', type = str, help = 'name of dataframe to save results to')
parser.add_argument('-b', '--train_neg', type = str, help = 'name of store to save results to')

args = parser.parse_args()

# Open data stores
train_store = HDFStore('queries/train_queries.h5')

# Extract data frames
train_df = concat([train_store[args.train_pos], train_store[args.train_neg]])

# Close data stores
train_store.close()

# read data
for f in args.fields:
	train_df[f] = train_df[f].replace('',np.nan)

# Obtain imputation values
median_values = train_df.ix[:, args.fields].median(axis = 0)
mean_values = train_df.ix[:, args.fields].mean(axis = 0)
impute_values = mean_values 

# set up imputation dictionary
impute_dict = dict(zip(args.fields, impute_values))
train_df = train_df.fillna(impute_dict)

y = train_df['Label'].values
X = train_df.ix[:,args.fields].values	

cv = StratifiedKFold(y, n_folds = 3, shuffle = True, random_state = 123)

#en = ElasticNetCV(l1_ratio = [0, .1, .5, .7, .9, .95, .99, 1], n_jobs = -1)
en = GaussianNB()
rf = RandomForestClassifier(oob_score = True)
lr = LogisticRegression()

scores = np.matrix([[0,0,0],[0,0,0],[0,0,0]])

fold = 0
for train_index, test_index in cv:
	fold +=1
	print "fold " + str(fold) + '...'
	X_train, X_test = X[train_index], X[test_index]
	y_train, y_test = y[train_index], y[test_index]

	for i, clf in enumerate([en, rf, lr]):
		print "Evaluating classifier" 
		print clf
		print "on fold" + str(fold)
		clf.fit(X, y)
		result = clf.predict_proba(X_test)
		cv_score = log_loss(y_test,result)
		print cv_score
		scores[fold-1][i] = cv_score

print en
print scores[:,0].mean()

print rf
print scores[:,1].mean()

print lr
print scores[:,2].mean()
