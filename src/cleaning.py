import pandas as pd
import click

@click.command()
@click.argument('x_train_csv_path', type=str)
@click.argument('y_train_csv_path', type=str)
@click.argument('processed_file', type=str)
def process_data(x_train_csv_path, y_train_csv_path, processed_file):
    """
    Concatenates features and targets from specified CSV files, cleans the resulting DataFrame
    by removing rows with null values and duplicates, and saves the cleaned data to a new CSV file.

    Arguments:
    - x_train_csv_path: Path to the CSV file containing features.
    - y_train_csv_path: Path to the CSV file containing targets.
    - processed_file: Path where the cleaned and processed CSV file will be saved.
    """
    # Concatenate train features and targets into a single DataFrame
    X_train = pd.read_csv(x_train_csv_path)
    y_train = pd.read_csv(y_train_csv_path)

    train_data = pd.concat([X_train, y_train], axis=1)
    click.echo("Features and targets concatenated.")

    # Cleaning Data
    # Checking and dropping null values
    null_values_before = train_data.isnull().sum().sum()
    train_data.dropna(inplace=True)
    null_values_after = train_data.isnull().sum().sum()
    click.echo(f"Null values before cleaning: {null_values_before}, after cleaning: {null_values_after}.")

    # Checking and removing duplicated rows
    duplicates_before = train_data.duplicated().sum()
    train_data.drop_duplicates(inplace=True)
    duplicates_after = train_data.duplicated().sum()
    click.echo(f"Duplicated rows before cleaning: {duplicates_before}, after cleaning: {duplicates_after}.")

    # Saving the cleaned data
    train_data.to_csv(processed_file, index=False)
    click.echo(f"Cleaned data saved to '{processed_file}'.")

if __name__ == '__main__':
    process_data()



# @click.command()
# @click.argument('input_file', type=str)
# @click.argument('processed_file', type=str)
# def clean_data(input_file, processed_file):
#     # Read in data from the CSV file
#     data = pd.read_csv(input_file)
    
#     # Data cleaning
#     # drop null
#     if data.isnull().sum().any():
#         null_values = data.isnull().sum()
#         click.echo(f"Null values before cleaning:\n{null_values}")
#         data.dropna(inplace = True)
#         click.echo(f"Null values after cleaning:\n{data.isnull().sum()}")

#     # drop duplicates
#     if data.duplicated().any():
#         duplicates = data[data.duplicated()]
#         click.echo(f"Duplicates before cleaning:\n{duplicates}")

#         # drop duplicates
#         data.drop_duplicates(inplace=True)
#         click.echo(f"Duplicates after cleaning: \n{data[data.duplicated()]}")

#         # Drop "OperatingSystems" column as mentioned in ipynb file
#         data.drop(columns = ["OperatingSystems"], inplace = True)
#         click.echo(f"dropped OperatingSystems Column")

#     else :
#         click.echo(f"No duplicates found!")
#         data.drop(columns = ["OperatingSystems"])
#         click.echo(f"dropped OperatingSystems Column")

#     # Save the processed data to a new CSV file
#     data.to_csv(processed_file, index=False)
    
#     click.echo("Data cleaned and saved successfully to {}".format(processed_file))

# if __name__ == '__main__':
#     clean_data()
