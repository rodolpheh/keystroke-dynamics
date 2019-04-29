# -*- coding: utf-8 -*-
import pickle

from common import get_binary_validation
from common import get_file_list
from common import get_existing_filename
from common import get_sequence_from_file
from common import print_report
from SampleParser import SampleParser
from Model import Model

from sklearn.model_selection import train_test_split


def evaluator():
    existing_files = get_file_list("model", "mdl")

    if not existing_files:
        print("No models files found. Come back when you have models.")
        exit()

    target_filename = get_existing_filename(existing_files)
    if len(target_filename) == 0:
        print("No files selected, quitting...")
        exit()

    model = None
    print(target_filename)
    with open("model/" + target_filename, 'rb') as file:
        model = pickle.load(file)

    if model is None:
        return

    existing_files = get_file_list("sequence", "smp")

    if not existing_files:
        print("No models files found. Come back when you have samples.")
        return

    target_filenames = get_existing_filename(existing_files, True)
    if len(target_filenames) == 0:
        print("No files selected, quitting...")
        return

    sequence = []
    for target_filename in target_filenames:
        samples = get_sequence_from_file(target_filename)
        sequence.extend(samples)

    timings_sequences = []
    compared_size = None
    print("")

    for raw_sample in sequence:
        parser = SampleParser(raw_sample)
        timings_sequences.append(parser.timings)
        if compared_size is None:
            compared_size = parser.timings[-1]
        else:
            if parser.timings[-1] != compared_size:
                print(
                    "Error, one sample has a different size ({}), removing it"
                    .format(parser.timings[-1])
                )
                del timings_sequences[-1]

    print("{} samples".format(len(timings_sequences)))

    # Build the data
    trueData = [smp[:smp[-1]] for smp in timings_sequences if smp[-2] == 1]
    fakeData = [smp[:smp[-1]] for smp in timings_sequences if smp[-2] == 0]

    # Split for training/optimization and final evaluation
    train, test = train_test_split(trueData, train_size=0.8, test_size=None)

    print("{} samples from user".format(len(trueData)))
    print("{} samples from impostor\n".format(len(fakeData)))

    # Print a final evaluation of the model agains impostors data
    report = Model.report(model, train, test, fakeData)

    print_report(report)


def main():
    is_running = True
    while is_running:
        evaluator()
        again = get_binary_validation(
            "Do you want to test another model ?",
            False
        )
        if not again:
            is_running = False


if __name__ == "__main__":
    main()
