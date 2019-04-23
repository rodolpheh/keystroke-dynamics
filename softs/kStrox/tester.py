# -*- coding: utf-8 -*-

import sys
import pickle

from keylogger import Sample, keylog_session
from io import StringIO

from SampleParser import SampleParser

from common import get_binary_validation, get_file_list, get_existing_filename


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


def tester():
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
