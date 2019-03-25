# Pip 0563: https://www.python.org/dev/peps/pep-0563/
from __future__ import annotations

# Pip 484 : typing
from typing import Dict

# Do the math ! Do the math !
import pandas as pd
import numpy as np

# Every scikit-learn import
from sklearn.svm import OneClassSVM
from sklearn.preprocessing import MinMaxScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import make_scorer
from sklearn.base import BaseEstimator
from sklearn.utils.validation import check_X_y, check_array, check_is_fitted
from sklearn.model_selection import GridSearchCV

from Data import Data
from ResultTable import ResultTable


class Model(BaseEstimator):

    def __init__(self, nu: float = 0.01, gamma: float = 0.01) -> None:
        self.nu = nu
        self.gamma = gamma


    def makePipeline(self) -> None:
        # Create the scaler and the OneClassSVM
        self._scaler = MinMaxScaler((0, 1))
        self._classifier = OneClassSVM(kernel="rbf", nu=self.nu, gamma=self.gamma)

        # Create the pipeline
        self._pipeline = Pipeline([('scaler', self.scaler), ('classifier', self.classifier)])

        # Create a scorer function
        self._scorer = make_scorer(self.score, greater_is_better=True)


    @property
    def scaler(self) -> MinMaxScaler:
        return self._scaler

    
    @property
    def classifier(self) -> OneClassSVM:
        return self._classifier


    @property
    def pipeline(self) -> Pipeline:
        try:
            return self._pipeline
        except AttributeError:
            self.makePipeline()
            return self._pipeline


    def fit(self, X: np.array, y: np.array = None) -> Model:

        # Check data
        #X, y = check_X_y(X, y)

        # Fit the pipeline
        self.pipeline.fit(X)

        # Mandatory filling and return
        self.is_fitted_ = True
        self.X_ = X
        self.y_ = y

        return self


    def predict(self, X: np.array):
        # Check is fit had been called
        check_is_fitted(self, ['X_', 'y_'])
        # Input validation
        X = check_array(X)

        return self.pipeline.predict(X)


    def score(self, X: np.array, y: np.array = None) -> float:
        y = self.predict(X)
        TP = y[y == 1].size
        FN = y[y == -1].size
        return TP / (TP + FN)

    
    @staticmethod
    def evaluate(pipeline: Pipeline, train: np.array, test: np.array) -> Dict[str, float]:
        # Predict on all data
        y_pred_test = pipeline.predict(test)
        
        TP = y_pred_test[y_pred_test == 1].size
        FN = y_pred_test[y_pred_test == -1].size
    
        return {
            "TP": TP,
            "FN": FN,
            "FNT": y_pred_train[y_pred_train == -1].size,
            "recall": TP / (TP + FN),
            "clf": pipeline
        }
    
    
    @staticmethod
    def report(pipeline: Pipeline, train: np.array, test: np.array, outliers: np.array):
        
        # Predict on all data
        y_pred_train = pipeline.predict(train)
        y_pred_test = pipeline.predict(test)
        y_pred_outliers = pipeline.predict(outliers)
        
        TP = y_pred_test[y_pred_test == 1].size
        TN = y_pred_outliers[y_pred_outliers == -1].size
        FP = y_pred_outliers[y_pred_outliers == 1].size
        FN = y_pred_test[y_pred_test == -1].size
        
        return {
            "TP": TP,
            "TN": TN,
            "FP": FP,
            "FN": FN,
            "FNT": y_pred_train[y_pred_train == -1].size,
            "precision": TP / (TP + FP + 0.0001),
            "recall": TP / (TP + FN),
            "accuracy": (TP + TN) / (TP + TN + FP + FN),
            "f1": (2 * TP) / (2 * TP + FP + FN),
            "clf": pipeline
        }

    
    @staticmethod
    def findParameters(pipeline: Pipeline, X: np.array, y: np.array = None, returnModel: bool = True):
        returned = {}
        gs = GridSearchCV(
            estimator=pipeline,
            param_grid={
                "nu": np.linspace(0.01, 0.99, 99),
                "gamma": np.logspace(-9, 3, 13)
            },
            cv=5,
            iid=False
        )
        gs.fit(X, y)
        returned["nu"] = gs.best_params_["nu"]
        returned["gamma"] = gs.best_params_["gamma"]
        if returnModel:
            returned["model"] = gs.best_estimator_
        return returned


if __name__ == "__main__":
    from sklearn.utils.estimator_checks import check_estimator
    check_estimator(Model)