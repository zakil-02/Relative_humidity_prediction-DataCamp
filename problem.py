import os
import pandas as pd
import numpy as np
import rampwf as rw
from sklearn.model_selection import TimeSeriesSplit

problem_title = "Relative Humidity Prediction in Morocco"


_target_column_name = "relative_humidity"

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
    
# rMSE score type
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
    RMSE(name='RMSE', precision=5),
    MAE(name='MAE', precision=5)
]

def get_train_data(path="."):
    data = pd.read_csv(os.path.join(path, "data", "train.csv"))
    y_train = data[_target_column_name].values
    X_train = data.drop(_target_column_name, axis=1)
    return X_train, y_train

def get_test_data(path="."):
    data = pd.read_csv(os.path.join(path, "data", "test.csv"))
    y_test = data[_target_column_name].values
    X_test = data.drop(_target_column_name, axis=1)
    return X_test, y_test


# def get_cv(X, y, n_splits=8):
#     # make a split 
#     n_samples = len(y)
#     indices = np.arange(n_samples)
#     split_size = n_samples // n_splits
#     for i in range(n_splits):
#         test_indices = indices[i * split_size: (i + 1) * split_size]
#         train_indices = np.concatenate((indices[:i * split_size], indices[(i + 1) * split_size:]))
#         yield train_indices, test_indices

#     return  

def get_cv(X, y, n_splits=3):
    ''' 
    Time series cross-validation with geo-balanced test sets :
        - Temporal Integrity: Uses TimeSeriesSplit to ensure training data always precedes test data
        - Geospatial Balance: Enforces equal samples per location
        - Empty Split Handling: Skips splits that would result in empty training/test sets
    '''

    # Sort data by time and reset index
    X_sorted = X.sort_values('valid_time').reset_index(drop=True)
    y_sorted = y[X_sorted.index]
    
    tscv = TimeSeriesSplit(n_splits=n_splits)
    
    for train_index, test_index in tscv.split(X_sorted):
        # Get raw test samples from sorted data
        test_subset = X_sorted.iloc[test_index]
        
        # Group by geolocation and find minimum samples per location
        grouped = test_subset.groupby(['latitude', 'longitude'])
        if grouped.ngroups == 0:
            continue
            
        # Find earliest common sample count across locations
        min_count = grouped.size().min()
        if min_count < 1:
            continue
            
        # Create balanced test set
        balanced_test = []
        for (lat, lon), group in grouped:
            # Get earliest samples per location
            loc_samples = group.index[:min_count].tolist()
            balanced_test.extend(loc_samples)
        
        full_train = X_sorted.index[:test_index[0]].tolist()
        
        # Ensure we have at least 1 sample in both sets
        if len(full_train) > 0 and len(balanced_test) > 0:
            yield (np.array(full_train), np.array(balanced_test))