#author: Calvin Choi, Nour Abdelfattah, Sana Shams, Sai Pusuluri
#date: 2024-04-09

"""
Splits cleaned feature and target datasets into training and testing sets and saves those sets to CSV files.

Usage: 
    data_split.py <cleaned_x_file> <cleaned_y_file> <x_train_output_path> <x_test_output_path> <y_train_output_path> <y_test_output_path> [--test_size=<test_size>] [--random_state=<random_state>]

Arguments:
    cleaned_x_file -- Path to the cleaned features CSV file.
    cleaned_y_file -- Path to the cleaned targets CSV file.
    x_train_output_path -- Path to save the training features CSV file.
    x_test_output_path -- Path to save the testing features CSV file.
    y_train_output_path -- Path to save the training targets CSV file.
    y_test_output_path  -- Path to save the testing targets CSV file.

Options:
--test_size=<test_size>         The proportion of the dataset to include in the test split.
--random_state=<random_state>   The seed used by the random number generator. 

"""

import pandas as pd
import click
from sklearn.model_selection import train_test_split

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