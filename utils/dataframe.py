import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt


def write_unique_values_to_file(data: pd.DataFrame, column: str, file_name: str, sort: bool = True):
    """
    Write unique values of a column in a dataframe to a file
    :param data: dataframe
    :param column: column name
    :param file_name: file to write
    :param sort: if to sort the unique values
    :return: None
    """
    if sort:
        unique_values = sorted(data[column].unique())
    else:
        unique_values = data[column].unique()
    with open(file_name, 'w') as f:
        for value in unique_values:
            f.write(str(value) + '\n')


def plot_hist(data: pd.DataFrame, column: str, kde: bool, title: str, x_label: str, y_label: str, file_name: str):
    """
    Plot histogram of a column in a dataframe
    :param data: dataframe
    :param column: column name
    :param kde: if to plot kde
    :param title: title of the plot
    :param x_label: label of x-axis
    :param y_label: label of y-axis
    :param file_name: file to save the plot
    :return: None
    """
    plt.figure(figsize=(10, 6))
    sns.histplot(data=data, x=column, kde=kde)
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.savefig(file_name, dpi=300, bbox_inches='tight')
    plt.show()


def extract_lower_bound(x: str) -> int:
    """
    Extract lower bound from a string like '100-200'
    :param x: string
    :return: lower bound
    """
    lower_bound = x.split('-')[0]
    if lower_bound == '':
        lower_bound = -1
    try:
        return int(lower_bound)
    except ValueError:
        print(x)


if __name__ == '__main__':
    df = pd.read_csv('../data/glassdoor_benefits_highlights.csv')
    write_unique_values_to_file(df, 'benefits.highlights.val.name', '../data/benefits_highlights.txt', False)
