from sklearn.neighbors import KNearestNeighbors
import pandas as pd
import numpy as np

df = pd.read_json('train.json')
X = df[['longitude', 'latitude']].as_matrix
y = df['interest_level'].values

np.random.seed(123)

model = KNearestNeighbors(k = 30)
model.fit(X, y)

print model.score(X,y)

# Read data
# Normalize longitude and latitude
# Param grid find, optimize number of k
# Find best params
# cross val score

