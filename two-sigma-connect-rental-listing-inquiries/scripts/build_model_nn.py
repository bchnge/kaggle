import keras
from keras.utils import np_utils
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.model_selection import GridSearchCV


np.random.seed(123)

df = pd.read_csv('features/features.csv')

y = df['interest_level'].values
X = df.drop('interest_level', axis = 1).as_matrix()

encoder = LabelEncoder()
encoder.fit(y)
y_transform = encoder.transform(y)
y_encoded = np_utils.to_categorical(y_transform)


from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.optimizers import SGD


num_input_features = X.shape[1]


def create_model(optimizer = 'sgd', init = 'uniform', dropout_rate = 0.5):
    model = Sequential()
    model.add(Dense(150, input_dim = num_input_features, init = init, activation = 'tanh'))
    model.add(Dropout(dropout_rate))
    model.add(Dense(100, init = init, activation = 'tanh'))
    model.add(Dropout(dropout_rate))
    model.add(Dense(3, init = init, activation = 'softmax'))

    model.compile(loss = 'categorical_crossentropy', optimizer = optimizer, metrics = ['accuracy','categorical_crossentropy'])

    return model

model = KerasClassifier(build_fn = create_model, verbose = 0)

sgd = SGD(lr = 0.1, decay = 0.02, momentum = 0.9, nesterov = True)

optimizers = [sgd, 'adam']

init = ['uniform']
epochs =  [125]
batches = [25]
dropout_rates = [0.15]
#param_grid = dict(optimizer = optimizers, nb_epoch = epochs, batch_size = batches, init = init, dropout_rate = dropout_rates)

param_grid = dict(optimizer = optimizers, nb_epoch = epochs, batch_size = batches, init = init, dropout_rate = dropout_rates)

grid = GridSearchCV(estimator = model, param_grid = param_grid)
grid_result = grid.fit(X, y_encoded)

print ("Best: %f using %s" % (grid_result.best_score_, grid_result.best_params_))




# model.fit(X, y_encoded, nb_epoch = 1000, batch_size = 16)

# score = model.evaluate(X, y_encoded, batch_size = 16)

# print score
