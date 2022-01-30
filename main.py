import os
from random import shuffle
from PyQt5.QtWidgets import *
from PyQt5 import uic, QtCore, QtWidgets
import sys

from Daily import Daily

main_ui = uic.loadUiType("MainWindow.ui")[0]
test_ui = uic.loadUiType("TestWindow.ui")[0]
dailyop_ui = uic.loadUiType("DailyOption.ui")[0]

class MainWindow(QMainWindow, main_ui):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.btn1.clicked.connect(self.DailyBtn)
        self.btn2.clicked.connect(self.TotalBtn)
    
    def DailyBtn(self):
        self.dailyOption = DailyOption()
        self.dailyOption.exec_()
        
    def TotalBtn(self):
        pass

class DailyOption(QDialog, dailyop_ui):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()
        self.btn.clicked.connect(self.Btn)
        self.fbtn.clicked.connect(self.Fopen)
    
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
        self.dailyWindow = TestWindow(0, self.chk1.isChecked(), plist, self.fdir[0])
        self.dailyWindow.exec_()

class TestWindow(QDialog, test_ui):
    def __init__(self, mode, rnd, plist, fdir):
        super().__init__()
        self.setupUi(self)
        if mode == 0:
            self.agent = Daily(rnd, plist, fdir)
        self.total = len(self.agent.word)
        self.score = 0
        self.n = 0
        self.data = None
        self.wans = []
        self.cnt = 1
        self.curr = 0
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
                self.agent.review(self.wans, self.cnt)
                self.cnt += 1
            self.close()
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
    
if __name__ == '__main__':
    path = os.getcwd() + '\\data'
    if not os.path.isdir(path):
        os.mkdir(path)
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
