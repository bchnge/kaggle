import pandas as pd
import numpy as np

class features(object):
    def __init__(self, name, func):
	self.name = name
	self.func = func

    def apply_transform(self, X):
	return np.apply_along_axis(self.func, axis = 1, X)

def get_data(fname, y_label = 'interest_level', train = True):
    df = pd.read_json(fname)
    if train:
	X = df.drop(y_label)
	X_labels = X.columns
	X = X.values
	y = df[y_label).values
	return X,y,X_labels
    else:
	X_labels = df.columns
	X = df.values
	return X, X_labels

