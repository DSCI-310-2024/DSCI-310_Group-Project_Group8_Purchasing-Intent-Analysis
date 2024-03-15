import pandas as pd
import click
from sklearn.model_selection import train_test_split

@click.command()
@click.argument('clean_data', type=str)
@click.argument('output_folder', type=str)
def data_split_train_test(clean_data, output_folder):
    """
    Splits preprocessed data into train and test sets and saves them to the output folder.
    """
    # Read preprocessed data from the CSV file
    data = pd.read_csv(clean_data)
    
    # Define the target column
    target = 'Revenue'
    
    # Split the data into train and test sets
    train_df, test_df = train_test_split(data, test_size=0.3, random_state=123)
    
    # Create file paths for train and test data
    train_file = f"{output_folder}/train_data.csv"
    test_file = f"{output_folder}/test_data.csv"
    
    # Save the train and test sets to CSV files
    train_df.to_csv(train_file, index=False)
    test_df.to_csv(test_file, index=False)
    
    click.echo(f"Train and test sets saved to {output_folder}")

if __name__ == '__main__':
    data_split_train_test()