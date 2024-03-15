import pandas as pd 
import click

@click.command()
@click.argument('input_url', type = str)
@click.argument('output_path', type = str)
def read_data(input_url, output_path): 
    #read in data from input URL
    data = pd.read_csv(input_url)

    #save data to output file 
    data.to_csv(output_path, index = False)

    click.echo("Data downloaded and saved successfully")

if __name__ == '__main__':
    read_data()

