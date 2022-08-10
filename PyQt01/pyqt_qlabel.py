import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QPainter, QColor, QFont, QIcon
from PyQt5.QtCore import Qt


# 클래스 OOP
class qlabel_exam(QWidget):
    # 생성자
    def __init__(self) -> None :        # 리턴값이 None (생성자는 기본적으로 return 값이 없다.)
        super().__init__()
        self.initUI()

    # 화면 정의를 위해 사용자 함수
    def initUI(self) -> None :
        self.addControls()
        self.setGeometry(500,300,500,500)  #X,Y, 너비, 높이
        self.setWindowTitle('QLabel!')  #창 제목
        self.show()

    def addControls(self) -> None:
        self.setWindowIcon(QIcon('./PyQt01/image/lion.png')) #창 아이콘
        label1 = QLabel('', self)       #내용을 안적는게 바람직함
        label2 = QLabel('Label 2', self)
        label1.setStyleSheet(
            'border-width: 3px;'
            'border-style:solid;'
            'border-color: blue;'
            'image: url(./PyQt01/image/image1.png)'     #django 환경에서 stylesheet 작성법과 동일
        )
        label2.setStyleSheet(
            'border-width: 3px;'
            'border-style: dot-dot-dash;'
            'border-color: red;'
            'image: url(./PyQt01/image/image2.png)'
        )

        box = QHBoxLayout()
        box.addWidget(label1)
        box.addWidget(label2)

        self.setLayout(box)

        

 


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ins = qlabel_exam()
    app.exec_()