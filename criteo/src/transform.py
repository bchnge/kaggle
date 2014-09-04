### transform.py
''' 
Pipeable utility for  transforming a dataset per instructions of feature dictionary

Details
    -f: the field dictionary which indicates the directions for transforming each field
           ex: d = {field1 : ('impute', 0.5),
                    field2 : ('categorical', ['dummy_value_1', dummy_value_2',...'])
                    }
        Currently supports 'impute' and 'categorical' types
       
Usage example: in bash...
cat data.csv | python src/transform.py -f features.pkl > processed_data.csv
'''

from sklearn.externals import joblib
import numpy as np
import sys, argparse
parser = argparse.ArgumentParser()
parser.add_argument('-f', '--f_features', type = str, help = 'Feature dictionary to instruct how to transform data')
args = parser.parse_args()
features = joblib.load(args.f_features)

def process(row, dictionary, field_header):
# transform row of data based on dictionary feature and file header header
    new_row = []
    for idx, field in enumerate(field_header): 
        if field in dictionary.keys():
            field_type = dictionary[field][0]
            field_value = dictionary[field][1]
            old_val = row[idx]

            # if missing numeric
            if field_type == 'impute' and old_val == '':
                new_row.append(field_value)
            elif field_type == 'impute' and old_val !='':
                new_row.append(old_val)
            # if categorical    
            elif field_type == 'categorical' and field_value!=[]:
                feats = list((np.array(old_val) == field_value)*1)
                new_row.extend(feats)
        else:
            new_row.append(row[idx])
    return new_row   

def main():
    import csv
    reader = csv.reader(sys.stdin, delimiter = ',')
    writer = csv.writer(sys.stdout, delimiter = ',')
    header = reader.next()
    new_header = []
    for idx, field in enumerate(header):
        if field in features.keys():
            if features[field][0] == 'impute':
                new_header.append(field)
            elif features[field][0] == 'categorical' and features[field][1]!=[]:
                for feat in features[field][1]:
                    new_header.append(field + "_" + feat)
        else:
            new_header.append(field)
    
    writer.writerow(new_header)
    for row in reader:
        processed_row = process(row, features, header)
        writer.writerow(processed_row)
        
if __name__ == "__main__":
    main()