#author: Calvin Choi, Nour Abdelfattah, Sana Shams, Sai Pusuluri
#date: 2024-04-09

"""
Cleans data by removing duplicates from the provided CSV files of features and targets,
then saves the cleaned data back to new CSV files.

Usage: 
    cleaning.py <x_data> <y_data> <cleaned_x_file> <cleaned_y_file>

Arguments:
    x_data -- Path to the CSV file containing features.
    y_data -- Path to the CSV file containing targets.
    cleaned_x_file -- Path where the cleaned features CSV file will be saved.
    cleaned_y_file -- Path where the cleaned targets CSV file will be saved.
"""

import pandas as pd
import click

@click.command()
@click.argument('x_data', type=str)
@click.argument('y_data', type=str)
@click.argument('cleaned_x_file', type=str)
@click.argument('cleaned_y_file', type=str)
def clean_data(x_data, y_data, cleaned_x_file, cleaned_y_file):
    """
    Concatenates features and targets from specified CSV files, cleans the resulting DataFrame
    by removing rows with duplicates, and saves the cleaned data to new CSV files for features and targets.

    Arguments:
    - x_data: Path to the CSV file containing features.
    - y_data: Path to the CSV file containing targets.
    - cleaned_x_file: Path where the cleaned features CSV file will be saved.
    - cleaned_y_file: Path where the cleaned targets CSV file will be saved.
    """
    # Concatenate train features and targets into a single DataFrame
    X = pd.read_csv(x_data)
    y = pd.read_csv(y_data)

    # # Cleaning Data
    # # Checking and dropping null values
    # null_values_before = train_data.isnull().sum().sum()
    # train_data.dropna(inplace=True)
    # null_values_after = train_data.isnull().sum().sum()
    # click.echo(f"Null values before cleaning: {null_values_before}, after cleaning: {null_values_after}.")

    # Checking and removing duplicated rows
    duplicates_before = X.duplicated().sum()
    X.drop_duplicates(inplace=True)
    y = y.loc[X.index]  # Ensure targets align with the cleaned features
    duplicates_after = X.duplicated().sum()

    click.echo(f"Duplicated rows in features before cleaning: {duplicates_before}, after cleaning: {duplicates_after}.")

    # Note: Adjust additional cleaning steps for features (X) and targets (y) as needed

    # Saving the cleaned data
    X.to_csv(cleaned_x_file, index=False)
    y.to_csv(cleaned_y_file, index=False)

    click.echo(f"Cleaned features saved to '{cleaned_x_file}'.")
    click.echo(f"Cleaned targets saved to '{cleaned_y_file}'.")

if __name__ == '__main__':
    clean_data()

