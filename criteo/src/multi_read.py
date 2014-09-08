import random
import multiprocessing
import numpy as np
import pandas as pd
import sys
def list_append(chunk, output):
	"""
	Creates an empty list and then appends a 
	random number to the list 'count' number
	of times. A CPU-heavy operation!
	"""
	# output.put(sum([1 for x in data[start_index: start_index+50]]))
	with open(chunk,'rb') as f:
		for i in f:
			output.put(i)

if __name__ == "__main__":
	procs = 4   # Number of processes to create

	output = multiprocessing.Queue()
		
	# data = np.ones(5000)

	chunks = ['x00', 'x01', 'x02','x03']
	# Create a list of jobs and then iterate through
	# the number of processes appending each process to
	# the job list 
	jobs = []
	for i in range(0, procs):
		out_list = list()
		process = multiprocessing.Process(target=list_append, args=(chunks[i],output))
		jobs.append(process)

	# Start the processes (i.e. calculate the random number lists)		
	for j in jobs:
		j.start()

	# Ensure all of the processes have finished
	for j in jobs:
		j.join()

	print 'blah'
	results = [output.get() for j in jobs]
	with open(sys.stdout, 'wb') as nf:
		for j in results:
			sys.stdout.write(j)