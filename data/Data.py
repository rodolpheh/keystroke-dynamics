import sqlite3
import numpy as np


class Data(object):
    """docstring for Data."""
    def __init__(self):
        super(Data, self).__init__()

        self.samples = []
        self.targets = []
        self.description = "A database of keystrokes"
        self.headers = []
        self.headersMask = []
        self.rrTime = True
        self.ppTime = False
        self.rpTime = False
        self.prTime = False

        self.computeHeadersMask()
        self.retrieveData()

    def retrieveData(self):
        conn = sqlite3.connect("./keystroke.db")
        c = conn.cursor()
        c.execute('''
        SELECT kd.user_id, rrTime, ppTime, rpTime, prTime, time_to_type, vector
        FROM keystroke_datas as kd, keystroke_typing as kt
        WHERE kt.keystroke_datas_id == kd.id
        AND kt.success == TRUE
        AND kt.keyboard_number == 1
        AND kd.password == 'greyc laboratory'
        ''')

        self.headers = []
        self.headers.extend([("rrTime" + str(index)) for index in range(15)])
        self.headers.extend([("ppTime" + str(index)) for index in range(15)])
        self.headers.extend([("rpTime" + str(index)) for index in range(15)])
        self.headers.extend([("prTime" + str(index)) for index in range(15)])
        self.headers = np.array(self.headers)

        for row in c:
            features = []
            features.extend(row[6].split(' ')[1:61])
            self.samples.append(features)
            self.targets.append(row[0])

        self.samples = np.array(self.samples, dtype=np.float64)
        self.targets = np.array(self.targets)

    def computeHeadersMask(self):
        self.headersMask = []
        self.headersMask.extend([True if self.rrTime else False
                                for index in range(15)])
        self.headersMask.extend([True if self.ppTime else False
                                for index in range(15)])
        self.headersMask.extend([True if self.rpTime else False
                                for index in range(15)])
        self.headersMask.extend([True if self.prTime else False
                                for index in range(15)])
        self.headersMask = np.array(self.headersMask)

    def getTargets(self):
        return self.targets

    def getSamples(self):
        return self.samples[:, self.headersMask]

    def getHeaders(self):
        return self.headers[self.headersMask]
