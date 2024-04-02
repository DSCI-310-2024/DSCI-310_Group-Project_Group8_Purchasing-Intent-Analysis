import os
import pandas as pd
import pytest
from click.testing import CliRunner
from src.preprocessing import preprocess_data

@pytest.fixture
def setup_files(tmpdir):
    # Generate mock data
    x_train = pd.DataFrame({
        'Administrative': [0, 2], 'Administrative_Duration': [0.0, 80.0],
        'Informational': [0, 0], 'Informational_Duration': [0.0, 0.0],
        'ProductRelated': [1, 2], 'ProductRelated_Duration': [0.0, 64.0],
        'BounceRates': [0.2, 0.0], 'ExitRates': [0.2, 0.05],
        'PageValues': [0.0, 0.0], 'SpecialDay': [0.0, 0.0],
        'Month': ['Feb', 'March'], 'VisitorType': ['Returning_Visitor', 'New_Visitor'],
        'Weekend': [False, True], 'Browser': [1, 2], 'Region': [1, 3],
        'TrafficType': [1, 4], 'OperatingSystems': [1, 2]
    })
    y_train = pd.DataFrame({'Revenue': [False, True]})
    
    # Save to temporary files
    x_train_file = tmpdir.join("x_train.csv")
    y_train_file = tmpdir.join("y_train.csv")
    x_train.to_csv(x_train_file, index=False)
    y_train.to_csv(y_train_file, index=False)

    # Repeat for X_test, y_test with your test data

    # Output files
    train_output_file = tmpdir.join("train_output.csv")
    test_output_file = tmpdir.join("test_output.csv")

    return str(x_train_file), str(y_train_file), str(train_output_file), str(test_output_file)

def test_preprocess_data(setup_files):
    x_train_file, y_train_file, train_output_file, test_output_file = setup_files
    runner = CliRunner()
    result = runner.invoke(preprocess_data, [x_train_file, x_train_file, y_train_file, y_train_file, train_output_file, test_output_file])

    assert result.exit_code == 0
    assert os.path.exists(train_output_file)
    assert os.path.exists(test_output_file)

    # Further assertions can be made here to verify the contents of the output files


def test_preprocess_data_contents(setup_files):
    x_train_file, y_train_file, train_output_file, test_output_file = setup_files
    
    runner = CliRunner()
    runner.invoke(preprocess_data, [x_train_file, x_train_file, y_train_file, y_train_file, train_output_file, test_output_file])

    processed_train = pd.read_csv(train_output_file)
    processed_test = pd.read_csv(test_output_file)

    # Example of how to define expected data frames
    # Note: In a real test, you would want to define these expectations based on known transformations applied to the input data.
    expected_columns_train = ['Administrative', 'Administrative_Duration', ...]  # Complete as necessary
    expected_columns_test = ['Administrative', 'Administrative_Duration', ...]  # Complete as necessary

    # Verify the structure of the processed files
    assert list(processed_train.columns) == expected_columns_train, "Train output columns do not match expected"
    assert list(processed_test.columns) == expected_columns_test, "Test output columns do not match expected"
    
    # Further checks could include:
    # - Row counts match expectations
    assert len(processed_train) == 2, "Unexpected number of rows in the processed train file"
    assert len(processed_test) == 2, "Unexpected number of rows in the processed test file"
