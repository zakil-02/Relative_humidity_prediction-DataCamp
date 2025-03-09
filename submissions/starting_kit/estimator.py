import numpy as np
import pandas as pd
from sklearn.preprocessing import FunctionTransformer
from sklearn.compose import make_column_transformer
from sklearn.pipeline import make_pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer


def extract_date_components(df):
    df = df.copy()
    df["valid_time"] = pd.to_datetime(df["valid_time"])
    df["year"] = df["valid_time"].dt.year
    df["month"] = df["valid_time"].dt.month
    df["day"] = df["valid_time"].dt.day
    
    return df.drop(columns=["valid_time"])

datetime_transformer = FunctionTransformer(extract_date_components)

cols = [
    'latitude',
    'longitude',
    'temperature',
    'divergence',
    'u_component_wind',
    'v_component_wind',
    'cloud_cover'
]

transformer = make_column_transformer(
    (datetime_transformer, ["valid_time"]),
    ('passthrough', cols)
)

pipe = make_pipeline(
    transformer,
    SimpleImputer(strategy='mean'),
    RandomForestRegressor(max_depth=5, n_estimators=10)
)


def get_estimator():
    return pipe