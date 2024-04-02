import numpy as np
import pandas as pd
import pytest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.function_model_cross_val import model_cross_validation

def test_model_cross_validation_results():

    results = model_cross_validation('data/cross_val_test_data.csv', 'data/cross_val_test_data.csv', 'target', 'most_frequent', 3, 0.01)

    assert 'dummy' in results, "Dummy model results should be in the output."
    assert 'knn' in results, "KNN model results should be in the output."
    assert 'SVM' in results, "SVM model results should be in the output."
    assert 'random_forest' in results, "Random Forest model results should be in the output."


def test_model_cross_validation_scores():

    results = model_cross_validation('data/cross_val_test_data.csv', 'data/cross_val_test_data.csv', 'target', 'most_frequent', 3, 0.01)

    # Check if the scores are in the expected format
    for model, scores in results.items():
        assert 'fit_time' in scores, f"Fit time should be in the {model} model scores."
        assert 'score_time' in scores, f"Score time should be in the {model} model scores."
        assert 'test_score' in scores, f"Test score should be in the {model} model scores."
        assert 'train_score' in scores, f"Train score should be in the {model} model scores."


def test_invalid_parameters():

    # Invalid k value for KNN
    with pytest.raises(ValueError):
        model_cross_validation('data/cross_val_test_data.csv', 'data/cross_val_test_data.csv', 'target', 'most_frequent', -1, 0.01)

    # Invalid gamma value for SVM
    with pytest.raises(ValueError):
        model_cross_validation('data/cross_val_test_data.csv', 'data/cross_val_test_data.csv', 'target', 'most_frequent', 3, -0.01)


if __name__ == '__main__':
    pytest.main([__file__])
