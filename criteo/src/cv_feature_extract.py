# cv_feature_extract.py
'''
Sampling speed is dependent on size of std.in, NOT sampling rate, which is nice.

'''
import csv
import random
import numpy as np
import sys, argparse
import itertools
# Set up Arguments
parser = argparse.ArgumentParser()
parser.add_argument('-s', '--sampling_rate', type = float, help = 'Feature dictionary to instruct how to transform data', default = 0.05)
parser.add_argument('-x', '--seedno', type = int, help = 'Feature dictionary to instruct how to transform data', default = 123)
parser.add_argument('-n', '--numeric_dict', type = str, help = 'Feature dictionary to instruct how to transform data', default = 'numerical_dictionary.pkl')
parser.add_argument('-c', '--categorical_dict', type = str, help = 'Feature dictionary to instruct how to transform data', default = 'categorical_dictionary.pkl')

args = parser.parse_args()

def load_dictionaries():
    from sklearn.externals import joblib
    num_dict = joblib.load(args.numeric_dict)
    cat_dict = joblib.load(args.categorical_dict)   
    return num_dict, cat_dict

def flatten_list(unflattened_list):
    # return itertools.chain(*unflattened_list) 
    return [item for sublist in unflattened_list for item in sublist]

def transform_categoric(row):
    # return [(np.array(val) == list(cat_dict[cat_cols[idx]]))*1 for idx,val in enumerate(row)]
    new_row = []
    for idx in xrange(26):
        # return np.array([[(row[idx] == key)*1 for key in cat_dict[cat_cols[idx]]] for idx in xrange(26)])
        new_row.extend([(row[idx] == key)*1 for key in cat_dict[cat_cols[idx]]])
    return new_row
    
def transform_numeric(row):
    new_row = []
    for idx in xrange(13):
        if row[idx] == '':
            new_row.extend([num_dict['avg'][num_cols[idx]],0])
        else:
            new_row.extend([int(row[idx]),1])
    return new_row
 
def process(subrow):
    unflattened_numeric = transform_numeric(subrow[0:13])
    unflattened_categoric = transform_categoric(subrow[13:])
    unflattened_numeric.extend(unflattened_categoric)
    return unflattened_numeric
def main():
    # sample y and X while processing features
    # print "Begin sampling and feature transformation..."
    for row in reader:
        if random.random() <= sample_rate:
            temp = [row[0], int(row[1])]
            temp.extend(process(row[2:]))
            writer.writerow(temp)            

if __name__ == "__main__":
    
    # Load feature dictionaries
    # print "Loading dictionaries..."
    num_dict, cat_dict = load_dictionaries()

    # Set sampling rate and random seed
    sample_rate = args.sampling_rate
    random.seed(args.seedno)

    # Obtain the number of rows
    reader = csv.reader(sys.stdin, delimiter = ',')
    writer = csv.writer(sys.stdout, delimiter = ',')
    original_header = reader.next()
    columns = original_header[2:]
    num_cols = columns[0:13]
    # print 'Numeric columns: %s' %(num_cols)
    cat_cols = columns[13:]
    # print 'Categoric columns: %s' %(cat_cols)

    main()