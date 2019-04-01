# -*- coding: utf-8 -*-
# Pip 0563: https://www.python.org/dev/peps/pep-0563/
from __future__ import annotations

from Model import Model

import glob
import os
import pickle
from typing import List

# CLI style imports
from PyInquirer import prompt
from examples import custom_style_2

from Sample import Sample


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

    for raw_sample in sequence:
        sample = raw_sample.timings
        print(sample)


if __name__ == '__main__':
    trainer()
