import pandas as pd
from featureSelection.FilterMethods import AnovaF, ChiSquare, PearsonCorrelationCoefficient
from featureSelection.GA.main import genetic_algorithm
from featureSelection.RecursiveFeatureElimination import RecursiveFeatureElimination
from featureSelection.SA.SimulatedAnnealing import SimulatedAnnealing
from predictValidate import ModelValidator
from sklearn.model_selection import train_test_split
import numpy as np


from trainer import ModelTrainer


def LoadDataPoints():
    try:
        df = pd.read_csv('data\glassdoor_clean_data.csv')
        X = df.drop('salary', axis=1)
        y = df['salary']
        return True, (X, y)
    except Exception as e:
        print("Error loading data: " + str(e))
        return False, None


def validation_function(X, y, classifier, metric='MSE'):
    train_success, train_result = ModelTrainer.train_by_grid_search(
        X, y, classifier)
    if not train_success:
        print("Error[in validation function]: training failed")
        return False, 0
    # {
    #     "model_name": model_name,
    #     "training_time": training_time,
    #     "best_params": grid_search.best_params_,
    #     "best_model": grid_search.best_estimator_
    # }
    model = train_result['best_model']
    metric_success, metric_result = ModelValidator.get_general_metrics(
        X, y, model)
    if not metric_success:
        print("Error[in validation function]: validation failed")
        return False, 0
    return True, -metric_result[metric]


def threshold_function(fitness):
    print("IN Threshold function: %s" % fitness)
    return abs(fitness) <= 40000


valid_algo = {
    'GA': 'GA',
    'SA': 'SA',
    'PCC': 'PCC',
    'C2': 'C2',
    'AF': 'AF',
    'RFE': 'RFE',
}


def FeatureSelectionAdapter(X_train, y_train, method, algorithm='LinearRegression'):
    if method == 'GA':
        return genetic_algorithm(
            X_train,
            y_train,
            algorithm,
            validation_function=validation_function,
            threshold_function=threshold_function,
        )
    elif method == "SA":
        return SimulatedAnnealing.simulated_annealing(
            X_train,
            y_train,
            algorithm,
            validation_function=validation_function,
            threshold_function=threshold_function,
        )
    elif method == 'PCC':
        return PearsonCorrelationCoefficient.feature_selection(X_train, 0.25)
    elif method == 'C2':
        return ChiSquare.feature_selection(X_train, y_train, 50)
    elif method == 'AF':
        return AnovaF.feature_selection(X_train, y_train, 50)
    elif method == 'RFE':
        return RecursiveFeatureElimination.feature_seleciton(
            X_train, y_train, 40, 10)
    return False, None


def main():
    load_success, loaded_data = LoadDataPoints()
    if not load_success:
        return
    X, y = loaded_data
    X = np.asarray(X)

    feature_selection_success, feature_selection_result = FeatureSelectionAdapter(
        X, y, 'GA', 'KNeighborsRegressor')
    if not feature_selection_success:
        return
    #  result_obj = {
    #             "X": result,
    #             "mask": mask,
    #             "time_used": time_used,
    #             "number_of_iterations": 0,
    #             "number_of_features": sum([1 if item else 0 for item in mask])
    #         }

    X = X[:, feature_selection_result['mask']]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2)

    train_success, train_result = ModelTrainer.train_by_grid_search(
        X_train, y_train)
    if not train_success:
        return
    #     result_obj = {
    #     "model_name": model_name,
    #     "training_time": training_time,
    #     "best_params": grid_search.best_params_,
    #     "best_model": grid_search.best_estimator_
    # }
    best_model = train_result['best_model']
    validate_success, validate_result = ModelValidator.get_general_metrics(
        X_test, y_test, best_model)
    if not validate_success:
        return
    print(validate_result)


if __name__ == "__main__":
    main()
