# sequence[0].string.encode('ISO-8859-1', 'surrogateescape').decode('utf-8')
import pickle
import os


orig_filename = os.path.dirname(os.path.realpath(__file__)) + "/sequence/JeMappelle.smp"
new_filename = os.path.dirname(os.path.realpath(__file__)) + "/sequence/JeMappelle_saved.smp"
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
