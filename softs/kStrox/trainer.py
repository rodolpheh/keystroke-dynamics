# -*- coding: utf-8 -*-
# Pip 0563: https://www.python.org/dev/peps/pep-0563/
from __future__ import annotations

from Model import Model
from Sample import Sample
from SampleParser import SampleParser

import glob
import os
import pickle
from typing import List

from sklearn.model_selection import train_test_split

# CLI style imports
from PyInquirer import prompt
from examples import custom_style_2
from termgraph.termgraph import chart, AVAILABLE_COLORS as colors
from progress.spinner import PixelSpinner

from threading import Thread, current_thread
from time import sleep


def get_binary_validation(message: str, default: bool = True) -> bool:
    """Validation on a binary alternative"""
    questions = [
        {
            'type': 'confirm',
            'message': message,
            'name': 'confirmed',
            'default': default,
        }
    ]
    return prompt(questions, style=custom_style_2)["confirmed"]


def get_path() -> str:
    """Path of current dir"""
    return os.path.dirname(os.path.realpath(__file__))


def get_sequence_from_file(filename: str) -> List[Sample]:
    """Recover sequence of samples from file"""
    samples = []

    with open(get_path() + "/sequence/" + filename, "rb") as file:
        while True:
            try:
                samples.append(pickle.load(file))
            except EOFError:
                break
    return samples


def get_existing_filename(existing_files: List[str]) -> str:
    """Choose file name from a list of filenames"""

    # Ask user which file only if there are multiple files

    if len(existing_files) == 1:
        return existing_files[0]

    questions = [
        {
            'type': 'checkbox',
            'name': 'target_filenames',
            'message': 'Which file do you want to load ?',
            'choices': existing_files
        }
    ]
    return prompt(questions, style=custom_style_2)["target_filenames"]


def get_file_list() -> List[str]:
    """Get the list of candidate files in `sequence/` dir"""
    filenames = []
    os.makedirs("sequence", exist_ok=True)
    for file in glob.glob("sequence/*.smp"):
        filenames.append({'name': file.replace("sequence/", "")})
    return filenames


def print_report(report):
    print("\n# Metrics\n")
    labels = ['User', 'Impostor']
    data = [
        [report["TP"], report["FN"]],
        [report["TN"], report["FP"]]
    ]
    args = {
        'stacked': True, 'width': 80, 'no_labels': False, 'format': '{:<5.2f}',
        'suffix': '', "vertical": False
    }
    chart(colors=[
        colors['green'],
        colors['red']
        ], data=data, args=args, labels=labels)

    print("\n# Evaluation\n")
    labels = ['Precision', 'Recall', 'F1', 'Accuracy']
    data = [
        [report["precision"] * 100],
        [report["recall"] * 100],
        [report["f1"] * 100],
        [report["accuracy"] * 100]
    ]
    args = {
        'stacked': False, 'width': 50, 'no_labels': False,
        'format': '{:<5.2f}', 'suffix': '', "vertical": False
    }
    chart(colors=[], data=data, args=args, labels=labels)


def trainer():
    print("--=== Welcome to kStrokes model trainer ! ===--\n")

    existing_files = get_file_list()

    if not existing_files:
        print("No samples files found. Come back when you have samples.")
        exit()

    target_filenames = get_existing_filename(existing_files)
    if len(target_filenames) == 0:
        print("No files selected, quitting...")
        exit()

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

    model = Model()

    print("{} samples".format(len(timings_sequences)))

    # Build the data
    trueData = [smp[:smp[-1]] for smp in timings_sequences if smp[-2] == 1]
    fakeData = [smp[:smp[-1]] for smp in timings_sequences if smp[-2] == 0]

    # Split for training/optimization and final evaluation
    train, test = train_test_split(trueData, train_size=0.8, test_size=None)

    print("{} samples from user".format(len(trueData)))
    print("    {:3d} samples for training".format(len(train)))
    print("    {:3d} samples for testing".format(len(test)))
    print("{} samples from impostor\n".format(len(fakeData)))

    spinner = PixelSpinner("Fitting data to the model... ",)
    spinner.start()

    # Create a thread for the spinner
    t = Thread(target=spinner_loop, args=(spinner,))
    t.do_run = True
    t.start()

    # Train and optimize
    params = Model.findParameters(model, train)

    t.do_run = False
    t.join()
    print("")

    # Print a report on the training/optimization phase
    evaluate = Model.evaluate(params["model"], train, test)

    # Print a final evaluation of the model agains impostors data
    report = Model.report(params["model"], train, test, fakeData)

    print_report(report)

    save_model = get_binary_validation(
            "Do you want to keep this model ?", True
        )

    if save_model:
        with open("model/model.mdl", 'wb') as file:
            pickle.dump(params["model"], file, pickle.HIGHEST_PROTOCOL)
            print("Model saved in model/model.mdl")


def spinner_loop(spinner):
    t = current_thread()
    while getattr(t, "do_run", True):
        spinner.next()
        sleep(0.5)


if __name__ == '__main__':
    trainer()
