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
cpn_name = [] #회사 이름
rep_name = [] #대표 이름
recruit_url_messy = [] #채용공고 url (비정형)
recruit_url = [] #채용공고 url
cpn_url = [] #회사 url
cpn_add_messy = [] #회사 주소 (비정형)
cpn_add = [] #회사 주소
rec_title = [] #채용공고 제목
rec_main_text = [] #채용공고 본문
rec_full_text = [] #채용공고 제목 + 본문
rec_newcomer = [] #신입
rec_career = [] #경력
rec_intern = [] #인턴
rec_dl_messy = [] #채용공고 마감기한 (비정형)
rec_dl = [] #마감기한


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
for recruit_crawl in recruit_url:
    driver.get(recruit_crawl)
    driver.implicitly_wait(10)
    #회사 이름
    company_name = driver.find_element(By.CSS_SELECTOR, "div.left.col-6.col-md-auto.pl-0-xs > h2").text
    cpn_name.append(company_name)
    #대표 이름
    representative_name = driver.find_element(By.XPATH, "/html/body/div[6]/div[1]/section[2]/div/div[1]/div[2]/div[2]/span[1]").text
    rep_name.append(representative_name)
    #회사 url
    company_url = driver.find_element(By.XPATH, "/html/body/div[6]/div[1]/section[2]/div/div[1]/div[2]/div[2]/span[3]/a").text
    cpn_url.append(company_url)
    #회사 주소
    company_address = driver.find_element(By.XPATH, "/html/body/div[6]/div[1]/section[2]/div/div[1]/div[2]/div[2]/span[4]").text
    cpn_add_messy.append(company_address)
    #채용공고 제목
    recriut_title = driver.find_element(By.XPATH, "/html/body/div[6]/div[1]/section[1]/div/div/div/div/div[2]/p").text
    rec_title.append(recriut_title)
    #채용공고 본문
    recriut_main_text = driver.find_element(By.XPATH, "/html/body/div[6]/div[1]/section[2]/div/div[1]/div[1]/div").text
    rec_main_text.append(recriut_main_text)
    #채용공고 마감기한
    recriut_deadline = driver.find_element(By.XPATH, "/html/body/div[6]/div[1]/section[2]/div/div[1]/div[1]/div/div/span[1]").text
    rec_dl_messy.append(recriut_deadline)


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
    else:
        a = i.split()
        cpn_add.append(a[1] + " " + a[2])



# 채용공고 제목 또는 본문에서 신입, 경력, 인턴 구분
for sentence in rec_full_text:
    if "신입" in sentence:
        rec_newcomer.append('o')
    else:
        rec_newcomer.append('')

def line_sentence(x): #x가 들어간 줄을 추출
    a = sentence.find('년 경력')
    ch = '\n'
    indexes = [i for i, c in enumerate(sentence) if c == ch]
    front = []
    back = []

    for i in indexes: #앞뒤 구분
        dif = a - i
        if dif >= 0:
            front.append(dif)
        else:
            back.append(dif)

    if not front:
        front.append(0)

    front_near = front[0]
    back_near = back[0]

    for i in front: #앞에서 가까운
        if i < front_near:
            front_near = i
    for i in back: #뒤에서 가까운
        if i > back_near:
            back_near = i

    x = a - front_near
    y = a - back_near

    if x == a:
        x = -1

    rec_career.append(sentence[x+1:y])

for sentence in rec_full_text:
    if '년 경력' in sentence:
        line_sentence('년 경력')
    elif '년 이상' in sentence:
        line_sentence('년 이상')
    elif sentence.count("경력") >= 2:
        rec_career.append('o')
    elif sentence.count("경험") >= 1:
        rec_career.append('o')
    else:
        rec_career.append('')
    
for sentence in rec_full_text:
    if "인턴" in sentence:
        rec_intern.append('o')
    else:
        rec_intern.append('')
    
#채용공고 마감기한 0월0일 or 충원시 형태로 변환
for i in rec_dl_messy:
    if i.count('.') == 4:
        rec_dl.append(i[18:20] + '월 ' + i[21:23] + '일')
    elif i.count('.') == 0:
        rec_dl.append('충원 시')
    elif i.endswith(' ~  '):
        rec_dl.append(i[5:7] + '월 ' + i[8:10] + '일 ~ 충원 시')
    elif i.startswith('~ '):
        rec_dl.append(i[7:9] + '월 ' + i[10:12] + '일')
    else:
        rec_dl.append('확인 필요!')






# print(cpn_name)
# print(rep_name)
# print(recruit_url)
# print(cpn_url)
# print(cpn_add)
# print(rec_title)
# print(rec_main_text)
# print(rec_full_text)
# print(rec_newcomer)
# print(rec_newcomer)
# print(rec_career)
# print(rec_intern)
# print(rec_dl)





#csv파일로 변환----------------------------
# from pandas import DataFrame
# df = DataFrame({'신입':rec_newcomer, '경력':rec_career, '인턴':rec_intern, '마감기한':rec_dl,
#                 '회사 이름':cpn_name,'위치':cpn_add, '채용링크':recruit_url,
#                 '회사 웹사이트':cpn_url, '대표이름':rep_name})

# df.to_csv('./채용공고 리스트.csv', sep = ',', encoding= 'utf-8-sig')


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
                '회사 이름':cpn_name,'위치':cpn_add, '채용링크':recruit_url,
                '회사 웹사이트':cpn_url, '대표이름':rep_name})
worksheet.update([df.columns.values.tolist()] + df.values.tolist())

