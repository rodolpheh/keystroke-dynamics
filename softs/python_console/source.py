# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

import sys
from PyInquirer import style_from_dict, Token, prompt, Separator
from io import StringIO
from examples import custom_style_2
import glob, os, datetime, re

from Sample import Sample

# Void, print logo from logo file
def print_logo():
    f = open('logo.txt')
    for line in f:
        print (line, end="")
    f.close()

# Array of string, .smp file names in sequence folder
def get_files_list():
    file_names = []
    os.chdir("sequence/")
    for file in glob.glob("*.smp"):
        file_names.append(file)
    return file_names

# Boolean, True = confirmed
def get_validation(message, default = True):
    questions = [
        {
            'type': 'confirm',
            'message': message,
            'name': 'confirmed',
            'default': default,
        }
    ]
    return prompt(questions, style=custom_style_2)["confirmed"]

# String, file name chosen from list
def get_existing_file_name(existing_files):
    questions = [
        {
            'type': 'list',
            'name': 'target_file_name',
            'message': 'Which file do you want to load ?',
            'choices': existing_files
        }
    ]
    return prompt(questions, style=custom_style_2)["target_file_name"]

# String, default file name based on date and time
def get_default_file_name():
    return datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# String, full file name chosen by user
def get_custom_file_name(existing_files):
    questions = [
        {
            'type': 'input',
            'name': 'custom_file_name',
            'message': 'Name your new sample :',
            'default': get_default_file_name(),
            'validate': lambda text: (len(re.findall(r'^[A-Za-z0-9_\-.]{3,40}$', text)) > 0 and text+'.smp' not in existing_files) or 'Typed file name contains illegal characters or already exist'
        }
    ]
    return prompt(questions, style=custom_style_2)['custom_file_name']+'.smp'

# String, introduction information
def get_intro_message():
    return "\nYou are about to begin a new record.\nType the text sample you want to record.\nFor now, this sample will be displayed as is so avoid secrets like passwords."

# Sample, sample provided by C program
def get_single_sample():
    ##### Todo replace by true get input
    print("\tRecording... ", end=" : ")
    orig_out = sys.stdout
    sys.stdout = StringIO()
    user_entry = Sample(input("").replace("\n", ""))
    sys.stdout = orig_out
    ##### Todo end
    return user_entry

# Sequence (array of samples), first input
def get_first_input():
    print(get_intro_message())
    user_satisfied = False
    user_entry = False
    while not user_satisfied:
        user_entry = get_single_sample()
        print(user_entry.get_string_value())

        user_satisfied = get_validation("Do you want to keep this sample ?", True)

    return user_entry

# Sequence, (array of samples)
def capture_n_sequence(sequence):
    output = []
    reference = sequence[0].get_string_value()
    while True:
        local_sample = get_single_sample()
        if local_sample.get_string_value() == reference:
            output.append(local_sample)
            print(local_sample.get_string_value())
        else:
            if local_sample.get_string_value() == "":
                print(">> END")
                break
            else:
                print(local_sample.get_string_value()+" mismatch the reference: "+reference)
    return output

# String, path to current dir
def get_path():
    return os.path.dirname(os.path.realpath(__file__)).replace("/sequence", "")

# Array of samples, representing existing sequence content
def get_sequence_from_file(file_name):
    # TODO replace by true loader function
    samples = []
    f = open(get_path()+"/sequence/"+file_name, "r")
    for line in f:
        samples.append(Sample(line.replace("\n", "")))
    f.close()
    return samples
    # TODO end

# Void
def save_to_file(file_name, sequence):
    # TODO replace by true saver finction
    f = open(get_path()+"/sequence/"+file_name, "a+")
    for sample in sequence:
        f.write(sample.get_string_value()+"\n")
    f.close()


#### == program start == ####

print_logo()
print("--=== Welcome to kStrokes sequence manager ! ===--\n")

# Get list of files in samples folder
existingFiles = get_files_list()

# If a file exist then ask user if he want to use an existing file
if len(existingFiles) > 0:
    useExistingFile = get_validation("Do you want to use an existing sequence (file) ?", False)
else:
    useExistingFile = False

# Choose/define a file name
if useExistingFile:
    # Ask user to choose existing one
    targetFileName = get_existing_file_name(existingFiles)
    theSequence = get_sequence_from_file(targetFileName)
    print("\tSequence loaded, reference sample is: '"+theSequence[0].get_string_value()+"'")
else:
    # Ask user for a new one
    targetFileName = get_custom_file_name(existingFiles)
    # Start sequence container with the first sample
    theSequence = [get_first_input()]
    print("\tThe first sequence has been successfully recorded !")


while True:
    if not get_validation(str(len(theSequence)) + " sample(s) in this sequence. Do you want to add another sample ?", True):
        break
    theSequence = theSequence + capture_n_sequence(theSequence)

print("Saving sequence... ", end="")
save_to_file(targetFileName, theSequence)
print("saved!")