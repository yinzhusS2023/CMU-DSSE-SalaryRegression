import joblib


class ModelIO:

    @staticmethod
    def save_model(model, filepath):
        try:
            joblib.dump(model, filepath)
            print("Successfully saved model to file: " + filepath)
            return True
        except:
            print("Failed to save model to file: " + filepath)
            return False

    @staticmethod
    def load_model(filepath):
        try:
            loaded_model = joblib.load(filepath)
            return True, loaded_model
        except Exception as e:
            print("Failed to load model from file: ", filepath)
            print(e)
            return False, None
