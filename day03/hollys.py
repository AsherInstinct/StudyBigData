from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import datetime

def hollys_store(result):
    for page in range(1, 54):
        Hollys_url = f'https://www.hollys.co.kr/store/korea/korStore2.do?pageNo={page}'

        # print(Hollys_url)
        html = urllib.request.urlopen(Hollys_url)
        soupHollys = BeautifulSoup(html,'html.parser')
        tag_tbody = soupHollys.find('tbody')
        for store in tag_tbody.find_all('tr'):
            if len(store) <= 3:
                break
            store_td = store.find_all('td')
            store_name = store_td[1].string
            store_sido = store_td[0].string
            store_adress = store_td[3].string
            store_phone = store_td[5].string
            result.append([store_name]+[store_sido]+[store_adress]+[store_phone])
    
    print('호출 완료')
    return

def main():
    result= []
    print('할리스커피 매장정보 크롤링')
    hollys_store(result)        #조회
    hollys_tb = pd.DataFrame(result, columns= ('store', 'sido-gu','address','phone'))
    hollys_tb.to_csv('./hollys.csv', encoding='utf-8', mode='w', index=True)        #상대경로
    # hollys_tb.to_csv('C:/localRepository/StudyBigData/day03/hollys.csv', encoding='utf-8', mode='w', index=True)    #절대경로

    print('할리스커피 매장정보 저장완료')
    del result[:]

if __name__ =='__main__':
    main()