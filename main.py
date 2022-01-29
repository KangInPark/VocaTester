from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5 import QtCore
import sys

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
    
    def Btn(self):
        plist = []
        if self.chk2.isChecked():
            plist.append(1)
        if self.chk3.isChecked():
            plist.append(2)
        self.close()
        self.dailyWindow = DailyWindow(self.chk1.isChecked(), plist)

class DailyWindow(QDialog, daily_ui):
    def __init__(self, rnd, plist):
        super().__init__()
        self.setupUi(self)
        self.rnd = rnd
        self.plist = plist
        self.show()
    
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