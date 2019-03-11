from ctypes import *

class KbEvt(Structure):
    _fields_ = [("seconds", c_int),("nsec", c_long), ("code", c_uint), ("state", c_int)]

class Sample(Structure):
    _fields_ = [("sampleSize", c_int),("kbEvts", POINTER(KbEvt))]

if __name__ == "__main__":
    print("Start sample collecting program")

    keylogger = cdll.LoadLibrary("./keylogger.so")

    myEmptySample = Sample()

    keylogger.keylogSession(byref(myEmptySample));

    for i in range(myEmptySample.sampleSize):
        print("{};{};{};{}".format(
            myEmptySample.kbEvts[i].seconds,
            myEmptySample.kbEvts[i].nsec,
            myEmptySample.kbEvts[i].code,
            myEmptySample.kbEvts[i].state
            )
        )