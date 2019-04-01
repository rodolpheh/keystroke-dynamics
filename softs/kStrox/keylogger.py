from ctypes import byref, cdll
from Sample import Sample

# Globally import external library
keylogger = cdll.LoadLibrary("./keylogger_dll.so")


def keylog_session() -> Sample:
    """Capture a Sample from keyboard events

    End the capture by pressing the Enter key
    """
    # Declaring empty sample for memory allocation in Python
    empty_sample = Sample()

    # Call to extern function
    keylogger.keylogSession(byref(empty_sample))
    # Stupid but just to prove that data is in local scope
    collected_sample = empty_sample
    del empty_sample

    return collected_sample


def replay_sample(sample: Sample):
    """Replays a given Sample

    Keyboard input events are written in the keyboard event file
    """

    # Call to extern function
    keylogger.replaySample(byref(sample))
