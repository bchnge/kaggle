## get_categorical_features.py

import sqlite3
import argparse
from pandas import DataFrame,HDFStore

# Set parameters
parser = argparse.ArgumentParser()
parser.add_argument('-d', '--database', type = str, help = 'Name of database')
parser.add_argument('-f', '--fields', nargs='+', type = str, help = "Fields to get categorical features for")
parser.add_argument('-t', '--top', type = int, help = 'Query WHERE condition', default = None)
parser.add_argument('-m', '--min_instance', type = int, help = 'Name of dataframe to save results to', default = 10000)

args = parser.parse_args()

for field in args.fields:
	# Perform query
	query_filter = ' ' if args.min_instance == None else ' HAVING N >= ' + str(args.min_instance)
	query_limit = ' ' if args.top == None else ' LIMIT ' + str(args.top)

	query = "SELECT %s, sum(N) as N, sum(Label*N)*1.0/sum(N) as PctPos FROM ct_%s GROUP BY  %s %s ORDER BY abs(0.5 - PctPos) ASC %s;" %(field, field.lower(), field, query_filter, query_limit)
	print query

	# Connect to database
	conn = sqlite3.connect(args.database)
	result = conn.execute(query).fetchall()
	conn.close()

	# List of categorical features to binarize dataset with
	features = [item[0] for item in result]

	print field + ' has ' + str(len(features)) + ' features'

	with open('data/categorical_features/feats_%s.csv' % field, 'w') as theFile: 
		for item in features:
			theFile.write("%s\n" % item)
	# would be interesting to perform variable selection here....for future work