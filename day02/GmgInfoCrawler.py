import os
import sys
import urllib.request
import datetime
import time
import json
import pandas as pd
import pymysql


serviceKey = 'aLCcyoriLTekyFt1s6F0PDQ7QsM8j4jtyHd%2FWeEJrv7MbLANaxKWZfnOTpbntkJ2TE78jBAPgvagfOJsMydHrw%3D%3D'

#[code 1] url 접속 요청하고 응답받아서 return   
def getRequestUrl(url):
    '''
    Url 접속요청 후 응답함수
    ---------------------
    parameter : url -> openAPI 전체 URL
    '''
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
def getGMGInfo():
    base = 'http://apis.data.go.kr/6260000/fbusangmgcourseinfo/getgmgcourseinfo'
    # parameters = f'?resultType=json&serviceKey={serviceKey}'
    # parameters += '&numOfRows=30'
    # parameters += f'&pageNo=1'
    parameters = f'?serviceKey={serviceKey}&numOfRows=30&pageNo=1&resultType=json'

    url = base + parameters
    print(url)
    retData = getRequestUrl(url)     #[code 1]

    if (retData == None):
        return None
    else:
        return json.loads(retData)


#[code 3]
def getGMGSersvice():
    result = []
    jsonData = getGMGInfo()
    # print(jsonData)
    # course_nm = [getgmgcourseinfo][item][course_nm]
    if jsonData['getgmgcourseinfo']['header']['code'] == '00':
        if jsonData['getgmgcourseinfo']['item'] == '':
            print(f'서비스 오류')
        else:
            for item in jsonData['getgmgcourseinfo']['item']:
                seq = item['seq']
                course_nm = item['course_nm']
                gugan_nm =item['gugan_nm']
                gm_range=item['gm_range']
                gm_degree=item['gm_degree']
                start_pls=item['start_pls']
                start_addr=item['start_addr']
                middle_pls=item['middle_pls']
                middle_adr=item['middle_adr']
                end_pls = item['end_pls']
                end_addr =item['end_addr']
                gm_course =item['gm_course']
                gm_text=item['gm_text']
                
                result.append([seq,course_nm,gugan_nm,gm_range,gm_degree,start_pls,start_addr,middle_pls,middle_adr,end_pls,end_addr,gm_course,   gm_text])

    return result




def main():
    result=[]

    print('부산 갈맷길 코스를 조회힙니다.')
    result = getGMGSersvice()

    if len(result) >0:
        #파일저장csv
        columns = ['seq','course_nm','gugan_nm','gm_range','gm_degree','start_pls','start_addr','middle_pls','middle_adr','end_pls','end_addr','gm_course','gm_text']
        result_df =pd.DataFrame(result, columns=columns)
        result_df.to_csv(f'./부산갈맷길정보.csv', index= False, encoding='utf-8')

        #db저장
        connection = pymysql.connect(host='localhost',
                                    user='root',
                                    password='1234',
                                    db='crawling_data')

        #create_cursor
        cursor = connection.cursor()

        #컬럼명 동적으로 만들기
        cols = '`,`'.join([str(i) for i in result_df.columns.tolist()])

        for i, row in result_df.iterrows():
            sql = 'INSERT INTO `galmatgil_info` (`' + cols + '`) VALUES (' + '%s, '*(len(row)-1)+'%s)'
            cursor.execute(sql, tuple(row))

        connection.commit()
        connection.close()

        print('DB저장완료') 

if __name__ == '__main__':
    main()
