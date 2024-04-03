import pandas as pd
import numpy as np
import pytest
import sys
import os


sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.function_preprocessing import preprocessing


@pytest.fixture
def sample_data():
    # Define your feature columns here
    numeric_features = ['Administrative', 'Administrative_Duration', 'Informational', 'Informational_Duration', 'ProductRelated', 'ProductRelated_Duration', 'BounceRates', 'ExitRates', 'PageValues', 'SpecialDay']
    categorical_features = ['Month', 'VisitorType']
    binary_features = ['Weekend']
    passthrough_features = ['Browser', 'Region', 'TrafficType', 'OperatingSystems']
    
    # Sample data setup
    X_train = pd.DataFrame({
        'Administrative': [1, 2, 3],
        'Administrative_Duration': [10, 20, 30],
        'Informational': [4, 5, 6],
        'Informational_Duration': [40, 50, 60],
        'ProductRelated': [7, 8, 9],
        'ProductRelated_Duration': [70, 80, 90],
        'BounceRates': [0.1, 0.2, 0.3],
        'ExitRates': [0.4, 0.5, 0.6],
        'PageValues': [0.7, 0.8, 0.9],
        'SpecialDay': [0.0, 0.1, 0.2],
        'Month': ['Jan', 'Feb', 'Mar'],
        'VisitorType': ['New_Visitor', 'Returning_Visitor', 'Other'],
        'Browser': [1, 2, 3],
        'Region': [1, 2, 3],
        'TrafficType': [1, 2, 3],
        'OperatingSystems': [1, 2, 3],
        'Weekend': [True, False, True]
    })

    X_test = pd.DataFrame({
        'Administrative': [4, 5, 6],
        'Administrative_Duration': [40, 50, 60],
        'Informational': [7, 8, 9],
        'Informational_Duration': [70, 80, 90],
        'ProductRelated': [10, 11, 12],
        'ProductRelated_Duration': [100, 110, 120],
        'BounceRates': [0.4, 0.5, 0.6],
        'ExitRates': [0.7, 0.8, 0.9],
        'PageValues': [1.0, 1.1, 1.2],
        'SpecialDay': [0.3, 0.4, 0.5],
        'Month': ['Apr', 'May', 'Jun'],
        'VisitorType': ['Returning_Visitor', 'New_Visitor', 'Other'],
        'Browser': [4, 5, 6],
        'Region': [4, 5, 6],
        'TrafficType': [4, 5, 6],
        'OperatingSystems': [4, 5, 6],
        'Weekend': [False, True, False]
    })

    y_train = pd.Series([0, 1, 0], name='Revenue')
    y_test = pd.Series([1, 0, 1], name='Revenue')

    return X_train, X_test, y_train, y_test, numeric_features, categorical_features, binary_features, passthrough_features


def test_shapes(sample_data):
    X_train, X_test, y_train, y_test, numeric_features, categorical_features, binary_features, passthrough_features = sample_data
    train_transformed, test_transformed, transformed_columns = preprocessing(X_train, X_test, y_train, y_test, numeric_features, categorical_features, binary_features, passthrough_features)
    
    assert train_transformed.shape[0] == X_train.shape[0], "Incorrect number of rows in train_transformed."
    assert test_transformed.shape[0] == X_test.shape[0], "Incorrect number of rows in test_transformed."

def test_revenue_preservation(sample_data):
    X_train, X_test, y_train, y_test, numeric_features, categorical_features, binary_features, passthrough_features = sample_data
    train_transformed, test_transformed, transformed_columns = preprocessing(X_train, X_test, y_train, y_test, numeric_features, categorical_features, binary_features, passthrough_features)
    
    assert 'Revenue' in train_transformed.columns, "'Revenue' column missing in train_transformed."
    assert 'Revenue' in test_transformed.columns, "'Revenue' column missing in test_transformed."
    
    assert np.array_equal(train_transformed['Revenue'].values, y_train.values), "Revenue data altered in training set."
    assert np.array_equal(test_transformed['Revenue'].values, y_test.values), "Revenue data altered in testing set."

def test_numeric_scaling(sample_data):
    X_train, X_test, y_train, y_test, numeric_features, categorical_features, binary_features, passthrough_features = sample_data
    train_transformed, test_transformed, transformed_columns = preprocessing(X_train, X_test, y_train, y_test, numeric_features, categorical_features, binary_features, passthrough_features)
    
    # Numeric scaling check
    assert not np.array_equal(X_train['Administrative'], train_transformed['Administrative']), "Numeric feature 'Administrative' appears untransformed."

def test_one_hot_encoding(sample_data):
    X_train, X_test, y_train, y_test, numeric_features, categorical_features, binary_features, passthrough_features = sample_data
    train_transformed, test_transformed, transformed_columns = preprocessing(X_train, X_test, y_train, y_test, numeric_features, categorical_features, binary_features, passthrough_features)
    
    # One-hot encoding check
    expected_one_hot_features = ['Month_Jan', 'Month_Feb', 'Month_Mar', 'VisitorType_New_Visitor', 'VisitorType_Returning_Visitor', 'VisitorType_Other']
    assert all(feature in train_transformed.columns for feature in expected_one_hot_features), "One-hot encoded features missing in the transformed dataset."

def test_binary_feature(sample_data):
    X_train, X_test, y_train, y_test, numeric_features, categorical_features, binary_features, passthrough_features = sample_data
    train_transformed, test_transformed, transformed_columns = preprocessing(X_train, X_test, y_train, y_test, numeric_features, categorical_features, binary_features, passthrough_features)
    
    # Binary feature check
    assert 'Weekend' in train_transformed.columns, "Binary feature 'Weekend' missing in the transformed dataset."
    assert set(train_transformed['Weekend'].unique()) == {0, 1}, "Binary feature 'Weekend' should only contain {0, 1}."

def test_transformed_data_columns(sample_data):
    X_train, X_test, y_train, y_test, numeric_features, categorical_features, binary_features, passthrough_features = sample_data
    train_transformed, test_transformed, transformed_columns = preprocessing(X_train, X_test, y_train, y_test, numeric_features, categorical_features, binary_features, passthrough_features)
    
    # Expected columns check
    expected_columns = [
        'Administrative', 'Administrative_Duration', 'Informational', 'Informational_Duration',
        'ProductRelated', 'ProductRelated_Duration', 'BounceRates', 'ExitRates', 'PageValues',
        'SpecialDay', 'Month_Apr', 'Month_Feb', 'Month_Jan', 'Month_Jun', 'Month_Mar', 'Month_May',
        'VisitorType_New_Visitor', 'VisitorType_Returning_Visitor', 'VisitorType_Other', 'Browser', 'Region', 'TrafficType',
        'OperatingSystems', 'Weekend', 'Revenue'
    ]

    assert all(col in train_transformed.columns for col in expected_columns), "Train transformed data columns are incorrect."
    assert all(col in test_transformed.columns for col in expected_columns), "Test transformed data columns are incorrect."
