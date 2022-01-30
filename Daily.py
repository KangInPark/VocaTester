from copy import deepcopy
import datetime
import os
import pickle
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
        self.warn = 0
        if 2 in plist or 3 in plist:
            with open(os.getcwd() + f'\\data\\{str(datetime.date.today())}.pkl', 'rb') as f:
                self.mlist = pickle.load(f)
            if len(self.mlist) < 6:
                self.word = []
                self.warn = 1
    def setWord(self):
        self.word = []
        for row in self.ws.iter_rows():
            self.word.append((row[0].value, row[1].value, row[2].value))
        self.accumulate(self.word)
    
    def nextQ(self):
        if not self.word:
            if self.warn == 1:
                return -1, None
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
                sam = choice(self.mlist)[2]
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
            ws.cell(i,1).value = wans[i-1][0][0]
            if wans[i-1][0][1] == None:
                ws.cell(i,2).value = ""
            else:
                ws.cell(i,2).value = wans[i-1][0][1]
            ws.cell(i,3).value = wans[i-1][0][2]
            ws.cell(i,4).value = wans[i-1][1]
        wb.save(path)
        
    def accumulate(self, words):
        word = deepcopy(words)
        path = os.getcwd() + '\\data\\CumulativeWords.xlsx'
        dup = {}
        today = str(datetime.date.today())
        if not os.path.isfile(path):
            wb = Workbook()
            ws = wb['Sheet']
            ws.title = today
        else:
            wb = load_workbook(path)
            if today in wb.sheetnames:
                ws = wb[today]
                for item in word:
                    if item[0] not in dup:
                        dup[item[0]] = 1
                for row in ws.iter_rows():
                    if row[0].value not in dup:
                        word.append((row[0].value, row[1].value, row[2].value))
                del wb[today]
            ws = wb.create_sheet(today)
        for i in range(1, len(word)+1):
            ws.cell(i,1).value = word[i-1][0]
            if word[i-1][1] == None:
                ws.cell(i,2).value = ""
            else:
                ws.cell(i,2).value = word[i-1][1]
            ws.cell(i,3).value = word[i-1][2]
        wb.save(path)
        pick = []
        idx = wb.sheetnames.index(today) 
        if idx > 0:
            with open(os.getcwd() + f'\\data\\{wb.sheetnames[idx-1]}.pkl', 'rb') as f:
                pick = pickle.load(f)
        pick.extend(word)
        with open(os.getcwd() + f'\\data\\{today}.pkl', 'wb') as f:
            pickle.dump(pick, f)