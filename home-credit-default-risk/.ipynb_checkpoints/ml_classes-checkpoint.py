from utils import get_design_matrix_lbl
from sklearn.preprocessing import FunctionTransformer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from lightgbm.sklearn import LGBMClassifier
from sklearn.model_selection import StratifiedKFold
import numpy as np
from sklearn.model_selection import cross_val_score

class Model:
    def __init__(self, name, desc):
        self.name = name
        self.desc = desc
        self.cv = StratifiedKFold(n_splits=5, random_state=123)

    def define_model(self, clf):
        self.clf = clf
        self.is_lgbm = str(type(clf)) == 'lightgbm.sklearn.LGBMClassfier'
        
    def set_categorical_features(self, categorical_features):
        self.categorical_feature = categorical_features
        
    def train(self, X, y):
        self.clf.fit(X, y)
        
    def validate_model(self, X, y):
        if hasattr(self, 'clf') is False:
            print('Stop. You must define a model before validating.')
        else:
            self.validation_scores = cross_val_score(self.clf, X, y, scoring = 'roc_auc', cv = self.cv)

    def tune_model(self, X, y, param_grid):
        if hasattr(self, 'clf') is False:
            print('Stop. You must define a model before tuning.')
        else:
            gs = GridSearchCV(estimator = self.clf, param_grid = param_grid, 
                              scoring = 'roc_auc', cv = self.cv)
            if self.is_lgbm:
                gs.fit(X, y, clf__categorical_feature = self.categorical_feature)
            else:
                gs.fit(X, y)
                
            self.best_estimator = gs.best_estimator_
            self.best_score = gs.best_score_
            self.best_params = gs.best_params_
            self.cv_results = gs.cv_results_
            
class Dataset:
    def __init__(self, train_data, test_data):
        train_features = train_data.columns
        test_features = test_data.columns
        features = list(set(train_features) & set(test_features))
        
        print('...creating training matrix')
        self.X_train, self.y_train = get_design_matrix_lbl(train_data, 
                                                           features, train = True, train_test_split = False, 
                                                           convert_categorical = True)
        
        print('...creating test matrix')
        self.X_test = get_design_matrix_lbl(test_data, features, train = False, train_test_split = False,
                                           convert_categorical = True)
        
        self.features_initial = list(self.X_test.columns)
        self.features_initial_categorical = list(test_data.columns[test_data.dtypes == object])
        
        self.ae_discovery_ratios = []
        
    
    def preprocess(self):
        # Remove nonvariant column
        yield
        
    
    def ae_train_model(self, model):
        model.fit(self.X_train, self.y_train)        
        self.ae_feature_importances_dict = dict(zip(self.X_train.columns, model.feature_importances_))
        self.ae_feature_importances = model.feature_importances_        
    

  


    def autoengineer_ratios(self, n_iter = 1000):
        ae_params = {'boosting_type': 'gbdt',
                  'max_depth' : -1,
                  'objective': 'binary',
                  'learning_rate': 0.0212,
                  'reg_alpha': 0.8,
                  'reg_lambda': 0.4,
                  'subsample': 1,
                  'feature_fraction': 0.3,
                  'device_type': 'gpu',
                  'metric' : 'auc',
                  'random_state': 123,
                  'n_estimators': 300, 
                  'num_leaves': 40, 
                  'max_bin': 255,
                  'min_data_in_leaf': 2400,
                  'min_data_in_bin': 5}
        
        def _fn_column_selector(X, k):
            ''' 
                select up to kth column
            '''
            return X[:,:k]

        ColumnSelector = FunctionTransformer(_fn_column_selector, validate = False)

        importance_weights = self.ae_feature_importances / self.ae_feature_importances.sum()
        
        kfold = StratifiedKFold(n_splits=5, random_state=123)
        
        model = Pipeline([('selector', ColumnSelector),
                  ('clf', LGBMClassifier(**ae_params))])
        
        for i in range(n_iter):
            random_vars = list(np.random.choice(self.X_train.columns, 
                                                size = 2, p = importance_weights, 
                                                replace= False))

            X_tmp = self.X_train.loc[:, random_vars ]
            X_tmp['_DIV_'.join(random_vars)] = X_tmp.iloc[:,0] / (X_tmp.iloc[:,1] + 1)

            gs = GridSearchCV(estimator = model,
                              param_grid = {'selector__kw_args': [{'k':2},{'k':3}]},
                              scoring = 'roc_auc',
                              cv = kfold)
            gs.fit(X_tmp.values, self.y_train)
            perf_1, perf_2 = gs.cv_results_.get('mean_test_score')
            if perf_2 > perf_1:
                self.ae_discovery_ratios.append((random_vars[0], random_vars[1], perf_2/perf_1))
                


