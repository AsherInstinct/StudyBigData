import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt

# 클래스 OOP
class qPushbutton(QWidget):
    # 생성자
    def __init__(self) -> None :        # 리턴값이 None (생성자는 기본적으로 return 값이 없다.)
        super().__init__()
        self.initUI()

    def initUI(self):
        self.addControls()
        self.setGeometry(1100,300,600, 300)  #X,Y, 너비, 높이
        self.setWindowTitle('QPushButton!')  #창 제목
        self.show()

    def addControls(self) -> None:
        btn01 = QPushButton('Click', self)
        btn01.setGeometry(470,250,120,40)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ins = qPushbutton()
    app.exec_()