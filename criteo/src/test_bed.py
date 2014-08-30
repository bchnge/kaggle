# test_bed.py
import sqlite3
field = "C1"
min_instance = 10000
top = 10

query_filter = ' ' if min_instance == None else ' HAVING N >= ' + str(min_instance)
query_limit = ' ' if top == None else ' LIMIT ' + str(top)

query = "SELECT %s, sum(N) as N, sum(Label*N)*1.0/sum(N) as PctPos FROM ct_%s GROUP BY  %s %s ORDER BY abs(0.5 - PctPos) ASC %s;" %(field, field.lower(), field, query_filter, query_limit)

print query

conn = sqlite3.connect('../db/advertising.db')
result = conn.execute(query).fetchall()
conn.close()

features = [item[0] for item in result]

import numpy as np
print features

with open('feats_%s.csv' % field, 'w') as theFile: 
	for item in features:
		theFile.write("%s\n" % item)

# from pandas import DataFrame, HDFStore, read_csv

# df = read_csv('../data/train.csv', usecols = ['Id','C1'], chunksize = 1000)

# df_2 = df.get_chunk(5)

# for f in features:
# 	df_2['C1_'+f] = (df_2['C1'] == f )*1

# df_outcome = df_2.drop('C1', axis = 1)

# print df_outcome