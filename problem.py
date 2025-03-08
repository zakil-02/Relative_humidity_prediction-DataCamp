import os
import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedKFold
import rampwf as rw

problem_title = "Relative humidity prediction in Morocco"


_target_column_name = "r"

Predictions = rw.prediction_types.make_regression()
workflow = rw.workflows.Estimator()

# MAE score type
class MAE(rw.score_types.BaseScoreType):
    is_lower_the_better = True
    minimum = 0.0
    maximum = float('inf')

    def __init__(self, name='mae', precision=4):
        self.name = name
        self.precision = precision

    def __call__(self, y_true, y_pred):
        mask = y_true != -1
        return np.mean(np.abs((y_true - y_pred)[mask]))
    
# RMSE score type
class RMSE(rw.score_types.BaseScoreType):
    is_lower_the_better = True
    minimum = 0.0
    maximum = float('inf')

    def __init__(self, name='rmse', precision=4):
        self.name = name
        self.precision = precision

    def __call__(self, y_true, y_pred):
        mask = y_true != -1
        return np.sqrt(np.mean((y_true - y_pred)[mask]**2))

score_types = [
    MAE(name='mean_absolute_error', precision=5),
    RMSE(name='root_mean_squared_error', precision=5)
]

def get_train_data(path="."): # for the public data path will be "public"
    data = pd.read_csv(os.path.join(path, "data","train.csv"))
    y_train = data[_target_column_name].values
    X_train = data.drop(_target_column_name, axis=1)
    return X_train, y_train

def get_test_data(path="."):
    data = pd.read_csv(os.path.join(path, "data", "test.csv"))
    y_test = data[_target_column_name].values
    X_test = data.drop(_target_column_name, axis=1)
    return X_test, y_test

def get_cv(X, y):
    cv = StratifiedKFold(n_splits=7, shuffle = True, random_state=42)
    return cv.split(X, y)

