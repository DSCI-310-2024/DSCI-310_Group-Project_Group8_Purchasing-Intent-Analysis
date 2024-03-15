import click
import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import make_column_transformer

@click.command()
@click.argument('cleaned_data', type=str)
@click.argument('output_file', type=str)
def preprocess_data(cleaned_data, output_file):
    """
    Reads data from cleaned_data (output of the clean_data script),
    performs data preprocessing, and saves the preprocessed data to the output file.
    """
    # Read the data from the input file
    data = pd.read_csv(cleaned_data)
    
    # Define transformers
    numeric_transformer = StandardScaler()
    categorical_transformer = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    binary_transformer = OneHotEncoder(drop='if_binary', dtype=int)

    # Define feature groups
    numeric_features = ['Administrative', 'Administrative_Duration', 'Informational',
                        'Informational_Duration', 'ProductRelated', 'ProductRelated_Duration',
                        'BounceRates', 'ExitRates', "PageValues", 'SpecialDay']

    categorical_features = ['Month', 'VisitorType']

    passthrough_features = ['Browser', 'Region', 'TrafficType']

    binary_features = ['Weekend']

    drop_features = ['OperatingSystems']
    
    # Create preprocessor with feature groups and transformers
    preprocessor = make_column_transformer(
        (numeric_transformer, numeric_features),
        (categorical_transformer, categorical_features),
        (binary_transformer, binary_features),
        ('passthrough', passthrough_features),
        ('drop', drop_features)
    )
    
    # Fit and transform the data
    preprocessed_data = preprocessor.fit_transform(data)
    
    # Convert the preprocessed data to a DataFrame
    preprocessed_df = pd.DataFrame(preprocessed_data, columns=numeric_features +
                                   list(preprocessor.named_transformers_['onehotencoder'].get_feature_names(categorical_features)) +
                                   binary_features + passthrough_features)
    
    # Save the preprocessed data to the output file
    preprocessed_df.to_csv(output_file, index=False)
    
    click.echo("Data preprocessing completed. Preprocessed data saved to:", output_file)

if __name__ == "__main__":
    preprocess_data()