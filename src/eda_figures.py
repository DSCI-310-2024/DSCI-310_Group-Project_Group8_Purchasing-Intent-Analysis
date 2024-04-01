import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import click


@click.command()
@click.argument('cleaned_x_file', type=str)
@click.argument('cleaned_y_file', type=str)
@click.argument('figure_prefix', type=str)
def visualize_data(cleaned_x_file,cleaned_y_file, figure_prefix):
    # Read the data into a pandas DataFrame
    X = pd.read_csv(cleaned_x_file)
    y = pd.read_csv(cleaned_y_file)

    # Combine the features and target into a single DataFrame
    data = pd.concat([X, y], axis=1)

    # Path where figures will be saved
    img_dir = '../img/'
    
    # Revenue Class Distribution
    plt.figure(figsize=(10, 5))
    sns.countplot(data=data, x='Revenue')
    plt.title('Revenue Class Distribution')
    plt.xlabel('Revenue')
    plt.ylabel('Count')
    plt.savefig(img_dir + f'{figure_prefix}_revenue_class_distribution.png')
    plt.close()
    click.echo("Revenue Class Distrubution plots Complete!")

    # Month Distribution: Pie and Bar Plots
    fig, axs = plt.subplots(1, 2, figsize=(14, 7))
    month_counts = data['Month'].value_counts()
    axs[0].pie(month_counts, labels=month_counts.index, autopct='%1.1f%%', startangle=140)
    axs[0].set_title('Distribution of Sessions by Month')
    revenue_true_per_month = data[data['Revenue'] == True].groupby('Month').size()
    revenue_true_per_month.plot(kind='bar', color='skyblue', ax=axs[1])
    axs[1].set_title('Number of Purchases (Revenue=True) by Month')
    axs[1].set_xlabel('Month')
    axs[1].set_ylabel('Number of Purchases')
    axs[1].grid(axis='y')
    plt.tight_layout()
    plt.savefig(img_dir + f'{figure_prefix}_month_distribution.png')
    plt.close()
    click.echo("Month Distrubution plots Complete!")

    # Browser Distribution: Pie and Bar Plots
    fig, axs = plt.subplots(1, 2, figsize=(14, 7))
    browser_counts = data['Browser'].value_counts()
    axs[0].pie(browser_counts, labels=browser_counts.index, autopct='%1.1f%%', startangle=140)
    axs[0].set_title('Distribution of Sessions by Browser')
    axs[0].legend()
    revenue_true_browser = data[data['Revenue'] == True].groupby('Browser').size()
    revenue_true_browser.plot(kind='bar', color='skyblue', ax=axs[1])
    axs[1].set_title('Number of Purchases (Revenue=True) by Browser')
    axs[1].set_xlabel('Browser')
    axs[1].set_ylabel('Revenue (Number of Purchases)')
    axs[1].grid(axis='y')
    plt.tight_layout()
    plt.savefig(img_dir + f'{figure_prefix}_browser_distribution.png')
    plt.close()
    click.echo("Browser Distrubution plots Complete!")

    # Region Distribution: Pie and Bar Plots
    fig, axs = plt.subplots(1, 2, figsize=(14, 7))
    region_counts = data['Region'].value_counts()
    axs[0].pie(region_counts, labels=region_counts.index, autopct='%1.1f%%', startangle=140)
    axs[0].set_title('Distribution of Sessions by Region')
    axs[0].legend()
    revenue_true_region = data[data['Revenue'] == True].groupby('Region').size()
    revenue_true_region.plot(kind='bar', color='skyblue', ax=axs[1])
    axs[1].set_title('Number of Purchases (Revenue=True) by Region')
    axs[1].set_xlabel('Region')
    axs[1].set_ylabel('Revenue (Number of Purchases)')
    axs[1].grid(axis='y')
    plt.tight_layout()
    plt.savefig(img_dir + f'{figure_prefix}_region_distribution.png')
    plt.close()
    click.echo("Region Distrubution plots Complete!")

    # Traffic Type Distribution: Pie and Bar Plots
    fig, axs = plt.subplots(1, 2, figsize=(14, 7))
    traffic_counts = data['TrafficType'].value_counts()
    axs[0].pie(traffic_counts, labels=traffic_counts.index, autopct='%1.1f%%', startangle=140)
    axs[0].set_title('Distribution of Sessions by Traffic Type')
    axs[0].legend()
    revenue_true_traffic = data[data['Revenue'] == True].groupby('TrafficType').size()
    revenue_true_traffic.plot(kind='bar', color='skyblue', ax=axs[1])
    axs[1].set_title('Number of Purchases (Revenue=True) by Traffic Type')
    axs[1].set_xlabel('Traffic Type')
    axs[1].set_ylabel('Revenue (Number of Purchases)')
    axs[1].grid(axis='y')
    plt.tight_layout()
    plt.savefig(img_dir + f'{figure_prefix}_traffic_type_distribution.png')
    plt.close()
    click.echo("Traffic Type Distrubution plots Complete!")

    # Visitor Type Distribution: Pie and Bar Plots
    fig, axs = plt.subplots(1, 2, figsize=(14, 7))
    visitor_counts = data['VisitorType'].value_counts()
    axs[0].pie(visitor_counts, labels=visitor_counts.index, autopct='%1.1f%%', startangle=140)
    axs[0].set_title('Distribution of Sessions by Visitor Type')
    axs[0].legend()
    revenue_true_visitor = data[data['Revenue'] == True].groupby('VisitorType').size()
    revenue_true_visitor.plot(kind='bar', color='skyblue', ax=axs[1])
    axs[1].set_title('Number of Purchases (Revenue=True) by Visitor Type')
    axs[1].set_xlabel('Visitor Type')
    axs[1].set_ylabel('Revenue (Number of Purchases)')
    axs[1].grid(axis='y')
    plt.tight_layout()
    plt.savefig(img_dir + f'{figure_prefix}_visitor_type_distribution.png')
    plt.close()
    click.echo("Visitor Type Distrubution plots Complete!")

    # Weekend Distribution: Pie and Bar Plots
    fig, axs = plt.subplots(1, 2, figsize=(14, 7))
    weekend_counts = data['Weekend'].value_counts()
    axs[0].pie(weekend_counts, labels=weekend_counts.index, autopct='%1.1f%%', startangle=140)
    axs[0].set_title('Distribution of Sessions by Weekend')
    axs[0].legend()
    revenue_true_weekend = data[data['Revenue'] == True].groupby('Weekend').size()
    revenue_true_weekend.plot(kind='bar', color='skyblue', ax=axs[1])
    axs[1].set_title('Number of Purchases (Revenue=True) by Weekend')
    axs[1].set_xlabel('Weekend')
    axs[1].set_ylabel('Revenue (Number of Purchases)')
    axs[1].grid(axis='y')
    plt.tight_layout()
    plt.savefig(img_dir + f'{figure_prefix}_weekend_distribution.png')
    plt.close()
    click.echo("Weekend Distrubution plots Complete!")

    # Correlation Matrix of Numerical Features

    numerical_features = data.select_dtypes(include=['int64', 'float64'])
    corr_matrix = numerical_features.corr()
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap='coolwarm')
    plt.title('Correlation Matrix of Numerical Features')
    plt.savefig(img_dir + f'{figure_prefix}_correlation_matrix.png')
    plt.close()
    click.echo("Correlation Matrix of Numerical Features plots Complete!")

    click.echo("All visualizations created and saved with prefix {}".format(figure_prefix))

if __name__ == '__main__':
    visualize_data()
