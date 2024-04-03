import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer

def preprocessing(X_train, X_test, y_train, y_test, numeric_features, categorical_features, binary_features, passthrough_features):
    """
    Applies preprocessing transformations to the data, including scaling, encoding, and passing through features as specified.
    This function requires target data to be provided and includes it in the output DataFrames.

    Parameters:
    - X_train: DataFrame, training feature data
    - X_test: DataFrame, testing feature data
    - y_train: DataFrame, training target data
    - y_test: DataFrame, testing target data
    - numeric_features: list, names of numeric features to scale
    - categorical_features: list, names of categorical features to encode
    - binary_features: list, names of binary features to encode
    - passthrough_features: list, names of features to pass through without transformation
    
    Returns:
    - Tuple containing preprocessed training and testing DataFrames including target data, and transformed column names
    """
    
    # Setup transformers
    numeric_transformer = StandardScaler()
    categorical_transformer = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    binary_transformer = OneHotEncoder(drop='if_binary', dtype=int)
    
    # Define the preprocessor
    preprocessor = ColumnTransformer(
        transformers=[
            ('numeric', numeric_transformer, numeric_features),
            ('categorical', categorical_transformer, categorical_features),
            ('binary', binary_transformer, binary_features),
            ('passthrough', 'passthrough', passthrough_features),
        ]
    )
    
    # Apply transformations
    X_train_transformed = preprocessor.fit_transform(X_train)
    X_test_transformed = preprocessor.transform(X_test)
    
    # Retrieve transformed column names for future reference
    transformed_columns = preprocessor.get_feature_names_out()
    
    # Reconstruct DataFrames with transformed data and target columns
    X_train_transformed_df = pd.DataFrame(X_train_transformed, columns=transformed_columns)
    X_test_transformed_df = pd.DataFrame(X_test_transformed, columns=transformed_columns)
    
    # Concatenate transformed features with target data
    train_transformed = pd.concat([X_train_transformed_df, y_train.reset_index(drop=True)], axis=1)
    test_transformed = pd.concat([X_test_transformed_df, y_test.reset_index(drop=True)], axis=1)

    return train_transformed, test_transformed, transformed_columns
