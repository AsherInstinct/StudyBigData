import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt

from urllib.parse import quote
import urllib.request
import json
import webbrowser
import pandas as pd #csv 저장용

# 클래스 OOP
class qPushbutton(QWidget):

    start = 1       # api를 호출할때 시작하는 데이터 번호
    max_display = 100       # 한페이지에 나올 데이터 수 지정
    saveResult = []     #저장할 때 담을 데이터(딕셔너리 리스트) -> DataFrame
    


    # 생성자
    def __init__(self) -> None :        # 리턴값이 None (생성자는 기본적으로 return 값이 없다.)
        super().__init__()
        uic.loadUi('./PyQt03/navernews_2.ui', self)
        self.initUI()

    def initUI(self):
        self.addControls()
        self.show()

    def addControls(self) -> None:          # 위젯 정의, 이벤트(시그널) 처리
        self.btnSearch.clicked.connect(self.btnSearchClicked)
        self.txtSearch.returnPressed.connect(self.btnSearchClicked)
        self.tblResult.itemSelectionChanged.connect(self.tblResultSelected)
        # 220818 추가버튼 이벤트(시그널) 확장
        self.btnNext.clicked.connect(self.btnNextClicked)
        self.btnSave.clicked.connect(self.btnSaveClicked)

    def tblResultSelected(self) -> None:
        selected = self.tblResult.currentRow()      # 현재 선택된 열의 인덱스
        link = self.tblResult.item(selected, 1).text()
        webbrowser.open(link)

    def btnSearchClicked(self):         # 슬롯(이벤트핸들러)
        jsonResult = []
        totalResult = []
        keyword = 'news'
        search_word = self.txtSearch.text()


        # QMessageBox.information(self, '결과', search_word)     # 일반정보창
        jsonResult = self.getNaverSearch(keyword, search_word, self.start, self.max_display)
        # print(jsonResult)

        for post in jsonResult['items']:
            totalResult.append(self.getPostData(post))

        self.makeTable(totalResult)

        #saveResult 값 할당, lblStatus /2 상태값을 표시
        total = jsonResult['total']
        current = self.start + self.max_display - 1

        self.lblStatus.setText(f'Data : {current} / {total}')

        #saveResult 변수에 저장할 데이터를 복사
        for post in totalResult:
            self.saveResult.append(post[0])

        self.lblStatus2.setText(f'저장할데이터 > {len(self.saveResult)}개')

        if current >= 1000:
            self.btnNext.setDisabled(True)      # 특정 갯수 도달시 다음버튼 비활성화
        else:
            self.btnNext.setEnabled(True)

    def btnNextClicked(self) -> None:
        self.start = self.start + self.max_display
        self.btnSearchClicked()


    def btnSaveClicked(self) -> None:
        if len(self.saveResult) >0:
            df = pd.DataFrame(self.saveResult)
            df.to_csv(f'./PyQt03/{self.txtSearch.text()}_뉴스검색결과.csv', encoding='utf-8', index=True)

        QMessageBox.information(self, '저장','저장완료')
        # 저장 후 모든 변수 초기화
        self.saveResult = []
        self.start = 1
        self.txtSearch.setText('')
        self.lblStatus.setText('Data : ')
        self.lblStatus2.setText('저장할 데이터 >')
        self.tblResult.setRowCount(0)
        self.btnNext.setEnabled(True)

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
        title = self.strip_tag(post['title'])
        originallink = post['originallink']
        link = post['link']
        description = self.strip_tag(post['description'])
        pubDate = post['pubDate']

        temp.append({'title':title,
                     'description':description,
                     'originallink':originallink, 
                     'link':link,
                     'pubDate':pubDate})
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