import pandas as pd

from IO import ModelIO, ObjectManager


class Predictor:
    def __init__(self, model_path, gene_path):
        _, self.model = ModelIO.load_model(model_path)
        _, self.mask = ObjectManager.read_object(gene_path)

    def predict(self, X: pd.DataFrame):
        data_np = X.to_numpy().reshape(1, -1)
        data_np_masked = data_np[:, self.mask]
        salary = self.model.predict(data_np_masked) * 1.3
        salary = round(salary[0], 2)
        return salary


if __name__ == '__main__':
    predictor = Predictor('result/best.model', 'result/best.genes')
    data_df = pd.read_csv('data/glassdoor_clean_data.csv')
    data_df = data_df.drop('salary', axis=1)
    data = data_df.iloc[0]
    print(predictor.predict(data))
