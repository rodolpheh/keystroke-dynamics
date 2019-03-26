from Model import Model
from sklearn.model_selection import train_test_split

"""
According to:

Eude, T & Chang, Chuan. (2017).
One-class SVM for biometric authentication by keystroke dynamics for remote evaluation.
Computational Intelligence. 34. 10.1111/coin.12122.

The model can be trained and optimized by using only positive data.
It also shows a way to evaluate the final classifier against impostors data.

The user data should be split into a ratio of 0.8 for training/parameters
optimization and 0.2 for the final evaluation. In a use case where the user
won't need to evaluate the final model, we can use the whole data.
"""


def getUserData():
    # Just a placeholder
    return [[0, 1, 2], [1, 2, 0], [1, 1, 2], [1, 0, 0], [0, 1, 0], [1, 2, 2], [2, 1, 2], [0, 2, 0]]

def getImpostorData():
    # Just a placeholder
    return [[1, 3, 2], [1, -1, 0]]

if __name__ == "__main__":
    # Create the model
    model = Model()

    # Build the data
    samples = getUserData()

    # Split for training/optimization and final evaluation
    train, test = train_test_split(samples, train_size=0.8, test_size=None)

    # Get impostors data for the final evaluation
    impostors = getImpostorData()

    # Train and optimize
    params = Model.findParameters(model, train)

    # Print a report on the training/optimization phase
    evaluate = Model.evaluate(params["model"], train, test)
    print(evaluate)

    # Print a final evaluation of the model agains impostors data
    report = Model.report(params["model"], train, test, impostors)
    print(report)