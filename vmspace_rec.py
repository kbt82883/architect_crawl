from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

chrome_options = webdriver.ChromeOptions()

chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
driver.maximize_window()
driver.get("https://vmspace.com/job/job.html")

driver.implicitly_wait(2)

#리스트 정의 
rec_newcomer = [] #신입
rec_career = [] #경력
rec_intern = [] #인턴
rec_dl_messy = [] #채용공고 마감기한 (비정형)
rec_dl = [] #마감기한
cpn_name = [] #회사 이름
people = [] #직원 수
cpn_add_messy = [] #회사 주소 (비정형)
cpn_add = [] #회사 주소
recruit_url_messy = [] #채용공고 url (비정형)
recruit_url = [] #채용공고 url
cpn_url = [] #회사 url
rep_name = [] #대표 이름

rec_title = [] #채용공고 제목
rec_main_text = [] #채용공고 본문
rec_full_text = [] #채용공고 제목 + 본문


#vmspace에서 각각의 채용공고 url 추출
recruits = driver.find_elements(By.CSS_SELECTOR, "h4.mb-0 a")
for recruit in recruits:
    recruit_list = recruit.get_attribute("href")
    recruit_url_messy.append(recruit_list)

#recruit_url_messy에서 중복된 채용공고 제거
for value in recruit_url_messy:
    if value not in recruit_url:
        recruit_url.append(value)

#url에 접속해서 회사 채용정보 추출
def text_crawling(list, selector, elm):
    list.append(driver.find_element(selector, elm).text)

# del recruit_url[14] #문제있는 채용공고 발견시 사용하기

for recruit_crawl in recruit_url:
    driver.get(recruit_crawl)
    driver.implicitly_wait(10)
    #회사 이름
    text_crawling(cpn_name, By.CSS_SELECTOR, "div.left.col-6.col-md-auto.pl-0-xs > h2")
    #대표 이름
    text_crawling(rep_name, By.XPATH, "/html/body/div[6]/div[1]/section[2]/div/div[1]/div[2]/div[2]/span[1]")
    #회사 url
    text_crawling(cpn_url, By.XPATH, "/html/body/div[6]/div[1]/section[2]/div/div[1]/div[2]/div[2]/span[3]/a")
    #회사 주소
    text_crawling(cpn_add_messy, By.XPATH, "/html/body/div[6]/div[1]/section[2]/div/div[1]/div[2]/div[2]/span[4]")
    #채용공고 제목
    text_crawling(rec_title, By.XPATH, "/html/body/div[6]/div[1]/section[1]/div/div/div/div/div[2]/p")
    #채용공고 본문
    text_crawling(rec_main_text, By.XPATH, "/html/body/div[6]/div[1]/section[2]/div/div[1]/div[1]/div")
    #채용공고 마감기한
    text_crawling(rec_dl_messy, By.XPATH, "/html/body/div[6]/div[1]/section[2]/div/div[1]/div[1]/div/div/span[1]")


#채용공고 제목 + 본문
i = 0
while len(rec_full_text) != len(rec_title):
    a = rec_title[i] + rec_main_text[i]
    rec_full_text.append(a)
    i = i + 1

#회사 주소 00 00구 형태로 변환
for i in cpn_add_messy:
    if i.startswith(' '):
        cpn_add.append('확인 필요!')
    elif len(i.split()) < 2:
        cpn_add.append('확인 필요!')
    else:
        a = i.split()
        cpn_add.append(a[1] + " " + a[2])



# 채용공고 제목 또는 본문에서 신입, 경력, 인턴 구분
for sentence in rec_full_text:
    if "신입" in sentence:
        rec_newcomer.append('o')
    else:
        rec_newcomer.append('-')

for sentence in rec_full_text:
    if sentence.count('경력') >= 2:
        rec_career.append('o')
    else:
        rec_career.append('-')
    
for sentence in rec_full_text:
    if "인턴" in sentence:
        rec_intern.append('o')
    else:
        rec_intern.append('-')
    
#채용공고 마감기한 0월0일 or 충원시 형태로 변환
for i in rec_dl_messy:
    if i.count('.') == 4:
        rec_dl.append(i[18:20] + '월 ' + i[21:23] + '일')
    elif i.count('.') == 0:
        rec_dl.append('충원 시')
    elif i.endswith(' ~  '):
        rec_dl.append('충원 시')
    elif i.startswith('~ '):
        rec_dl.append(i[7:9] + '월 ' + i[10:12] + '일')
    else:
        rec_dl.append('확인 필요!')


#직원 수 - 빈 리스트로 채우기
for i in cpn_name:
    people.append('')


print('리스트 개수입니다')
print(len(rec_newcomer))
print(len(rec_career))
print(len(rec_intern))
print(len(rec_dl))
print(len(cpn_name))
print(len(people))
print(len(cpn_add))
print(len(recruit_url))
print(len(cpn_url))
print(len(rep_name))


#스프레드 시트에 작성----------------------------
import gspread
from pandas import DataFrame

# json 파일이 위치한 경로를 값으로 줘야 합니다.
json_file_path = "architects-recruit-automation-dcd380c15faa.json"
gc = gspread.service_account(json_file_path)
spreadsheet_url = "https://docs.google.com/spreadsheets/d/1HsA4HH5KptEeEUz6MRTHxRMJcAEU7H9_0GO3gMXiEXE/edit?usp=sharing"
doc = gc.open_by_url(spreadsheet_url)

worksheet = doc.worksheet("vmspace 크롤링") #작성하려는 시트를 기입

df = DataFrame({'신입':rec_newcomer, '경력':rec_career, '인턴':rec_intern, '마감기한':rec_dl,
                '회사 이름':cpn_name, '직원 수':people, '위치':cpn_add, '채용링크':recruit_url,
                '회사 웹사이트':cpn_url, '대표이름':rep_name})
worksheet.update([df.columns.values.tolist()] + df.values.tolist())


driver.close()