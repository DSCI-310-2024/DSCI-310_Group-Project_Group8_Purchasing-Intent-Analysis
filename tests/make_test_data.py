import pandas as pd
def create_dummy_data():
    data = {
        'feature1': [1, 2, 3, 4, 5],
        'feature2': [5, 4, 3, 2, 1],
        'target': [0, 1, 0, 1, 0]
    }
    df = pd.DataFrame(data)
    df.to_csv('data/test-data/cross_val_test_data.csv', index=False)