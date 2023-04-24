import pandas as pd

from preprocessing import Preprocessor


class DataLoader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = None
        self.processed_data = None

    def load(self):
        self.data = pd.read_csv(self.file_path)
        preprocessor = Preprocessor(verbose=1)
        self.processed_data = preprocessor.fit(self.data)


if __name__ == '__main__':
    dataloader = DataLoader('../data/glassdoor.csv')
    dataloader.load()
    print(dataloader.processed_data.shape)
