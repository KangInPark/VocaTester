import os
from random import shuffle
from PyQt5.QtWidgets import *
from PyQt5 import uic, QtCore, QtWidgets
import sys

from Daily import Daily
from Memorize import Memorize

main_ui = uic.loadUiType("MainWindow.ui")[0]
test_ui = uic.loadUiType("TestWindow.ui")[0]
dailyop_ui = uic.loadUiType("DailyOption.ui")[0]
memo_ui = uic.loadUiType("MemorizeWindow.ui")[0]

class MainWindow(QMainWindow, main_ui):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.btn1.clicked.connect(self.DailyBtn)
        self.btn2.clicked.connect(self.TotalBtn)
    
    def DailyBtn(self):
        cnt = 1
        while True:
            self.dailyOption = DailyOption(cnt)
            self.dailyOption.exec_()
            if self.dailyOption.dailyWindow.end == 1:
                break
            self.memorizeWindow = MemorizeWindow(cnt)
            self.memorizeWindow.exec_()
            cnt += 1
        
    def TotalBtn(self):
        pass

class DailyOption(QDialog, dailyop_ui):
    def __init__(self, cnt):
        super().__init__()
        self.setupUi(self)
        self.cnt = cnt
        self.show()
        self.fbtn.hide()
        self.btn.clicked.connect(self.Btn)
        if cnt == 1:
            self.fbtn.clicked.connect(self.Fopen)
            self.fbtn.show()
        else:
            self.btn.setEnabled(True)
    
    def Fopen(self):
        self.fdir = QtWidgets.QFileDialog.getOpenFileName(self,'OpenFile')
        self.label.setText('파일 선택 완료')
        self.btn.setEnabled(True)
    
    def Btn(self):
        plist = []
        if self.chk2.isChecked():
            plist.append(1)
        if self.chk3.isChecked():
            plist.append(2)
        self.close()
        if self.cnt == 1:
            path = self.fdir[0]
        else:
            path = os.getcwd() + f'\\data\\review.xlsx'
        self.dailyWindow = TestWindow(0, self.chk1.isChecked(), plist, path, self.cnt)
        self.dailyWindow.exec_()

class TestWindow(QDialog, test_ui):
    def __init__(self, mode, rnd, plist, fdir, cnt):
        super().__init__()
        self.setupUi(self)
        self.cnt = cnt
        if mode == 0:
            self.agent = Daily(rnd, plist, fdir, self.cnt)
        self.total = len(self.agent.word)
        self.score = 0
        self.n = 0
        self.data = None
        self.wans = []
        self.curr = 0
        self.end = 0
        self.btn1.clicked.connect(self.submit)
        self.btn2.clicked.connect(self.submit)
        self.btn3.clicked.connect(self.submit)
        self.btn4.clicked.connect(self.submit)
        self.btnHide()
        self.lineEdit.hide()
        self.show()
        self.loadQ()
    
    def submit(self):
        if self.n == 1:
            ans = self.lineEdit.text()
            if ans == "":
                return
            if ans == self.data[0][0]:
                self.score += 1
            else:            
                self.wans.append((self.data[0], ans))
            self.lineEdit.hide()
            self.lineEdit.setText("")
        elif self.n == 2:
            if self.sender().text() == self.data[0][2]:
                self.score += 1
            else:
                self.wans.append((self.data[0], self.sender().text()))
            self.btnHide()
        self.loadQ()
    
    def loadQ(self):
        self.n, self.data = self.agent.nextQ()
        if self.n == 0 and self.data == None:
            print(f"학습종료.\n점수{self.score}/{self.total}\n오답내용:{self.wans}")
            if self.score != self.total:
                self.agent.review(self.wans)
            else:
                self.end = 1
            self.close()
            return
        elif self.n == -1:
            QtWidgets.QMessageBox.critical(self, "경고", "선택한 유형의 테스트를 진행하기에 저장된 단어 데이터의 수가 부족합니다.\n고르기 유형의 경우 최소 6개 이상의 단어 데이터가 필요합니다.\n테스트를 종료합니다.")
            self.end = 1
            self.close()
            return
        self.curr += 1
        self.setWindowTitle(f'오늘의 단어 ({self.curr}/{self.total})')
        if self.n == 1:
            cls = ""
            if self.data[0][1] != None:
                cls = f'[{self.data[0][1]}]'
            self.label.setText(f'{cls}\n{self.data[0][2]}')
            self.ans = self.data[0][0]
            self.lineEdit.raise_()
            self.lineEdit.show()
        elif self.n == 2:
            self.label.setText(self.data[0][0])
            ans = []
            ans.append(self.data[0][2])
            ans.append(self.data[1])
            ans.append(self.data[2])
            ans.append(self.data[3])
            shuffle(ans)
            self.btn1.setText(ans[0])
            self.btn2.setText(ans[1])
            self.btn3.setText(ans[2])
            self.btn4.setText(ans[3])
            self.btnShow()

    def btnShow(self):
        self.btn1.show()
        self.btn2.show()
        self.btn3.show()
        self.btn4.show()
        
    def btnHide(self):
        self.btn1.hide()
        self.btn2.hide()
        self.btn3.hide()
        self.btn4.hide() 
    
    def keyReleaseEvent(self, e):
        if e.key() == QtCore.Qt.Key.Key_Enter or e.key() == QtCore.Qt.Key.Key_Return:
            if self.lineEdit.text() != "":
                self.submit()

class MemorizeWindow(QDialog, memo_ui):
    def __init__(self, cnt):
        super().__init__()
        self.setupUi(self)
        self.cnt = cnt
        self.agent = Memorize(self.cnt)
        self.btn.clicked.connect(self.btnclick)
        self.total = len(self.agent.memolist)
        self.curr = 0
        self.show()
        self.load()
        
    def load(self):
        self.data = self.agent.nextMemo()
        if self.data == None:
            self.close()
            return
        s = self.data[0] + '\n\n'
        if self.data[1] != None:
            s += f'[{self.data[1]}] '
        s += self.data[2]
        self.label1.setText(s)
        self.label2.setText(self.data[3])
        self.curr += 1
        self.setWindowTitle(f'오답 점검 ({self.curr}/{self.total})')

    def btnclick(self):
        self.load()
    
if __name__ == '__main__':
    path = os.getcwd() + '\\data'
    if not os.path.isdir(path):
        os.mkdir(path)
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
