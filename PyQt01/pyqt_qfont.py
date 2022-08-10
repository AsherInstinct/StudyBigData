import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtCore import Qt


# 클래스 OOP
class qfont_exam(QWidget):
    # 생성자
    def __init__(self) -> None :        # 리턴값이 None (생성자는 기본적으로 return 값이 없다.)
        super().__init__()
        self.initUI()

    # 화면 정의를 위해 사용자 함수
    def initUI(self):
        self.setGeometry(500,300,500,500)  #X,Y, 너비, 높이
        self.setWindowTitle('QFont!!')  #창 제목
        self.text = 'What the heck!'
        self.show()

    def paintEvent(self, event) -> None:
        paint = QPainter()
        paint.begin(self)
        self.drawText(event, paint)     # 그리는 함수 추가
        paint.end()

    def drawText(self, event, paint):
        paint.setPen(QColor(50,50,50))
        paint.setFont(QFont('NanumGothic', 20))
        paint.drawText(105,100, 'hello world')
        paint.setPen(QColor(5,250,150))
        paint.setFont(QFont('NanumGothic', 15))
        paint.drawText(event.rect(), Qt.AlignCenter, self.text)     #event.rect 정중앙에 표시


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ins = qfont_exam()
    app.exec_()