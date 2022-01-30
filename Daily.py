import datetime
import os
from random import choice, randint
import sys
from openpyxl import Workbook, load_workbook

class Daily():
    def __init__(self, rnd, plist, fdir):
        self.rnd = rnd
        self.plist = plist
        self.fdir = fdir
        self.wb = load_workbook(fdir)
        self.ws = self.wb.active
        self.setWord()
    
    def setWord(self):
        self.word = []
        self.mlist = []
        for row in self.ws.iter_rows():
            self.word.append((row[0].value, row[1].value, row[2].value))
            self.mlist.append(row[2].value)
        if len(self.word) <= 4 and 2 in self.plist:
            self.plist.remove(2)
    
    def nextQ(self):
        if not self.word:
            return 0, None
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
            while len(ret) < 4:
                sam = choice(self.mlist)
                if sam != ret[0][2] and sam not in ret:
                    ret.append(sam)
        return n, ret
    
    def review(self, wans, cnt):
        path = os.getcwd() + '\\data\\review.xlsx'
        if not os.path.isfile(path):
            wb = Workbook()
            ws = wb['Sheet']
            ws.title = f'{str(datetime.date.today())}-({cnt})'
        else:
            wb = load_workbook(path)
            ws = wb.create_sheet(f'{str(datetime.date.today())}-({cnt})')
        for i in range(1, len(wans)+1):
            ws.cell(i,1).value = wans[i-1][0]
            if wans[i-1][1] == None:
                ws.cell(i,2).value = ""
            else:
                ws.cell(i,2).value = wans[i-1][1]
            ws.cell(i,3).value = wans[i-1][2]
        wb.save(path)