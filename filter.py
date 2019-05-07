#! /usr/bin/env python

# sequence[0].string.encode('ISO-8859-1', 'surrogateescape').decode('utf-8')
import pickle
import os
import sys
import argparse

def sanitize_encoding(filename : str ):
    print(filename)
    orig_filename = filename
    new_filename = filename.split('.')
    new_filename.insert(1, '_sanitized.')

    new_filename = "".join(new_filename)

    # print("Filename : {} ; new : {}".format(orig_filename, new_filename))
    samples = []

    with open(orig_filename, "rb") as file:
        while True:
            try:
                samples.append(pickle.load(file))
            except EOFError:
                break

    for sample in samples:
        sample.string = sample.string.encode(
                'ISO-8859-1', 'surrogateescape'
            ).decode('utf-8')

    with open(new_filename, "ab+") as file:
        for sample in samples:
            pickle.dump(sample, file, pickle.HIGHEST_PROTOCOL)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("FILENAME", nargs='+', help='One or multiple file names')
    parser.add_argument("-x", "--exclude", help='A range with the format start,finish for example : 10,30. Dataset values to exclude from provided file')
    parser.add_argument("-d", "--display", help="Displays informations on dataset(s) in provided files")
    args = vars(parser.parse_args())

    if len(args["FILENAME"]) > 1 and args["exclude"]:
        parser.error("Can only exclude data from single file")
    elif args["display"]:
        print("Priting file(s) contents of {}".format(args["FILENAME"]))
    else:
        print("Sanitizing files : {}".format(args["FILENAME"]))


if __name__ == '__main__' :
    main()