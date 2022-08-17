import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import time

# UI 스레드와 작업 스레드 분리
class Worker(QThread):

    valChangeSignal = pyqtSignal(int) # QThread는 화면을 그릴 권한이 없음. >> 대신 통신을 통해서 UI Thread가 그림을 그릴 수 있도록 통신 수행

    def __init__(self, parent):
        super().__init__(parent)            # 누가불렀는지는 알려주는 parent 인자값으로 삽입
        self.parent = parent
        self.working = True         # 클래스 내부변수 working을 만들어서 지정

    def run(self):              # 스레드는 항상 run이라는 함수가 동작함.
        while self.working:
            for i in range(0, 100000):       # 너무 값을 높게 잡으면 스레드 초과로 응답없음
                print(f'출력 : {i}')
                # self.pgbTask.setValue(i)
                # self.txbLog.append(f'출력 > {i}')
                self.valChangeSignal.emit(i)     # UI Thread야 화면은 너가 그려줘.
                time.sleep(0.0001)   # 1micro sec



# 클래스 OOP
class qPushbutton(QWidget):
    # 생성자
    def __init__(self) -> None :        # 리턴값이 None (생성자는 기본적으로 return 값이 없다.)
        super().__init__()
        uic.loadUi('./PyQt02/ttask.ui', self)
        self.initUI()

    def initUI(self):
        self.addControls()
        # self.setGeometry(1100,300,600, 500)  #X,Y, 창너비, 창높이
        # self.setWindowTitle('QPushButton!')  #창 제목
        self.show()

    def addControls(self) -> None:
        self.BtnStart.clicked.connect(self.btn1_clicked)    # signal 연결
        # Worker 클래스 생성
        self.worker =  Worker(self)
        self.worker.valChangeSignal.connect(self.updateProgress)    #스레드에서 받은 시그널은 updateProgress 함수에서 처리해줌

    @pyqtSlot(int)
    def updateProgress(self, val): # val이 워커스레드에서 전달받은 반복값
        self.pgbTask.setValue(val)
        self.txbLog.append(f'출력 > {val}')
        if val == 9999:
            self.worker.working = False

    def btn1_clicked(self):
        self.txbLog.append('실행')
        self.pgbTask.setRange(0, 99999)
        self.worker.start()
        self.worker.working = True

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ins = qPushbutton()
    app.exec_()