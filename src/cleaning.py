import pandas as pd
import click

@click.command()
@click.argument('input_file', type=str)
@click.argument('processed_file', type=str)
def clean_data(input_file, processed_file):
    # Read in data from the CSV file
    data = pd.read_csv(input_file)
    
    # Data cleaning
    # drop null
    if data.isnull().sum().any():
        null_values = data.isnull().sum()
        click.echo(f"Null values before cleaning:\n{null_values}")
        data.dropna(inplace = True)
        click.echo(f"Null values after cleaning:\n{data.isnull().sum()}")

    # drop duplicates
    if data.duplicated().any():
        duplicates = data[data.duplicated()]
        click.echo(f"Duplicates before cleaning:\n{duplicates}")

        # drop duplicates
        data.drop_duplicates(inplace=True)
        click.echo(f"Duplicates after cleaning: \n{data[data.duplicated()]}")

        # Drop "OperatingSystems" column as mentioned in ipynb file
        data.drop(columns = ["OperatingSystems"], inplace = True)
        click.echo(f"dropped OperatingSystems Column")

    else :
        click.echo(f"No duplicates found!")
        data.drop(columns = ["OperatingSystems"])
        click.echo(f"dropped OperatingSystems Column")

    # Save the processed data to a new CSV file
    data.to_csv(processed_file, index=False)
    
    click.echo("Data cleaned and saved successfully to {}".format(processed_file))

if __name__ == '__main__':
    clean_data()
