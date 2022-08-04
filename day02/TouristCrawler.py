import os
import sys
import urllib.request
import datetime
import time
import json
import pandas as pd

serviceKey = 'Ody77GLuYeR%2FeFqbpduMN2Bi4Cka2fztbgnj6E2Eux1kUhy3e4epR28XKBUaObiqPoVzAizxXMBPXtMyuC9v9Q%3D%3D'

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
def getTourismStatsItem(yyyymm, nat_cd, ed_cd):
    base = 'http://openapi.tour.go.kr/openapi/service/EdrcntTourismStatsService/getEdrcntTourismStatsList'
    parameters = '?_type=json&serviceKey='+ serviceKey
    parameters += '&YM=' + yyyymm
    parameters += '&NAT_CD=' + nat_cd
    parameters += '&ED_CD=' + ed_cd

    url = base + parameters
    print(url)
    responseDecode = getRequestUrl(url)     #[code 1]

    if (responseDecode == None):
        return None
    else:
        return json.loads(responseDecode)


#[code 3]
def getTourismStatsService(nat_cd, ed_cd, nStartYear, nEndYear):
    jsonResult = []     #json 파일로 저장하기 위한 리스트  튜플 형태
    result = []         #csv 파일로 저장하기 위한 리스트 딕셔너리 형태
    natName = ''
    dataEND = '{0}{1:0>2}'.format(str(nEndYear), str(12))        #수집할 데이터의 끝 날짜인 dataEND를 nEndYear의12월로 설정
    isDataEnd = 0 #데이터 끝 확인용 플래그 False or 0
    for year in range(nStartYear, nEndYear+1):
        for month in range(1, 13):
            if(isDataEnd == 1):
                break
            yyyymm = '{0}{1:0>2}'.format(str(year), str(month)) #f'{year}{month:0>2}'
            jsonData = getTourismStatsItem(yyyymm, nat_cd, ed_cd)   #[code 2] 2022 1월 >> 202201
            if jsonData['response']['header']['resultMsg'] == 'OK':     #데이터가 없는 경우라면 서비스 종료
                if jsonData['response']['body']['items'] == '' :
                    isDataEnd =1
                    dataEND = '{0}{1:0>2}'.format(str(year), str(month-1))
                    print(f'데이터없음... \n 제공되는 통계 데이터는 {year}년 {month-1}월 까지 입니다.')
                    break
                print(json.dumps(jsonResult, indent=4, sort_keys=True, ensure_ascii=False))
                natName = jsonData['response']['body']['items']['item']['natKorNm']
                natName = natName.replace(' ','')
                num = jsonData['response']['body']['items']['item']['num']
                ed = jsonData['response']['body']['items']['item']['ed']
                print(f'[{natName}_{yyyymm} : {num}]')
                print('________________________________________________')
                jsonResult.append({'natName': natName, 'nat_cd' : nat_cd, 'yyyymm' : yyyymm, 'visit_cnt' : num})
                result.append([natName, nat_cd, yyyymm, num])
    return(jsonResult, result, natName, ed, dataEND)





#[code 0] 메인 구조 함수
def main():
    jsonResult = []
    result = []


    print('<<국내에 입국한 외국인의 통계 데이터를 수집합니다.>>')
    nat_cd = input('국가 코드를 입력하세요(중국 : 112 / 일본 : 130 / 미국 : 275) : ')
    nStartYear = int(input('데이터를 몇 년부터 수집할까요? : '))
    nEndYear = int(input('데이터를 몇 년까지 수집할까요? '))  
    ed_cd = 'E'     #E 방한외래관광객

    jsonResult, result, natName, ed, dataEND = getTourismStatsService(nat_cd, ed_cd, nStartYear, nEndYear) #[code 3]

    if natName == '':
        print('데이터 호출 실패. 공공데이터포털 확인 요망')
    else:
        

        # 파일저장 1 json file
        with open(f'./{natName}_{ed}_{nStartYear}_{nEndYear}.json', mode='w', encoding='utf-8') as outfile:
            jsonFile = json.dumps(jsonResult, indent=4, sort_keys=True, ensure_ascii=False)
            outfile.write(jsonFile)
    
        # 파일저장2 csv
        columns = ['입국자국가','국가코드','입국연월','입국자 수']
        result_df = pd.DataFrame(result, columns=columns)
        result_df.to_csv(f'./{natName}_{ed}_{nStartYear}_{nEndYear}.csv', index= False, encoding='utf-8')
        
        print('파일 저장 완료.')
if __name__ == '__main__':
    main()