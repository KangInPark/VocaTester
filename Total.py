from collections import defaultdict
from copy import deepcopy
from pathlib import Path
import pickle
from random import sample
import sys
from openpyxl import load_workbook
from Daily import Daily

class Total(Daily):
    def __init__(self, rnd, plist, info, cnt, same, mode):
        if getattr(sys, 'frozen', False):
            self.p = Path(sys.executable).parent.resolve()/"data"
        else:
            self.p = Path(__file__).parent.resolve()/"data"
        self.rnd = rnd
        self.plist = plist
        self.fdir = info[0]
        self.start = info[1]
        self.end = info[2]
        self.qnum = info[3]
        self.cnt = cnt
        self.same = same
        self.mode = mode
        self.cls = []
        pkl = "Wdata.pkl"
        self.wb = load_workbook(self.fdir)
        self.setWord()
        self.warn = 0
        if 2 in plist or 3 in plist:
            with (self.p/pkl).open('rb') as f:
                self.mlist = list(pickle.load(f))
            if len(self.mlist) < 6:
                self.word = []
                self.warn = 1
            if self.same:
                tmp = defaultdict(int)
                for w in self.mlist:
                    if w[1] in self.cls:
                        tmp[w[1]] += 1
                        if tmp[w[1]] == 6:
                            self.cls.remove(w[1])
                            if not self.cls:
                                break    
    
    def setWord(self):
        self.wlist = []
        sname = self.wb.sheetnames
        if self.mode == 2:
            self.start += '_1'
            for s in sname[::-1]:
                if s.split('_')[0] == self.end:
                    self.end += '_' + s.split('_')[1]
                    break
        scope = sname[sname.index(self.start):sname.index(self.end)+1]
        for s in scope:
            self.ws = self.wb[s]
            for row in self.ws.iter_rows():
                if row[0].value == '1차시':
                    continue
                elif row[2].value == None:
                    break
                self.wlist.append((row[0].value, row[1].value, row[2].value))
        if self.qnum > len(self.wlist):
            tmp = deepcopy(self.wlist)
        while self.qnum > len(self.wlist):
            self.wlist.extend(tmp)
        self.word = sample(self.wlist, self.qnum)
        for w in self.word:
            if(w[1] != None and w[1] not in self.cls):
                self.cls.append(w[1])
        self.wb.close()
