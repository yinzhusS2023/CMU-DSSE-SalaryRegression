from logging import *

import pandas as pd

label = 'salary.salaries'


class Preprocessor:
    def __init__(self, verbose=0):
        self.verbose = verbose

    def _select_cols(self, data: pd.DataFrame):
        pre_select = data.copy()
        if self.verbose == 1:
            info(f'columns before selection: {pre_select.columns}')
        pre_select = pre_select.loc[:, columns]
        if self.verbose == 1:
            info(f'columns before selection: {pre_select.columns}')
        return pre_select

    def _drop_na(self, data: pd.DataFrame):
        pre_drop = data.copy()
        if self.verbose == 1:
            info(f'NaN counts before drop: {pre_drop.isna().sum()}')
        pre_drop = pre_drop.dropna()
        if self.verbose == 1:
            info(f'NaN counts after drop: {pre_drop.isna().sum()}')
        return pre_drop

    def fit(self, data: pd.DataFrame):
        selected_cols = self._select_cols(data)
        dropped = self._drop_na(selected_cols)
        return dropped
