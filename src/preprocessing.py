#author: Calvin Choi, Nour Abdelfattah, Sana Shams, Sai Pusuluri
#date: 2024-04-09

"""
Preprocesses training and testing datasets by applying standard scaling to numeric features and 
one-hot encoding to categorical features. 
Saves the preprocessed datasets to specified output files.

Usage:
    preprocessing.py <x_train_file> <x_test_file> <y_train_file> <y_test_file> <train_output_file> <test_output_file>

Arguments:
    x_train_file -- Path to the CSV file containing training set features.
    x_test_file -- Path to the CSV file containing test set features.
    y_train_file -- Path to the CSV file containing training set targets.
    y_test_file -- Path to the CSV file containing test set targets.
    train_output_file -- Path where the preprocessed training dataset will be saved.
    test_output_file -- Path where the preprocessed test dataset will be saved.
"""

import click
import pandas as pd
from py_predpurchase.function_preprocessing import numerical_categorical_preprocess
# from sklearn.preprocessing import StandardScaler, OneHotEncoder
# from sklearn.compose import ColumnTransformer

@click.command()
@click.argument('x_train_file', type=click.Path(exists=True))
@click.argument('x_test_file', type=click.Path(exists=True))
@click.argument('y_train_file', type=click.Path(exists=True))
@click.argument('y_test_file', type=click.Path(exists=True))
@click.argument('train_output_file', type=str)
@click.argument('test_output_file', type=str)
def preprocess_data(x_train_file, x_test_file, y_train_file, y_test_file, train_output_file, test_output_file):
    """
    Reads the input dataset, applies numeric and categorical feature transformations, and saves
    the preprocessed data to an output file.
    """
    # Load the datasets
    X_train = pd.read_csv(x_train_file)
    X_test = pd.read_csv(x_test_file)
    y_train = pd.read_csv(y_train_file)
    y_test = pd.read_csv(y_test_file)

    # Define feature groups
    numeric_features = ['Administrative', 'Administrative_Duration', 'Informational',
                        'Informational_Duration', 'ProductRelated', 'ProductRelated_Duration',
                        'BounceRates', 'ExitRates', "PageValues", 'SpecialDay']

    categorical_features = ['Month', 'VisitorType']

    # Use function from py_predpurchase package 
    train_transformed, test_transformed, transformed_column_names = numerical_categorical_preprocess(
        X_train, X_test, y_train, y_test, numeric_features, categorical_features
    )

    # Save the preprocessed data to an output file
    train_transformed.to_csv(train_output_file, index=False)
    test_transformed.to_csv(test_output_file, index=False)

    click.echo(f"Preprocessed data saved to {train_output_file} and {test_output_file}")

if __name__ == '__main__':
    preprocess_data()