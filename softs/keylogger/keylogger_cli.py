from ctypes import *
import sys

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

if __name__ == "__main__":

    print("Start sample collecting program")

    keylogger = cdll.LoadLibrary("./keylogger.so")

    # Declaring empty sample for memory allocation in Python
    empty_sample = Sample()

    # Call to extern function
    keylogger.keylogSession(byref(empty_sample))

    # Stupid but just to prove that data is in local scope
    collected_sample = empty_sample
    del empty_sample

    print(collected_sample)

    # Loop to replay evts with the help of the library
    # Empty stdin from previous keystrokes
    input();
    res = "rubbishplaceholder"
    while(res[-1] is not "n"):
        res = input("Do you want to replay ? [y/n]")

        while(res[-1] is not "y" and res[-1] is not "n"):
            res = input(
                "It is a yes or no question really... "
                + "Do you want to replay ? [y/n]"
            )

        if (res[-1] is "y"):
            keylogger.replaySample(byref(collected_sample))
            # Add newline char
            print("")

    print("Exiting program")