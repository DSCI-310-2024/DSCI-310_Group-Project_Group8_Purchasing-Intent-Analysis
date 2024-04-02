import pytest
import pandas as pd
from click.testing import CliRunner
from your_script import preprocess_data  # Ensure your script is named or adjust this import accordingly.

@pytest.fixture
def input_data():
    """Fixture to create and clean up temporary input data files."""
    # Create temporary CSV files for testing
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

    # ,PageValues,SpecialDay,Month,OperatingSystems,Browser,Region,TrafficType,VisitorType,Weekend

    x_test = pd.DataFrame({
        'Administrative': [0, 2], 'Administrative_Duration': [0.0, 80.0],
        'Informational': [0, 0], 'Informational_Duration': [0.0, 0.0],
        'ProductRelated': [1, 2], 'ProductRelated_Duration': [0.0, 64.0],
        'BounceRates': [0.2, 0.0], 'ExitRates': [0.2, 0.05],
        'PageValues': [0.0, 0.0], 'SpecialDay': [0.0, 0.0],
        'Month': ['Feb', 'March'], 'VisitorType': ['Returning_Visitor', 'New_Visitor'],
        'Weekend': [False, True], 'Browser': [1, 2], 'Region': [1, 3],
        'TrafficType': [1, 4], 'OperatingSystems': [1, 2]

    })  

    y_train = pd.DataFrame({'Revenue' : [0, 1]})
    y_test = pd.DataFrame({'Revenue' : [1, 1]})

    x_train.to_csv("x_train.csv", index=False)
    x_test.to_csv("x_test.csv", index=False)
    y_train.to_csv("y_train.csv", index=False)
    y_test.to_csv("y_test.csv", index=False)
    yield "x_train.csv", "x_test.csv", "y_train.csv", "y_test.csv"
    # Cleanup
    os.remove("x_train.csv")
    os.remove("x_test.csv")
    os.remove("y_train.csv")
    os.remove("y_test.csv")

def test_file_loading(input_data):
    """Test that input files are correctly loaded."""
    runner = CliRunner()
    result = runner.invoke(preprocess_data, [*input_data, 'train_output.csv', 'test_output.csv'])
    assert result.exit_code == 0
    assert "Preprocessed data saved" in result.output
    # Further checks can be added to ensure the data was loaded and processed

