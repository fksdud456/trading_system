from KiwoomTrade import *
import sys
import time
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
from PyQt5.QtCore import *


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('stock')
        self.setGeometry(100, 100, 100, 100)

        self.kiwoom = KiwoomTrade()
        self.kiwoom.comm_connect()
        self.timer = QTimer(self)
        self.timer.start(1000)
        self.timer.timeout.connect(self.timeout)

    def timeout(self):
        current_time = QTime.currentTime()
        text_time = current_time.toString("hh:mm:ss")
        time_msg = "현재시간: " + text_time

        state = self.kiwoom.get_connect_state()
        if state == 1:
            state_msg = "서버 연결 중"
        else:
            state_msg = "서버 미 연결 중"

        self.statusbar.showMessage(state_msg + " | " + time_msg)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()

    window.show()
    app.exec_()
