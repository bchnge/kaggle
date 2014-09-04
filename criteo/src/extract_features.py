# extract_features.py

''' extract features and create training set
'''
import argparse
from pandas import DataFrame,HDFStore,concat
from sklearn.linear_model import LogisticRegression
from sklearn.externals import joblib

# Set parameters
parser = argparse.ArgumentParser()
parser.add_argument('-d', '--datastore', type = str, help = 'Name of database')
parser.add_argument('-n', '--numeric_fields', nargs='+', type = str, help = "Fields to get categorical features for")
parser.add_argument('-c', '--categorical_fields', nargs='+', type = str, help = "Fields to get categorical features for")
parser.add_argument('-o', '--output_filename', type = str, help = "Fields to get categorical features for")
parser.add_argument('-r', '--C', type = float, help = 'name of store to save results to', default = 0.001)
parser.add_argument('-f', '--training_filename', type = str, help = "Fields to get categorical features for")
parser.add_argument('-x', '--seedno', type = int, help = 'name of store to save results to', default = 123)
args = parser.parse_args()

data_store = HDFStore(args.datastore)
df = concat([ data_store['pos'], data_store['neg']])
df.to_csv(args.training_filename, index = False)
print 'Finished saving training file as ' + args.training_filename
first_col = 'Label'
data_store.close()

y = df[first_col].values

clf = LogisticRegression(C=args.C, penalty = 'l1', random_state = args.seedno)

d = {}

print "Processing numerical features"
mean_values = df.ix[:, args.numeric_fields].mean(axis = 1).values
print mean_values
for idx in range(0, len(args.numeric_fields)):
	d[args.numeric_fields[idx]] = ('impute', mean_values[idx])

print "Processing categorical features"
for field in args.categorical_fields:
	print field
	# Load feature file for field
	features = []
	with open('data/categorical_features/feats_%s.csv' % field, 'r') as theFile:
		for item in theFile:
			features.append(item.strip('\n'))
	X = (df[field].values.reshape((len(df[field]),1)) == features) * 1

	# Classify using field features
	clf.fit(X,y)

	# Store selected features
	coefficients = clf.coef_[0]
	selected_features = []
	for idx in xrange(0,len(coefficients)):
		if coefficients[idx] !=0:
			selected_features.append(features[idx])

	d[field] = ('categorical', selected_features)
    
joblib.dump(d, args.output_filename)