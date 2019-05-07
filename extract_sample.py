import pickle
import os
import time

def sample_to_date(a_sample):
    kb_evt = next(iter(a_sample))
    return time.localtime(kb_evt.seconds)

orig_filename = os.path.dirname(os.path.realpath(__file__)) + "/sequence/jemappelle_saved.smp"

samples = []

with open(orig_filename, "rb") as file:
    while True:
        try:
            samples.append(pickle.load(file))
        except EOFError:
            break

print('{} samples'.format(len(samples)))

dates = [sample_to_date(sample) for sample in samples]

for date in dates[159:]:
    print(time.strftime("%a, %d %b %Y %H:%M:%S +0000", date))

for date in dates[140:159]:
    print(time.strftime("%a, %d %b %Y %H:%M:%S +0000", date))


with open('sequence/jemappelle_sans_lucile.smp', 'wb') as f:
    for sample in samples[:159]:
        pickle.dump(sample, f, pickle.HIGHEST_PROTOCOL)

with open('sequence/jemappelle_lucile.smp', 'wb') as f:
    for sample in samples[159:]:
        pickle.dump(sample, f, pickle.HIGHEST_PROTOCOL)
