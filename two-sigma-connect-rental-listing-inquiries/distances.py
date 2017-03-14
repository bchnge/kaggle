import pandas as pd
import numpy as np
import calendar
import datetime
from pprint import pprint
from scipy.spatial import distance_matrix
import sys
import csv

from sklearn.cluster import DBSCAN

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

#http://geoffboeing.com/2014/08/clustering-to-reduce-spatial-data-set-size/

def main():
	df = pd.read_json('train.json')

	coords = df.as_matrix(columns=['latitude', 'longitude'])

	kms_per_radian = 6371.0088
	epsilon = np.mean([df.latitude.std(), df.longitude.std()])

	epsilon = epsilon / kms_per_radian * 0.1

	db = DBSCAN(eps=epsilon, min_samples=25, algorithm='ball_tree', metric='haversine').fit(np.radians(coords))
	cluster_labels = db.labels_
	num_clusters = len(set(cluster_labels))

	clusters = pd.Series([coords[cluster_labels == n] for n in range(num_clusters)])

	writer = csv.writer(sys.stdout)
	writer.writerow(cluster_labels)
    
	coords_df = df[['longitude','latitude']]
	coords_df.to_csv('features_lon_lat.csv', index = False)
	# num_coords = len(x)
	
	# coords = np.array(coords)
	
	# dist = distance_matrix(coords, coords)

	# print dist

if __name__ == '__main__':
	main()


