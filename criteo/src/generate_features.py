# generate_features.py
''' summarize large files through streaming readers. for numeric fields, calculate the sum, ct, and mean. for categorical fields, get the feature counts
'''
import sys, argparse
import csv
import time
from sklearn.externals import joblib
import numpy as np

def record_numeric(row):
    ones = list(1-(np.array(row) == ''))

    vals = [int(x) if x != '' else 0 for x in row]
    numeric_dict['count'] = dict(zip(numeric_fields, [sum(x) for x in zip(numeric_dict['count'].values(), list(ones))]))
    numeric_dict['sum'] = dict(zip(numeric_fields, [sum(x) for x in zip(numeric_dict['sum'].values(), list(vals))]))

def record_categoric(row):
    for item in zip(categorical_fields, row):
        categorical_dict[item[0]].update({item[1] : categorical_dict[item[0]].get(item[1], 0) + 1})
              
def main():
    for row in reader:
        record_numeric(row[2:15])
        record_categoric(row[15:])

    print "Creating numeric features..."
    numeric_dict['avg'] = numeric_dict['sum'].copy()
    for field in numeric_fields:
        numeric_dict['avg'][field] = numeric_dict['avg'][field]/numeric_dict['count'][field]

    print "Deleting sparse features..."
    for field in categorical_fields:
        for feat in categorical_dict[field].keys():
            if categorical_dict[field][feat] < args.minsize:
                del categorical_dict[field][feat]
        categorical_dict[field] = set(categorical_dict[field].keys())

    # print "Setting categorical fields to sets"
    # for field in categorical_fields:

    print "Saving feature dictionaries"
    joblib.dump(numeric_dict, args.num_dict)
    joblib.dump(categorical_dict, args.cat_dict)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--cat_dict', type = str, help = 'Feature dictionary to instruct how to transform data', default = "features/cat_dict.pkl")
    parser.add_argument('-n', '--num_dict', type = str, help = 'Feature dictionary to instruct how to transform data', default = "features/num_dict.pkl")
    parser.add_argument('-m', '--minsize', type=int, help = 'Minimum number of instances of feature value', default = 50000)
    args = parser.parse_args()

    # INITIALIZE DICTIONARIES
    numeric_dict = {'count': {}, 'sum':{}}
    numeric_fields = ['I1','I2','I3','I4','I5','I6','I7','I8','I9','I10','I11','I12','I13']
    for field in numeric_fields:
        numeric_dict['count'][field] = 1
        numeric_dict['sum'][field] = 0

    categorical_dict = {}
    categorical_fields = ['C1','C2','C3','C4','C5','C6','C7','C8','C9','C10','C11','C12','C13','C14','C15','C16','C17','C18','C19','C20','C21', 'C22', 'C23', 'C24','C25','C26']
    for field in categorical_fields:
        categorical_dict[field] = {'' : 0}

    reader = csv.reader(sys.stdin, delimiter = ',', quoting = csv.QUOTE_NONE)
    header = reader.next()
    columns = header[2:]

    start_time = time.time()
    main()
    print time.time() - start_time
