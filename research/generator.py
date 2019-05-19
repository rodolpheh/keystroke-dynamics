import sys
from Data import Data
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.base import clone
import csv
import copy
sys.path.append("..")
from Model import Model

def getUserData(userId, data, columns):
    # We select the data of the user
    studiedUserData = data.table.loc[(data.table["user_id"] == userId), columns].astype('float')
    # We select the rest of the data. It will be used as outliers.
    otherUsersData = data.table.loc[(data.table["user_id"] != userId), columns].astype('float')

    return [studiedUserData, otherUsersData]


if __name__ == "__main__":
    data = Data()
    samples = data.getSamples()
    targets = data.getTargets()

    minimum = np.array(samples, dtype=np.float64).min(axis=0).min(axis=0)
    maximum = np.array(samples, dtype=np.float64).max(axis=0).max(axis=0)

    print("Maximum: " + str(maximum))
    print("Minimum: " + str(minimum))

    uniques = np.array(data.usersCounts)
    users = uniques[uniques[:, 1] >= 30]

    columns = ["rrTime" + str(index) for index in range(15)]
    columns.extend(["ppTime" + str(index) for index in range(15)])
    columns.extend(["rpTime" + str(index) for index in range(15)])
    columns.extend(["prTime" + str(index) for index in range(15)])

    reports = []

    for user in users:
        studiedUserData, otherUsersData = getUserData(user[0], data, columns)
        print("{} - {}".format(user[0], studiedUserData.shape))

        temp_params = None
        temp_evaluate = {"recall": 0}
        for i in range(4):
            model = Model()

            # Split for training/optimization and final evaluation
            train, test = train_test_split(studiedUserData, train_size=0.8, test_size=None)

            # Train and optimize
            params = Model.findParameters(model, train)

            # Print a report on the training/optimization phase
            evaluate = Model.evaluate(params["model"], train, test)
            print(evaluate)

            if evaluate["recall"] > temp_evaluate["recall"]:
                print("Found a better model !")
                temp_params = Model.copyParameters(params)
                temp_evaluate = copy.deepcopy(evaluate)

        params = Model.copyParameters(temp_params)
        evaluate = copy.deepcopy(temp_evaluate)

        # Print a final evaluation of the model agains impostors data
        report = Model.report(params["model"], train, test, otherUsersData)

        report["userId"] = user[0]
        report["TD"] = len(studiedUserData)
        report["FD"] = len(otherUsersData)
        report["eval_TP"] = evaluate["TP"]
        report["eval_FN"] = evaluate["FN"]
        report["eval_FNT"] = evaluate["FNT"]
        report["eval_recall"] = evaluate["recall"]
        report["gamma"] = params["gamma"]
        report["nu"] = params["nu"]
        del report['clf']
        print(report)
        reports.append(report)

    with open('dump2.csv', 'w') as file:
        dump = csv.DictWriter(file, delimiter=';', fieldnames=[
            "userId",
            "gamma",
            "nu",
            "TD",
            "FD",
            "eval_TP",
            "eval_FN",
            "eval_FNT",
            "eval_recall",
            "TP",
            "TN",
            "FP",
            "FN",
            "FNT",
            "precision",
            "recall",
            "accuracy",
            "f1"
        ])

        dump.writeheader()
        for report in reports:
            dump.writerow(report)
