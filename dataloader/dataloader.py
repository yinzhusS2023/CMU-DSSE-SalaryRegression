import pandas as pd


class DataLoader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = None

    def load(self):
        self.data = pd.read_csv(self.file_path)


if __name__ == '__main__':
    dataloader = DataLoader('../data/glassdoor.csv')
    dataloader.load()
    print(dataloader.data.head())
