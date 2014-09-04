### classify.py
'''
Classify dataset given saved trained model
'''
import numpy as np
import csv
import sys
import argparse
from sklearn.externals import joblib

# Set parameters
parser = argparse.ArgumentParser()
parser.add_argument('-m', '--model', type = str, help = 'Path to pickled trained model')
parser.add_argument('-v', '--submission_header', nargs='+', type = str, help = "Column header for submission")
args = parser.parse_args()

reader = csv.reader(sys.stdin, delimiter = ',')
header = reader.next()
writer = csv.writer(sys.stdout, delimiter = ',')
writer.writerow(args.submission_header)

# Open trained model
clf = joblib.load(args.model)
if hasattr(clf, 'predict_proba'):
    for row in reader:
        value = [float(x) for x in row[1:]]
        result = clf.predict_proba(value)
        y_hat = result[0][1]
        writer.writerow([row[0], y_hat])
else:
    for row in reader:
        value = [float(x) for x in row[1:]]
        result = clf.predict(value)
        y_hat = result[0]
        writer.writerow([row[0], y_hat])
        