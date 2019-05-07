# -*- coding: utf-8 -*-

from Model import Model
from SampleParser import SampleParser

import glob
import os
import pickle
from typing import List
import datetime
import re

from sklearn.model_selection import train_test_split

# CLI style imports
from PyInquirer import prompt
from examples import custom_style_2
from progress.spinner import PixelSpinner

from threading import Thread, current_thread
from time import sleep

from common import get_binary_validation
from common import print_report
from common import get_existing_filename
from common import get_sequence_from_file


def get_custom_filename(existing_files: List[str]) -> str:
    """Prompt user for new filename"""
    questions = [
        {
            'type': 'input',
            'name': 'custom_filename',
            'message': 'Name your model :',
            'default': get_default_filename(),
            'validate': lambda text: (
                (len(re.findall(r'^[A-Za-z0-9_\-.]{3,40}$', text)) > 0
                 and text+'.smp' not in existing_files) or
                'Typed file name contains illegal characters or already exist'
            )
        }
    ]
    return prompt(questions, style=custom_style_2)['custom_filename']+'.mdl'


def get_default_filename() -> str:
    """Generate default filename based on timestamp"""
    return datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


def get_file_list() -> List[str]:
    """Get the list of candidate files in `sequence/` dir"""
    filenames = []
    os.makedirs("sequence", exist_ok=True)
    for file in glob.glob("sequence/*.smp"):
        filenames.append({'name': file.replace("sequence/", "")})
    return filenames


def trainer():
    existing_files = get_file_list()

    if not existing_files:
        print("No samples files found. Come back when you have samples.")
        exit()

    target_filenames = get_existing_filename(existing_files, True)
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
    # evaluate = Model.evaluate(params["model"], train, test)

    # Print a final evaluation of the model agains impostors data
    report = Model.report(params["model"], train, test, fakeData)

    print_report(report)

    save_model = get_binary_validation(
            "Do you want to keep this model ?", True
        )

    if save_model:
        filename = get_custom_filename(target_filenames)
        os.makedirs("model", exist_ok=True)
        with open("model/" + filename, 'wb') as file:
            pickle.dump(params["model"], file, pickle.HIGHEST_PROTOCOL)
            print("Model saved in model/" + filename)


def spinner_loop(spinner):
    t = current_thread()
    while getattr(t, "do_run", True):
        spinner.next()
        sleep(0.5)


def main():
    is_running = True
    while is_running:
        trainer()
        again = get_binary_validation(
            "Do you want to train another model ?",
            False
        )
        if not again:
            is_running = False


if __name__ == '__main__':
    main()
