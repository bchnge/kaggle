from pandas import DataFrame, HDFStore, Series
import numpy as np
from zipfile import ZipFile
from sklearn.cross_validation import StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, log_loss
import random as rd

# Read dataframes from stores
store = HDFStore('store1')
df = store['train_sample_123']
store.close()

rd.seed(123)

test_store = HDFStore('test_store')
test_df = test_store['test_1']
test_store.close()

# Replace '' with NaN
for column in df.columns[1:]:
	df[column] = df[column].replace('',np.nan)
	test_df[column] = test_df[column].replace('',np.nan)

# obtain impute value
median_values = df.median(axis = 0)
mean_values = df.mean(axis = 0)

# set up imputation dictionary
impute_dict = dict(zip(df.columns[1:], mean_values[1:]))
df = df.fillna(impute_dict)
test_df = test_df.fillna(impute_dict)

y = df['Label'].values
X = df.ix[:,1:].values	

test_X = test_df.ix[:,1:].values


### CV

# cv = StratifiedKFold(y, n_folds = 3)

# score = []
# for train_index, test_index in cv:
# 	print("TRAIN:", train_index, "TEST:", test_index)
# 	X_train, X_test = X[train_index], X[test_index]
# 	y_train, y_test = y[train_index], y[test_index]

# 	clf = LogisticRegression(C = 0.5)
# 	clf.fit(X_train, y_train)
# 	result = clf.predict_proba(X_test)
# #	y_hat = [class_prob[1] for class_prob in result]
# #	score.append(roc_auc_score(y_test, y_hat))
# 	score.append(log_loss(y_test, result))


# print score
# print np.array(score).mean()
# print np.array(score).std()


#####
CLF = LogisticRegression(C = 0.5)
print "Training final model..."
CLF.fit(X, y)

print "Making predictions..." 
result = CLF.predict_proba(test_X)
y_hat = [class_prob[1] for class_prob in result]

submission = DataFrame(test_df['Id'])
submission['Predicted'] = Series(y_hat)

submission.to_csv('submission_2.csv', index = False)
