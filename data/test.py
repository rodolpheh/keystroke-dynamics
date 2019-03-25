from Model import Model
from Data import Data

import numpy as np

from sklearn.model_selection import ShuffleSplit
from sklearn.model_selection import ParameterGrid
from sklearn.model_selection import GridSearchCV


def getUserData(user: int, data, columns):
    # We select the data of the user
    studiedUserData = data.table.loc[(data.table["user_id"] == user), columns].astype('float')
    # We select the rest of the data. It will be used as outliers.
    otherUsersData = data.table.loc[(data.table["user_id"] != user), columns].astype('float')
    
    return [studiedUserData, otherUsersData]


def customGridSearch(user: int, data, columns):
    studiedUserData, otherUsersData = getUserData(user, data, columns)

    # Use a ShuffleSplit to select 80% of the user's data
    splitter = ShuffleSplit(n_splits=1, train_size=0.5, test_size=None)
    dataOneIndices, dataTwoIndices = list(splitter.split(studiedUserData))[0]

    dataOne = studiedUserData.iloc[dataOneIndices]
    dataTwoPositive = studiedUserData.iloc[dataTwoIndices]

    splitter = ShuffleSplit(n_splits=1, train_size=10, test_size=None)
    trainIndices, testIndices = list(splitter.split(dataOne))[0]

    train = dataOne.iloc[trainIndices]
    test = dataOne.iloc[testIndices]

    grid = {'gamma' : np.logspace(-9, 3, 13),
            'nu' : np.linspace(0.01, 0.99, 99)}

    bestRecall = 0
    bestRecallParameters = None

    for hyperparams in ParameterGrid(grid):
        model = Model(nu=hyperparams["nu"], gamma=hyperparams["gamma"])
        model.fit(train)
        report = Model.evaluate(model, train, test)
        
        if report["recall"] > bestRecall:
            print("'TP': {}, 'FN': {}, 'FNT': {}, 'recall': {}".format(
                report["TP"], report["FN"], report["FNT"], report["recall"]
            ))
            bestRecall = report["recall"]
            bestRecallParameters = {
                "nu": hyperparams["nu"],
                "gamma": hyperparams["gamma"]
            }

    if bestRecallParameters is not None:
        print("Best params : nu = {}, gamma = {}".format(bestRecallParameters["nu"], bestRecallParameters["gamma"]))


def gridSearchCV(user, data, columns):
    studiedUserData, otherUsersData = getUserData(user, data, columns)

    # Use a ShuffleSplit to select 80% of the user's data
    splitter = ShuffleSplit(n_splits=1, train_size=0.8, test_size=None)
    dataOneIndices, dataTwoIndices = list(splitter.split(studiedUserData))[0]

    dataOne = studiedUserData.iloc[dataOneIndices]
    dataTwoPositive = studiedUserData.iloc[dataTwoIndices]

    model = Model()
    gs = GridSearchCV(
        estimator=model,
        param_grid={
            "nu": np.linspace(0.01, 0.99, 99),
            "gamma": np.logspace(-9, 3, 13)
        },
        cv=5,
        iid=False
    )

    gs.fit(dataOne, list([1 for i in range(len(dataOne.index))]))
    shortParams = {
        'gamma': gs.best_params_["gamma"],
        'nu': gs.best_params_["nu"]
    }

    print("Best params : nu = {}, gamma = {}".format(shortParams["nu"], shortParams["gamma"]))

if __name__ == "__main__":
    data = Data()

    columns = ["rrTime" + str(index) for index in range(15)]
    columns.extend(["ppTime" + str(index) for index in range(15)])
    columns.extend(["rpTime" + str(index) for index in range(15)])
    columns.extend(["prTime" + str(index) for index in range(15)])

    studiedUserData, otherUsersData = getUserData(1, data, columns)

    # Use a ShuffleSplit to select 80% of the user's data
    splitter = ShuffleSplit(n_splits=1, train_size=0.8, test_size=None)
    dataOneIndices, dataTwoIndices = list(splitter.split(studiedUserData))[0]

    dataOne = studiedUserData.iloc[dataOneIndices]
    dataTwoPositive = studiedUserData.iloc[dataTwoIndices]

    model = Model()
    params = Model.findParameters(model, dataOne)
    results = Model.report(params["model"], dataOne, dataTwoPositive, otherUsersData)
    print(results)