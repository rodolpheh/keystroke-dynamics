'''
Example with 'thisisatest' (11 chars, 22 events registered)

----  ----  ----  ----  ----  ----  ----  ----  ----  ----  ----
   ----  ----  ----  ----  ----  ----  ----  ----  ----  ----
p  r  p  r  p  r  p  r  p  r  p  r  p  r  p  r  p  r  p  r  p  r
 ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
    ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

n = N / 2

11 pr       n
10 rp       n-1
10 pp       n-1
10 rr       n-1
----------------
41 timings  4n-3
'''


class SampleParser:

    def __init__(self, sample, *args, **kwargs):
        self.sample = sample
        self.pp = []
        self.rr = []
        self.pr = []
        self.rp = []

        for index in range(0, len(self.sample), 2):
            first = self.sample.kb_evts[index]
            prSecond = self.sample.kb_evts[index + 1]
            ppSecond = self.sample.kb_evts[index + 2]

            firstTmg = first.seconds * 1000000 + first.nsec
            prSecondTmg = prSecond.seconds * 1000000 + prSecond.nsec
            ppSecondTmg = ppSecond.seconds * 1000000 + ppSecond.nsec

            prTmg = prSecondTmg - firstTmg
            ppTmg = ppSecondTmg - firstTmg

            self.pr.append(prTmg)
            self.pp.append(ppTmg)
        for index in range(1, len(self.sample), 2):
            first = self.sample.kb_evts[index]
            rpSecond = self.sample.kb_evts[index + 1]
            rrSecond = self.sample.kb_evts[index + 2]

            firstTmg = first.seconds * 1000000 + first.nsec
            rpSecondTmg = rpSecond.seconds * 1000000 + rpSecond.nsec
            rrSecondTmg = rrSecond.seconds * 1000000 + rrSecond.nsec

            rpTmg = rpSecondTmg - firstTmg
            rrTmg = rrSecondTmg - firstTmg

            self.rp.append(rpTmg)
            self.rr.append(rrTmg)

        self.rp = self.rp[:-1]
        self.pp = self.pp[:-1]
        self.rr = self.rr[:-1]

    @property
    def timings(self):
        return self.pr + self.rp + self.pp + self.rr + \
            ([0] if self.sample.impostor else [1]) + \
            [len(self.pr) + len(self.rp) + len(self.pp) + len(self.rr)]
