#-*- coding:utf-8 -*-

import openpyxl
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import json
import os
import urllib.request

#엑셀파일경로
filename="file_name.xlsx"
wb=openpyxl.load_workbook(filename)
sheet=wb.worksheets[0] #첫번째 시트 지정

#크롬드라이버 경로 설정
driver = webdriver.Chrome('chromedriver')
driver.implicitly_wait(5)

for row in sheet.rows:
    keword=str(row[0].value) #첫번째 행의 값을 검색 키워드로 지정

    #폴더생성
    if not(os.path.isdir(keword)):
        os.makedirs(os.path.join(keword))


    #검색시작
    url = "https://www.google.co.in/search?q="+wine_name+"&source=lnms&tbm=isch"
    driver.get(url)

    #스크롤 내리기
    for _ in range(1000):
        driver.execute_script("window.scrollBy(0,10000)")
    
    counter = 0

    #이미지가 들어간 태그 xpath를 통한 접근
    for x in driver.find_elements_by_xpath('//div[contains(@class,"rg_meta")]'):
        
        #현재 어떤 키워드로 크롤링을 하고있는지 출력
        print (keword+"URL:",json.loads(x.get_attribute('innerHTML'))["ou"])
        
        #이미지의 url
        img =json.loads(x.get_attribute('innerHTML'))["ou"]
        
        #이미지의 파일형식 jpg, png, etc.
        imgtype =json.loads(x.get_attribute('innerHTML'))["ity"]

        #저장해줄 경로
        img_path = keword + "/" + keword + "_" + str(counter) + "." + imgtype
        try:
            #이미지 저장
            urllib.request.urlretrieve(img, img_path)
            counter = counter + 1
        except:
            print ("can't get img")         

driver.close()
