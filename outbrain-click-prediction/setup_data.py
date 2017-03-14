import h5py
import pandas as pd

df = pd.read_csv('clicks_train.csv')
df.to_hdf('training.h5','clicks', mode = 'w', data_columns = True, format = 'table')
