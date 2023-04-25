import pandas as pd


# read unique values from a column and write to a file
def write_unique_values_to_file(data: pd.DataFrame, column: str, file_name: str):
    with open(file_name, 'w') as f:
        for value in data[column].unique():
            f.write(str(value) + '\n')


if __name__ == '__main__':
    df = pd.read_csv('../data/glassdoor_benefits_highlights.csv')
    write_unique_values_to_file(df, 'benefits.highlights.val.name', '../data/benefits_highlights.txt')
