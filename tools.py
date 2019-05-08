#! /usr/bin/env python

import pickle
import os
import sys
import argparse
import time
from typing import List

from keylogger import Sample, keylog_session



def sanitize_encoding(filename : str):
    """Clean a record of Samples

    Some encoding issues have been spotted across machines.
    This function solves this problem and reserialized the cleaned
    sequence to a new file.

    At the end of the process, a new file is created, called
    `filename + "_sanitized"` and containing the serialized sanitized
    sequence of samples.
    """

    # Building new filename
    new_filename = filename.split('.')
    new_filename.insert(1, '_sanitized.')
    new_filename = "".join(new_filename)

    samples = get_samples(filename)

    for sample in samples:
        sample.string = sample.string.encode(
                'ISO-8859-1', 'surrogateescape'
            ).decode('utf-8')

    with open(new_filename, "ab+") as file:
        for sample in samples:
            pickle.dump(sample, file, pickle.HIGHEST_PROTOCOL)

def display_file(filename : str, indent : bool = False):
    """Display the serialized samples in a file"""

    samples = get_samples(filename)
    for sample in samples:
        print("{}{}\t{}\t[{}]".format(
            "\t" if indent else "",
            time.strftime(
                "%a, %d %b %Y %H:%M:%S", sample_to_localtime(sample)),
            len(sample),
            "Impostor" if sample.impostor else "Legit")
        )

def get_samples(filename : str) -> List[Sample]:
    """Get the serialized sequence of Samples from a file"""
    samples = []
    with open(filename, 'rb') as file:
        while True:
            try:
                samples.append(pickle.load(file))
            except EOFError:
                break
    return samples

def sample_to_localtime(a_sample : Sample) -> time.struct_time:
    """Find the exact date of a sample"""
    kb_evt = next(iter(a_sample))
    return time.localtime(kb_evt.seconds)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("FILENAME", nargs='+', help='One or multiple file names')
    parser.add_argument("-x", "--exclude", help='A range with the format start,finish for example : 10,30. Dataset values to exclude from provided file')
    parser.add_argument("-d", "--display", help="Displays informations on dataset(s) in provided files", action="store_const", const=True)
    parser.add_argument("-e", "--encoding", help="Clean encoding issues on serialized files", action="store_const", const=True)

    args = vars(parser.parse_args())

    if len(args["FILENAME"]) > 1 and args["exclude"]:
        parser.error("Can only exclude data from single file")
    elif args["exclude"]:
        slice_str = [int(x) for x in args["exclude"].split(',')]

        # myslice can be an index if there is only one bound
        start = slice_str[0]
        if len(slice_str) > 1:
            end = slice_str[1]
            myslice = slice(start, end)
        else :
            myslice = start
        print("Excluding range {}".format(myslice))
        excluded = get_samples(args["FILENAME"][0])[myslice]
        print("Elements excluded : {}".format(excluded))
    elif args["display"]:
        print("Priting file(s) contents of {}".format(args["FILENAME"]))

        files = args["FILENAME"]
        if len(files) > 1 :
            for filename in files:
                print("{} :".format(filename))
                display_file(filename, indent=True)
                print()
        else:
            display_file(files[0])

    elif args["encoding"]:
        print("Cleaning encoding problems on file(s) : {}".format(args["FILENAME"]))
    else:
        parser.error("No operation provided")

if __name__ == '__main__' :
    main()