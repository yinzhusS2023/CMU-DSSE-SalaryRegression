from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score


class ModelValidator:
    @staticmethod
    def get_general_metrics(X, real_y, classifier):
        """
        X: data point for prediction
        real_y: real label
        classifier: classifier
        :return True, Metrics {R2: MSE: MAE:}
                False, None       
        """    
        predicted_y = classifier.predict(X)
        try:
            gm = {
                'R2': r2_score(real_y, predicted_y),
                'MSE': mean_squared_error(real_y, predicted_y),
                'MAE': mean_absolute_error(real_y, predicted_y),
            }
            return True, gm
        except Exception as e:
            print("Get general metrics failed: " + str(e))
            return False, None
