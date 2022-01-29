from random import choice, randint
import sys
from openpyxl import Workbook, load_workbook

class Daily():
    def __init__(self, rnd, plist, fdir):
        self.rnd = rnd
        self.plist = plist
        self.fdir = fdir
        self.wb = load_workbook(fdir, data_only=True)
        self.ws = self.wb.active
        self.setWord()
    
    def setWord(self):
        self.word = []
        for row in self.ws.iter_rows():
            self.word.append((row[0].value, row[1].value, row[2].value))
    
    def nextQ(self):
        if not self.word:
            return None
        if self.rnd:
            idx = randint(0,len(self.word)-1)
        else:
            idx = 0
        n = choice(self.plist)
        tmp = self.word.pop(idx)
        ret = []
        if n == 1:
            ret.append(tmp)
        elif n == 2:
            ret.append(tmp)
            for i in range(3):
                sam = choice(self.word)
                ret.append(sam[2])        
        return n, ret