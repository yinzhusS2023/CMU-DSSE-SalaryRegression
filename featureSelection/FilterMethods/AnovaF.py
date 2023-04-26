import time
import pandas as pd
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_classif


class AnovaF:
    @staticmethod
    def feature_selection(X, y,k=10):
        try:
            time_start = time.time()
            best_features = SelectKBest(score_func=f_classif, k=k).fit(X, y)
            mask = best_features.get_support()
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
            print(
            "Error[in AnovaF.feature_selection]: Feature selection failed: " + str(e))
            return False, None
