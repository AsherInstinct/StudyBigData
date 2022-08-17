import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt

from urllib.parse import quote
import urllib.request
import json
import webbrowser

# 클래스 OOP
class qPushbutton(QWidget):
    # 생성자
    def __init__(self) -> None :        # 리턴값이 None (생성자는 기본적으로 return 값이 없다.)
        super().__init__()
        uic.loadUi('./PyQt02/navernews.ui', self)
        self.initUI()

    def initUI(self):
        self.addControls()
        self.show()

    def addControls(self) -> None:          # 위젯 정의, 이벤트(시그널) 처리
        self.btnSearch.clicked.connect(self.btnSearchClicked)
        self.txtSearch.returnPressed.connect(self.btnSearchClicked)
        self.tblResult.itemSelectionChanged.connect(self.tblResultSelected)

    def tblResultSelected(self) -> None:
        selected = self.tblResult.currentRow()      # 현재 선택된 열의 인덱스
        link = self.tblResult.item(selected, 1).text()
        webbrowser.open(link)

    def btnSearchClicked(self):         # 슬롯(이벤트핸들러)
        jsonResult = []
        totalResult = []
        keyword = 'news'
        search_word = self.txtSearch.text()
        display_count = 50

        # QMessageBox.information(self, '결과', search_word)     # 일반정보창
        jsonResult = self.getNaverSearch(keyword, search_word, 1, display_count)
        # print(jsonResult)

        for post in jsonResult['items']:
            totalResult.append(self.getPostData(post))

        self.makeTable(totalResult)
        return


    def makeTable(self, result):
        self.tblResult.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tblResult.setColumnCount(2)
        self.tblResult.setRowCount(len(result))     # display_count 에 따라 변경
        self.tblResult.setHorizontalHeaderLabels(['기사제목','뉴스링크'])
        self.tblResult.setColumnWidth(0, 350)
        self.tblResult.setColumnWidth(1, 100)
        self.tblResult.setEditTriggers(QAbstractItemView.NoEditTriggers)    #readonly

        i = 0
        for item in result:
            title = self.strip_tag(item[0]['title'])
            link = item[0]['originallink']
            self.tblResult.setItem(i, 0, QTableWidgetItem(title))
            self.tblResult.setItem(i, 1, QTableWidgetItem(link))
            i += 1
        
    def strip_tag(self, title):     # html 태그를 없애주는 함수
        ret = title.replace('&lt;', '<')
        ret = ret.replace('&gt;', '>')
        ret = ret.replace('&quot;', '"')
        ret = ret.replace('&apos;', "'")
        ret = ret.replace('&amp;', '&')
        ret = ret.replace('<b>', '')
        ret = ret.replace('</b>', '')
        return ret


    def getPostData(self, post):
        temp = []
        title = post['title']
        originallink = post['originallink']
        link = ['link']
        description = ['description']
        pubDate = ['pubDate']

        temp.append({'title':title,
                     'originallink':originallink, 
                     'link':link})
        return temp


# 네이버 api 크롤링을 위한 함수
    def getNaverSearch(self, keyword, search, start, display):
        url = f'https://openapi.naver.com/v1/search/{keyword}.json?query={quote(search)}&start={start}&display={display}'
        req = urllib.request.Request(url)
        #네이버인증 추가
        req.add_header('X-Naver-Client-Id', 'mhxEQkbMH3NqkJQjEBIf')
        req.add_header('X-Naver-Client-Secret', 'hXIGJmXASj')

        res = urllib.request.urlopen(req)
        if res.getcode() == 200:   # 200 ok,  40x error, 50x server error
            print('Url Request Success')
        else:
            print('URL request failed')

        ret =  res.read().decode('utf-8')
        if ret == None :
            return None
        else:
            return json.loads(ret)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ins = qPushbutton()
    app.exec_()