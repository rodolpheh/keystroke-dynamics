import pandas as pd
import numpy as np

class ResultTable:

    def __init__(self, *args, **kwargs):
        self.columns = ["User","TP", "TN", "FP", "FN", "Best f1", "Accuracy", "Precision", "Recall", "Gamma", "Nu", "Grade"]
        self.table = pd.DataFrame(columns=self.columns)

    def append(self, user, TP, TN, FP, FN, f1, accuracy, precision, recall, gamma, nu):
        self.table.loc[self.table.size] = [
            user, TP, TN, FP, FN, f1, accuracy, precision, recall, gamma, nu, (f1 + recall) / 2
        ]
        self.format()

    def appendResults(self, user, results, parameters):
        self.append(
            user,
            results["TP"],
            results["TN"],
            results["FP"],
            results["FN"],
            results["f1"],
            results["accuracy"],
            results["recall"],
            results["precision"],
            parameters["gamma"],
            parameters["nu"]
        )

    def format(self):
        self.table["User"] = self.table["User"].astype(np.int32)
        self.table["TP"] = self.table["TP"].astype(np.int32)
        self.table["TN"] = self.table["TN"].astype(np.int32)
        self.table["FP"] = self.table["FP"].astype(np.int32)
        self.table["FN"] = self.table["FN"].astype(np.int32)

    def __repr__(self):
        return self.table.__repr__()

    def _repr_html_(self):
        return self.table._repr_html_()

