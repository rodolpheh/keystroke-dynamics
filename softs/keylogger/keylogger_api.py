from ctypes import *
import sys

# Globally import external library
keylogger = cdll.LoadLibrary("./keylogger.so")

MAX_KBEVTS = 2000

class KbEvt(Structure):
    _fields_ = [
        ("seconds", c_int),
        ("nsec", c_long),
        ("code", c_uint),
        ("state", c_int)
    ]

    def __str__(self):
        return "{:011d}{:09d}:{:03d}:{}".format(self.seconds, self.nsec, self.code, "Release" if (self.state == 0) else "Press")

    def __repr__(self):
        return 'KbEvt: ' + str(self)

class Sample(Structure):
    _fields_ = [
        ("size", c_int),
        ("kb_evts", (KbEvt * MAX_KBEVTS))
    ]

    def __str__(self):
        str_repr = "["
        for i in range(len(self)):
            str_repr += "{},\n".format(self.kb_evts[i])

        str_repr = str_repr[:-2] + "]"
        return str_repr

    def __repr__(self):
        return 'Sample: ' + str(self)

    def __len__(self) -> int:
        return self.size

def char_sequence(sample: Sample) -> str:
    """Returns the character sequence corresponding to a Sample"""
    pass

def keylog_session() -> Sample:
    # Declaring empty sample for memory allocation in Python
    empty_sample = Sample()

    # Call to extern function
    keylogger.keylogSession(byref(empty_sample))
        # Stupid but just to prove that data is in local scope
    collected_sample = empty_sample
    del empty_sample

    return collected_sample

def replay_sample(sample: Sample):
    keylogger.replaySample(byref(sample))