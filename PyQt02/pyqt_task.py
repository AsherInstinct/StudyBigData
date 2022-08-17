import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt

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
        # self.label = QLabel('메세지:', self)
        # self.label.setGeometry(10,10,600,40)
        # self.btn1 = QPushButton('클릭', self)       #  self.btn1 으로 해도 동일하게 작동함.
        # self.btn1.setGeometry(470,450,120,40)   # X좌표, Y좌표, 버튼너비, 버튼높이
        self.BtnStart.clicked.connect(self.btn1_clicked)    # signal 연결
        # 씨언어, 자바 등에서 event라고 부르는 것을 파이썬에서 signal 로 명명한다. 의미 동일
        # event = signal(python)

    def btn1_clicked(self):
        # self.label.setText('메세지 : button1 clicked')
        # QMessageBox.information(self, 'Signal', 'Button Clicked')     # 일반정보창
        # QMessageBox.warning(self, 'Signal', 'Button Clicked')         # 경고창
        # QMessageBox.critical(self, 'Signal', 'Button Clicked')          # 에러창
        self.txbLog.append('실행')
        self.pgbTask.setRange(0, 9999)
        for i in range(0, 10000):       # 너무 값을 높게 잡으면 스레드 초과로 응답없음
            print(f'출력 : {i}')
            self.pgbTask.setValue(i)
            self.txbLog.append(f'출력 > {i}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ins = qPushbutton()
    app.exec_()