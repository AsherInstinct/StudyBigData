import sys
from PyQt5.QtWidgets import QApplication, QWidget

# 클래스 OOP
class qTemplate(QWidget):
    # 생성자
    def __init__(self) -> None :        # 리턴값이 None (생성자는 기본적으로 return 값이 없다.)
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(500,300,500,200)  #X,Y, 너비, 높이
        self.setWindowTitle('QTemplate!!')  #창 제목
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ins = qTemplate()
    app.exec_()