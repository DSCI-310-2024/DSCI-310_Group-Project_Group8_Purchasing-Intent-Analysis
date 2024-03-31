import pandas as pd 
from ucimlrepo import fetch_ucirepo
import click

# @click.command()
# @click.argument('input_url', type = str)
# @click.argument('output_path', type = str)
# def read_data(input_url, output_path): 
#     #read in data from input URL
#     data = pd.read_csv(input_url)

#     #save data to output file 
#     data.to_csv(output_path, index = False)

#     click.echo("Data downloaded and saved successfully")

# if __name__ == '__main__':
#     read_data()

@click.command()
@click.argument('dataset_id', type=int)
@click.argument('features_output_path', type=str)
@click.argument('targets_output_path', type=str)
def fetch_and_save_dataset(dataset_id, features_output_path, targets_output_path):
    """
    Fetches a dataset from the UCI ML repository using its ID and saves
    the features and targets to separate CSV files.
    """
    # Fetch the dataset
    dataset = fetch_ucirepo(id=dataset_id)

    # Extract features and targets
    X = dataset.data.features
    y = dataset.data.targets

    # immediately converting y to numerical form as it is needed for EDA visualizations and later model compatibility
    y = y.astype(int)

    # Save features and targets to CSV files
    X.to_csv(features_output_path, index=False)
    y.to_csv(targets_output_path, index=False)

    click.echo(f"Dataset {dataset_id} downloaded and saved successfully. Features: {features_output_path}, Targets: {targets_output_path}")

if __name__ == '__main__':
    fetch_and_save_dataset()