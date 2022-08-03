import os
import sys
import urllib.request
import datetime
import time
import json
import pandas as pd

serviceKey = 'aLCcyoriLTekyFt1s6F0PDQ7QsM8j4jtyHd%2FWeEJrv7MbLANaxKWZfnOTpbntkJ2TE78jBAPgvagfOJsMydHrw%3D%3D'

#[code 1] url 접속 요청하고 응답받아서 return
def getRequestIrl(url):
    req = urllib.request.Request(url)
    
    try:
        res = urllib.request.urlopen(req)
        if res.getcode() == 200:   # 200 ok,  40x error, 50x server error
            print(f'[{datetime.datetime.now()}] Url Request Success')
            return res.read().decode('utf-8')
    except Exception as e:
        print(e)
        print(f'[{datetime.datetime.now()}] Error for URL : {url}')
        return None


#[code 2] 데이터 요청 url 만들기
def getTourismStatsItem(yyyymm, nat_cd, ed_cd):
    base = 'http://openapi.tour.go.kr/openapi/service/EdrcntTourismStatsService/getEdrcntTourismStatsList'
    parameters = '?_type=json&serviceKey='+ serviceKey
    parameters += '&YM=' + yyyymm
    parameters += '&NAT_CD=' + nat_cd
    parameters += '&ED_CD=' + ed_cd

    url = base + parameters
    print(url)
    responseDecode = getRequestIrl(url)     #[code 1]

    if (responseDecode == None):
        return None
    else:
        return json.loads(responseDecode)


#[code 3]
def getTourismStatsService(nat_cd, ed_cd, nStartYear, nEndYear):
    jsonResult = []
    result = []
    natName = ''
    dataEND = '{0}{1:0>2}'.format(str(nEndYear), str(12))        #수집할 데이터의 끝 날짜인 dataEND를 nEndYear의12월로 설정
    isDataEnd = 0 
    



#[code 0] 메인 구조 함수
def main():
    jsonResult = []
    result = []

    print('<<국내에 입국한 외국인의 통계 데이터를 수집합니다.>>')
    nat_cd = input('국가 코드를 입력하세요(중국 : 112 / 일본 : 130 / 미국 : 275) : ')
    nStartYear = int(input('데이터를 몇 년부터 수집할까요? : '))
    nEndYear = int(input('데이터를 몇 년까지 수집할까요? '))  
    ed_cd = 'E'     #E 방한외래관광객

    jsonResult, result, natName, dataEnd = getTourismStatsService(nat_cd, ed_cd, nStartYear, nEndYear) #[code 3]

    #파일저장 1 json file
    with open(f'./{natName}_{ed}_{nStartYear}_{nEndYear}.json', mode='w', encoding='utf-8') as outfile:
        jsonFile = json.dumps(jsonResult, indent=4, sort_keys=True, ensure_ascii=False)
        outfile.write(jsonFile)

    #파일저장2 csv
    columns = ['입국자국가','국가코드','입국연월','입국자 수']
    
