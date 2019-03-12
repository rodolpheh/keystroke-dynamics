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

class Sample(Structure):
    _fields_ = [
        ("sampleSize", c_int),
        ("kbEvts", (KbEvt * MAX_KBEVTS))
    ]

if __name__ == "__main__":
    print("Start sample collecting program")

    keylogger = cdll.LoadLibrary("./keylogger.so")

    # Declaring empty sample for memory allocation in Python
    myEmptySample = Sample()

    # Call to extern function
    keylogger.keylogSession(byref(myEmptySample));
    print("Recovered sample size : {}".format(myEmptySample.sampleSize))

    for i in range(myEmptySample.sampleSize):
        print("{};{};{};{}".format(
            myEmptySample.kbEvts[i].seconds,
            myEmptySample.kbEvts[i].nsec,
            myEmptySample.kbEvts[i].code,
            myEmptySample.kbEvts[i].state
            )
        )

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
            keylogger.replaySample(byref(myEmptySample))
            # Add newline char
            print("")

    print("Exiting program")