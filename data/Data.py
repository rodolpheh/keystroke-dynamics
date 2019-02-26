import sqlite3
import numpy as np
import pandas as pd

class Data:
    """docstring for Data."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.samples = []
        self.targets = []
        self.description = "A database of keystrokes"
        self.headers = []
        self.headersMask = []
        self.table = None
        self.rrTime = True
        self.ppTime = False
        self.rpTime = False
        self.prTime = False

        self.computeHeadersMask()
        self.retrieveData()

    def retrieveData(self):
        conn = sqlite3.connect("./keystroke.db")
        c = conn.cursor()

        query = '''
        SELECT kd.user_id, rrTime, ppTime, rpTime, prTime, time_to_type, vector
        FROM keystroke_datas as kd, keystroke_typing as kt
        WHERE kt.keystroke_datas_id == kd.id
        AND kt.success == TRUE
        AND kt.keyboard_number == 1
        AND kd.password == 'greyc laboratory'
        '''

        c.execute(query)

        self.table = pd.read_sql_query(query, conn)
        toDivide = ["rrTime", "ppTime", "rpTime", "prTime"]

        for name in toDivide:
            column = self.table[name]
            columns = column.str.split(' ', expand=True)
            columns = columns.drop(columns=[0, 16]).astype('int64')
            columns.columns = ["{}{}".format(name, i) for i in range(15)]
            self.table.drop(columns=[name], inplace=True)
            self.table = pd.concat([self.table, columns], axis=1)
            
        self.table.drop(columns=["vector"], inplace=True)
        self.table[["time_to_type", "user_id"]] = self.table[["time_to_type", "user_id"]].astype('int64')

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
    
    @property
    def usersCounts(self):
        unique, counts = np.unique(self.table["user_id"], return_counts=True)
        return sorted(list(zip(unique, counts)), key=lambda el : el[1])[::-1]
            
    def printUsersCounts(self):
        for count in self.usersCounts:
            print("User {:<3} - {:3} records".format(count[0], count[1]))