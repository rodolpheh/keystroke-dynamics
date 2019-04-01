from ctypes import Structure, c_int, c_long, c_uint

MAX_KBEVTS = 2000


class KbEvt(Structure):
    """Representation of a single keyboard event from device input
    """
    _fields_ = [
        ("seconds", c_int),
        ("nsec", c_long),
        ("code", c_uint),
        ("state", c_int)
    ]

    def __str__(self):
        return "{:011d}{:09d}:{:03d}:{}".format(
            self.seconds,
            self.nsec,
            self.code,
            "Release" if (self.state == 0) else "Press"
        )

    def __repr__(self):
        return 'KbEvt: ' + str(self)


class Sample(Structure):
    """Representation of an array of KbEvt

    Max size of Sample = 2000 defined by external library

    Is iterable.
    """
    _fields_ = [
        ("size", c_int),
        ("kb_evts", (KbEvt * MAX_KBEVTS))
    ]

    def __init__(self):
        # Internal property for iterator state
        self.current_pos = 0

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

    def __iter__(self):
        for i in range(len(self)):
            yield self.kb_evts[i]

    @property
    def string(self):
        return self._string

    @string.setter
    def string(self, value):
        self._string = value

    @property
    def impostor(self):
        return self._impostor

    @impostor.setter
    def impostor(self, is_impostor: bool):
        self._impostor = is_impostor

    @property
    def timings(self):
        for event in self:
            pass
