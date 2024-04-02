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

# @click.command()
# @click.argument('x_train_file', type=str)
# @click.argument('y_train_file', type=str)
# @click.argument('x_test_file', type=str)
# @click.argument('y_test_file', type=str)
# @click.argument('train_output_file', type=str)
# @click.argument('test_output_file', type=str)
# def preprocess_data(x_train_file, y_train_file, x_test_file, y_test_file, train_output_file, test_output_file):
#     """
#     Reads train and test feature and target data, performs data preprocessing,
#     and saves the preprocessed train and test data to separate output files.
#     """
#     # Read the feature and target data
#     X_train = pd.read_csv(x_train_file)
#     y_train = pd.read_csv(y_train_file)
#     X_test = pd.read_csv(x_test_file)
#     y_test = pd.read_csv(y_test_file)
    
#     # Define transformers
#     numeric_transformer = StandardScaler()
#     categorical_transformer = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
#     binary_transformer = OneHotEncoder(drop='if_binary', dtype=int)

#     # Define feature groups
#     numeric_features = ['Administrative', 'Administrative_Duration', 'Informational', 'Informational_Duration',
#                         'ProductRelated', 'ProductRelated_Duration', 'BounceRates', 'ExitRates', "PageValues", 'SpecialDay']
#     categorical_features = ['Month', 'VisitorType']

#     passthrough_features = ['Browser', 'Region', 'TrafficType']

#     binary_features = ['Weekend']
    
#     # Create preprocessor
#     preprocessor = make_column_transformer(
#         (numeric_transformer, numeric_features),
#         (categorical_transformer, categorical_features),
#         (binary_transformer, binary_features),
#         ('passthrough', passthrough_features)
#     )
    
#     # Preprocess the data
#     X_train_preprocessed = preprocessor.fit_transform(X_train)
#     X_test_preprocessed = preprocessor.transform(X_test)
    
#     # Combine preprocessed features with targets
#     train_df_preprocessed = pd.DataFrame(X_train_preprocessed, columns=preprocessor.get_feature_names_out())
#     train_df_preprocessed['Revenue'] = y_train.values.ravel()  
#     test_df_preprocessed = pd.DataFrame(X_test_preprocessed, columns=preprocessor.get_feature_names_out())
#     test_df_preprocessed['Revenue'] = y_test.values.ravel()

#     # Save the preprocessed data
#     train_df_preprocessed.to_csv(train_output_file, index=False)
#     test_df_preprocessed.to_csv(test_output_file, index=False)
    
#     click.echo(f"Preprocessed train data saved to: {train_output_file}")
#     click.echo(f"Preprocessed test data saved to: {test_output_file}")

# if __name__ == "__main__":
#     preprocess_data()


# # @click.command()
# # @click.argument('train_data', type=str)
# # @click.argument('test_data', type=str)
# # @click.argument('train_output_file', type=str)
# # @click.argument('test_output_file', type=str)
# # def preprocess_data(train_data, test_data, train_output_file, test_output_file):
# #     """
# #     Reads train and test data, performs data preprocessing, 
# #     and saves the preprocessed train and test data to separate output files.
# #     """
# #     # Read the train and test data
# #     train_df = pd.read_csv(train_data)
# #     test_df = pd.read_csv(test_data)
    
# #     # Separate the target variable
# #     y_train = train_df['Revenue']
# #     y_test = test_df['Revenue']

# #     # Remove the target variable from features
# #     train_df = train_df.drop(columns=['Revenue'])
# #     test_df = test_df.drop(columns=['Revenue'])
    
# #     # Define transformers
# #     numeric_transformer = StandardScaler()
# #     categorical_transformer = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
# #     binary_transformer = OneHotEncoder(drop='if_binary', dtype=int)

# #     # Define feature groups
# #     numeric_features = ['Administrative', 'Administrative_Duration', 'Informational',
# #                         'Informational_Duration', 'ProductRelated', 'ProductRelated_Duration',
# #                         'BounceRates', 'ExitRates', "PageValues", 'SpecialDay']

# #     categorical_features = ['Month', 'VisitorType']

# #     passthrough_features = ['Browser', 'Region', 'TrafficType']

# #     binary_features = ['Weekend']
    
# #     # Create preprocessor with feature groups and transformers
# #     preprocessor = make_column_transformer(
# #         (numeric_transformer, numeric_features),
# #         (categorical_transformer, categorical_features),
# #         (binary_transformer, binary_features),
# #         ('passthrough', passthrough_features)
# #     )
    
# #     # Fit and transform the train data
# #     preprocessed_train_data = preprocessor.fit_transform(train_df)
    
# #     # Transform the test data
# #     preprocessed_test_data = preprocessor.transform(test_df)

# #     # Get the names of the new columns generated by one-hot encoding
# #     categorical_encoder = preprocessor.named_transformers_['onehotencoder-1']
# #     one_hot_encoded_columns = list(categorical_encoder.get_feature_names_out(categorical_features))
    
# #     # Update column_names to include the new one-hot encoded columns
# #     column_names = numeric_features + one_hot_encoded_columns + passthrough_features + binary_features
    
# #     # Convert preprocessed data back to DataFrame
# #     train_df_preprocessed = pd.DataFrame(preprocessed_train_data, columns=column_names)
# #     test_df_preprocessed = pd.DataFrame(preprocessed_test_data, columns=column_names)

# #     # Add the 'Revenue' column back
# #     train_df_preprocessed['Revenue'] = y_train.values
# #     test_df_preprocessed['Revenue'] = y_test.values
    
# #     # Save the preprocessed train and test data to output files
# #     train_df_preprocessed.to_csv(train_output_file, index=False)
# #     test_df_preprocessed.to_csv(test_output_file, index=False)
    
# #     click.echo(f"Data preprocessing completed. Preprocessed train data saved to: {train_output_file}")
# #     click.echo(f"Preprocessed test data saved to: {test_output_file}")

# # if __name__ == "__main__":
# #     preprocess_data()