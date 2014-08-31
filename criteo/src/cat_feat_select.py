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
parser.add_argument('-f', '--field', type = str, help = "Fields to extract from table")
parser.add_argument('-x', '--seedno', type = int, help = 'set random seed number')
parser.add_argument('-a', '--train_pos', type = str, help = 'name of dataframe to save results to')
parser.add_argument('-b', '--train_neg', type = str, help = 'name of store to save results to')

args = parser.parse_args()

# Open data stores
train_store = HDFStore('queries/train_queries.h5')
# Extract data frames
train_df = concat([train_store[args.train_pos].ix[:,['Label',args.field]], train_store[args.train_neg].ix[:,['Label',args.field]]])
# Close data stores
train_store.close()

features = []
with open('data/categorical_features/feats_%s.csv' % args.field, 'r') as theFile:
	for item in theFile:
		features.append(item.strip('\n'))

print features

for f in features:
	print f
	print args.field + f
	print train_df[args.field]
	train_df[args.field+"_"+f] = (train_df[args.field] == f)*1

train_df = train_df.drop(args.field, axis = 1)

y = train_df['Label'].values
X = train_df.ix[:,1:].values	

from sklearn.svm import LinearSVC

clf = LinearSVC(C = 0.01, penalty = "l1", dual = False)

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
print clf.get_params()