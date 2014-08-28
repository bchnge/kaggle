# sample.py

# sample.py takes in a data set as stdin, and performs column and row filtering
# first argument is a list of columns to filter
# second argument is the percent of rows to filter
# third argument is the target column
# fourth argument is the downsampling rate for target column

# set argument input
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--filename', type = str, help = 'data file')
parser.add_argument('-c', '--cols', nargs='+', type = int, help = "column filter")
parser.add_argument('-r', '--rowsample', type = float, help = "row sample %")
parser.add_argument('-t', '--targetcol', nargs=1, type = int, help = "target column #")
parser.add_argument('-s', '--sampletarget', nargs=1, type = float, help = "sampling rate of target value")
args = parser.parse_args()


def file_len(fname):
	with open(fname) as f:
		for i, l in enumerate(f):
			pass
	return i+1

def subsample(fname):
	import random as rd
	import numpy as np
	import pandas as pd

	total_size = file_len(fname)
	print 'total number of rows: ' + str(total_size)

	drop_size = int(np.floor((1-args.rowsample) * total_size))
	print 'number of rows dropped: ' + str(drop_size)

	drop_indices = rd.sample(xrange(total_size),drop_size)

	df = pd.read_csv(args.filename, usecols = args.cols, skiprows = drop_indices)
	print 'number of rows remaining:' + str(len(df))


def main():

	data = ....
	if downsample == True:
		data = rebalance(args.filename, args.sampletarget)

	result = subsample(data)	
		

if __name__ == "__main__":
	main()