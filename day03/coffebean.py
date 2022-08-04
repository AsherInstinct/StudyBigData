from bs4 import BeautifulSoup
from selenium import webdriver
import urllib.request
import pandas as pd
import datetime
import time

#[code 1]
def CoffeeBean_Store(result):
    CoffeBean_Url = 'https://www.coffeebeankorea.com/store/store.asp'
    # wd = webdriver.Chrome('C:/localRepository/StudyBigData/chromedriver.exe')
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    wd = webdriver.Chrome('./chromedriver.exe',options=options)  
    #selenium 4버전 이후 드라이버경고 문구 없애는 코드
    

    for i in range(1, 2):  #총매장숫자를 어떻게 가져올 것인가?
        wd.get(CoffeBean_Url)
        time.sleep(1)
        try:
            wd.execute_script(f'storePop2({i})')           #자바스크립트함수 호출
            time.sleep(1)
            html = wd.page_source
            soup = BeautifulSoup(html, 'html.parser')
            # store_name_h2 = soup.select('div.store_txt>h2')
            # store_name = store_name_h2[0].string
            store_name = soup.select('div.store_txt>h2')[0].string
            store_info = soup.select('table.store_table>tbody>tr>td')
            store_address_list = list(store_info[2])
            store_address = store_address_list[0].strip()
            store_phone = store_info[3].string
            result.append([store_name]+[store_address]+[store_phone])
        except:
            continue
    wd.close()
    print('커피빈 매장정보 호출 완료')
    return

def main():
    result=[]
    print('커피빈 매장 정보 크롤링 시작')
    CoffeeBean_Store(result)

    CoffeeBean_Tb = pd.DataFrame(result, columns=('store','address','phone'))
    CoffeeBean_Tb.to_csv('./CoffeeBean.csv', mode='w', encoding='utf-8',index=True)
    print('커피빈 매장정보 데이터 저장 완료')

if __name__ == '__main__':
    main()