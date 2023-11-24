from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

chrome_options = webdriver.ChromeOptions()

chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
driver.maximize_window()
driver.get("https://www.kira.or.kr/jsp/main/03/02_01.jsp")

#리스트 정의 
rec_newcomer = [] #신입
rec_career = [] #경력
rec_intern = [] #인턴
rec_dl_messy = [] #채용공고 마감기한 (비정형)
rec_dl = [] #마감기한
cpn_name = [] #회사 이름
people_messy = [] #직원 수 (비정형)
people = [] #직원 수
cpn_add_messy = [] #회사 주소 (비정형)
cpn_add = [] #회사 주소
recruit_url_messy = [] #채용공고 url (비정형)
recruit_url = [] #채용공고 url
cpn_url = [] #회사 url
rep_name = [] #대표 이름
recruit_career = [] #신입·경력·인턴 부분
recruit_id = []#채용공고 글번호
rec_main_text = [] #채용공고 본문

#각 채용공고에 접속하여 회사 채용정보 추출
def text_crawling(list, selector, elm):
    list.append(driver.find_element(selector, elm).text)

page = 10 #크롤링 할 범위 마지막 페이지 입력
for p in range(1,page+1): # 원하는 페이지까지 반복문
    driver.implicitly_wait(10)
    # for문 안에 page_bar를 넣어주어 매번 지정
    page_bar = driver.find_elements(By.CSS_SELECTOR,'#s_container > div.bg_gray.sub_wrap > div > div > div.sub_cont > div.paginate_wrap > div > ol > li > a')

    for button in page_bar:
        if button.text == str(p):
            button.click()
            break

    for i in range(1,11):
        driver.implicitly_wait(10)
        driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div[3]/div/div/div[2]/div[3]/table/tbody/tr[' + str(i) + ']').click()

        #채용공고 글번호
        text_crawling(recruit_id, By.XPATH, '//*[@id="s_container"]/div[3]/div/div/div[2]/div/div[2]/div[1]/div/div[2]/div[1]/div[1]/div[2]')
        #회사 이름
        text_crawling(cpn_name, By.XPATH, '//*[@id="s_container"]/div[3]/div/div/div[2]/div/div[2]/div[1]/div/div[1]/div[2]')
        #회사 주소
        text_crawling(cpn_add_messy, By.XPATH, '//*[@id="s_container"]/div[3]/div/div/div[2]/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/div[2]/span')
        #채용공고 마감기한
        text_crawling(rec_dl_messy, By.XPATH, '//*[@id="s_container"]/div[3]/div/div/div[2]/div/div[2]/div[1]/div/div[2]/div[6]/div/div[2]/span')
        #신입·경력·인턴 부분
        text_crawling(recruit_career, By.XPATH, '//*[@id="s_container"]/div[3]/div/div/div[2]/div/div[2]/div[1]/div/div[2]/div[4]/div[1]/div[2]/span')
        #직원 수
        text_crawling(people_messy, By.XPATH, '//*[@id="s_container"]/div[3]/div/div/div[2]/div/div[2]/div[1]/div/div[2]/div[3]/div[1]/div[2]')
        #채용공고 본문
        text_crawling(rec_main_text, By.XPATH, '//*[@id="s_container"]/div[3]/div/div/div[2]/div/div[2]/div[1]/div/div[2]/div[10]/div/div[2]/div')
        

        driver.implicitly_wait(10)
        driver.find_element(By.XPATH, '//*[@id="s_container"]/div[3]/div/div/div[2]/div/div[2]/div[2]/div[1]/button[1]').click()


#신입 구분
for i in recruit_career:
    if "신입" in i:
        rec_newcomer.append('o')
    else:
        rec_newcomer.append('-')

#경력 구분
for i in recruit_career:
    if '경력' in i:
        rec_career.append('o')
    else:
        rec_career.append('-')
    
#인턴 구분
for i in recruit_career:
    if "인턴" in i:
        rec_intern.append('o')
    else:
        rec_intern.append('-')


#회사 주소 없으면 확인 필요 입력
for i in cpn_add_messy:
    if i.startswith('/'):
        cpn_add.append('확인 필요!')
    elif i.endswith('/'):
        cpn_add.append('확인 필요!')
    else:
        a = i.split()
        cpn_add.append(a[0] + " " + a[2])

#직원 수에서 명 제거
for i in people_messy:
    if i.startswith('0'):
        people.append('-')
    else:
        a = i.split()
        people.append(a[0])

#채용공고 글번호로 채용공고 url 생성
for i in recruit_id:
    recruit_url.append('https://www.kira.or.kr/jsp/main/03/02_01.jsp?jobId=BBS_00_GUIN&sc_gi_jobId=BBS_00_GUIN&mode=read&sc_gi_compSctcode=&sc_gi_careerType=&sc_gi_compLoccode=&sc_gi_bizType=&sc_gi_payType=&sc_gi_compNameL=&gi_itemId=' + str(i))

#상세요강에 마감기한이 있으면 확인 필요!
num = 0
for i in rec_dl_messy:
    if i.startswith('상시'):
        rec_dl.append('상시 채용')
    elif i.startswith('충원 시'):
        if rec_main_text[num] in '기간' or rec_main_text[num] in '기한':
            rec_dl.append('확인 필요!')
        else:
            rec_dl.append('충원 시')
    else:
        rec_dl.append('확인 필요!')
    num = num + 1


print(len(rec_newcomer))
print(len(rec_career))
print(len(rec_intern))
print(len(rec_dl))
print(len(cpn_name))
print(len(people))
print(len(cpn_add))
print(len(recruit_url))



#스프레드 시트에 작성----------------------------
import gspread
from pandas import DataFrame

# json 파일이 위치한 경로를 값으로 줘야 합니다.
json_file_path = "architects-recruit-automation-dcd380c15faa.json"
gc = gspread.service_account(json_file_path)
spreadsheet_url = "https://docs.google.com/spreadsheets/d/1HsA4HH5KptEeEUz6MRTHxRMJcAEU7H9_0GO3gMXiEXE/edit?usp=sharing"
doc = gc.open_by_url(spreadsheet_url)

worksheet = doc.worksheet("대한건축사협회 크롤링") #작성하려는 시트를 기입

df = DataFrame({'신입':rec_newcomer, '경력':rec_career, '인턴':rec_intern, '마감기한':rec_dl,
                '회사 이름':cpn_name, '직원 수':people, '위치':cpn_add, '채용링크':recruit_url})
worksheet.update([df.columns.values.tolist()] + df.values.tolist())

