# cv_feature_extract.py
'''
Sampling speed is dependent on size of std.in, NOT sampling rate, which is nice.

'''
import csv
import random
import numpy as np
import sys, argparse
import multiprocessing

# Set up Arguments
parser = argparse.ArgumentParser()
parser.add_argument('-s', '--sampling_rate', type = float, help = 'Feature dictionary to instruct how to transform data', default = 0.05)
parser.add_argument('-x', '--seedno', type = int, help = 'Feature dictionary to instruct how to transform data', default = 123)
parser.add_argument('-n', '--numeric_dict', type = str, help = 'Feature dictionary to instruct how to transform data', default = 'numerical_dictionary.pkl')
parser.add_argument('-c', '--categorical_dict', type = str, help = 'Feature dictionary to instruct how to transform data', default = 'categorical_dictionary.pkl')
parser.add_argument('-f', '--filename', type = str, help = 'Feature dictionary to instruct how to transform data', default = 'categorical_dictionary.pkl')
parser.add_argument('-j', '--njobs', type = int, default = 2)
args = parser.parse_args()


def load_dictionaries():
    from sklearn.externals import joblib
    num_dict = joblib.load(args.numeric_dict)
    cat_dict = joblib.load(args.categorical_dict)   
    return num_dict, cat_dict
    
def flatten_list(unflattened_list):
    return [item for sublist in unflattened_list for item in sublist]

# def transform(element, field):
#     # Based on num_dict and cat_dict,  transform each input element into imputed values (and whether or not hte value was missing) and binary vectors.

#     if field in num_dict['avg'].keys():
#         if element == '':
#             result = [num_dict[field]['avg'], 0] 
#         else:
#             result = [int(element), 1]
#     elif field in cat_dict.keys():
#         result = list((np.array(element) == cat_dict[field].keys())*1)
#     return result

def transform_categoric(row):
    return [(np.array(val) == list(cat_dict[cat_cols[idx]]))*1 for idx,val in enumerate(row)]

def transform_numeric(row):
    return [[num_dict['avg'][num_cols[idx]],0] if val == '' else  [int(val),1] for idx, val in enumerate(row)]
    
def process(subrow):
    unflattened_numeric = transform_numeric(subrow[0:13])
    unflattened_categoric = transform_categoric(subrow[13:])
    unflattened_numeric.extend(unflattened_categoric)
    return flatten_list(unflattened_numeric)

def main_func(item):
    if random.random() <= args.sampling_rate:
        row = reader.next()
        temp = [row[0], int(row[1])]
        temp.extend(process(row[2:]))
        writer.writerow(temp)


def main():
    # sample y and X while processing features
    # print "Begin sampling and feature transformation..."
    pool = multiprocessing.Pool(args.njobs)
    num_iters = xrange(10000)
    result = pool.map(main_func, num_iters)
    pool.close()
    pool.join()

if __name__ == "__main__":
    
    # Load feature dictionaries
    # print "Loading dictionaries..."
    num_dict, cat_dict = load_dictionaries()

    # Set sampling rate and random seed
    random.seed(args.seedno)

    # Obtain the number of rows
    with open(args.filename) as f:
        reader = csv.reader(args.filename, delimiter = ',')
    writer = csv.writer(sys.stdout, delimiter = ',')
    original_header = reader.next()
    columns = original_header[2:]
    num_cols = columns[0:13]
    # print 'Numeric columns: %s' %(num_cols)
    cat_cols = columns[13:]
    # print 'Categoric columns: %s' %(cat_cols)

    main()