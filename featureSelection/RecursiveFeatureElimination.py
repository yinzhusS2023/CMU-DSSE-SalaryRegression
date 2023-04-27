
import time
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression


class RecursiveFeatureElimination:
    @staticmethod
    def feature_seleciton(X,y, n=10, step=10):
        try:
            time_start = time.time()
            estimator = LogisticRegression()
            selector = RFE(estimator, n_features_to_select=n, step=step)
            selector = selector.fit(X, y)
            mask = selector.support_
            time_used = time.time() - time_start
            result_obj = {
                "X": X[:, mask],
                "mask": mask,
                "time_used": time_used,
                "number_of_iterations": 0,
                "number_of_features": sum([1 if item else 0 for item in mask])
            }
            return True, result_obj
        except Exception as e:
            print( "Error[in RecursiveFeatureElimination.feature_selection]: Feature selection failed: " + str(e))
            return False, None

