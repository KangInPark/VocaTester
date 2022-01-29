from random import shuffle
from PyQt5.QtWidgets import *
from PyQt5 import uic, QtCore, QtWidgets
import sys

from Daily import Daily

main_ui = uic.loadUiType("MainWindow.ui")[0]
daily_ui = uic.loadUiType("DailyWindow.ui")[0]
total_ui = uic.loadUiType("TotalWindow.ui")[0]
dailyop_ui = uic.loadUiType("DailyOption.ui")[0]

class MainWindow(QMainWindow, main_ui):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.btn1.clicked.connect(self.DailyBtn)
        self.btn2.clicked.connect(self.TotalBtn)
    
    def DailyBtn(self):
        self.dailyOption = DailyOption()
        
    def TotalBtn(self):
        self.totalWindow = TotalWindow()

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
        self.dailyWindow = DailyWindow(self.chk1.isChecked(), plist, self.fdir[0])

class DailyWindow(QDialog, daily_ui):
    def __init__(self, rnd, plist, fdir):
        super().__init__()
        self.setupUi(self)
        self.daily = Daily(rnd, plist, fdir)
        self.total = len(self.daily.word)
        self.score = 0
        self.btn1.clicked.connect(self.submit)
        self.btn2.clicked.connect(self.submit)
        self.btn3.clicked.connect(self.submit)
        self.btn4.clicked.connect(self.submit)
        self.lineEdit.returnPressed.connect(self.submit)
        self.btn1.hide()
        self.btn2.hide()
        self.btn3.hide()
        self.btn4.hide()
        self.lineEdit.hide()
        self.show()
        self.loadQ()
    
    def submit(self):
        if self.lineEdit.text() == "":
            return
    
    def loadQ(self):
        n, tmp = self.daily.nextQ()
        if n == 1:
            cls = ""
            if tmp[0][1] != None:
                cls = f'[{tmp[0][1]}]'
            self.label.setText(f'{cls}\n{tmp[0][2]}')
            self.lineEdit.show()
        elif n == 2:
            self.label.setText(tmp[0][0])
            ans = []
            ans.append(tmp[0][2])
            ans.append(tmp[1])
            ans.append(tmp[2])
            ans.append(tmp[3])
            shuffle(ans)
            self.btn1.setText(ans[0])
            self.btn2.setText(ans[1])
            self.btn3.setText(ans[2])
            self.btn4.setText(ans[3])
            self.btn1.show()
            self.btn2.show()
            self.btn3.show()
            self.btn4.show()
    
class TotalWindow(QDialog, total_ui):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())