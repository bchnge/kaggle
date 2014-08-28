# query.py

import sqlite3
import argparse
from pandas import DataFrame,HDFStore

# Set parameters
parser = argparse.ArgumentParser()
parser.add_argument('-d', '--database', type = str, help = 'Name of database')
parser.add_argument('-t', '--table', type = str, help = 'Name of table')
parser.add_argument('-f', '--fields', nargs='+', type = str, help = "Fields to extract from table")
parser.add_argument('-w', '--filter', type = str, help = 'Filter condition')
parser.add_argument('-l', '--limit', type = int, help = 'Max no. results')
parser.add_argument('-s', '--store', type = str, help = 'Name of store')
parser.add_argument('-n', '--name', type = str, help = 'Name of stored query')

args = parser.parse_args()

print args.filter
# Parse fields to query
cols = ' '
for f in args.fields:
	cols = cols + ', ' + f +' ' if cols != ' ' else f
print cols

query_filter = ' WHERE ' + args.filter if args.filter != None else ""
query_limit = ' LIMIT ' + str(args.limit) if args.limit != None else ""

query = 'SELECT ' + cols + 'FROM ' + args.table + query_filter + query_limit

print query_filter
print 'SQL Query:' + '\n' + query


# Connect to and query from database
conn = sqlite3.connect(args.database)
result = conn.execute(query).fetchall()
conn.close()

# Save query results
df = DataFrame(result, columns = args.fields).ix[1:,:]

store = HDFStore(args.store)
store.put(args.name, df)
store.close()

print 'Query complete. Saved in ' + args.store + ' as ' + args.name