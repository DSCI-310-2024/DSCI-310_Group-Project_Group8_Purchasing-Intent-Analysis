import pandas as pd
import click

@click.command()
@click.argument('input_file', type=str)
@click.argument('processed_file', type=str)
def process_data(input_file, processed_file):
    # Read in data from the CSV file
    data = pd.read_csv(input_file)
    
    # Data cleaning/pre-processing steps go here
    # drop duplicates
    data.drop_duplicates(inplace=True)
        
    # Drop "OperatingSystems" column as mentioned in ipynb file
    data.drop(columns = ["OperatingSystems"])


    # Save the processed data to a new CSV file
    data.to_csv(processed_file, index=False)
    
    click.echo("Data processed and saved successfully to {}".format(processed_file))

if __name__ == '__main__':
    process_data()
