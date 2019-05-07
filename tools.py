#! /usr/bin/env python

# sequence[0].string.encode('ISO-8859-1', 'surrogateescape').decode('utf-8')
import pickle
import os
import sys
import argparse
import time


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

def display_file(filename):
    samples = get_samples(filename)
    print("{} :".format(filename))
    for sample in samples:
        print("\t{}\t{}\t[{}]".format(time.strftime("%a, %d %b %Y %H:%M:%S", sample_to_localtime(sample)), len(sample),"Impostor" if sample.impostor else "Legit"))
    print()

def get_samples(filename):
    samples = []
    with open(filename, 'rb') as file:
        while True:
            try:
                samples.append(pickle.load(file))
            except EOFError:
                break
    return samples

def sample_to_localtime(a_sample):
    kb_evt = next(iter(a_sample))
    return time.localtime(kb_evt.seconds)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("FILENAME", nargs='+', help='One or multiple file names')
    parser.add_argument("-x", "--exclude", help='A range with the format start,finish for example : 10,30. Dataset values to exclude from provided file')
    parser.add_argument("-d", "--display", help="Displays informations on dataset(s) in provided files", action="store_const", const=True)
    parser.add_argument("-e", "--encoding", help="Clean encoding issues on serialized files", action="store_const", const=True)

    args = vars(parser.parse_args())

    print(args)

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
        for filename in args["FILENAME"]:
            display_file(filename)
    elif args["encoding"]:
        print("Cleaning encoding problems on file(s) : {}".format(args["FILENAME"]))
    else:
        parser.error("No operation provided")

if __name__ == '__main__' :
    main()