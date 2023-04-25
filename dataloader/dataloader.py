import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

from config import dataloader_config


def _select_cols(data: pd.DataFrame, columns: list):
    pre_select = data.copy()
    pre_select = pre_select.loc[:, columns]
    print(f'After selecting columns, main data shape: {pre_select.shape}')
    return pre_select


def _drop_na(data: pd.DataFrame):
    # drop rows with any kind of null values
    pre_drop = data.copy()
    pre_drop.dropna(axis=0, how='any', subset=None, inplace=True)
    print(f'After dropping null values, main data info: {pre_drop.info()}')
    return pre_drop


def _search_title(data: pd.DataFrame):
    # attain only rows containing search words in job title while preserving all the columns
    search_words = dataloader_config.JOB_TITLE_SEARCH_WORDS
    search_words = [word.lower() for word in search_words]
    search_words = '|'.join([r'\b' + word + r'\b' for word in search_words])
    data = data.copy()
    data['title'] = data['salary.salaries.val.jobTitle'].str.lower()
    data['title'] = data['title'].fillna('')
    data = data[data['title'].str.contains(search_words)]
    print(f'After searching job title, main data info: {data.info()}')
    # write the result data to a csv file
    print('Writing searched data to ../data/glassdoor_searched.csv')
    data.to_csv('../data/glassdoor_searched.csv', index=False)
    return data


def _calib_salary(data: pd.DataFrame):
    salary_cols = ['salary.salaries.val.salaryPercentileMap.payPercentile10',
                   'salary.salaries.val.salaryPercentileMap.payPercentile90']
    salary_period = 'salary.salaries.val.payPeriod'

    # change the salary_cols of the data to yearly salary based on pay period
    def calib(row):
        if row[salary_period] == 'HOURLY':
            return (row[salary_cols[0]] + row[salary_cols[1]]) / 2 * 40 * 52
        elif row[salary_period] == 'MONTHLY':
            return (row[salary_cols[0]] + row[salary_cols[1]]) / 2 * 12
        else:
            return (row[salary_cols[0]] + row[salary_cols[1]]) / 2

    data = data.copy()
    data['salary'] = data.apply(calib, axis=1)
    return data


def _eliminate_outlier(data: pd.DataFrame, col: list or str):
    # eliminate outliers in the data
    data = data.copy()
    if isinstance(col, str):
        col = [col]
    for c in col:
        data = data[data[c] > data[c].quantile(0.05)]
        data = data[data[c] < data[c].quantile(0.95)]
        sns.histplot(data=data, x=c)
        plt.show()
    print(f'After eliminating outliers, main data info: {data.info()}')
    return data


class DataLoader:
    def __init__(self, main_file, benefit_file, review_file, salary_file):
        self.main_data = pd.read_csv(main_file)
        self.beni_data = pd.read_csv(benefit_file)
        self.review_data = pd.read_csv(review_file)
        self.salary_data = pd.read_csv(salary_file)
        self.data = self._join(self.main_data, self.beni_data, self.review_data, self.salary_data)
        self.processed_data = None

    @staticmethod
    def _join(data: pd.DataFrame, beni_data: pd.DataFrame, review_data: pd.DataFrame, salary_data: pd.DataFrame):
        # join benefit, review, salary data to the main data
        data = data.copy()
        data = pd.merge(data, beni_data, how='left', left_on='benefits.highlights', right_on='id')
        data = pd.merge(data, review_data, how='left', left_on='reviews', right_on='id')
        data = pd.merge(data, salary_data, how='left', left_on='salary.salaries', right_on='id')
        print(f'Original main data shape: {data.shape}')
        return data

    def _cleanse(self):
        data = _select_cols(self.data, dataloader_config.SELECTED_COLS)
        data = _drop_na(data)
        data = _eliminate_outlier(data, dataloader_config.OUTLIER_COLS)
        data = _search_title(data)
        data = _calib_salary(data)
        data = _eliminate_outlier(data, 'salary')
        return data

    def load(self):
        self.processed_data = self._cleanse()
        # preprocessor = Preprocessor(verbose=1)
        # self.processed_data = preprocessor.fit(self.data)


if __name__ == '__main__':
    dataloader = DataLoader(*dataloader_config.DATA_FILE_PATHS)
    dataloader.load()
    print(dataloader.processed_data.shape)
    # visualize the distribution of salary using seaborn
    sns.histplot(dataloader.processed_data['salary'])
    plt.show()
    print(dataloader.processed_data['salary'].describe())
