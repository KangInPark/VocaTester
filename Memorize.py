from collections import deque
import os
from openpyxl import load_workbook


class Memorize():
    def __init__(self, cnt):
        self.cnt = cnt
        self.wb = load_workbook(os.getcwd() + f'\\data\\review.xlsx')
        self.ws = self.wb[self.wb.sheetnames[-1]]
        self.memolist = deque()
        self.setMemo()
        
    def setMemo(self):
        chk = 0
        for row in self.ws.iter_rows():
            if row[0].value == str(self.cnt) + "차시":
                chk = 1
                continue
            if chk == 0:
                continue
            self.memolist.append((row[0].value, row[1].value, row[2].value, row[3].value))
        self.wb.close()
    
    def nextMemo(self):
        if not self.memolist:
            return None
        else:
            return self.memolist.popleft()
            
