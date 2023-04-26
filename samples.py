

def GA_Feature_Selection_Sample():

    from sklearn.datasets import load_iris
    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LinearRegression
    # Modules
    from predictValidate import ModelValidator
    from trainer import ModelTrainer
    from featureSelection.GA.main import genetic_algorithm

    # Load the iris dataset
    iris = load_iris()

    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        iris.data, iris.target, test_size=0.2)

    def validation_function(X, y, classifier):
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
        return True, metric_result['R2']

    def threshold_function(fitness):
        return abs(fitness) < 0.00001

    result = genetic_algorithm(
        X_train,
        y_train,
        "LinearRegression",
        validation_function=validation_function,
        threshold_function=threshold_function,
        population_size=100
    )

    print(result)


def SA_Feature_Selection_Sample():

    from sklearn.datasets import load_iris
    from sklearn.model_selection import train_test_split
    # Modules
    from predictValidate import ModelValidator
    from trainer import ModelTrainer
    from featureSelection.SA.SimulatedAnnealing import SimulatedAnnealing

    # Load the iris dataset
    iris = load_iris()

    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        iris.data, iris.target, test_size=0.2)

    def validation_function(X, y, classifier):
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
        return True, metric_result['R2']

    def threshold_function(fitness):
        return abs(fitness) < 0.00001

    result = SimulatedAnnealing.simulated_annealing(
        X_train,
        y_train,
        "LinearRegression",
        validation_function=validation_function,
        threshold_function=threshold_function,
        max_iterations=10,
        temperature_constant=10
    )

    print(result)


def FilterMethod_PearsonCorrelationCoefficient_Sample():
    from featureSelection.FilterMethods import PearsonCorrelationCoefficient


    from sklearn.datasets import load_iris
    from sklearn.model_selection import train_test_split
    # Modules

    # Load the iris dataset
    iris = load_iris()

    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        iris.data, iris.target, test_size=0.2)

    result = PearsonCorrelationCoefficient.feature_selection(X_train, 0.5)

    print(result)

def FilterMethod_ChiSquare_Sample():
    from featureSelection.FilterMethods import ChiSquare


    from sklearn.datasets import load_iris
    from sklearn.model_selection import train_test_split
    # Modules

    # Load the iris dataset
    iris = load_iris()

    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        iris.data, iris.target, test_size=0.2)

    result = ChiSquare.feature_selection(X_train, y_train, 2)

    print(result)

def FilterMethod_AnovaF_Sample():
    from featureSelection.FilterMethods import AnovaF


    from sklearn.datasets import load_iris
    from sklearn.model_selection import train_test_split
    # Modules

    # Load the iris dataset
    iris = load_iris()

    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        iris.data, iris.target, test_size=0.2)

    result = AnovaF.feature_selection(X_train, y_train, 2)

    print(result)

# GA_Feature_Selection_Sample()
# SA_Feature_Selection_Sample()
# FilterMethod_PearsonCorrelationCoefficient_Sample()
# FilterMethod_ChiSquare_Sample()
FilterMethod_AnovaF_Sample()
