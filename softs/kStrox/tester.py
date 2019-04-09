# -*- coding: utf-8 -*-

from typing import List

# CLI style imports
from PyInquirer import prompt
from examples import custom_style_2

import glob
import os
import sys
import pickle

from keylogger import Sample, keylog_session
from io import StringIO

from SampleParser import SampleParser


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


def get_single_sample() -> Sample:
    """Record a single sample"""
    print("Recording ... : ", end="")
    sys.stdout.flush()

    # Mute stdout while recording events to avoid double output
    orig_out = sys.stdout
    sys.stdout = StringIO()

    # Recording key events
    sample = keylog_session()

    # After recording, restore stdout
    sys.stdout = orig_out

    str_pw = input()
    sample.string = str_pw

    return sample


def get_file_list() -> List[str]:
    """Get the list of candidate files in `sequence/` dir"""
    filenames = []
    os.makedirs("sequence", exist_ok=True)
    for file in glob.glob("model/*.mdl"):
        filenames.append({'name': file.replace("model/", "")})
    return filenames


def get_existing_filename(existing_files: List[str]) -> str:
    """Choose file name from a list of filenames"""

    # Ask user which file only if there are multiple files

    if len(existing_files) == 1:
        return existing_files[0]["name"]

    questions = [
        {
            'type': 'list',
            'name': 'target_filename',
            'message': 'Which file do you want to load ?',
            'choices': existing_files
        }
    ]
    return prompt(questions, style=custom_style_2)["target_filename"]


def tester():
    existing_files = get_file_list()

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

    is_running = True

    while is_running:
        raw_sample = get_single_sample()
        raw_sample.impostor = True
        parser = SampleParser(raw_sample)
        timings = parser.timings
        timings = timings[:timings[-1]]
        try:
            results = model.pipeline.predict([timings])
            if results[0] == -1:
                print('''\u001b[38;5;196m
 █████▒▄▄▄       ██▓ ██▓    ▓█████ ▓█████▄
▓██   ▒▒████▄    ▓██▒▓██▒    ▓█   ▀ ▒██▀ ██▌
▒████ ░▒██  ▀█▄  ▒██▒▒██░    ▒███   ░██   █▌
░▓█▒  ░░██▄▄▄▄██ ░██░▒██░    ▒▓█  ▄ ░▓█▄   ▌
░▒█░    ▓█   ▓██▒░██░░██████▒░▒████▒░▒████▓
 ▒ ░    ▒▒   ▓▒█░░▓  ░ ▒░▓  ░░░ ▒░ ░ ▒▒▓  ▒
 ░       ▒   ▒▒ ░ ▒ ░░ ░ ▒  ░ ░ ░  ░ ░ ▒  ▒
 ░ ░     ░   ▒    ▒ ░  ░ ░      ░    ░ ░  ░
             ░  ░ ░      ░  ░   ░  ░   ░
                                     ░
                \u001b[0m''')
            else:
                print('''\u001b[38;5;76m
███████╗██╗   ██╗ ██████╗ ██████╗███████╗███████╗███████╗
██╔════╝██║   ██║██╔════╝██╔════╝██╔════╝██╔════╝██╔════╝
███████╗██║   ██║██║     ██║     █████╗  ███████╗███████╗
╚════██║██║   ██║██║     ██║     ██╔══╝  ╚════██║╚════██║
███████║╚██████╔╝╚██████╗╚██████╗███████╗███████║███████║
╚══════╝ ╚═════╝  ╚═════╝ ╚═════╝╚══════╝╚══════╝╚══════╝
                \u001b[0m''')
            again = get_binary_validation("Do you want to try again ?", False)
            if not again:
                is_running = False
        except ValueError:
            print("It seems that you made a mistake, try again")
            continue


def main():
    is_running = True
    while is_running:
        tester()
        again = get_binary_validation(
            "Do you want to test another model ?",
            False
        )
        if not again:
            is_running = False


if __name__ == "__main__":
    main()
