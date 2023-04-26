
import time
import pandas as pd
import numpy as np


class PearsonCorrelationCoefficient:

    def feature_selection(data, threshold=0.5):
        try:     
            time_start = time.time()
            if not  isinstance(data, pd.DataFrame):
                data = pd.DataFrame(data)
            corr_matrix = data.corr(method='pearson')
            highly_correlated_features = []
            for i in range(len(corr_matrix.columns)):
                for j in range(i):
                    if abs(corr_matrix.iloc[i, j]) > threshold:
                        column_i = corr_matrix.columns[i]
                        highly_correlated_features.append(column_i)
            highly_correlated_features = list(set(highly_correlated_features))
            mask = np.ones(len(data.columns), dtype=bool)
            for feature in highly_correlated_features:
                mask[data.columns.get_loc(feature)] = False
            result = data.loc[:, mask]
            time_used = time.time() - time_start
            result_obj = {
                "X": result,
                "mask": mask,
                "time_used": time_used,
                "number_of_iterations": 0,
                "number_of_features": sum([1 if item else 0 for item in mask])
            }
            return True, result_obj
        except Exception as e:
            print(
                "Error[in PearsonCorrelationCoefficients.feature_selection]: Feature selection failed: " + str(e))
            return False, None
