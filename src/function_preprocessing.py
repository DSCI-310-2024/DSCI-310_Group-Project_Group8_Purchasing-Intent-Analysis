import click
import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer

def preprocessing(X_train, X_test, y_train, y_test):
    """
    Applies preprocessing transformations to the data.

    Parameters:
    - X_train: DataFrame, training feature data
    - X_test: DataFrame, testing feature data
    - y_train: DataFrame, training target data
    - y_test: DataFrame, testing target data
    
    Returns:
    - Tuple containing preprocessed training and testing DataFrames
    """

    numeric_transformer = StandardScaler()
    categorical_transformer = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    binary_transformer = OneHotEncoder(drop='if_binary', dtype=int)

    # feature groups
    numeric_features = ['Administrative', 'Administrative_Duration', 'Informational',
                        'Informational_Duration', 'ProductRelated', 'ProductRelated_Duration',
                        'BounceRates', 'ExitRates', "PageValues", 'SpecialDay']

    categorical_features = ['Month', 'VisitorType']

    passthrough_features = ['Browser', 'Region', 'TrafficType', 'OperatingSystems']

    binary_features = ['Weekend']

    preprocessor = ColumnTransformer(
        transformers=[
            ('numeric', numeric_transformer, numeric_features),
            ('categorical', categorical_transformer, categorical_features),
            ('binary', binary_transformer, binary_features),
            ('passthrough', 'passthrough', passthrough_features),
        ]
    )

    X_train_transformed = preprocessor.fit_transform(X_train)
    X_test_transformed = preprocessor.transform(X_test)

    categorical_columns = preprocessor.named_transformers_['categorical'].get_feature_names_out(categorical_features)
    transformed_column_names = numeric_features + list(categorical_columns) + binary_features + passthrough_features

    X_train_transformed_df = pd.DataFrame(X_train_transformed, columns=transformed_column_names)
    X_test_transformed_df = pd.DataFrame(X_test_transformed, columns=transformed_column_names)

    train_transformed = pd.concat([X_train_transformed_df, y_train], axis=1)
    test_transformed = pd.concat([X_test_transformed_df, y_test], axis=1)

    return train_transformed, test_transformed

