import os
import sys
import urllib.request
import datetime
import time
import json
import pandas as pd

apiKey = '4Nt3716GbS188UbORJ4uePG87l3G5tNd8wvL487H'

#[code 1] url 접속 요청하고 응답받아서 return
def getRequestUrl(url):
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
def getChargeItem(metroCd, cityCd):
    base = 'https://bigdata.kepco.co.kr/openapi/v1/EVcharge.do'
    parameters = '?returnType=json&apiKey=' + apiKey
    parameters += '&metroCd=' + metroCd
    parameters += '&cityCd=' + cityCd

    url = base + parameters
    print(url)
    responseDecode = getRequestUrl(url)     #[code 1]

    if (responseDecode == None):
        return None
    else:
        return json.loads(responseDecode)

#[code 3] 호출한 데이터를 리스트로 묶어 반환
def getChargeData(data, jsonResult):
    metro = data['metro']
    city = data['city']
    stnPlace = data['stnPlace']
    stnAddr = data['stnAddr']
    carType = data['carType']

    jsonResult.append({'metro':metro,'city':city, 'stnPlace':stnPlace,
                        'stnAddr':stnAddr, 'carType':carType})


#[code 0] 
def main():
    print('<<지역 내 전기차 충전소의 정보를 수집합니다.>>')
    metroCd = input('찾고자 하는 대상 시/도 코드를 입력하세요(서울특별시 : 11 / 부산광역시 : 21) : ')
    cityCd = input('찾고자 하는 대상 시/군/구 코드를 입력하세요(강남구 : 26) : ')
    cnt = 0
    
    jsonResult = []
    jsonRes = getChargeItem(metroCd, cityCd)        #[code 2]

    

    for data in jsonRes['data']:
        getChargeData(data, jsonResult)     #code 3
        cnt = cnt + 1
    
    #file output
    with open(f'./Charger_{metroCd}_{cityCd}.json', mode='w', encoding='utf-8') as outfile:
        jsonFile = json.dumps(jsonResult, indent=4, sort_keys=True, ensure_ascii=False)
        outfile.write(jsonFile)

    print(f'조회된 충전소 : {cnt} 건')
    print('Charger_{metroCd}_{cityCd}.json SAVED')
        

if __name__ == '__main__':
    main()