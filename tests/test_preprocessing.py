import pandas as pd
import numpy as np
import pytest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.function_preprocessing import preprocessing

def test_preprocessing():
    # Create sample data
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
        'VisitorType': ['New_Visitor', 'Returning_Visitor', 'New_Visitor'],
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
        'VisitorType': ['Returning_Visitor', 'New_Visitor', 'Returning_Visitor'],
        'Browser': [4, 5, 6],
        'Region': [4, 5, 6],
        'TrafficType': [4, 5, 6],
        'OperatingSystems': [4, 5, 6],
        'Weekend': [False, True, False]
    })

    y_train = pd.DataFrame({'Revenue': [0, 1, 0]})
    y_test = pd.DataFrame({'Revenue': [1, 0, 1]})

    train_transformed, test_transformed = preprocessing(X_train, X_test, y_train, y_test)

    # Check if the transformed data has the expected shape
    assert train_transformed.shape == (3, 21), "Train transformed data has incorrect shape."
    assert test_transformed.shape == (3, 21), "Test transformed data has incorrect shape."

    # Check if the transformed data contains the expected columns
    expected_columns = [
        'Administrative', 'Administrative_Duration', 'Informational', 'Informational_Duration',
        'ProductRelated', 'ProductRelated_Duration', 'BounceRates', 'ExitRates', 'PageValues',
        'SpecialDay', 'Month_Apr', 'Month_Feb', 'Month_Jan', 'Month_Jun', 'Month_Mar', 'Month_May',
        'VisitorType_New', 'VisitorType_Returning', 'Browser', 'Region', 'TrafficType',
        'OperatingSystems', 'Weekend'
    ]
    assert all(col in train_transformed.columns for col in expected_columns), "Train transformed data columns are incorrect."
    assert all(col in test_transformed.columns for col in expected_columns), "Test transformed data columns are incorrect."

    # Check if the transformed data contains the expected values
    expected_values = np.array([
        [0.0, -1.22474487, -1.22474487, -1.22474487, -1.22474487, -1.22474487, -1.22474487,
         -1.22474487, -1.22474487, -0.89442719, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0],
        [1.22474487, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.4472136, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [-1.22474487, 1.22474487, 1.22474487, 1.22474487, 1.22474487, 1.22474487, 1.22474487,
         1.22474487, 1.22474487, 1.34164079, 1.0, 0.0, 0.0, 0.0, 1.0, 1.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0]
    ])
    np.testing.assert_array_almost_equal(train_transformed.values, expected_values, decimal=6)
    np.testing.assert_array_almost_equal(test_transformed.values, expected_values, decimal=6)