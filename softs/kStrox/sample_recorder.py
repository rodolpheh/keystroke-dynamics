# -*- coding: utf-8 -*-

import datetime
import glob
import os
import pickle
import re
import sys
from io import StringIO
from typing import List

# CLI style imports
from PyInquirer import prompt
from examples import custom_style_2
# Custom C library wrapped
from keylogger import Sample, keylog_session

def print_logo():
    """Displays the text logo as the program starts"""
    with open('logo.txt', 'r') as file:
        for line in file:
            print(line)

def get_intro_message() -> str:
    """Holds a message for the beginning of a new sequence"""
    return """You are about to begin a new record.
Type the text sample you want to record.
This first sample MUST be typed by the real user (no impostor data)."""

def get_file_list() -> List[str]:
    """Get the list of candidate files in `sequence/` dir"""
    filenames = []
    os.makedirs("sequence", exist_ok=True)
    for file in glob.glob("sequence/*.smp"):
        filenames.append(file.replace("sequence/", ""))
    return filenames

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

def get_existing_filename(existing_files: List[str]) -> str:
    """Choose file name from a list of filenames"""

    # Ask user which file only if there are multiple files

    if len(existing_files) == 1:
        return existing_files[0]

    questions = [
        {
            'type': 'list',
            'name': 'target_filename',
            'message': 'Which file do you want to load ?',
            'choices': existing_files
        }
    ]
    return prompt(questions, style=custom_style_2)["target_filename"]

def get_default_filename() -> str:
    """Generate default filename based on timestamp"""
    return datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

def get_custom_filename(existing_files: List[str]) -> str:
    """Prompt user for new filename"""
    questions = [
        {
            'type': 'input',
            'name': 'custom_filename',
            'message': 'Name your new sample :',
            'default': get_default_filename(),
            'validate': lambda text: (
                (len(re.findall(r'^[A-Za-z0-9_\-.]{3,40}$', text)) > 0
                 and text+'.smp' not in existing_files
                ) or
                'Typed file name contains illegal characters or already exist'
            )
        }
    ]
    return prompt(questions, style=custom_style_2)['custom_filename']+'.smp'

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

def get_first_sample() -> Sample:
    """Record the first sample of a file"""
    print(get_intro_message())

    user_satisfied = False
    while not user_satisfied:
        sample = get_single_sample()

        print("Sample recorded : \"" + sample.string + "\"")
        user_satisfied = get_binary_validation(
            "Do you want to keep this sample ?", True
        )

    sample.impostor = False

    return sample

def get_n_samples(reference: str) -> List[Sample]:
    """Record multiple samples sequentially"""
    output = []

    is_impostor = get_binary_validation("Are you an impostor ?", False)
    while True:
        local_sample = get_single_sample()
        local_sample.impostor = is_impostor
        if local_sample.string == reference:
            output.append(local_sample)
        else:
            if local_sample.string == "":
                print(">> END")
                break
            else:
                print(
                    "\"" +
                    local_sample.string +
                    "\" mismatches the reference: " +
                    reference
                )
    return output

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

def save_to_file(filename: str, sequence: List[Sample]):
    """Save a sequence of Sample to a file"""

    with open(get_path() + "/sequence/" + filename, "ab+") as file:
        for sample in sequence:
            pickle.dump(sample, file, pickle.HIGHEST_PROTOCOL)

def sample_recorder():
    """Main program"""
    print_logo()
    print("--=== Welcome to kStrokes sequence manager ! ===--\n")

    init_seq_size = 0

    # Get list of files in `sequence/` directory
    existing_files = get_file_list()

    # If a file exist then ask user if he wants to use an existing file
    if existing_files:
        use_existing_file = get_binary_validation(
            "Do you want to use an existing sequence (file) ?", False
        )
    else:
        use_existing_file = False

    # Choose/define a file name
    if use_existing_file:
        target_filename = get_existing_filename(existing_files)
        sequence = get_sequence_from_file(target_filename)
        print(
            "\tSequence loaded, reference sample is: '"+sequence[0].string+"'")
        init_seq_size = len(sequence)
    else:
        # Ask user for a new one
        target_filename = get_custom_filename(existing_files)
        # Start sequence container with the first sample
        sequence = [get_first_sample()]
        print("\tThe first sequence has been successfully recorded !")

    while True:
        if not get_binary_validation(
                (str(len(sequence)) +
                 " sample(s) in this sequence." +
                 " Do you want to add another sample ?"),
                True
        ):
            break
        sequence = sequence + get_n_samples(sequence[0].string)

    # Append only new part of sequence to file
    print("Saving sequence... ", end="")
    save_to_file(target_filename, sequence[init_seq_size:])
    print("saved!")

#### == program start == ####
if __name__ == '__main__':
    sample_recorder()