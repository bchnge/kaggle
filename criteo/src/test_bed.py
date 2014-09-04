import sys
sys.path.insert(0,"/home/bchelli/Projects/kaggle/util/")

import bigdata

da = bigdata.DataAsset('train.csv', 'test.csv')
print da