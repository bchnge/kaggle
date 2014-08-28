import sqlite3
import sys
import argparse
import random as rd

# Set parameters
parser = argparse.ArgumentParser()
parser.add_argument('-d', '--database', type = str, help = 'Name of database')
parser.add_argument('-t', '--table', type = str, help = 'Name of table')
parser.add_argument('-n', '--n_sample', type = int, help = 'Number of rows to sample')
parser.add_argument('-f', '--fields', nargs='+', type = str, help = "Fields to extract from table")
parser.add_argument('-w', '--filter', type = str, help = 'Query WHERE condition')
parser.add_argument('-s', '--size', type = int, help = 'Size of entire sample -- optional')
parser.add_argument('-a', '--dfname', type = str, help = 'name of dataframe to save results to')
parser.add_argument('-b', '--storename', type = str, help = 'name of store to save results to')
parser.add_argument('-x', '--seedno', type = int, help = 'set random seed number')

args = parser.parse_args()

rd.seed(args.seedno)

# Parse fields to query
cols = ' '
for f in args.fields:
	cols = cols + ',' + f +' ' if cols != ' ' else f
print cols


# Connect to database
conn = sqlite3.connect(args.database)

# Obtain number of rows in entire sample
if args.size == None:
	N = conn.execute('select count(_ROWID_) from ' + args.table).fetchone()[0]

	print 'Total number of rows: ' + str(N)
else:
	N = args.size

# Obtain sampled indexes
indices = rd.sample(xrange(2,N+2),args.n_sample)

# Convert to array of string elements
indices = map(lambda x : str(x), indices)

# Convert array to string
indices_statement = '(' + ','.join(indices) + ')'


# Perform query
query_filter = ' WHERE _ROWID_ IN' + indices_statement + ' AND ' +args.filter if args.filter != None else ' WHERE _ROWID_ IN' + indices_statement

query = 'SELECT ' + cols + 'FROM ' + args.table + query_filter


result = conn.execute(query).fetchall()

# Save query results
from pandas import DataFrame,HDFStore
df = DataFrame(result, columns = args.fields)


print 'Preview...' 
print df.head()

store = HDFStore(args.storename)
store.put(args.dfname, df)
store.close()

print 'Query complete. Saved in ' + args.storename + ' as ' + args.dfname