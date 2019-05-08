#! /usr/bin/env python

import pickle
import os
import sys
import argparse
import time
from typing import List

from keylogger import Sample, keylog_session

def sanitize_encoding(filename : str) -> List[Sample]:
    """Clean a record of Samples"""

    samples = get_samples(filename)

    for sample in samples:
        sample.string = sample.string.encode(
                'ISO-8859-1', 'surrogateescape'
            ).decode('utf-8')

    return samples

def display_file(
    filename : str,
    custom_slice : slice = slice(None),
    indent : bool = False
    ):
    """Display the serialized samples in a file"""

    samples = get_samples(filename)
    print("custom_slice : {}".format(custom_slice))
    print("Custom start : {}".format(custom_slice.start))
    i = custom_slice.start if custom_slice.start else 0
    for sample in samples[custom_slice]:
        print("{}[{:3d}]\t{}\t{}\t{}".format(
            "\t" if indent else "",
            i,
            time.strftime(
                "%a, %d %b %Y %H:%M:%S", sample_to_localtime(sample)),
            len(sample),
            "Impostor" if sample.impostor else "Legit")
        )
        i += (custom_slice.step if custom_slice.step else 1)

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

def save_to_file(samples : List[Sample], filename : str):
    with open(filename, "ab+") as file:
        for sample in samples:
            pickle.dump(sample, file, pickle.HIGHEST_PROTOCOL)

def sanitize_flag(filename : str):
    """Manage the `-e` option
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
    save_to_file(sanitize_encoding(filename), new_filename )

def extract_flag(filename : str, a_slice_args, dest : str = None):

    try:
        slice_str = [int(x) for x in a_slice_args.split(',')]
    except:
        raise Exception("Incorrect range format")

    # Building the slice object
    start = slice_str[0]
    if len(slice_str) > 1:
        end = slice_str[1]
        if start >= end:
            raise Exception(
                "Incorrect range value : [{}:{}]".format(start, end))
        else: myslice = slice(start, end)
    else :
        myslice = slice(start, start+1)

    if dest:
        orig_samples = get_samples(filename)
        save_to_file(orig_samples[myslice], dest[0])
    else:
        display_file(filename, myslice)


def define_args(parser):
    parser.add_argument(
        "FILENAME",
        nargs='+',
        help='One or multiple file names')
    parser.add_argument(
        "-x",
        "--extract",
        help='A range with the format start,finish for example : 10,30. '
        'Dataset values to extract from provided file'
        )
    parser.add_argument(
        "-d",
        "--display",
        help="DisplaExcludingys informations on dataset(s) in provided files",
        action="store_const",
        const=True
        )
    parser.add_argument(
        "-e",
        "--encoding",
        help="Clean encoding issues on serialized files",
        action="store_const",
        const=True
        )
    parser.add_argument(
        "-o",
        "--output-file",
        nargs=1
    )

def check_args(parser):

    args = vars(parser.parse_args())

    if args["output_file"] and os.path.isfile(args["output_file"][0]):
        parser.error("Cannot export to already existing file, "
        "please implement --append")

    if len(args["FILENAME"]) > 1 and args["extract"]:
        parser.error("Can only extract data from single file")
    elif args["extract"]:
        try :
            extract_flag(
                args["FILENAME"][0],
                args["extract"],
                args["output_file"]
            )
        except Exception as e:
            parser.error(str(e))

    elif args["display"]:
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

def main():
    parser = argparse.ArgumentParser()

    define_args(parser)

    check_args(parser)


if __name__ == '__main__' :
    main()