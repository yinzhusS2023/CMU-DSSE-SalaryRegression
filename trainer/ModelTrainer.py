# Packages
import time

# All Models
from sklearn.linear_model import BayesianRidge, LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import GradientBoostingRegressor

# Grid Search Related
from sklearn.model_selection import GridSearchCV


class ModelTrainer:
    MODEL_MAP = {
        "LinearRegression": LinearRegression,
        "BayesianRidge": BayesianRidge,
        "DecisionTreeRegressor": DecisionTreeRegressor,
        "MLPRegressor": MLPRegressor,
        "KNeighborsRegressor": KNeighborsRegressor,
        "GradientBoostingRegressor": GradientBoostingRegressor
    }

    MODEL_PARAMS = {
        "LinearRegression": {
            # 'fit_intercept': [True, False],
            # 'copy_X': [True, False],
            # 'positive': [True, False],
        },
        "BayesianRidge": {
            # 'alpha_1': [1e-6, 1e-5, 1e-4, 1e-3],
            # 'alpha_2': [1e-6, 1e-5, 1e-4, 1e-3],
            # 'lambda_1': [1e-6, 1e-5, 1e-4, 1e-3],
            # 'lambda_2': [1e-6, 1e-5, 1e-4, 1e-3],
        },
        "DecisionTreeRegressor": {
            # 'max_depth': [2, 4, 6, 8, 10],
            # 'min_samples_split': [2, 4, 6, 8, 10],
            # 'min_samples_leaf': [1, 2, 3, 4, 5],
            # 'max_features': ['auto', 'sqrt', 'log2']
        },
        "MLPRegressor": {
            # 'hidden_layer_sizes': [(10,), (20,), (10, 20,), (20, 10,)],
            # 'activation': ['identity', 'logistic', 'tanh', 'relu'],
            # 'solver': ['lbfgs', 'sgd', 'adam'],
            # 'alpha': [0.0001, 0.001, 0.01],
            # 'learning_rate': ['constant', 'invscaling', 'adaptive']
        },
        "KNeighborsRegressor": {
            # 'n_neighbors': [3, 5, 7, 9],
            # 'weights': ['uniform', 'distance'],
            # 'p': [1, 2]
        }, "GradientBoostingRegressor": {
            # 'n_estimators': [50, 100, 200],
            # 'learning_rate': [0.01, 0.1, 1],
            # 'max_depth': [3, 5, 7],
            # 'min_samples_split': [2, 5, 10],
            # 'min_samples_leaf': [1, 2, 4],
            # 'max_features': ['auto', 'sqrt', 'log2']
        }
    }

    @staticmethod
    def train_by_grid_search(X, y, model_name='LinearRegression', model_params=None, cv=10):
        try:
            training_start = time.time()
            grid_search = GridSearchCV(ModelTrainer.MODEL_MAP[model_name](), param_grid=model_params if (
                model_params is not None) else ModelTrainer.MODEL_PARAMS[model_name], cv=cv, n_jobs=-1)
            grid_search.fit(X, y)
            training_time = time.time() - training_start
            # Return Result
            result_obj = {
                "model_name": model_name,
                "training_time": training_time,
                "best_params": grid_search.best_params_,
                "best_model": grid_search.best_estimator_
            }
            return True, result_obj
        except Exception as e:
            print(
                "Error[In ModelTrainer.train_by_grid_search]: Failed to train: " + str(e))
            return False, None
