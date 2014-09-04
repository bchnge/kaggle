### train.py

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
import argparse
from sklearn.externals import joblib

# Set parameters
parser = argparse.ArgumentParser()
parser.add_argument('-x', '--seedno', type = int, help = 'set random seed number', default = 123)
parser.add_argument('-i', '--input_file', type = str, help = 'name of dataframe to save results to')
parser.add_argument('-m', '--model', type = str, help = 'name of dataframe to save results to')
args = parser.parse_args()

# Read data
df = pd.read_csv(args.input_file)
y = df.ix[:,0].values
X = df.ix[:,1:].values

print "Now training classifier"
clf = LogisticRegression(C = 0.5, random_state = args.seedno)
clf.fit(X,y)

print "Finished. Now saving model"
joblib.dump(clf, args.model)