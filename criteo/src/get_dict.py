#get_dict.py

#Given a column of categorical values, return a count dictionary

import sys

d = {}
for item in sys.stdin:
	if item != '':
		if item in d.keys():
			d[item] += 1
		else:
			d[item] = 1
print d