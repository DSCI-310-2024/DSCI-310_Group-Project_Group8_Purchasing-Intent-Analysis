import pandas as pd
import click
from sklearn.model_selection import train_test_split

# @click.command()
# @click.argument('clean_data', type=str)
# @click.argument('output_folder', type=str)
# def data_split_train_test(clean_data, output_folder):
#     """
#     Splits preprocessed data into train and test sets and saves them to the output folder.
#     """
#     # Read preprocessed data from the CSV file
#     data = pd.read_csv(clean_data)
    
#     # Define the target column
#     target = 'Revenue'
    
#     # Split the data into train and test sets
#     train_df, test_df = train_test_split(data, test_size=0.3, random_state=123)
    
#     # Create file paths for train and test data
#     train_file = f"{output_folder}/train_data.csv"
#     test_file = f"{output_folder}/test_data.csv"
    
#     # Save the train and test sets to CSV files
#     train_df.to_csv(train_file, index=False)
#     test_df.to_csv(test_file, index=False)
    
#     click.echo(f"Train and test sets saved to {output_folder}")

# if __name__ == '__main__':
#     data_split_train_test()

@click.command()
@click.argument('cleaned_x_file', type=str)
@click.argument('cleaned_y_file', type=str)
@click.argument('x_train_output_path', type=str)
@click.argument('x_test_output_path', type=str)
@click.argument('y_train_output_path', type=str)
@click.argument('y_test_output_path', type=str)
@click.option('--test_size', default=0.3, help='Size of the test set. Default is 0.3.')
@click.option('--random_state', default=42, help='Seed for the random number generator. Default is 42.')
def create_train_test_split(cleaned_x_file, cleaned_y_file, x_train_output_path, x_test_output_path, y_train_output_path, y_test_output_path, test_size, random_state):
    """
    Reads the features and targets from CSV files, creates a train-test split,
    and saves the splits into separate CSV files.
    """
    # Read in data from CSV files
    X = pd.read_csv(cleaned_x_file)
    y = pd.read_csv(cleaned_y_file)

    

    # Creating a train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)

    # Save the splits to CSV files
    X_train.to_csv(x_train_output_path, index=False)
    X_test.to_csv(x_test_output_path, index=False)
    y_train.to_csv(y_train_output_path, index=False)
    y_test.to_csv(y_test_output_path, index=False)

    click.echo("Train-test split created and saved successfully.")

if __name__ == '__main__':
    create_train_test_split()