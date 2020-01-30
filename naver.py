import urllib.request
from bs4 import BeautifulSoup
import openpyxl
import os
from selenium import webdriver

#엑셀 파일 설정
filename="file_name.xlsx"
wb=openpyxl.load_workbook(filename)
sheet=wb.worksheets[0]

#크롬웹드라이버 설정
driver = webdriver.Chrome('chromedriver')
driver.implicitly_wait(5)

#각각의 행의 1번째 열의 keword에 대하여
for row in sheet.rows:
    keword=str(row[0].value)

    #해당 키워드 폴더생성
    if not(os.path.isdir(keword)):
        os.makedirs(os.path.join(keword))

    #url get
    url = str("https://search.naver.com/search.naver?where=image&sm=tab_jum&query=")+keword
    driver.get(url)

    #scroll down
    for _ in range(1000):
        driver.execute_script("window.scrollBy(0,10000)")

    counter = 0

    #xpath를 이용한 태그 접근
    for x in (driver.find_elements_by_xpath("//img")):
        try:
            # img태그안에 있는 outerHTML 불러오기
            soup= x.get_attribute('outerHTML')
            if soup.find("http")!=-1:
                #태그안에서 http라는 패턴이 시작하는 위치와 url의 끝인 "의 위치로 substring을 구한다.
                soup=soup[soup.find("http"):soup.find("\"",soup.find("http"))]
                print ("success :" + soup)
                #이미지 저장
                urllib.request.urlretrieve(soup, keword + "/" + keword + "_naver_" + str(counter) + ".jpg")
                counter = counter + 1
        except Exception as e:
            print(e)

driver.close()
