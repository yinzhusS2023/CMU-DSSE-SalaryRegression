from config import dataloader_config
from sentianalysis import SentimentAnalyzer
from utils.dataframe import *


def _search_title(data: pd.DataFrame):
    # attain only rows containing search words in job title while preserving all the columns
    search_words = dataloader_config.JOB_TITLE_SEARCH_WORDS
    search_words = [word.lower() for word in search_words]
    search_words = '|'.join([r'\b' + word + r'\b' for word in search_words])
    data = data.copy()
    data['title'] = data['salary.salaries.val.jobTitle'].str.lower()
    data['title'] = data['title'].fillna('')
    data = data[data['title'].str.contains(search_words)]
    return data


def _calib_salary(data: pd.DataFrame):
    salary_cols = ['salary.salaries.val.salaryPercentileMap.payPercentile10',
                   'salary.salaries.val.salaryPercentileMap.payPercentile90']
    salary_period = 'salary.salaries.val.payPeriod'

    def calib(row):
        if row[salary_period] == 'HOURLY':
            return (row[salary_cols[0]] + row[salary_cols[1]]) / 2 * 40 * 52
        elif row[salary_period] == 'MONTHLY':
            return (row[salary_cols[0]] + row[salary_cols[1]]) / 2 * 12
        else:
            return (row[salary_cols[0]] + row[salary_cols[1]]) / 2

    data = data.copy()
    data['salary'] = data.apply(calib, axis=1)
    data = data.drop(columns=salary_cols)
    data = data.drop(columns=salary_period)
    return data


def _count_tech_words(data: pd.DataFrame):
    """
    Count the number of technical words in the job description
    :param data:
    :return:
    """
    tech_words = dataloader_config.TECH_STACK
    data = data.copy()
    data['description'] = data['job.description'].str.lower()
    data['description'] = data['description'].fillna('')
    for word in tech_words:
        word_regex = word.replace('+', '\+')
        word_regex = word_regex.replace('.', '\.')
        word_regex = r'\b' + word_regex + r'\b'
        data[word] = data['description'].str.count(word_regex)
    data = data.drop(columns=['job.description', 'description'])
    return data


def _eliminate_outlier(data: pd.DataFrame, col: list or str):
    # eliminate outliers in the data
    data = data.copy()
    if isinstance(col, str):
        col = [col]
    for c in col:
        data = data[data[c] > data[c].quantile(0.05)]
        data = data[data[c] < data[c].quantile(0.95)]
    return data


def _sentiment(text: str):
    # get the sentiment of a text
    analyzer = SentimentAnalyzer(text)
    return analyzer.get_sentiment()


def _location(text: str):
    # check if the text is a location in the US
    state = text.split(',')[-1].strip().upper()
    if state in dataloader_config.US_STATES:
        return 1
    else:
        return 0


def _type(text: str):
    # check if the text is not a company
    if text != 'Company - Private' and text != 'Company - Public':
        return 'Other'
    else:
        return text


class DataLoader:
    def __init__(self, main_file, benefit_file, review_file, salary_file):
        self.main_data = pd.read_csv(main_file)
        self.beni_data = pd.read_csv(benefit_file)
        self.review_data = pd.read_csv(review_file)
        self.salary_data = pd.read_csv(salary_file)
        self.clean_data = None

    @staticmethod
    def _join(data: pd.DataFrame, beni_data: pd.DataFrame, review_data: pd.DataFrame, salary_data: pd.DataFrame):
        # join benefit, review, salary data to the main data
        data = data.copy()
        data = pd.merge(data, beni_data, how='left', left_on='benefits.highlights', right_on='id')
        data = pd.merge(data, review_data, how='left', left_on='reviews', right_on='id')
        data = pd.merge(data, salary_data, how='left', left_on='salary.salaries', right_on='id')
        return data

    def _clean_beni(self):
        print('Cleaning benefit data...')
        self.beni_data = self.beni_data.loc[:, dataloader_config.SELECTED_COLS_BENI]
        self.beni_data = self.beni_data.dropna(axis=0, how='any')
        self.beni_data = pd.get_dummies(self.beni_data, 'benefits.highlights.val.name')
        self.beni_data = self.beni_data.groupby('id').agg('sum')
        print(f'After cleaning, benefit data shape: {self.beni_data.shape}')

    def _clean_review(self):
        print('Cleaning review data...')
        self.review_data = self.review_data.loc[:, dataloader_config.SELECTED_COLS_REVIEW]
        self.review_data = self.review_data.dropna(axis=0, how='any')
        self.review_data['pro_sentiment'] = self.review_data['reviews.val.pros'].apply(lambda x: _sentiment(x))
        self.review_data = self.review_data[self.review_data['pro_sentiment'] != 0]
        self.review_data['con_sentiment'] = self.review_data['reviews.val.cons'].apply(lambda x: _sentiment(x))
        self.review_data = self.review_data[self.review_data['con_sentiment'] != 0]
        self.review_data = self.review_data.groupby('id').agg('mean')
        print(f'After cleaning, review data shape: {self.review_data.shape}')

    def _clean_salary(self):
        print('Cleaning salary data...')
        self.salary_data = self.salary_data.loc[:, dataloader_config.SELECTED_COLS_SALARY]
        self.salary_data = self.salary_data.dropna(axis=0, how='any')
        self.salary_data = _search_title(self.salary_data)
        self.salary_data = _calib_salary(self.salary_data)
        self.salary_data = _eliminate_outlier(self.salary_data, 'salary')
        print(f'After cleaning, salary data shape: {self.salary_data.shape}')

    def _clean_main(self):
        print('Cleaning main data...')
        self.main_data = self.main_data.loc[:,
                         dataloader_config.SELECTED_COLS_MAIN + dataloader_config.SELECTED_COLS_ID]
        self.main_data = self.main_data.dropna(axis=0, how='any')
        self.main_data = _eliminate_outlier(self.main_data, dataloader_config.OUTLIER_COLS_MAIN)
        self.main_data = _count_tech_words(self.main_data)
        self.main_data['header.sponsored'] = self.main_data['header.sponsored'].astype(int)
        self.main_data['map.location'] = self.main_data['map.location'].apply(lambda x: _location(x))
        self.main_data['overview.type'] = self.main_data['overview.type'].apply(lambda x: _type(x))
        self.main_data = pd.get_dummies(self.main_data, columns=['gaTrackerData.empSize',
                                                                 'gaTrackerData.industry',
                                                                 'overview.type'])
        print(f'After cleaning, main data shape: {self.main_data.shape}\n')

    def _cleanse(self):
        self._clean_beni()
        self._clean_review()
        self._clean_salary()
        self._clean_main()

    def load(self):
        self._cleanse()
        self.clean_data = self._join(self.main_data, self.beni_data, self.review_data, self.salary_data)
        self.clean_data = self.clean_data.drop(columns=dataloader_config.SELECTED_COLS_ID)
        self.clean_data = self.clean_data.drop(columns=['id'])
        self.clean_data.dropna(axis=0, how='any', inplace=True)


if __name__ == '__main__':
    dataloader = DataLoader(*dataloader_config.DATA_FILE_PATHS)
    dataloader.load()
    print(dataloader.clean_data.shape)
    plot_hist(data=dataloader.clean_data,
              column='salary',
              kde=True,
              title='Salary Distribution',
              x_label='Salary',
              y_label='Count',
              file_name='../plots/salary_distribution.png')
    dataloader.clean_data.to_csv('../data/glassdoor_clean_data.csv', index=False)
