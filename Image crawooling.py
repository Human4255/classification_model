"""
*데이터의 형태
   1. 정형데이터-일정한규칙으로 구성된 데이터 ex)DB
   2. 반정형데이터-규칙이 없으나 구조를 갖춘 데이터 ex)XML,JSON(딕셔너리구조),HTML
   3. 비정형데이터-규칙과 규격구조가 존재하지 않는 데이터 ex)SNS글,동영상,이미지,음성,텍스트

*페이지
 -웹페이지는 인터넷을 통해 가져오기에 느리다. 때문에 time이라는 함수를 통해 시간을 벌 수 있음
 -동적페이지 , 정적페이지
 -웹페이지에서 가져오면 os에 저장을 해야한다.


"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys #키전송
from selenium.webdriver.common.by import By
from urllib import parse, request
import time
import os
import requests #프로그램에서 직접 서버로 요청하는 것
driver = webdriver.Chrome()
driver.get("https://www.google.com") #페이지 요청 > driver 페이지 파일이 저장
driver.implicitly_wait(0.5) #selenium 레퍼런스참조
#print(dir(driver))
# print(driver.page_source)

img = driver.find_element(By.XPATH,"/html/body/div[1]/div[2]/div/img") #F12에서 image class를 xpath로 가져옴
src_img = img.get_attribute(("src"))
res = requests.get(src_img)
#print((res))
#print(res.content) #다운로드 받은 이미지가 여기로 들어감
with open("save_img/test.png","wb") as fp: #글씨, 실행파일 빼고 다 바이너리임
    fp.write(res.content)
time.sleep(600)
#print(driver) #가상키보드, 가상마우스 작동할 수 있는 크롬드라이버
"""
1. get으로 접속 할 주소에 들어감 이때 딜레이(timesleep,implicityly_wait,...)를 반드시 해줘야 한다.
2. 드라이브에 방금 다운로드 받은 접속한 페이지의 정보가 담겨있음
3. DOM에서 element로 바뀌어 있음 By,xpath로 찾아오면 구조로 접속하기 때문에 구조의 특징을 찾아 들어가야 한다.
4. 3번을 통해 엘리먼틑 태그 자체가 들어온다. src를 통해 이미지의 주소를 따내는 것임
5. src속성에 접근하면 src 속성에 있는 값이 들어가진다. 
6. requests get으로 값들이 다시 들어가지고, content에 우리가 저장한 이미지가 있으므로, 이를 바이너리로 저장한다. 

"""