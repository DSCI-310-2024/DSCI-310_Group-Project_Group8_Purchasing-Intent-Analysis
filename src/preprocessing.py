#author: Calvin Choi, Nour Abdelfattah, Sana Shams, Sai Pusuluri
#date: 2024-04-09

"""
Preprocesses training and testing datasets by applying standard scaling to numeric features, 
one-hot encoding to categorical features, and preserving binary and passthrough features. 
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
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer

@click.command()
@click.argument('x_train_file', type=click.Path(exists=True))
@click.argument('x_test_file', type=click.Path(exists=True))
@click.argument('y_train_file', type=click.Path(exists=True))
@click.argument('y_test_file', type=click.Path(exists=True))
@click.argument('train_output_file', type=str)
@click.argument('test_output_file', type=str)
def preprocess_data(x_train_file, x_test_file, y_train_file, y_test_file, train_output_file, test_output_file):
    """
    Reads the input dataset, applies preprocessing transformations, and saves
    the preprocessed data to an output file.
    """
    # Load the datasets
    X_train = pd.read_csv(x_train_file)
    X_test = pd.read_csv(x_test_file)

    # Define the transformers
    numeric_transformer = StandardScaler()
    categorical_transformer = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    binary_transformer = OneHotEncoder(drop='if_binary', dtype=int)

    # Define feature groups
    numeric_features = ['Administrative', 'Administrative_Duration', 'Informational',
                        'Informational_Duration', 'ProductRelated', 'ProductRelated_Duration',
                        'BounceRates', 'ExitRates', "PageValues", 'SpecialDay']

    categorical_features = ['Month', 'VisitorType']

    passthrough_features = ['Browser', 'Region', 'TrafficType', 'OperatingSystems']

    binary_features = ['Weekend']

    # Create the preprocessor
    # preprocessor = make_column_transformer(
    #     (numeric_transformer, numeric_features),
    #     (categorical_transformer, categorical_features),
    #     (binary_transformer, binary_features),
    #     ("passthrough", passthrough_features),
    #     ("drop", drop_features),
    # )

    preprocessor = ColumnTransformer(
        transformers=[
            ('numeric', numeric_transformer, numeric_features),
            ('categorical', categorical_transformer, categorical_features),
            ('binary', binary_transformer, binary_features),
            ('passthrough', 'passthrough', passthrough_features),
            ]
    )

    # fitting and transforming data
    X_train_transformed = preprocessor.fit_transform(X_train)

    X_test_transformed = preprocessor.transform(X_test)

    y_train = pd.read_csv(y_train_file)
    y_test = pd.read_csv(y_test_file)

    # obtaining transformed column names
    categorical_columns = preprocessor.named_transformers_['categorical'].get_feature_names_out(categorical_features)
    transformed_column_names = numeric_features + list(categorical_columns) + binary_features + passthrough_features

    X_train_transformed_df = pd.DataFrame(X_train_transformed, columns=transformed_column_names)
    X_test_transformed_df = pd.DataFrame(X_test_transformed, columns=transformed_column_names)

    train_transformed = pd.concat([X_train_transformed_df, y_train], axis=1)
    test_transformed = pd.concat([X_test_transformed_df, y_test], axis=1)

    # Save the preprocessed data to an output file
    train_transformed.to_csv(train_output_file, index=False)
    test_transformed.to_csv(test_output_file, index=False)

    click.echo(f"Preprocessed data saved to {train_output_file} and {test_output_file}")

if __name__ == '__main__':
    preprocess_data()