import os
import pandas as pd
import numpy as np
from click.testing import CliRunner
import pytest
from src.preprocessing import preprocess_data 

@pytest.fixture
def setup_csv_files():
    # path directory and setup
    x_train_path = "data/x_train.csv" 
    y_train_path = "data/y_train.csv"
    x_test_path = "data/x_test.csv"
    y_test_path = "data/y_test.csv"
    train_output_path = "data/preprocessed_train_data.csv"
    test_output_path = "data/preprocessed_test_data.csv"

    yield x_train_path, x_test_path, y_train_path, y_test_path, train_output_path, test_output_path


    if os.path.exists(train_output_path):
        os.remove(train_output_path)
    if os.path.exists(test_output_path):
        os.remove(test_output_path)

# Test if the function preprocesses and saves output correctly
def test_preprocess_data_functionality(setup_csv_files):
    x_train_path, x_test_path, y_train_path, y_test_path, train_output_path, test_output_path = setup_csv_files

    runner = CliRunner()
    result = runner.invoke(preprocess_data, [x_train_path, x_test_path, y_train_path, y_test_path, train_output_path, test_output_path])
    
    assert result.exit_code == 0
    assert os.path.exists(train_output_path) and os.path.exists(test_output_path)

    # Load output files and check if they have the expected columns
    train_output = pd.read_csv(train_output_path)
    test_output = pd.read_csv(test_output_path)

    expected_columns = ['Administrative', 'Administrative_Duration', 'Informational',
                        'Informational_Duration', 'ProductRelated', 'ProductRelated_Duration',
                        'BounceRates', 'ExitRates', 'PageValues', 'SpecialDay',
                        'Weekend', 'Browser', 'Region', 'TrafficType', 'OperatingSystems']
    for column in expected_columns:
        assert any(col.startswith(column) for col in train_output.columns)
        assert any(col.startswith(column) for col in test_output.columns)


# Test handling of non-existing files
def test_non_existing_files():
    runner = CliRunner()
    result = runner.invoke(preprocess_data, ["non_existing_x_train.csv", "non_existing_x_test.csv", "non_existing_y_train.csv", "non_existing_y_test.csv", "train_output.csv", "test_output.csv"])
    assert result.exit_code != 0